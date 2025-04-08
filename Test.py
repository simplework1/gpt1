from langchain_core.vectorstores import InMemoryVectorStore
from langchain.embeddings import HuggingFaceBgeEmbeddings
import json

# Function to create vector stores from dataframes
def create_vector_stores_from_dfs(df_dict, model_name="BAAI/bge-base-en-v1.5", device="cuda"):
    model_kwargs = {'device': device}
    encode_kwargs = {'normalize_embeddings': True}

    embeddings_model = HuggingFaceBgeEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )

    vector_store_dict = {}

    for df_name, df in df_dict.items():
        texts = df.apply(lambda row: json.dumps(row.to_dict()), axis=1).tolist()
        metadata = df.apply(lambda row: row.to_dict(), axis=1).tolist()

        # Create InMemoryVectorStore from texts and dictionaries as metadata
        vector_store = InMemoryVectorStore.from_texts(
            texts=texts,
            embedding=embeddings_model,
            metadatas=metadata
        )

        vector_store_dict[df_name] = vector_store

    return vector_store_dict

# Retrieval function from vector store using metadata
def retrieve_from_vector_store(vector_store, query, embeddings_model, top_k=5):
    results = vector_store.similarity_search(query, k=top_k)
    retrieved_metadata = [result.metadata for result in results]
    return retrieved_metadata
