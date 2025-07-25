import time
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import InMemoryVectorStore
from langchain_core.documents import Document

def create_in_memory_vectorstore(large_text: str, chunk_size: int = 1000, chunk_overlap: int = 200):
    """
    Takes a large text, splits it into chunks, and creates an in-memory vector store.

    Args:
        large_text (str): The large block of text to process.
        chunk_size (int): The maximum size of each text chunk (in characters).
        chunk_overlap (int): The number of characters to overlap between chunks.

    Returns:
        InMemoryVectorStore: A LangChain vector store ready for similarity searches.
    """
    if not isinstance(large_text, str) or not large_text.strip():
        raise ValueError("Input text must be a non-empty string.")

    print("Step 1: Splitting the text into chunks...")
    # This text splitter is recommended for generic text.
    # It tries to split on paragraphs, then sentences, then words.
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
    )
    chunks = text_splitter.split_text(large_text)
    # Convert string chunks to LangChain Document objects
    documents = [Document(page_content=chunk) for chunk in chunks]
    print(f"--> Successfully created {len(documents)} documents.")
    print("-" * 20)

    print("Step 2: Initializing the embedding model...")
    # We use a local, open-source model. The first time you run this,
    # it will be downloaded and cached.
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    embeddings = HuggingFaceEmbeddings(model_name=model_name)
    print(f"--> Embedding model '{model_name}' initialized.")
    print("-" * 20)
    
    print("Step 3: Creating the in-memory vector store...")
    start_time = time.time()
    # The from_documents method handles embedding and storing the documents.
    vectorstore = InMemoryVectorStore.from_documents(
        documents=documents, 
        embedding=embeddings
    )
    end_time = time.time()
    print(f"--> Vector store created in {end_time - start_time:.2f} seconds.")
    print("-" * 20)

    return vectorstore

# --- Example Usage ---
if __name__ == "__main__":
    # A very large paragraph/text about the history of artificial intelligence
    sample_large_text = """
    Artificial intelligence (AI) has its roots in the mid-20th century, a period of intellectual ferment where the boundaries of computation and cognition were being explored. The term "artificial intelligence" was coined by John McCarthy in 1956 at the Dartmouth Conference, which is widely considered the birthplace of AI as a field. Early pioneers like Alan Turing had already laid the theoretical groundwork with concepts like the Turing Test, a measure of a machine's ability to exhibit intelligent behavior indistinguishable from that of a human. The initial years were filled with optimism, leading to significant funding and research. Early AI programs demonstrated remarkable capabilities for the time, solving algebra word problems, proving logical theorems, and speaking English.

    However, the initial excitement gave way to the first "AI winter" in the mid-1970s. The limitations of the early computers, the combinatorial explosion of problems, and the failure to deliver on overly ambitious promises led to a significant reduction in funding and interest. Researchers had underestimated the profound difficulty of creating true intelligence. For example, common-sense knowledge and reasoning, things humans do effortlessly, proved incredibly hard to codify. The ALPAC report in the US and the Lighthill Report in the UK were highly critical of the progress in AI, leading to government funding cuts.

    The field re-emerged in the 1980s with the commercial success of "expert systems," a form of AI program that emulated the decision-making ability of a human expert in a narrow domain. Companies around the world used expert systems to solve specific problems in fields like medicine, finance, and manufacturing, which revived interest and investment. This boom was followed by a second, shorter AI winter in the late 1980s and early 1990s as the technology matured and the market for specialized AI hardware collapsed.

    The modern era of AI, starting from the late 1990s and accelerating in the 2010s, is characterized by the dominance of machine learning, especially deep learning. This resurgence was fueled by three key factors: the availability of vast amounts of data (big data), the development of powerful parallel computing hardware like GPUs, and the creation of more sophisticated algorithms. Deep learning models, with their layered neural networks, have achieved state-of-the-art results in areas like image recognition (e.g., ImageNet competition), natural language processing (e.g., large language models like GPT), and game playing (e.g., AlphaGo defeating the world champion in Go). This progress has brought AI into the mainstream, powering everything from search engines and recommendation systems to autonomous vehicles and medical diagnostics. The future of AI continues to be a subject of intense debate, focusing on its potential for societal benefit, ethical considerations, and the long-term goal of achieving Artificial General Intelligence (AGI).
    """

    print("Starting the vector store creation process...\n")
    try:
        # 1. Create the vector store from our sample text
        vector_store = create_in_memory_vectorstore(sample_large_text)

        print("\nVector store is ready! Now let's test it with a query.")
        
        # 2. Perform a similarity search
        query = "What caused the AI winter in the 1970s?"
        print(f"\nQuerying the vector store for: '{query}'")
        
        # The similarity_search method finds the most relevant document chunks
        search_results = vector_store.similarity_search(query, k=2) # Find the top 2 most relevant chunks
        
        print("\n--- Top Search Results ---")
        for i, result in enumerate(search_results):
            print(f"Result {i+1}:")
            print(result.page_content)
            print("--------------------------")

    except ValueError as e:
        print(f"Error: {e}")

