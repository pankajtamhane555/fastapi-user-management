import os
import pytest
from fastapi.testclient import TestClient
from app.api.v1.endpoints.rag import router
from fastapi import FastAPI
from dotenv import load_dotenv
from unittest.mock import patch

# Load environment variables from .env file
load_dotenv()

app = FastAPI()
app.include_router(router)

client = TestClient(app)

@pytest.fixture(scope="module")
def set_groq_api_key():
    os.environ["GROQ_API_KEY"] = "test_groq_api_key"
    yield
    del os.environ["GROQ_API_KEY"]

def test_upload_pdf(set_groq_api_key):
    # Ensure the sample.pdf file exists in the tests directory
    sample_pdf_path = "tests/sample.pdf"
    assert os.path.exists(sample_pdf_path), f"{sample_pdf_path} does not exist."

    with open(sample_pdf_path, "rb") as pdf_file:
        response = client.post("/upload_pdf/", files={"file": ("sample.pdf", pdf_file, "application/pdf")})
    assert response.status_code == 200
    assert response.json() == {"message": "PDF processed successfully", "filename": "sample.pdf"}

def test_ask_question_no_vector_db(set_groq_api_key):
    response = client.post("/ask_question/", data={"question": "What is the content of the PDF?"})
    assert response.status_code == 400
    assert response.json() == {"detail": "No vector database found. Upload and process a PDF first."}