from typing import List
from pydantic import BaseModel, Field
from llama_index.core import (
    SimpleDirectoryReader,
    StorageContext,
    VectorStoreIndex,
    load_index_from_storage,
    Settings,
)


from llama_index.llms.groq import Groq

from llama_index.embeddings.jinaai import JinaEmbedding

from llama_index.core.agent import ReActAgent
from llama_index.core.tools import QueryEngineTool, ToolMetadata, FunctionTool
from llama_index.core.memory import ChatMemoryBuffer
import os
from dotenv import load_dotenv
import datetime

load_dotenv()

class Document(BaseModel):
    content: str = Field(..., description="The content of the document")
    metadata: dict = Field(
        default_factory=dict, description="Metadata associated with the document"
)

class QueryResult(BaseModel):
    answer: str = Field(..., description="The answer to the query")
    source_nodes: List[str] = Field(
        ..., description="The source nodes used to generate the answer"
    )

class MedicalAssistant:
    def __init__(
        self,
        data_path: str,
        index_path: str = "index",
    ):    
        self.data_path = data_path
        self.index_path = index_path
        self.system_prompt = """
        You are a Medical Assistant AI specializing in identifying symptoms and diseases based on health-related prompts.
        
        Your primary goals are to:
        
        - Identify symptoms related to specific diseases or vice versa based on user queries.
        - Explain symptoms and diseases in a clear and understandable manner for users without a medical background.
        - Guide users on potential causes and provide context for symptom clusters associated with various conditions.
        - Encourage users to consult healthcare professionals for diagnosis and treatment.
        - Suggest possible questions to ask healthcare providers based on the information provided.

        Medical Agents:
        - Researcher Agent: Gathers symptom and disease information from validated sources, providing insights on common and rare symptoms.
        - Reporting Analyst Agent: Analyzes the information to present it in an easy-to-understand format, including details such as symptom severity and possible complications.

        Assist users by:
        - Clarifying the health query to ensure accurate identification.
        - Using non-technical language for accessibility.
        - Offering guidance on seeking medical evaluation.
        """
        
        self.configure_settings()
        self.index = None
        self.agent = None

        # Load or create index
        self.load_or_create_index()

    def configure_settings(self):
        Settings.llm = Groq(model="llama3-70b-8192", api_key=os.getenv("GROQ_API_KEY"))
        Settings.embed_model = JinaEmbedding(
            api_key=os.getenv("JINA_API_KEY"),
            model="jina-embeddings-v2-base-en",
        )

    def load_or_create_index(self):
        if self.check_existing_index():
            self.load_index()
        else:
            self.create_index()
        self._create_agent()

    def check_existing_index(self) -> bool:
        return os.path.exists(self.index_path)

    def load_index(self):
        print("Loading existing index...")
        storage_context = StorageContext.from_defaults(persist_dir=self.index_path)
        self.index = load_index_from_storage(storage_context)
        print("Index loaded successfully.")

    def create_index(self):
        print("Creating new index...")
        documents = SimpleDirectoryReader(
            self.data_path,
            recursive=True,
        ).load_data()
        if not documents:
            raise ValueError("No documents loaded. Check the data path.")
        self.index = VectorStoreIndex.from_documents(documents)
        self.save_index()
        print("New index created and saved successfully.")

    def _create_agent(self):
        query_engine = self.index.as_query_engine(similarity_top_k=5)
        
        search_tool = QueryEngineTool(
            query_engine=query_engine,
            metadata=ToolMetadata(
                name="MedicalAssistant",
                description="Retrieve symptoms or disease information based on user-provided health prompts.",
            ),
        )

        def get_symptom_details(symptom: str) -> str:
            # Stub function to provide details about a specific symptom
            return f"Details about {symptom}."

        symptom_details_tool = FunctionTool.from_defaults(
            fn=get_symptom_details,
            name="get_symptom_details",
            description="Provide details about a specific symptom."
        )

        def get_disease_information(disease: str) -> str:
            # Stub function to provide information about a specific disease
            return f"Information about {disease}."

        disease_info_tool = FunctionTool.from_defaults(
            fn=get_disease_information,
            name="get_disease_information",
            description="Provide information about a specific disease."
        )

        self.agent = ReActAgent.from_tools(
            [search_tool, symptom_details_tool, disease_info_tool],
            verbose=True,
            system_prompt=self.system_prompt,
            memory=ChatMemoryBuffer.from_defaults(token_limit=4096),
        )

    def query(self, query: str) -> QueryResult:
        if not self.agent:
            raise ValueError(
                "Agent not created. There might be an issue with index loading or creation."
            )
        response = self.agent.chat(query)
        return QueryResult(
            answer=response.response,
            source_nodes=[],  # Note: ReActAgent doesn't provide source nodes directly
        )

    def save_index(self):
        os.makedirs(self.index_path, exist_ok=True)
        self.index.storage_context.persist(persist_dir=self.index_path)

# Example usage:
# if __name__ == "__main__":
#     medical_assistant = MedicalAssistant(
#         data_path="./medical_data",
#         index_path="medical_index"
#     )

#     result = medical_assistant.query("What are the symptoms of diabetes?")
#     print(result.answer)
