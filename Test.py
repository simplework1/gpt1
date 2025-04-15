from rank_bm25 import BM25Okapi
from typing import List
import nltk

# Download tokenizer resources if not already downloaded
nltk.download('punkt')
from nltk.tokenize import word_tokenize

def retrieve_with_bm25(texts: List[str], query: str, top_k: int = 1) -> List[str]:
    """
    Retrieve the most relevant text(s) using BM25.

    Parameters:
        texts (List[str]): List of candidate documents.
        query (str): The input query.
        top_k (int): Number of top results to return.

    Returns:
        List[str]: Top-k most relevant texts.
    """
    # Tokenize the corpus
    tokenized_corpus = [word_tokenize(doc.lower()) for doc in texts]
    
    # Initialize BM25
    bm25 = BM25Okapi(tokenized_corpus)
    
    # Tokenize the query
    tokenized_query = word_tokenize(query.lower())
    
    # Get scores
    scores = bm25.get_scores(tokenized_query)
    
    # Rank and return top-k results
    top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]
    return [texts[i] for i in top_indices]