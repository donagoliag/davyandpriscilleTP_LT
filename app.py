import streamlit as st
from PIL import Image

# Configuration de la page
st.set_page_config(
    page_title="TP : Langage et traducteurs",
    page_icon="🧠",
    layout="wide"
)

# CSS personnalisé
st.markdown("""
<style>
    .sidebar .sidebar-content {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    .sidebar .sidebar-content .sidebar-title {
        color: white !important;
        font-size: 24px !important;
    }
    .nav-button {
        background-color: #4CAF50 !important;
        color: white !important;
        margin: 5px 0;
        padding: 10px;
        border-radius: 5px;
        text-align: center;
        font-weight: bold;
    }
    .nav-button:hover {
        background-color: #45a049 !important;
    }
    .title-container {
        background: linear-gradient(90deg, #EAECFF 0%, #EAECFF 100%);
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar - Navigation
with st.sidebar:
    st.title("🧠 Menu de Navigation")
    
    col1, col2 = st.columns([1,3])
    
    st.markdown("### TP : Langage et traducteurs")
    st.markdown("*Exercices 6 à 10*")
    
    st.markdown("---")
    
    # Boutons de navigation
    if st.button("🏠 Page d'Accueil", key="home", use_container_width=True, 
                help="Retour à la page principale"):
        st.session_state.current_page = "home"
    
    st.markdown("**Exercices :**")
    for i in range(6, 11):
        if st.button(f"Exercice {i}", key=f"exo{i}", use_container_width=True, 
                    type="primary" if st.session_state.get("current_page") == f"exo{i}" else "secondary"):
            st.session_state.current_page = f"exo{i}"

# Page courante
current_page = st.session_state.get("current_page", "home")

# Contenu principal
if current_page == "home":
    st.markdown('<div class="title-container"><h1>TP : Langage et traducteurs</h1></div>', 
               unsafe_allow_html=True)
    
    st.markdown("""
    ## Bienvenue !
    
    Sélectionnez un exercice dans le menu de gauche pour voir les différentes implémentations :
    
    - **Exercice 6** : Simulateur de machine de Turing
    - **Exercice 7** :  Machines spécialisées
    - **Exercice 8** : Machine de Turing à k rubans
    - **Exercice 9** : Machine de Turing universelle
    - **Exercice 10** : Analyse comparative
    
    """)
    
    
elif current_page.startswith("exo"):
    exo_num = current_page[3:]  # Récupère le numéro (6 à 10)
    st.markdown(f'<div class="title-container"><h1>Exercice {exo_num}</h1></div>', 
               unsafe_allow_html=True)
    
    # Import dynamique de l'exercice
    try:
        module = __import__(f"exo{exo_num}")
        module.main()  # Supposons que chaque fichier exo a une fonction main()
    except ImportError:
        st.error(f"Le fichier exo{exo_num}.py n'a pas été trouvé")
    except AttributeError:
        st.error(f"La fonction main() n'existe pas dans exo{exo_num}.py")