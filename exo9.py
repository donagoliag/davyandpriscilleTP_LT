import streamlit as st
from simulators9.universal_turing_machine import UniversalTuringMachine

def main():
    st.title("🧠 Machine de Turing Universelle (MTU)")
    st.markdown("Simulateur web d'une MT universelle encodée (alphabet unaire)")

    st.subheader("1️⃣ Encodage de la machine (transitions)")
    trans_code = st.text_area("Encodage binaire des transitions", height=150)

    st.subheader("2️⃣ Entrée à traiter (encodée)")
    input_code = st.text_input("Encodage binaire du mot", value="1")

    accept_states = st.text_input("États acceptants (unaire, séparés par `,`)", value="111")

    if st.button("🚀 Exécuter la simulation"):
        if not trans_code.strip():
            st.error("Tu dois saisir un encodage de transitions.")
        else:
            accept_list = [s.strip() for s in accept_states.split(',')]
            mtu = UniversalTuringMachine(trans_code.strip(), input_code.strip(), accept_states=accept_list)
            accepted = mtu.run()
            st.success("✔ Accepté !" if accepted else "❌ Rejeté")
            st.markdown(f"**Ruban final** : `{''.join(mtu.tape)}`")
            st.markdown(f"**Position de la tête** : {mtu.head}")
            st.markdown(f"**État final** : {mtu.state}")

if __name__ == "__main__":
    main()
