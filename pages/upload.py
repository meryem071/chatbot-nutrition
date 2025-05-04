import streamlit as st
import os
from pdf_to_faiss import add_pdf_to_faiss
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings

DB_PATH = "faiss_database"

def load_db():
    return FAISS.load_local(DB_PATH, HuggingFaceEmbeddings(model_name="intfloat/multilingual-e5-small"),
                            allow_dangerous_deserialization=True)

st.set_page_config(page_title="Ajouter des documents", initial_sidebar_state='collapsed')


# Use CSS to hide the sidebar and its control button
st.markdown(
"""
<style>
[data-testid="stSidebar"] {
display: none;
}
[data-testid="collapsedControl"] {
display: none;
}
</style>
""",
unsafe_allow_html=True
)
st.title("📥 Ajout de Documents PDF")




# Sécurité : réservé à l'admin
if st.session_state.get("role") != "admin":
    st.error("Accès réservé à l'administrateur.")
    st.stop()

uploaded_files = st.file_uploader("Sélectionner des fichiers PDF", type="pdf", accept_multiple_files=True)

if uploaded_files and st.button("Ajouter à la base de données"):
    os.makedirs("temp", exist_ok=True)
    db = load_db()
    for file in uploaded_files:
        temp_path = os.path.join("temp", file.name)
        with open(temp_path, "wb") as f:
            f.write(file.getbuffer())
        db = add_pdf_to_faiss(temp_path, db)
        st.success(f"✅ {file.name} ajouté avec succès.")
    db.save_local(DB_PATH)

if st.button("⬅️ Retour à ma session"):
    st.switch_page("frontend.py")