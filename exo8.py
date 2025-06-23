# exo8.py
import streamlit as st
from simulators8.tm_2tape_palindrome import run as run_palindrome
from simulators8.tm_3tape_sort import run as run_sort
from benchmarks.compare import compare_versions

def display_trace(trace):
    """Affiche la trace de manière élégante"""
    st.subheader("🔍 Trace d'exécution")
    with st.expander("Voir les détails d'exécution"):
        for step in trace:
            if step == "---":
                st.divider()
            else:
                st.write(step)

def main():
    st.title("🧠 Simulateur de Machine de Turing à k rubans")
    
    st.markdown("""
    <style>
        .stTextInput input {font-family: monospace;}
        .ruban-display {background-color: #f0f2f6; padding: 10px; border-radius: 5px; 
                        font-family: monospace; margin: 5px 0;}
        .header {color: #1e88e5;}
        .success-box {background-color: #e6f7e6; padding: 10px; border-radius: 5px;}
        .error-box {background-color: #ffebee; padding: 10px; border-radius: 5px;}
    </style>
    """, unsafe_allow_html=True)

    task = st.selectbox("📌 Choisir une machine :", [
        "Reconnaissance L = {w#w} à 2 rubans",
        "Tri de nombres à 3 rubans",
        "Comparaison 1 ruban vs k rubans"
    ])

    if task == "Reconnaissance L = {w#w} à 2 rubans":
        st.markdown("""
        **Langage L = {w#w | w ∈ {0,1}*}**  
        Entrez un mot binaire avec un # au milieu (ex: `101#101`)
        """)
        input_data = st.text_input("Mot à tester:", value="101#101")
    elif task == "Tri de nombres à 3 rubans":
        st.markdown("""
        **Tri d'une liste de nombres**  
        Entrez des nombres séparés par des espaces (ex: `5 2 7 1`)
        """)
        input_data = st.text_input("Liste à trier:", value="5 2 7 1")
    else:
        st.markdown("""
        **Comparaison de performance**  
        Entrez un mot pour comparer les versions 1 ruban et 2 rubans
        """)
        input_data = st.text_input("Mot à tester:", value="101#101")

    if st.button("▶ Exécuter") and input_data.strip():
        if task == "Reconnaissance L = {w#w} à 2 rubans":
            result, trace = run_palindrome(input_data)
            if result:
                st.markdown("<div class='success-box'>✅ <b>Résultat:</b> Le mot est accepté</div>", 
                          unsafe_allow_html=True)
            else:
                st.markdown("<div class='error-box'>❌ <b>Résultat:</b> Le mot est rejeté</div>", 
                          unsafe_allow_html=True)
            display_trace(trace)
        
        elif task == "Tri de nombres à 3 rubans":
            sorted_out, trace = run_sort(input_data)
            if isinstance(sorted_out, list):
                st.markdown("<div class='success-box'>📊 <b>Résultat trié:</b></div>", 
                          unsafe_allow_html=True)
                st.write(sorted_out)
                display_trace(trace)
            else:
                st.error(sorted_out)
        
        elif task == "Comparaison 1 ruban vs k rubans":
            report = compare_versions(input_data)
            st.subheader("⏱ Comparaison de performance")
            col1, col2 = st.columns(2)
            col1.metric("1 ruban", report["Temps 1 ruban"])
            col2.metric("2 rubans", report["Temps 2 rubans"])
            st.write(report["Conclusion"])

if __name__ == "__main__":
    main()