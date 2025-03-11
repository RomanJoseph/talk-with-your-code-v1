from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from chromadb.config import Settings
from embeddings import get_local_embeddings
from math import ceil
import sys

def print_progress(iteration, total, bar_length=50):
    progress = int(bar_length * (iteration / total))
    bar = "█" * progress + "-" * (bar_length - progress)
    sys.stdout.write(f"\r[{bar}] {iteration}/{total} ({(iteration/total)*100:.2f}%)")
    sys.stdout.flush()

def ingest_codebase():
    print("Iniciando ingestão do codebase...")
    print("Configurando DirectoryLoader para carregar arquivos do diretório './codebase'...")
    loader = DirectoryLoader("./codebase", glob="**/*")
    docs = loader.load()
    print(f"Documentos carregados: {len(docs)}")
    
    print("Configurando RecursiveCharacterTextSplitter...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=256,
        chunk_overlap=100,
        separators=["\n\n", "\n", ";", "}", "]", ")", " "]
    )

    batch_size = 5
    total_batches = (len(docs) + batch_size - 1) // batch_size
    vector_store = None

    for i in range(0, len(docs), batch_size):
        batch = docs[i:i+batch_size]
        split_docs = splitter.split_documents(batch)
        current_batch_number = (i // batch_size) + 1
        print_progress(current_batch_number, total_batches)
        
        if i == 0:
            chroma_settings = Settings(
                chroma_server_host="localhost",
                chroma_server_http_port=8000
            )
            vector_store = Chroma.from_documents(
                split_docs,
                embedding=get_local_embeddings(),
                collection_name="codebase_v3",
                client_settings=chroma_settings
            )
        else:
            vector_store.add_documents(split_docs)
    
    print("\nIngestão do codebase concluída.")
    return vector_store

if __name__ == "__main__":
    ingest_codebase()
