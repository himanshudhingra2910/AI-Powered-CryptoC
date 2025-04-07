from duckduckgo_search import DDGS
from rapidfuzz import fuzz

def is_published_text(text, threshold=70):
    """
    Checks if the given text is already published online using a fuzzy matching approach.
    - text: the input text
    - threshold: similarity percentage threshold (0-100) for flagging as published
    Returns a tuple: (is_published (bool), source_url (str or None))
    """
    # Use the first 30 words as a snippet for search
    snippet = " ".join(text.strip().split()[:30])
    with DDGS() as ddgs:
        results = list(ddgs.text(snippet, max_results=5))
        for result in results:
            body = result.get("body", "")
            similarity = fuzz.token_set_ratio(snippet.lower(), body.lower())
            # Debug print (optional)
            # print(f"Comparing snippet with result body, similarity: {similarity}")
            if similarity >= threshold:
                return True, result.get("href", "")
    return False, None
