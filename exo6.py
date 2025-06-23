import streamlit as st
from simulators6 import machin_de_turing 
from simulators6.machin_de_turing import creer_machine_addition_unaire,creer_machine_anbn,creer_machine_palindromes

# Interface Streamlit

def main():
    st.title("🔧 Simulateur de Machine de Turing")
    st.markdown("---")
    
    # Sidebar pour la sélection de la machine
    st.sidebar.header("Configuration")
    
    machine_type = st.sidebar.selectbox(
        "Choisir une machine prédéfinie:",
        ["Palindromes", "a^n b^n", "Addition unaire", "Personnalisée"]
    )
    
    # Créer la machine selon le choix
    if machine_type == "Palindromes":
        machine = creer_machine_palindromes()
        st.info("🔍 Machine sélectionnée: Reconnaissance de palindromes")
        exemples = ["aba", "abba", "a", "", "abc", "abcba"]
    elif machine_type == "a^n b^n":
        machine = creer_machine_anbn()
        st.info("🔍 Machine sélectionnée: Reconnaissance de {aⁿbⁿ | n ≥ 0}")
        exemples = ["", "ab", "aabb", "aaabbb", "aab", "abb"]
    elif machine_type == "Addition unaire":
        machine = creer_machine_addition_unaire()
        st.info("🔍 Machine sélectionnée: Addition en unaire")
        exemples = ["1+1", "11+1", "1+11", "111+11"]
    else:
        st.warning("🚧 Mode personnalisé non implémenté dans cette version")
        return
    
    # Interface principale
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📝 Entrée")
        
        # Exemples rapides
        st.subheader("Exemples rapides:")
        cols = st.columns(3)
        for i, exemple in enumerate(exemples):
            with cols[i % 3]:
                if st.button(f"'{exemple}'" if exemple else "'ε' (vide)", key=f"ex_{i}"):
                    st.session_state.mot_test = exemple
        
        # Saisie manuelle
        mot_test = st.text_input(
            "Mot à tester:", 
            value=st.session_state.get('mot_test', ''),
            help="Entrez le mot à tester (laissez vide pour la chaîne vide)"
        )
        
        max_etapes = st.slider("Nombre maximum d'étapes:", 10, 2000, 500)
        
        if st.button("🚀 Exécuter", type="primary"):
            with st.spinner("Exécution en cours..."):
                resultat = machine.executer(mot_test, max_etapes)
                st.session_state.resultat = resultat
    
    with col2:
        st.header("📊 Résultats")
        
        if 'resultat' in st.session_state:
            resultat = st.session_state.resultat
            
            # Résultat principal
            if resultat['accepte']:
                st.success(f"✅ **Mot accepté** en {resultat['nb_etapes']} étapes")
            else:
                raison = resultat.get('raison', 'État non final atteint')
                st.error(f"❌ **Mot rejeté** après {resultat['nb_etapes']} étapes\n\nRaison: {raison}")
            
            # Informations détaillées
            st.subheader("Informations détaillées:")
            info_col1, info_col2 = st.columns(2)
            with info_col1:
                st.metric("État final", resultat['etat_final'])
                st.metric("Nombre d'étapes", resultat['nb_etapes'])
            with info_col2:
                st.text("Ruban final:")
                st.code(resultat['ruban_final'] if resultat['ruban_final'] else "ε (vide)")
    
    # Trace d'exécution
    if 'resultat' in st.session_state and st.session_state.resultat['trace']:
        st.markdown("---")
        st.header("🔍 Trace d'exécution")
        
        trace = st.session_state.resultat['trace']
        
        # Option pour afficher la trace complète ou pas à pas
        mode_trace = st.radio("Mode d'affichage:", ["Tableau complet", "Animation pas à pas"], horizontal=True)
        
        if mode_trace == "Tableau complet":
            # Affichage sous forme de tableau
            st.subheader("Trace complète:")
            trace_data = []
            for etape in trace:
                trace_data.append({
                    "Étape": etape['etape'],
                    "État": etape['etat'],
                    "Symbole lu": etape['symbole_lu'],
                    "Position": etape['position'],
                    "Configuration du ruban": etape['ruban']
                })
            st.dataframe(trace_data, use_container_width=True)
            
        else:
            # Animation pas à pas
            st.subheader("Animation pas à pas:")
            
            if 'etape_courante' not in st.session_state:
                st.session_state.etape_courante = 0
            
            col1, col2, col3 = st.columns([1, 2, 1])
            
            with col1:
                if st.button("⏮️ Début"):
                    st.session_state.etape_courante = 0
                if st.button("⏪ Précédent") and st.session_state.etape_courante > 0:
                    st.session_state.etape_courante -= 1
            
            with col3:
                if st.button("⏩ Suivant") and st.session_state.etape_courante < len(trace) - 1:
                    st.session_state.etape_courante += 1
                if st.button("⏭️ Fin"):
                    st.session_state.etape_courante = len(trace) - 1
            
            # Affichage de l'étape courante
            etape_actuelle = trace[st.session_state.etape_courante]
            
            st.info(f"**Étape {etape_actuelle['etape']}** | État: {etape_actuelle['etat']} | "
                   f"Symbole lu: '{etape_actuelle['symbole_lu']}' | Position: {etape_actuelle['position']}")
            
            # Affichage du ruban avec mise en évidence
            st.code(etape_actuelle['ruban'], language=None)
            
            # Barre de progression
            progress = st.session_state.etape_courante / (len(trace) - 1) if len(trace) > 1 else 0
            st.progress(progress)
            st.caption(f"Étape {st.session_state.etape_courante + 1} / {len(trace)}")

if __name__ == "__main__":
    main()
