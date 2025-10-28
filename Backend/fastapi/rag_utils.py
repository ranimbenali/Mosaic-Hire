import logging
from serpapi import GoogleSearch

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class RAGKnowledgeBaseWeb:
    """
    RAG qui récupère le contexte directement sur Internet via SerpAPI.
    """

    def __init__(self, serpapi_api_key: str, top_k: int = 5):
        self.serpapi_api_key = serpapi_api_key
        self.top_k = top_k

    def query(self, query_text, top_k=None):
        top_k = top_k or self.top_k
        results = []

        try:
            params = {
                "engine": "google",
                "q": query_text,
                "num": top_k,
                "api_key": self.serpapi_api_key
            }
            search = GoogleSearch(params)
            data = search.get_dict()
        except Exception as e:
            logger.exception("Erreur lors de la requête SerpAPI : %s", e)
            return ["Aucun document pertinent trouvé via SerpAPI."]

        organic_results = data.get("organic_results", [])
        for item in organic_results[:top_k]:
            title = item.get("title", "")
            snippet = item.get("snippet", "")
            link = item.get("link", "")
            if snippet:
                results.append(f"{title}\n{link}\n{snippet[:1000]}")

        if not results:
            results = ["Aucun document pertinent trouvé via SerpAPI."]
        logger.info("SerpAPI query: trouvé %d documents", len(results))
        return results
