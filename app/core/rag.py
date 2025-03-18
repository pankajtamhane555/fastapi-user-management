import os
import warnings
import logging
from typing import List
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from io import BytesIO
import pdfplumber

load_dotenv()
warnings.filterwarnings('ignore')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def process_pdf_from_bytes(pdf_bytes):
    """Process a PDF from bytes and split it into text chunks."""
    chunks = []
    
    with pdfplumber.open(BytesIO(pdf_bytes)) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            if text:
                chunks.append(Document(page_content=text, metadata={"page": i + 1}))

    # Split text into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    
    return text_splitter.split_documents(chunks)

def add_chunks_to_chroma(chunks: List[Document]):
    """Load the existing vector store and add new documents."""
    vector_store = get_vector_store()
    
    if vector_store:
        print("Adding new chunks to existing ChromaDB.")
        try:
            vector_store.add_documents(chunks)  # ✅ Efficiently add new docs
            vector_store.persist()  # Save changes
            logger.info("Documents successfully added to ChromaDB.")
        except Exception as e:
            logger.error(f"Error adding documents to ChromaDB: {e}")
    else:
        logger.error("No vector database found. Upload and process a PDF first.")

def get_vector_store():
    """Load the existing ChromaDB vector store."""
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    try:
        vector_store = Chroma(
            persist_directory="./chroma_db",
            embedding_function=embeddings
        )
        return vector_store
    except Exception as e:
        logger.error(f"Error loading ChromaDB: {e}")
        return None