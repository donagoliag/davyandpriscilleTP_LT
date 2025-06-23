import streamlit as st
from simulators7 import palindrome, unary_add, unary_sub, unary_mul, unary_div

def main():
    st.title("🧠 Machines spécialisées")

    option = st.selectbox("🧮 Choisir une machine :", [
        "Reconnaissance de palindrome",
        "Addition unaire",
        "Soustraction unaire",
        "Multiplication unaire",
        "Division unaire"
    ])

    user_input = st.text_input("🔤 Entrée (unaire, ex: 111#11 pour 3 et 2)", value="")

    if st.button("▶️ Exécuter") and user_input.strip():
        if option == "Reconnaissance de palindrome":
            result = palindrome.is_palindrome(user_input)
            st.success("✔ Mot accepté !" if result else "❌ Mot rejeté")
        elif option == "Addition unaire":
            st.write("Résultat :", unary_add.compute(user_input))
        elif option == "Soustraction unaire":
            st.write("Résultat :", unary_sub.compute(user_input))
        elif option == "Multiplication unaire":
            st.write("Résultat :", unary_mul.compute(user_input))
        elif option == "Division unaire":
            q, r = unary_div.compute(user_input)
            st.write(f"Quotient : {q}   Reste : {r}")
    else:
        st.info("Entrez une chaîne et cliquez sur Exécuter.")

if __name__ == "__main__":
    main()
