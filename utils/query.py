from langchain_deepseek import ChatDeepSeek
from langchain_chroma import Chroma
from chromadb.config import Settings
from langchain.schema import SystemMessage, HumanMessage  # Importação correta
from utils.embeddings import get_local_embeddings
from dotenv import load_dotenv
import os

load_dotenv()

def query_codebase(question):
    print(f"Iniciando query_codebase com a pergunta: {question}")
    try:
        print("Obtendo embeddings locais...")
        embeddings = get_local_embeddings()
        print("Embeddings obtidos.")

        # Configurações para conectar ao servidor Chroma
        chroma_settings = Settings(
            chroma_server_host="localhost",
            chroma_server_http_port=8000
        )
        print("Carregando o vector store do Chroma na URL: http://localhost:8000")
        vector_store = Chroma(
            embedding_function=embeddings,
            collection_name="codebase_v3",
            client_settings=chroma_settings
        )
        print("Vector store carregado.")

        print("Executando similarity search para a pergunta...")
        # reranker = CohereEmbeddings(model_name="rerank-english-v2.0")
        # relevant_docs = reranker.rerank(vector_store.similarity_search(query=question, k=20), top_k=5)
        relevant_docs = vector_store.similarity_search(query=question, k=5)
        print(f"Similarity search concluída. Documentos encontrados: {relevant_docs}")

        # Monta o contexto com os documentos encontrados
        context = "\n\n".join(
            f"[Documento {i+1}]\nArquivo: {doc.metadata.get('source')}\nTrecho:\n{doc.page_content}"
            for i, doc in enumerate(relevant_docs)
        )
        print(f"Contexto construído:\n{context}")

        print("Configurando ChatDeepSeek...")
        llm = ChatDeepSeek(
            model="deepseek-chat",
            temperature=0,
            max_tokens=1500,
            timeout=None,
            max_retries=2,
            top_p=0.95,
            api_key=os.getenv("DEEPSEEK_API_KEY"),
        )

        if context:
            system_content = (
                f"Você é um expert em código. Analise o contexto abaixo e responda de forma concisa e técnica:\n\n{context}"
            )
        else:
            system_content = "Você é um expert em código. Responda de forma técnica mesmo sem contexto adicional."

        messages = [
            SystemMessage(content=system_content),
            HumanMessage(content=f"Questão: {question}\nInstruções:\n        - Seja conciso e técnico\n        - Referencie arquivos quando relevante")
        ]

        print("Enviando mensagem para o LLM...")
        response = llm.invoke(messages)
        print("Resposta recebida do LLM.")
        return response.content
    except Exception as error:
        print(f"Erro na consulta: {error}")
        raise Exception(f"Falha ao processar a consulta. Detalhes: {error}")
