from fastapi import FastAPI, HTTPException
import uvicorn
from llm import ask_llm
from pydantic import BaseModel
from rag_handler import query_with_rag

from db_handler import save_user

app = FastAPI()

# Route qui utilise le modèle réel via llm.py
@app.get("/llm/{prompt}")
async def get_llm_response(prompt: str):
    try:
        # Appelle directement la fonction ask_llm définie dans llm.py
        response = ask_llm(prompt)
        return {"answer": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

from rag_handler import query_with_rag

class RAGRequest(BaseModel):
    question: str
    history: list  # [{"role": ..., "content": ...}]

@app.post("/rag_with_memory")
async def rag_with_memory(data: RAGRequest):
    try:
        answer = query_with_rag(data.question, history=data.history)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/rag/{question}")
async def rag_search(question: str):
    try:
        answer = query_with_rag(question)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Route simple de test (optionnelle)
@app.get("/")
def root():
    return {"message": "Bienvenue sur l'API intégrée avec le LLM !"}

class RegisterRequest(BaseModel):
    email: str
    password: str

@app.post("/register")
async def register_user(data: RegisterRequest):
    try:
        success = save_user(data.email, data.password)
        if success:
            return {"message": "Utilisateur enregistré"}
        else:
            raise HTTPException(status_code=409, detail="Utilisateur déjà existant")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
