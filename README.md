# RAG-Document-Assistant
This project implements a Retrieval-Augmented Generation (RAG) system that can retrieve relevant information from large documents (such as technical manuals, legal documents, or reports) and generate accurate answers to specific questions.
By combining document retrieval with a language model, the system provides enhanced information retrieval and generation capabilities.

## The main components include:

A document preprocessor that breaks down large documents into smaller, searchable chunks and turns them into embeddings using the distilroberta model.
A retrieval mechanism that retrieves the most relevant information based on a user query.
A generative model (flan T5) that generates answers based on the retrieved information.

## Requirements
Software Requirements:
Docker (for containerization)
Python 3.9+ (for local development)
Required Python libraries (see requirements.txt):
You can install the dependencies manually by running:

## Docker Setup
Clone the repository:
git clone https://github.com/blackdoll12/RAG-Document-Assistant.git
Go to the main folder
cd document-assistant-rag
Build the Docker image:
docker build -t rag-document-assistant .

Once the image is built, you can run the container:

docker run  rag-document-assistant
This will start the application inside the container and execute the src/main.py file.

## Running the Program

The system can be run using command-line arguments. You can run the program in two modes: default mode (using predefined documents) and custom mode (where you provide your own document and question).

Default Mode: In this mode, the program will process a default document (LinearAlgebra.txt) and retrieve answers for a predefined set of questions.

To run the program in default mode:

docker run --rm rag-document-assistant 
Custom Mode: In custom mode, you provide your own document file (in text format) and the specific question you want to ask.

If you want to use a file from your host machine (e.g., a custom PDF file), you can mount the file into the container using the -v flag:

docker run --rm -v /path/on/host:/app/data rag-document-assistant python src/main.py --file_path /app/data/MyDocument.txt --question "What is a matrix?"

