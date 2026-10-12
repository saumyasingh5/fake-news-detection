
import re
import requests
import streamlit as st
from google import genai
from google.genai import types


# Gemini model alias
MODEL_NAME = "gemini-flash-latest"


def get_api_key():
    return st.secrets.get("GEMINI_API_KEY", "")


def get_factcheck_key():
    return st.secrets.get("GOOGLE_FACTCHECK_API_KEY", "")


def search_fact_checks(news):
    """
    Search previously fact-checked claims.
    Does not restrict results to recent dates.
    """
    api_key = get_factcheck_key()

    if not api_key:
        return []

    try:
        response = requests.get(
            "https://factchecktools.googleapis.com/v1alpha1/claims:search",
            params={
                "key": api_key,
                "query": news[:500],
                "pageSize": 5
            },
            timeout=12
        )

        response.raise_for_status()
        data = response.json()

        results = []

        for claim in data.get("claims", []):
            for review in claim.get("claimReview", []):
                results.append({
                    "claim": claim.get("text", "Claim"),
                    "publisher": review.get("publisher", {}).get(
                        "name", "Fact-check publisher"
                    ),
                    "rating": review.get(
                        "textualRating", "Rating not provided"
                    ),
                    "title": review.get("title", "Read fact-check"),
                    "url": review.get("url", ""),
                    "date": review.get("reviewDate", "")
                })

        return results[:8]

    except requests.RequestException:
        return []
    except (ValueError, TypeError):
        return []


def extract_sources(response):
    """Extract source URLs returned by Gemini Search grounding."""
    sources = []
    seen_urls = set()

    try:
        candidates = getattr(response, "candidates", None) or []

        for candidate in candidates:
            metadata = getattr(candidate, "grounding_metadata", None)

            if not metadata:
                continue

            chunks = getattr(metadata, "grounding_chunks", None) or []

            for chunk in chunks:
                web_info = getattr(chunk, "web", None)

                if not web_info:
                    continue

                url = getattr(web_info, "uri", "")
                title = getattr(web_info, "title", "Web source")

                if url.startswith("https://") and url not in seen_urls:
                    seen_urls.add(url)
                    sources.append({
                        "title": title,
                        "url": url
                    })

    except (AttributeError, TypeError):
        pass

    return sources[:6]


def detect_news(news):
    """
    Returns:
        prediction, reason, error_text
    """

    news = news.strip()

    if not news:
        return "UNCERTAIN", "Please enter a news claim to analyze.", None

    api_key = get_api_key()

    if not api_key:
        return None, None, (
            "GEMINI_API_KEY is missing from Streamlit Secrets."
        )

    try:
        client = genai.Client(api_key=api_key)

        # Search existing fact-check reports, including older claims.
        fact_checks = search_fact_checks(news)

        factcheck_context = ""

        if fact_checks:
            factcheck_context = "\n\nMATCHING FACT-CHECK REPORTS:\n"

            for item in fact_checks:
                factcheck_context += (
                    f"\nClaim: {item['claim']}"
                    f"\nPublisher: {item['publisher']}"
                    f"\nRating: {item['rating']}"
                    f"\nReview date: {item['date']}"
                    f"\nTitle: {item['title']}"
                    f"\nURL: {item['url']}\n"
                )
        else:
            factcheck_context = (
                "\nNo matching report was returned by the optional "
                "Fact Check API. This does NOT prove the news is true "
                "or false.\n"
            )

        prompt = f"""
You are a careful news verification assistant.

Analyze the claim below using Google Search results and the
fact-check reports supplied in this prompt.

NEWS CLAIM:
{news}

FACT-CHECK SEARCH RESULTS:
{factcheck_context}

RULES:
1. Search for the exact claim, names, dates, location and context.
2. Check whether sources actually support or contradict the claim.
3. Prefer official statements, original documents and reputable
   news organizations.
4. Treat old news carefully. Check the original publication date
   and do not confuse an old event with a current event.
5. A matching fact-check report is useful only if it refers to
   the same claim and context.
6. Do not invent sources, dates, quotations or evidence.
7. Do not assume that a claim is fake merely because no source
   was found.
8. Use REAL only when reliable evidence supports the main claim.
9. Use FAKE only when reliable evidence clearly disproves it or
   establishes that it is materially false.
10. Use UNCERTAIN when evidence is insufficient, conflicting,
    outdated or unrelated.
11. A social-media post or search snippet alone is not conclusive.
12. Keep the explanation simple and concise.

Return exactly this format:

Prediction: REAL, FAKE, or UNCERTAIN
Reason: Explain the evidence and context in 2-4 simple sentences.
"""

        with st.spinner("Searching sources and analyzing the news..."):
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt,
                config=types.GenerateContentConfig(
                    tools=[
                        types.Tool(
                            google_search=types.GoogleSearch()
                        )
                    ],
                    temperature=0.1
                )
            )

        result = (getattr(response, "text", None) or "").strip()

        if not result:
            return None, None, (
                "Gemini returned an empty response. Please try again."
            )

        match = re.search(
            r"Prediction\s*:\s*(REAL|FAKE|UNCERTAIN)\b",
            result,
            re.IGNORECASE
        )

        if match:
            prediction = match.group(1).upper()
        else:
            prediction = "UNCERTAIN"

        reason_match = re.search(
            r"Reason\s*:\s*(.*)",
            result,
            re.IGNORECASE | re.DOTALL
        )

        reason = (
            reason_match.group(1).strip()
            if reason_match
            else result
        )

        # Add actual Google Search grounding sources, if returned.
        sources = extract_sources(response)

        if sources:
            reason += "\n\n**Web sources:**"

            for source in sources:
                title = source["title"].replace("[", "").replace("]", "")
                url = source["url"]
                reason += f"\n- [{title}]({url})"

        # Add matching fact-check reports with their publisher ratings.
        if fact_checks:
            reason += "\n\n**Fact-check reports:**"

            for item in fact_checks[:5]:
                title = item["title"].replace("[", "").replace("]", "")
                url = item["url"]

                if url.startswith("https://"):
                    reason += (
                        f"\n- [{title}]({url}) — "
                        f"{item['publisher']}; "
                        f"Rating: {item['rating']}; "
                        f"Review date: {item['date']}"
                    )

        return prediction, reason, None

    except Exception as error:
        message = str(error)
        lowered = message.lower()

        if any(term in lowered for term in [
            "429", "resource_exhausted", "quota"
        ]):
            friendly_error = (
                "Gemini API quota or rate limit reached. "
                "Please wait and try again, or check your API quota."
            )
        elif any(term in lowered for term in [
            "timeout", "connection", "getaddrinfo", "network"
        ]):
            friendly_error = (
                "Could not connect to the online service. "
                "Check the internet connection and try again."
            )
        elif any(term in lowered for term in [
            "404", "not_found", "model"
        ]):
            friendly_error = (
                "The selected Gemini model may not be available "
                "for this API key. Check the models available "
                "in your Google AI Studio project."
            )
        else:
            friendly_error = (
                "News analysis failed. Please check Streamlit logs "
                "for the technical error and try again."
            )

        return None, None, friendly_error
