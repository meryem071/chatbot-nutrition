import streamlit as st
import re
from db_handler import save_user, verify_duplicate_user
import time


st.set_page_config(page_title="Inscription", initial_sidebar_state="collapsed")


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

def is_valid_email(email):
    """Check if the provided email is valid using regex."""
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None

def input_field(input_param, type):
    """Render an input field based on the type and store the value in session state."""
    if type == 'text':
        st.session_state[input_param] = st.text_input(input_param)
    elif type == 'number':
        st.session_state[input_param] = st.number_input(input_param, step=1)

def signup_page(extra_input_params=False, confirmPass=False):
    """Render the signup page with optional extra input parameters and password confirmation."""

    if st.button("Retour à la connexion"):
        st.switch_page("pages\login_page.py")


    with st.empty().container(border=True):
        st.title("Page d'inscription")

        # Email input with validation
        st.session_state['email'] = st.text_input("Adresse email")
        if st.session_state['email'] and not is_valid_email(st.session_state['email']):
            st.error("Veuillez entrer une adresse email valide")

        # Password input
        st.session_state['password'] = st.text_input("Mot de passe", type='password')

        # Confirm password if required
        if confirmPass:
            confirm_password = st.text_input("Confirmer le mot de passe", type='password')

        # Extra input fields if any
        if extra_input_params:
            for input_param, type in st.session_state['extra_input_params'].items():
                input_field(input_param, type)

        # Validate all required fields before proceeding
        if st.session_state['email'] and st.session_state['password'] and \
           (not confirmPass or (confirmPass and st.session_state['password'] == confirm_password)):

            if extra_input_params and not all(st.session_state.get(param) for param in st.session_state['extra_input_params']):
                st.error("Veuillez remplir tous les champs requis")
            else:
                if st.button("S'inscrire"):
                    if verify_duplicate_user(st.session_state['email']):
                        st.error("L'utilisateur existe déjà")
                    else:
                        save_user(st.session_state['email'], st.session_state['password'], st.session_state.get('extra_input_params', {}))
                        st.success("Inscription réussie !")
                        time.sleep(1)
                        st.switch_page("pages/login_page.py")  
        else:
            if confirmPass and st.session_state['password'] != confirm_password:
                st.error("Les mots de passe ne correspondent pas")
            elif st.button("S'inscrire"):
                st.error("Veuillez remplir tous les champs requis")

if __name__ == "__main__" or "__streamlit__":
    signup_page(confirmPass=True)
