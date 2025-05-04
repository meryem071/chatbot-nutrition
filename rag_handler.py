from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

import torch
from llm import ask_llm

def get_embedding_model():
    return HuggingFaceEmbeddings(
        model_name="intfloat/multilingual-e5-small",
        model_kwargs={"device": torch.device("cuda" if torch.cuda.is_available() else "cpu")},
        encode_kwargs={"normalize_embeddings": True},
    )

def load_faiss(db_path="faiss_database"):
    embeddings = get_embedding_model()
    return FAISS.load_local(db_path, embeddings, allow_dangerous_deserialization=True)

def query_with_rag(question: str, history: list = None, k: int = 3, db_path="faiss_database"):
    """
    Génère une réponse en mode RAG avec ajout du contexte conversationnel (history).
    - `history` : liste de messages [{"role": "user"|"assistant", "content": "..."}]
    """

    # 1. Recherche de documents similaires
    db = load_faiss(db_path)
    docs = db.similarity_search(question, k=k)
    context = "\n\n".join([doc.page_content for doc in docs])

    # 2. Construire l'historique (chat memory simulée)
    history_prompt = ""
    if history:
        for msg in history:
            role = "Utilisateur" if msg["role"] == "user" else "Assistant"
            history_prompt += f"{role} : {msg['content']}\n"

    # 3. Prompt enrichi avec historique + contexte RAG
    enriched_prompt = f"""Tu es un assistant nutrition et cuisine. Voici la conversation précédente :

    {history_prompt}

    Voici des informations provenant de documents :
    {context}

    Nouvelle question : {question}

    Réponds de manière claire, utile et en français.
    """

    return ask_llm(enriched_prompt)

