import streamlit as st
from streamlit_extras.switch_page_button import switch_page

# Set page configuration to collapse the sidebar initially
st.set_page_config(initial_sidebar_state='collapsed')

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
st.title("Bienvenue sur NutriBot")
st.markdown("""
Bienvenue sur **NutriBot**, votre assistant intelligent dédié à la **cuisine** et à la **nutrition** !

Explorez nos fonctionnalités :
- Posez des questions sur la nutrition
- Découvrez des recettes équilibrées
- Obtenez des conseils personnalisés

**Choisissez un mode d'utilisation ci-dessous :**
""")

col1, col2 = st.columns(2)

with col1:
    if st.button("🧪 Tester sans compte"):
        st.session_state["guest_mode"] = True
        st.session_state["authenticated"] = True
        st.switch_page("Ma_session.py")
        st.rerun()

with col2:
    if st.button("🔐 Connexion / Inscription"):
        st.session_state["guest_mode"] = False
        st.session_state["authenticated"] = False
        st.switch_page("pages/Connexion.py")
        st.rerun()
