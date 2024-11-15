from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader, UnstructuredExcelLoader
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders.csv_loader import CSVLoader
import os
from langchain_pinecone import PineconeVectorStore

# Load environment variables (if needed)
from dotenv import load_dotenv
load_dotenv()
import os
import mimetypes




def get_file_type(file_path):
    """
    Determines the type of a file based on its path and checks if it is one of the following types:
    CSV, XLSX, PDF, DOCX, or TXT.

    Args:
        file_path (str): The path to the file.

    Returns:
        str: The file type as a string ('csv', 'xlsx', 'pdf', 'docx', 'txt') 
             or 'unknown' if the type cannot be determined.
    """
    # Check if it's a regular file
    if os.path.isfile(file_path):
        # Get the file extension
        _, file_extension = os.path.splitext(file_path)

        # Check based on the file extension
        if file_extension.lower() == ".csv":
            return "csv"
        elif file_extension.lower() == ".xlsx":
            return "xlsx"
        elif file_extension.lower() == ".pdf":
            return "pdf"
        elif file_extension.lower() == ".docx":
            return "docx"
        elif file_extension.lower() == ".txt":
            return "txt"
        else:
            return "unknown"
    else:
        return "Not a file"


def get_pdf_loader(file_path):
    loader = PyPDFLoader(file_path)
    return loader

def get_csv_loader(file_path):
    loader = CSVLoader(file_path=file_path)
    return loader 

def get_txt_loader(file_path):
    loader = TextLoader(file_path)
    return loader

def get_docx_loader(file_path):
    loader = Docx2txtLoader(file_path)
    return loader

def get_xlsx_loader(file_path):
    loader = UnstructuredExcelLoader(file_path, mode="elements")
    return loader


def get_file_loader(file_path):
    # check for file type:
    file_type = get_file_type(file_path=file_path)

    if file_type == 'pdf':
        return get_pdf_loader(file_path)
    elif file_type == 'csv':
        return get_csv_loader(file_path)
    elif file_type== 'txt':
        return get_csv_loader
    elif file_type == 'xlsx':
        return get_xlsx_loader
    else:
        return None

async def process_file(file_path,openai_api_key=os.getenv("OPENAI_API_KEY")):

    loader = get_file_loader(file_path)

    if loader:

        pages = await loader.aload()
        document_text = "".join([page.page_content for page in pages])

        # Split the document into chunks
        text_splitter = SemanticChunker(OpenAIEmbeddings(api_key=openai_api_key,model="text-embedding-3-large"))
        chunks = text_splitter.create_documents([document_text])

        return chunks
    else:
        return "Invalid File"


# Function to send document chunks (with embeddings) to the Qdrant vector database
async def send_to_pinecone(documents, embedding_model,namespace=None,pinecone_api_key=os.getenv("PINECONE_API_KEY")):
    """Send the document chunks to the Qdrant vector database."""
    try:
        pc = await PineconeVectorStore.afrom_documents(
            documents,
            embedding_model,
            api_key=pinecone_api_key,
            kwargs={"namespace":namespace}
  
        )
        return pc
    except Exception as ex:
        print(f"Failed to store data in the vector DB: {str(ex)}")
        return False


# Function to initialize the Qdrant client and return the vector store object
def pinecone_client(namespace=None,index_name=os.getenv("PINECONE_INDEX_NAME"),openai_api_key=os.getenv("OPENAI_API_KEY")):
    """Initialize Qdrant client and return the vector store."""

    embeddings = OpenAIEmbeddings(model="text-embedding-3-large",api_key=openai_api_key)
    pinecone_store = PineconeVectorStore(index=index_name, embedding=embeddings,namespace=namespace)

    return pinecone_store



