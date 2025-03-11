from transformers import AutoTokenizer
from langchain_community.embeddings import HuggingFaceEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()

#microsoft/graphcodebert-base
#bigcode/starcoder
def get_local_embeddings():
    print("Initializing HuggingFaceEmbeddings...")
    embeddings_instance = HuggingFaceEmbeddings(
         model_name="microsoft/graphcodebert-base",
         model_kwargs={"token": os.getenv("HF_TOKEN")}
    )
    
    st_model = embeddings_instance.client
    if st_model.tokenizer.pad_token is None:
        st_model.tokenizer.pad_token = st_model.tokenizer.eos_token
        print("Patched SentenceTransformer tokenizer with pad_token:", st_model.tokenizer.pad_token)
    
    print("HuggingFaceEmbeddings initialized.")
    return embeddings_instance