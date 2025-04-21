from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.embeddings.jinaai import JinaEmbedding
from llama_index.llms.groq import Groq
from llama_index.vector_stores.qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
import os
from dotenv import load_dotenv


load_dotenv()

# models for comparison
models = [
    "llama-3.1-70b-versatile",
    "mixtral-8x7b-32768",
    "gemma-7b-it"
]

# Configure the embedding model
Settings.embed_model = JinaEmbedding(
    api_key=os.getenv("JINA_API_KEY"),
    model="jina-embeddings-v3",
    task="retrieval.passage"
)

def create_rag_system(data_dir="./data", model="mixtral-8x7b-32768"):
    # Configure the LLM with the selected model
    Settings.llm = Groq(
        api_key=os.getenv("GROQ_API_KEY"),
        model=model,
        temperature=0.7
    )

    # Initialize Qdrant client
    client = QdrantClient(path="./qdrant_data")
    
    # Create a Qdrant vector store
    vector_store = QdrantVectorStore(
        client=client,
        collection_name="my_documents",
        dimension=1024  # Make sure this matches the embedding model dimension
    )
    
    # Load documents from the specified directory
    documents = SimpleDirectoryReader(data_dir).load_data()
    
    # Create a vector store index with Qdrant
    index = VectorStoreIndex.from_documents(
        documents,
        vector_store=vector_store
    )
    
    # Set up the query engine
    query_engine = index.as_query_engine()
    
    return query_engine

def query_rag(query_engine, question: str):
    response = query_engine.query(question)
    return response

def main():
    print("Enter your question below. Type 'quit' to exit.")
    
    # Interactive loop for asking questions
    while True:
        question = input("\nEnter your question (or 'quit' to exit): ")
        if question.lower() == 'quit':
            print("Exiting the question loop. Goodbye!")
            break
        
        # Model comparison
        print("\nModel Comparison Results:")
        for model in models:
            print(f"\nTesting model: {model}")
            # Initialize the RAG system for each model
            query_engine = create_rag_system(model=model)
            
            # Get and display the answer from the RAG system
            response = query_rag(query_engine, question)
            print(f"Answer from {model}: {response}")

if __name__ == "__main__":
    main()
