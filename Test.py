from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class InMemoryVectorStore:
    def __init__(self, texts):
        self.texts = texts
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.embeddings = self.model.encode(texts, convert_to_numpy=True)
        
    def retrieve(self, query, top_k=5):
        # Embed the query
        query_emb = self.model.encode([query], convert_to_numpy=True)
        # Compute cosine similarities
        similarities = cosine_similarity(query_emb, self.embeddings)[0]
        # Get top_k indices
        top_indices = np.argsort(similarities)[::-1][:top_k]
        # Return top strings and their scores
        return [(self.texts[i], similarities[i]) for i in top_indices]


# Example usage:
if __name__ == '__main__':
    corpus = [
        "The quick brown fox jumps over the lazy dog.",
        "A fast, dark-colored fox leaps across a sleeping canine.",
        "Artificial intelligence is transforming technology.",
        "Natural language processing is a fascinating field.",
        "Dogs are commonly domesticated pets.",
        "Foxes are wild animals.",
        "Machine learning is a subset of AI."
    ]
    store = InMemoryVectorStore(corpus)
    query = "Tell me about artificial intelligence."
    results = store.retrieve(query)
    for text, score in results:
        print(f"{score:.4f}: {text}")
