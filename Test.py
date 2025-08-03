import os
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import torch

class Document:
    def __init__(self, page_content, metadata={}):
        self.page_content = page_content
        self.metadata = metadata

class InMemoryVectorStore:
    def __init__(self, documents, folder_path, model_name='BAAI/bge-en-icl'):
        """
        documents: list of Document objects (with page_content, metadata)
        """
        self.folder_path = folder_path
        self.embedding_file = os.path.join(self.folder_path, "embeddings.pkl")
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        print(f"Using device: {self.device}")

        # Ensure folder exists
        os.makedirs(folder_path, exist_ok=True)

        if os.path.isfile(self.embedding_file):
            print("Loading embeddings from pickle...")
            with open(self.embedding_file, 'rb') as f:
                data = pickle.load(f)
                self.embeddings = data['embeddings']
                self.page_contents = data['page_contents']
                self.metadata = data['metadata']
        else:
            print("Computing and saving new embeddings...")
            self.page_contents = [doc.page_content for doc in documents]
            self.metadata = [doc.metadata for doc in documents]
            self.model = SentenceTransformer(model_name, device=self.device)
            self.embeddings = self.model.encode(
                self.page_contents, convert_to_numpy=True, device=self.device, show_progress_bar=True
            )
            with open(self.embedding_file, 'wb') as f:
                pickle.dump({
                    'embeddings': self.embeddings,
                    'page_contents': self.page_contents,
                    'metadata': self.metadata
                }, f)
            del self.model  # Free up memory

        # Load model for retrieval
        self.model = SentenceTransformer(model_name, device=self.device)

    def retrieve(self, query, top_k=5):
        query_emb = self.model.encode(
            [query], convert_to_numpy=True, device=self.device
        )
        similarities = cosine_similarity(query_emb, self.embeddings)[0]
        top_indices = np.argsort(similarities)[::-1][:top_k]
        results = []
        for i in top_indices:
            results.append({
                "page_content": self.page_contents[i],
                "metadata": self.metadata[i],
                "similarity": similarities[i]
            })
        return results

# Example usage
if __name__ == "__main__":
    docs = [
        Document("The quick brown fox jumps over the lazy dog.", {"page": 1}),
        Document("A fast, dark-colored fox leaps across a sleeping canine.", {"page": 2}),
        Document("Artificial intelligence is transforming technology.", {"topic": "AI"}),
        Document("Natural language processing is a fascinating field.", {"category": "NLP"}),
        Document("Dogs are commonly domesticated pets.", {"animal": "Dog"}),
        Document("Foxes are wild animals.", {"animal": "Fox"}),
        Document("Machine learning is a subset of AI.", {"topic": "AI"}),
    ]
    embedding_folder = "./embedding_cache"
    store = InMemoryVectorStore(docs, embedding_folder, model_name="BAAI/bge-en-icl")
    query = "Tell me about artificial intelligence."
    results = store.retrieve(query)
    for r in results:
        print(f"{r['similarity']:.4f}: {r['page_content']} | Meta {r['metadata']}")
