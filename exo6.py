import streamlit as st
from simulators6.machin_de_turing import MachineDeTuring
def main():
    st.title("🎮 Simulateur de Machine de Turing")

    # Style CSS personnalisé
    st.markdown("""
    <style>
        .stTextInput input {font-family: monospace;}
        .stTextArea textarea {font-family: monospace !important;}
        .ruban-display {background-color: #f0f2f6; padding: 10px; border-radius: 5px; 
                        font-family: monospace; margin: 5px 0;}
        .etat-display {color: #ff4b4b; font-weight: bold;}
        .header {color: #1e88e5;}
        .success-box {background-color: #e6f7e6; padding: 10px; border-radius: 5px;}
        .error-box {background-color: #ffebee; padding: 10px; border-radius: 5px;}
    </style>
    """, unsafe_allow_html=True)

    if 'exo6_result' not in st.session_state:
        st.session_state.exo6_result = None

    # Machines prédéfinies
    def get_machine_anbn():
        return MachineDeTuring(
            etats={'q0', 'q1', 'q2', 'q3', 'qf'},
            alphabet_entree={'a', 'b'},
            alphabet_travail={'a', 'b', 'X', 'Y', '_'},
            transitions={
                ('q0', 'a'): ('q1', 'X', 'R'),
                ('q1', 'a'): ('q1', 'a', 'R'),
                ('q1', 'b'): ('q2', 'Y', 'L'),
                ('q2', 'a'): ('q2', 'a', 'L'),
                ('q2', 'X'): ('q0', 'X', 'R'),
                ('q0', 'Y'): ('q0', 'Y', 'R'),
                ('q0', '_'): ('qf', '_', 'S')
            },
            etat_initial='q0',
            etats_finaux={'qf'}
        )

    def get_machine_palindrome():
        return MachineDeTuring(
            etats={'q0', 'q1', 'q2', 'q3', 'q4', 'qf'},
            alphabet_entree={'a', 'b'},
            alphabet_travail={'a', 'b', 'X', 'Y', '_'},
            transitions={
                ('q0', 'a'): ('q1', 'X', 'R'),
                ('q0', 'b'): ('q2', 'Y', 'R'),
                ('q0', '_'): ('qf', '_', 'S'),
                ('q1', 'a'): ('q1', 'a', 'R'),
                ('q1', 'b'): ('q1', 'b', 'R'),
                ('q1', '_'): ('q3', '_', 'L'),
                ('q3', 'a'): ('q4', 'X', 'L'),
                ('q4', 'a'): ('q4', 'a', 'L'),
                ('q4', 'b'): ('q4', 'b', 'L'),
                ('q4', 'X'): ('q0', 'X', 'R'),
                ('q2', 'a'): ('q2', 'a', 'R'),
                ('q2', 'b'): ('q2', 'b', 'R'),
                ('q2', '_'): ('q3', '_', 'L'),
                ('q3', 'b'): ('q4', 'Y', 'L'),
                ('q4', 'Y'): ('q0', 'Y', 'R')
            },
            etat_initial='q0',
            etats_finaux={'qf'}
        )

    def get_machine_addition():
        return MachineDeTuring(
            etats={'q0', 'q1', 'q2', 'qf'},
            alphabet_entree={'1', '+'},
            alphabet_travail={'1', '+', '_'},
            transitions={
                ('q0', '1'): ('q0', '1', 'R'),
                ('q0', '+'): ('q1', '_', 'R'),
                ('q1', '1'): ('q1', '1', 'R'),
                ('q1', '_'): ('q2', '1', 'L'),
                ('q2', '1'): ('q2', '1', 'L'),
                ('q2', '_'): ('qf', '_', 'S')
            },
            etat_initial='q0',
            etats_finaux={'qf'}
        )

    def display_trace(machine):
        """Affiche la trace d'exécution de manière élégante"""
        st.subheader("🔍 Trace d'exécution")
        
        for i, step in enumerate(machine.trace):
            ruban = step['ruban']
            pos = step['position']
            
            # Affichage stylisé du ruban avec position
            st.markdown(f"**Étape {i}** - État: <span class='etat-display'>{step['etat']}</span>", 
                        unsafe_allow_html=True)
            
            # Création de la représentation visuelle du ruban
            ruban_display = ruban[:pos] + f"<span style='background-color: #ffcc80;'>[{ruban[pos] if pos < len(ruban) else '_'}]</span>" + ruban[pos+1:]
            st.markdown(f"<div class='ruban-display'>{ruban_display}</div>", 
                    unsafe_allow_html=True)
            
            st.caption(f"Symbole lu: '{step['symbole_courant']}'")

    # Interface principale
    with st.sidebar:
        st.header("⚙️ Configuration")
        test_choice = st.radio(
            "Langage à tester:",
            ("aⁿbⁿ", "Palindromes", "Addition unaire"),
            index=0
        )

        if test_choice == "aⁿbⁿ":
            default_input = "aaabbb"
            description = "Langage {aⁿbⁿ | n ≥ 0}"
        elif test_choice == "Palindromes":
            default_input = "abba"
            description = "Palindromes sur {a,b}*"
        else:
            default_input = "111+11"
            description = "Addition en unaire"

        st.markdown(f"**Description:** {description}")

    # Colonnes principales
    col1, col2 = st.columns([1, 2])

    with col1:
        st.header("📥 Entrée")
        user_input = st.text_input(
            "Mot à tester:", 
            value=default_input,
            key=f"input_{test_choice}"
        )
        
        if st.button("🚀 Exécuter la simulation", use_container_width=True):
            with st.spinner("Simulation en cours..."):
                try:
                    # Initialisation de la machine
                    if test_choice == "aⁿbⁿ":
                        machine = get_machine_anbn()
                    elif test_choice == "Palindromes":
                        machine = get_machine_palindrome()
                    else:
                        machine = get_machine_addition()
                    
                    # Exécution
                    result = machine.executer(user_input)
                    
                    with col2:
                        st.header("📊 Résultats")
                        
                        # Onglets pour les résultats
                        tab_trace, tab_config = st.tabs(["Trace d'exécution", "Configuration machine"])
                        
                        with tab_config:
                            st.subheader("⚙️ Configuration de la machine")
                            st.json({
                                "États": sorted(list(machine.etats)),
                                "Alphabet d'entrée": sorted(list(machine.alphabet_entree)),
                                "Alphabet de travail": sorted(list(machine.alphabet_travail)),
                                "État initial": machine.etat_initial,
                                "États finaux": sorted(list(machine.etats_finaux)),
                                "Symbole vide": machine.symbole_vide,
                                "Nombre de transitions": len(machine.transitions)
                            })
                        
                        with tab_trace:
                            display_trace(machine)
                        
                        # Affichage du résultat
                        st.divider()
                        if result:
                            st.markdown("<div class='success-box'>✅ <b>Résultat:</b> Le mot est <span style='color:green'>accepté</span> par la machine!</div>", 
                                    unsafe_allow_html=True)
                        else:
                            st.markdown("<div class='error-box'>❌ <b>Résultat:</b> Le mot est <span style='color:red'>rejeté</span> par la machine!</div>", 
                                    unsafe_allow_html=True)
                
                except ValueError as e:
                    st.error(f"Erreur: {str(e)}")

    # Section d'exemples
    with st.expander("💡 Exemples prédéfinis - Cliquez pour voir"):
        if test_choice == "aⁿbⁿ":
            st.markdown("""
            **Exemples valides:**
            - `""` (mot vide)
            - `"ab"`
            - `"aabb"`
            - `"aaabbb"`
            
            **Exemples invalides:**
            - `"a"`
            - `"aab"`
            - `"abb"`
            - `"ba"`
            """)
        elif test_choice == "Palindromes":
            st.markdown("""
            **Exemples valides:**
            - `""` (mot vide)
            - `"a"`
            - `"aba"`
            - `"abba"`
            - `"babbab"`
            
            **Exemples invalides:**
            - `"ab"`
            - `"aab"`
            - `"abb"`
            """)
        else:
            st.markdown("""
            **Exemples valides:**
            - `"1+1"` → `"111"`
            - `"11+11"` → `"111111"`
            - `"111+1"` → `"11111"`
            
            **Exemples invalides:**
            - `"+11"`
            - `"11+"`
            - `"111++11"`
            """)

if __name__ == "__main__":
    main()