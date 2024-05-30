from flask import Flask, request, jsonify
from flask_cors import CORS
from threading import Lock
from llama_index.core import SimpleDirectoryReader, Settings, StorageContext, VectorStoreIndex
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.readers.file import PDFReader
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.azure_openai import AzureOpenAI
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core import get_response_synthesizer
from llama_index.core.agent import FunctionCallingAgentWorker, AgentRunner
from pathlib import Path
import os
import logging
import json
from dotenv import load_dotenv
from utils import get_doc_tools

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Configuration for global settings using HuggingFace Embeddings
embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5", trust_remote_code=True)
Settings.embed_model = embed_model

# Initialize the Azure language model with corrected parameters
model = AzureOpenAI(
    model=os.getenv('AZURE_OPENAI_LLM_MODEL_NAME'),
    deployment_name=os.getenv('AZURE_OPENAI_CHAT_DEPLOYMENT_NAME'),
    api_key=os.getenv('AZURE_OPENAI_API_KEY'),
    azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT'),
    api_version=os.getenv('AZURE_OPENAI_API_VERSION'),
    engine=os.getenv('AZURE_OPENAI_ENGINE')
)

# Define the directory containing the papers
papers_dir = 'papers'

# Initialize document tools for each paper
def initialize_tools():
    papers = [
        "metagpt.pdf",
        "longlora.pdf",
        "loftq.pdf",
        "swebench.pdf",
        "selfrag.pdf",
        "zipformer.pdf",
        "values.pdf",
        "finetune_fair_diffusion.pdf",
        "knowledge_card.pdf",
        "metra.pdf",
        "vr_mcl.pdf"
    ]

    paper_to_tools_dict = {}
    for paper in papers:
        logger.debug(f"Getting tools for paper: {paper}")
        vector_tool, summary_tool = get_doc_tools(f"{papers_dir}/{paper}", Path(paper).stem)
        paper_to_tools_dict[paper] = [vector_tool, summary_tool]

    initial_tools = [t for paper in papers for t in paper_to_tools_dict[paper]]

    return initial_tools

logger.info("Initializing tools and agent...")
initial_tools = initialize_tools()
agent_worker = FunctionCallingAgentWorker.from_tools(initial_tools, llm=model, verbose=True)
agent = AgentRunner(agent_worker)
logger.info("Initialization complete. Server is ready to accept requests.")

@app.route('/query', methods=['POST'])
def query_agent():
    query = request.json.get('query')
    if not query:
        return jsonify({'error': 'Query parameter is required'}), 400
    
    logger.debug(f"Received query: {query}")
    response = agent.query(query)
    logger.debug(f"Response: {response}")
    return jsonify({'response': str(response)})

if __name__ == '__main__':
    logger.info("Starting server...")
    app.run(host='0.0.0.0', port=8000)
