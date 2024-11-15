from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os

from utils import process_file,send_to_pinecone,  OpenAIEmbeddings

app = FastAPI()


# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=False,
    allow_methods=["*"],  # Allow all methods (POST, GET, etc.)

)

# Define a model for the question API
class FileProcessingRequest(BaseModel):
    file_path: str
    namespace: str = None     
    openai_api_key : str = os.getenv("OPENAI_API_KEY")
    pinecone_api_key : str = os.getenv("PINECONE_API_KEY")

# Endpoint to upload a PDF and process it, sending to Qdrant
@app.post("/process-file/")
async def process_pdf(processingReq : FileProcessingRequest):
    """
    Endpoint to process a file and store in the vector DB.
    """
    try:

        # Process the PDF to get document chunks and embeddings
        document_chunks = await process_file(processingReq.file_path)

        embedding_model = OpenAIEmbeddings(
            openai_api_key=processingReq.openai_api_key,  # Assuming you're using env vars
            model="text-embedding-3-large"
        )

        # Send the document chunks (with embeddings) to Qdrant
        pinecone_vector_store = await send_to_pinecone(document_chunks, embedding_model,namespace=processingReq.namespace,pinecone_api_key=processingReq.pinecone_api_key)


        if pinecone_vector_store:
            return {"message": "file successfully processed and stored in vector DB","vector store":pinecone_vector_store}
        else:
            raise HTTPException(status_code=500, detail="Failed to store file in vector DB")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process file: {str(e)}")


# A simple health check endpoint
@app.get("/")
async def health_check():
    return {"status": "Success"}

