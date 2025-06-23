import tkinter as tk
from universal_turing_machine import UniversalTuringMachine

def run_simulation():
    trans_code = trans_input.get("1.0", tk.END).strip()
    input_code = word_input.get("1.0", tk.END).strip()
    mtu = UniversalTuringMachine(trans_code, input_code)
    accepted = mtu.run()
    output.delete("1.0", tk.END)
    output.insert(tk.END, f"{'✔ Accepté' if accepted else '✘ Rejeté'}\n")
    output.insert(tk.END, f"Tête → {mtu.head}\nÉtat final : {mtu.state}\nRuban :\n")
    output.insert(tk.END, ''.join(mtu.tape))

root = tk.Tk()
root.title("Machine de Turing Universelle")

tk.Label(root, text="Encodage des transitions").pack()
trans_input = tk.Text(root, height=5, width=60)
trans_input.pack()

tk.Label(root, text="Encodage du mot d'entrée").pack()
word_input = tk.Text(root, height=2, width=60)
word_input.pack()

tk.Button(root, text="Exécuter", command=run_simulation).pack()

output = tk.Text(root, height=8, width=60)
output.pack()

root.mainloop()
