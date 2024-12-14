from langchain_huggingface import HuggingFacePipeline,HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from transformers import pipeline
from langchain.prompts import PromptTemplate
import torch

def extract_text(text_file_path):
    """
    Extracts text from a plain text file.

    Args:
        text_file_path (str): Path to the text file.

    Returns:
        str: The text extracted from the file.
    """
    with open(text_file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return text


def text2chunks(text, chunk_size=300, overlap=100):

    """
         Splits the text into chunks

        Args:
            text: the text
            chunk_size : size of each chunk (number of characters)
            overlap: the number of characters tolerated as overlap

        Returns:
            List[str]: A list of chunks obtained
        """
    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n"],
        chunk_size=chunk_size,
        chunk_overlap=overlap,
        length_function=len,
        add_start_index=True,
    )
    return text_splitter.split_text(text)


def vectorsore_builder(chunks, embedding_model_name = "sentence-transformers/all-distilroberta-v1"):
    """
     Uses a model to encode each chunk and builds  FAISS vector store with the embeddings

        Args:
            chunks: list of chunks to be embedded
            embedding_model_name: the name of the model used to encode each chunk
            

        Returns:
            FAISS: The vector store
     """
    embeddings = HuggingFaceEmbeddings(model_name=embedding_model_name)
    vector_store = FAISS.from_texts(chunks, embeddings)
    return vector_store

 
def qa_pipeline(vector_store):
    """
     Create the RetrievalQA pipeline using the vectorstore

        Args:
            vector_store: the vector store
            

        Returns:
            the qa chain
     """
   

    
        
    device = 0 if torch.cuda.is_available() else -1
    model_name = "google/flan-t5-xl" if torch.cuda.is_available() else "google/flan-t5-base"
    

    # Initialize the text generation pipeline
    hf_pipeline = pipeline("text2text-generation", model=model_name, device=device, max_length=1000, pad_token_id=50256)
    llm = HuggingFacePipeline(pipeline=hf_pipeline)

    
    retriever = vector_store.as_retriever(search_kwargs={"k": 5})  # Retrieve 5 documents

    #prompt template
    rawprompt = (
        "You are an assistant for question-answering tasks. Use the following context to answer the question. If the answer is not in the context, say 'I don't know.' "
        "Answer in concise language, with no more than three sentences. "
        "Context: {context}\nQuestion: {question}\nAnswer:"
    )
    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template=rawprompt
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",  
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": prompt}
    )

    return qa_chain
def preprocess_document(path):
    """
    Preprocesses the document by extracting text, splitting it into chunks,
    and building a vector store.

    Args:
        pdf_path (str): The path to the PDF document.

    Returns:
        obj: The QA pipeline ready to handle questions about the document.
    """
    text = extract_text(path)
    chunks = text2chunks(text)
    vector_store = vectorsore_builder(chunks)
    qa = qa_pipeline(vector_store)
    return qa