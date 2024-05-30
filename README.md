
# Multi-Document Agent

This project sets up a Flask application that uses Azure OpenAI and HuggingFace embeddings to provide querying and summarization tools for multiple PDF documents. The application is containerized using Docker and leverages Gunicorn as the WSGI server.

## Features

- Load and process multiple PDF documents.
- Use Azure OpenAI for querying and summarization.
- Expose a REST API to handle queries over the documents.

## Prerequisites

- Docker
- Docker Compose (optional, for easier management of Docker containers)

## Setup

### 1. Clone the Repository

```
git clone https://github.com/your-username/multi-document-agent.git
cd multi-document-agent
```
2. Environment Variables
Create a .env file in the root directory with the following content:

```
AZURE_OPENAI_LLM_MODEL_NAME=your-model-name
AZURE_OPENAI_CHAT_DEPLOYMENT_NAME=your-deployment-name
AZURE_OPENAI_API_KEY=your-api-key
AZURE_OPENAI_ENDPOINT=your-endpoint
AZURE_OPENAI_API_VERSION=your-api-version
AZURE_OPENAI_ENGINE=your-engine
```
3. Build and Run the Docker Container
Build the Docker Image
```
docker build -t multi-document-agent .
```
Run the Docker Container
```
docker run -it --rm -p 8000:8000 --name running-agent multi-document-agent
```
API Usage
Query Endpoint
URL: /query
Method: POST
Content-Type: application/json
Body: JSON object containing the query.
Example Request
```
curl -X POST http://localhost:8000/query -H "Content-Type: application/json" -d '{"query": "Tell me about the evaluation dataset used in LongLoRA, and then tell me about the evaluation results"}'
```
Example Response
```
{
    "response": "..."
}
```
Project Structure
```
multi-document-agent/
├── app.py                 # Main application file
├── utils.py               # Utility functions, including get_doc_tools
├── requirements.txt       # Python dependencies
├── Dockerfile             # Dockerfile for containerizing the application
├── download_papers.sh     # Shell script to download PDF documents
├── .env                   # Environment variables (not included in git)
├── .gitignore             # Git ignore file
└── README.md              # This README file
```
