from langchain.embeddings import HuggingFaceBgeEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore

model_name = "BAAI/bge-base-en-v1.5"
model_kwargs = {'device': 'cuda'}
encode_kwargs = {'normalize_embeddings': True}

model = HuggingFaceBgeEmbeddings(
    model_name=model_name,
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs,
)

vector_store = InMemoryVectorStore(model)
# Assuming col_list2 is your list of texts
_ = vector_store.add_texts(col_list2)

# Use similarity_search_with_score to get scores
results_with_scores = vector_store.similarity_search_with_score(input_, k=10)

# Set your matching threshold (e.g., 0.75 for 75% similarity)
threshold = 0.75

# Filter based on score
filtered_results = [doc for doc, score in results_with_scores if score >= threshold]

# Extract page content if needed
results = [doc.page_content for doc in filtered_results]