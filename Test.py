import os
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import torch

class InMemoryVectorStore:
    def __init__(self, texts, folder_path, model_name='BAAI/bge-en-icl'):
        self.texts = texts
        self.folder_path = folder_path
        self.embedding_file = os.path.join(folder_path, "embeddings.npz")
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        print(f"Using device: {self.device}")

        # Ensure folder exists
        os.makedirs(folder_path, exist_ok=True)

        if os.path.isfile(self.embedding_file):
            print("Loading embeddings from cache...")
            data = np.load(self.embedding_file, allow_pickle=True)
            self.embeddings = data['embeddings']
            self.texts = list(data['texts'])
        else:
            print("Computing and saving new embeddings...")
            self.model = SentenceTransformer(model_name, device=self.device)
            self.embeddings = self.model.encode(
                texts, convert_to_numpy=True, device=self.device, show_progress_bar=True
            )
            np.savez_compressed(self.embedding_file, embeddings=self.embeddings, texts=np.array(texts))
            del self.model  # Free memory if not needed further

        # Only load model if needed (retrieval step)
        self.model = SentenceTransformer(model_name, device=self.device)

    def retrieve(self, query, top_k=5):
        query_emb = self.model.encode(
            [query], convert_to_numpy=True, device=self.device
        )
        similarities = cosine_similarity(query_emb, self.embeddings)[0]
        top_indices = np.argsort(similarities)[::-1][:top_k]
        return [(self.texts[i], similarities[i]) for i in top_indices]

# Example usage:
if __name__ == "__main__":
    corpus = [
        "The quick brown fox jumps over the lazy dog.",
        "A fast, dark-colored fox leaps across a sleeping canine.",
        "Artificial intelligence is transforming technology.",
        "Natural language processing is a fascinating field.",
        "Dogs are commonly domesticated pets.",
        "Foxes are wild animals.",
        "Machine learning is a subset of AI."
    ]
    # Specify a folder to store embeddings cache
    embedding_folder = "./embedding_cache"
    store = InMemoryVectorStore(corpus, embedding_folder, model_name="BAAI/bge-en-icl")
    query = "Tell me about artificial intelligence."
    results = store.retrieve(query)
    for text, score in results:
        print(f"{score:.4f}: {text}")
