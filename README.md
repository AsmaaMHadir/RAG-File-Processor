# 📄 Document GPT - FastAPI Backend

Credits to Shaheryar Yousaf for original source code.
Expanding on his work to allow supporting larger datasets

This FastAPI backend serves as the core API for handling document uploads, processing PDF files, embedding document content into a vector database , and allowing users to ask questions based on the uploaded document. The AI model uses OpenAI's embeddings to generate intelligent responses from the document content.

### 🛠️ Features
 - **PDF Upload:** Upload PDF files to be processed and stored in a vector database  for querying.
 - **Question & Answer System:** Users can ask questions based on the content of the uploaded PDF.
 - **API Documentation:** Automatic API documentation available through Swagger at /docs.

### 📦 Libraries Used
 - **FastAPI:** For building the web API.
 - **Pinecone Client:** For storing and retrieving document embeddings.
 - **LangChain:** For handling PDF processing and embeddings.
 - **OpenAI:** For generating embeddings and AI model responses.
 - **PyPDFLoader:** For extracting text from PDF files.
 - **CORS Middleware:** For handling Cross-Origin Resource Sharing (CORS) to allow frontend requests from different domains.
 - **dotenv:** For managing environment variables (e.g., API keys).

### 🗂️ Project Structure
 - ```app.py```: Main FastAPI application file containing the API endpoints for PDF upload and question-answer system.
 - ```utils.py```: Contains utility functions for processing PDF files, sending embeddings to the vector DB, and retrieving answers from the embeddings.
 - **Environment Variables:** API keys for OpenAI and Pinecone are provided with the request

## 🚀 Getting Started

### Prerequisites
Before setting up the FastAPI backend, ensure you have the following installed:
 - Python 3.7+
 - Pip (Python package manager)
 - Pinecone
 - OpenAI API Key (for generating embeddings and responses)
 - Virtual environment (optional but recommended)

### 🛠️ Installation & Setup
Follow these steps to set up the FastAPI backend on your local machine:

#### Step 1: Clone the Repository
```
git clone <repo-url>
cd <repo-name>
```

#### Step 2: Set Up a Virtual Environment
It is recommended to create a virtual environment to manage the dependencies:
```
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### Step 3: Install Dependencies
Install the required dependencies using ```pip```:
```
pip install -r requirements.txt
```



#### Step 5: Run the FastAPI Application
Start the FastAPI server locally by running the following command:
```
uvicorn app:app --reload
```
This will start the server at ```http://127.0.0.1:8000/```.

#### Step 6: Test the API on Swagger UI
FastAPI automatically generates API documentation, accessible through Swagger.
Open your browser and navigate to: ```http://127.0.0.1:8000/docs```

Here you can test both API endpoints directly:
 - ```/process-file/```: process file of any of these types: csv, pdf, xlsx, docx, txt
