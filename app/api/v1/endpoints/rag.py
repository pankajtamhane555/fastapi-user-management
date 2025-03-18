from fastapi import APIRouter, File, UploadFile, Form, HTTPException
from app.core.rag import process_pdf_from_bytes, add_chunks_to_chroma, get_vector_store

import os
from langchain_groq import ChatGroq
from langchain.chains.retrieval_qa.base import RetrievalQA

router = APIRouter()

@router.post("/upload_pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    """Endpoint to upload and process a PDF (without saving to disk)."""
    pdf_bytes = await file.read()  # Read file as bytes
    chunks = process_pdf_from_bytes(pdf_bytes)  # Process bytes into chunks
    add_chunks_to_chroma(chunks)  # Store chunks in ChromaDB

    return {"message": "PDF processed successfully", "filename": file.filename}

@router.post("/ask_question/")
async def ask_question(question: str = Form(...)):
    """Endpoint to ask a question based on the uploaded PDF."""
    vector_store = get_vector_store()  # Load the existing DB

    if vector_store is None:
        raise HTTPException(status_code=400, detail="No vector database found. Upload and process a PDF first.")

    retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 2})

    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    if not GROQ_API_KEY:
        raise HTTPException(status_code=500, detail="Missing GROQ_API_KEY in environment variables")

    llm = ChatGroq(
        model="llama3-70b-8192",
        temperature=0.1,
        groq_api_key=GROQ_API_KEY
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm, 
        chain_type="stuff", 
        retriever=retriever,
        return_source_documents=True
    )

    response = qa_chain.invoke({"query": question})
    
    return {
        "question": question,
        "answer": response['result'],
        "sources": [f"Page {doc.metadata['page']}" for doc in response['source_documents']]
    }