import streamlit as st
import requests
import time
from requests.utils import quote
from db_handler import create_conversation, get_user_conversations, save_message

# Fonction pour appeler l'API backend
def response_generator(prompt):
    encoded_prompt = quote(prompt, safe="")
    response = requests.get(f"http://localhost:8000/llm/{encoded_prompt}")
    response_text = response.json().get("answer", "Erreur : aucune réponse reçue.")
    for word in response_text.split():
        yield word + " "
        time.sleep(0.03)  # Un peu plus rapide pour fluidité


def response_generator_rag_with_history(prompt, history):
    url = "http://localhost:8000/rag_with_memory"
    payload = {"question": prompt, "history": history}
    response = requests.post(url, json=payload)
    response_text = response.json().get("answer", "Erreur : aucune réponse reçue.")
    for word in response_text.split():
        yield word + " "
        time.sleep(0.03)



# CONFIG
st.set_page_config(page_title="🤖 Chatbot Nutrition", layout="wide")
st.markdown("## 🤖 Chatbot Nutrition & Cuisine")
st.markdown("---")

# AUTH
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "guest_mode" not in st.session_state:
    st.session_state.guest_mode = False

if not st.session_state.authenticated:
    st.switch_page("pages/home.py")
    st.stop()

# CHARGEMENT des conversations en BDD
if st.session_state.authenticated and not st.session_state.guest_mode:
    if "sessions" not in st.session_state:
        st.session_state.sessions = {}
        st.session_state.conversation_ids = {}

        conversations = get_user_conversations(st.session_state["email"])
        for conv in conversations:
            if conv.messages:
                st.session_state.sessions[conv.title] = [
                    {"role": msg.role, "content": msg.content} for msg in conv.messages
                ]
                st.session_state.conversation_ids[conv.title] = conv.id

# INIT état par défaut
if "sessions" not in st.session_state:
    st.session_state.sessions = {}
if "current_session" not in st.session_state:
    st.session_state.current_session = "Chat 1"
if "conversation_ids" not in st.session_state:
    st.session_state.conversation_ids = {}

# SIDEBAR – Historique et gestion des sessions
with st.sidebar:
    st.markdown("### 💬 Historique")
    session_names = list(st.session_state.sessions.keys())
    if session_names:
        selected = st.selectbox("Sélectionner un chat :", session_names,
                                index=session_names.index(st.session_state.current_session)
                                if st.session_state.current_session in session_names else 0)
        st.session_state.current_session = selected

    if st.button("➕ Nouveau Chat", use_container_width=True):
        existing = list(st.session_state.sessions.keys())
        i = 1
        while f"Chat {i}" in existing:
            i += 1
        new_title = f"Chat {i}"
        st.session_state.sessions[new_title] = []
        st.session_state.current_session = new_title
        st.rerun()
    


    st.markdown("---")
    st.caption("👤 Connecté en tant que :")
    st.write(st.session_state.get("email", "Invité"))

    st.markdown("### ⚙️ Mode d'interaction")
    mode = st.radio("Choisir un mode :", ["Standard", "RAG"], index=0)


    # 🔐 Bouton admin visible uniquement pour l'admin
    if st.session_state.get("role") == "admin":
        st.markdown("---")
        st.markdown("### 🔐 Zone Admin")
        if st.button("➕ Ajouter des documents"):
            st.switch_page("pages/Ajout_de_documents.py")  # Tu dois créer ce fichier

    st.markdown("---")
    if st.button("🚪 Déconnexion", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.switch_page("pages/Connexion.py")


# AFFICHAGE des messages
messages = st.session_state.sessions.get(st.session_state.current_session, [])

if not messages:
    st.info("Commencez une nouvelle conversation en posant une question ci-dessous. 🍏")
else:
    for msg in messages:
        avatar = "🤖" if msg["role"] == "assistant" else "🧑"
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])

# INPUT utilisateur
prompt = st.chat_input("Posez votre question...")

if prompt:
    # Ajout message utilisateur
    st.session_state.sessions[st.session_state.current_session].append(
        {"role": "user", "content": prompt}
    )

    # Création en DB si nouveau
    conv_title = st.session_state.current_session
    if not st.session_state.guest_mode and conv_title not in st.session_state.conversation_ids:
        conv_id = create_conversation(st.session_state["email"], title=conv_title)
        st.session_state.conversation_ids[conv_title] = conv_id
    else:
        conv_id = st.session_state.conversation_ids.get(conv_title)

    # Sauvegarde prompt
    if not st.session_state.guest_mode and conv_id:
        save_message(conv_id, "user", prompt)

    with st.chat_message("user", avatar="🧑"):
        st.markdown(prompt)

    # Générer la réponse
    with st.chat_message("assistant", avatar="🤖"):
        if mode == "RAG":
            history = st.session_state.sessions[conv_title][:-1]
            response = st.write_stream(response_generator_rag_with_history(prompt, history))
        else:
            response = st.write_stream(response_generator(prompt))



    # Sauvegarde réponse
    st.session_state.sessions[conv_title].append({"role": "assistant", "content": response})
    if not st.session_state.guest_mode and conv_id:
        save_message(conv_id, "assistant", response)
