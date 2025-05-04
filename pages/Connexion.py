import streamlit as st
from db_handler import authenticate_user
import time
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(page_title="Connexion - Chatbot",initial_sidebar_state="collapsed")
# Set page configuration to collapse the sidebar initially

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

st.title("Page de connexion")

col1, _, col2 = st.columns([10,1,10])
with col1:
    st.write("")
    st.image("data/ChatGPT Image 9 avr. 2025, 14_57_47.png")

with col2:
    email = st.text_input("E-mail")
    password = st.text_input("Mot de passe", type="password")

    if st.button("Connexion"):
        time.sleep(2)
        if not (email and password):
            st.error("Veuillez entrer votre e-mail et mot de passe")
        elif authenticate_user(email, password):
            st.session_state['authenticated'] = True
            st.session_state['guest_mode'] = False
            st.session_state['email'] = email

            # 🎯 Définir le rôle selon l'e-mail
            if email == "admin@test.com":  # Remplace par l'adresse réelle de l'admin
                st.session_state['role'] = "admin"
            else:
                st.session_state['role'] = "user"

            st.success("Connexion réussie !")
            st.switch_page("Ma_session.py")

        else:
            st.error("Identifiant de connexion invalide")

    if st.button("Créer un compte"):
        st.switch_page("pages/Inscription.py")  
