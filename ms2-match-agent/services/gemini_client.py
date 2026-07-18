"""
Thin wrapper around the Gemini client.

Nothing in this file knows anything about PDFs, resumes, or FastAPI —
on purpose. Right now its only job is proving MS2 can successfully
authenticate to Gemini and get a response back. Resume-parsing logic
will live in its own module later and will import get_gemini_client()
from here, rather than creating its own client.
"""

from google import genai
from config import GEMINI_API_KEY, GEMINI_MODEL
_client = genai.Client(api_key=GEMINI_API_KEY)

def get_gemini_client() -> genai.Client:
    """
    Returns the shared Gemini client instance.

    Exists so other modules (e.g. a future resume_parser.py) depend on
    this one function instead of importing the private `_client`
    variable directly or constructing their own client. That's the
    seam future code should plug into.
    """
    return _client


def test_gemini() -> None:
    """
    Sends a single test prompt to Gemini and prints the response.

    This function proves exactly one thing: that GEMINI_API_KEY is
    valid and MS2 can successfully reach the Gemini API. It does not
    parse anything, store anything, or touch FastAPI — that's
    intentional, per the task scope.
    """
    print("Using Gemini model:", GEMINI_MODEL)
    response = _client.models.generate_content(
        model=GEMINI_MODEL,
        contents="Hello Gemini",
    )
    print(response.text)

if __name__ == "__main__":
    test_gemini()
