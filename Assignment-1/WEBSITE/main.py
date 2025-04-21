from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.embeddings.cohere import CohereEmbedding
from llama_index.llms.groq import Groq
from llama_index.vector_stores.qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
# from llama_index.core import Settings 
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Cohere embedding model
Settings.embed_model = CohereEmbedding(
    api_key=os.getenv("COHERE_API_KEY"),
    model_name="embed-english-v3.0",
    input_type="search_query"
)

# Configure the LLM model from Groq
Settings.llm = Groq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.1-70b-versatile",
    temperature=0.7
)

def create_rag_system(data_dir="./data"):
    # Initialize Qdrant client
    client = QdrantClient(path="./qdrant_web_data")
    
    # Create Qdrant vector store
    vector_store = QdrantVectorStore(
        client=client,
        collection_name="web_documents",
        dimension=1024  
    )
    
    # Load documents from the specified directory
    documents = SimpleDirectoryReader(data_dir).load_data()
    
    # Create vector store index with Qdrant
    index = VectorStoreIndex.from_documents(
        documents,
        vector_store=vector_store
    )
    
    # Create query engine
    query_engine = index.as_query_engine()
    
    return query_engine

def query_rag(query_engine, question: str):
    # Query the system with the user's question
    response = query_engine.query(question)
    return response

def main():
    # Initialize the RAG system with the 'data' directory containing website_content.md
    query_engine = create_rag_system("./data")
    
    # Example usage: interactively asking questions based on website_content.md
    while True:
        question = input("\nEnter your question (or 'quit' to exit): ")
        if question.lower() == 'quit':
            break
            
        response = query_rag(query_engine, question)
        print(f"\nAnswer: {response}")

if __name__ == "__main__":
    main()
