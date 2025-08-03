from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import torch

class InMemoryVectorStore:
    def __init__(self, texts, model_name='sentence-transformers/all-MiniLM-L6-v2'):
        self.texts = texts
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        print(f"Using device: {self.device}")
        # Load model on correct device
        self.model = SentenceTransformer(model_name, device=self.device)
        # Compute embeddings and store on device
        self.embeddings = self.model.encode(
            texts, convert_to_numpy=True, device=self.device, show_progress_bar=True
        )
        
    def retrieve(self, query, top_k=5):
        # Embed the query on device
        query_emb = self.model.encode(
            [query], convert_to_numpy=True, device=self.device
        )
        # Compute cosine similarities (on CPU, as scikit-learn expects numpy)
        similarities = cosine_similarity(query_emb, self.embeddings)[0]
        # Get indices for top_k highest scores
        top_indices = np.argsort(similarities)[::-1][:top_k]
        # Return the most similar strings with their similarity scores
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
    store = InMemoryVectorStore(corpus, model_name='sentence-transformers/all-MiniLM-L6-v2')
    query = "Tell me about artificial intelligence."
    results = store.retrieve(query)
    for text, score in results:
        print(f"{score:.4f}: {text}")
