import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import time
from simulators10.tmsim import NondeterministicTuringMachine, DeterministicTuringMachine

def benchmark(trans_d, trans_nd, input_gen, max_len=50, step=5, trials=3):
    results = []
    for length in range(10, max_len + 1, step):
        input_data = input_gen(length)
        dt_stats = []
        nd_stats = []
        
        for _ in range(trials):
            # Machine déterministe
            dtm = DeterministicTuringMachine(trans_d)
            start = time.perf_counter()
            dt_result = dtm.simulate(input_data)
            dt_time = (time.perf_counter() - start) * 1000
            
            # Machine non-déterministe
            ndtm = NondeterministicTuringMachine(trans_nd)
            start = time.perf_counter()
            nd_result = ndtm.simulate(input_data)
            nd_time = (time.perf_counter() - start) * 1000
            
            dt_stats.append(dt_time)
            nd_stats.append({
                'time': nd_time,
                'paths': nd_result['paths_explored']
            })
        
        avg_dt = sum(dt_stats) / trials
        avg_nd = sum(x['time'] for x in nd_stats) / trials
        avg_paths = sum(x['paths'] for x in nd_stats) / trials
        
        results.append({
            'Length': length,
            'DT_time_ms': avg_dt,
            'ND_time_ms': avg_nd,
            'ND_paths': avg_paths,
            'Time_ratio': avg_nd / avg_dt if avg_dt > 0 else float('inf'),
            'Paths_per_char': avg_paths / length if length > 0 else 0
        })
    
    return pd.DataFrame(results)

def main():
    st.title("Analyse d'explosion combinatoire des machines de Turing")
    
    # Configuration
    col1, col2 = st.columns(2)
    with col1:
        max_len = st.slider("Taille maximale d'entrée", 10, 100, 50)
        mode = st.selectbox("Langage à tester", ["0ⁿ1ⁿ", "Palindrome", "Aléatoire"])
    with col2:
        trials = st.slider("Nombre d'essais par point", 1, 10, 3)
        step = st.select_slider("Pas d'incrémentation", options=[1, 5, 10])
    
    # Définition des machines
    if mode == "0ⁿ1ⁿ":
        trans_d = {
            ('q0', '0'): ('q1', 'X', 'R'),
            ('q1', '0'): ('q1', '0', 'R'),
            ('q1', '1'): ('q2', 'Y', 'L'),
            ('q2', '0'): ('q2', '0', 'L'),
            ('q2', 'X'): ('q0', 'X', 'R'),
            ('q0', 'Y'): ('q0', 'Y', 'R'),
            ('q0', '_'): ('q_accept', '_', 'S')
        }
        
        trans_nd = {
            ('q0', '0'): [('q0', '0', 'R'), ('q1', 'X', 'R')],
            ('q1', '0'): [('q1', '0', 'R')],
            ('q1', '1'): [('q2', 'Y', 'L')],
            ('q2', '0'): [('q2', '0', 'L')],
            ('q2', 'X'): [('q0', 'X', 'R')],
            ('q0', 'Y'): [('q0', 'Y', 'R')],
            ('q0', '_'): [('q_accept', '_', 'S')]
        }
        
        def input_gen(n):
            return '0'*(n//2) + '1'*(n//2)
    
    elif mode == "Palindrome":
        trans_d = {
            ('q0', '0'): ('q1', 'X', 'R'),
            ('q0', '1'): ('q2', 'Y', 'R'),
            ('q1', '0'): ('q1', '0', 'R'),
            ('q1', '1'): ('q1', '1', 'R'),
            ('q1', '_'): ('q3', '_', 'L'),
            ('q3', '0'): ('q4', 'X', 'L'),
            ('q4', '0'): ('q4', '0', 'L'),
            ('q4', '1'): ('q4', '1', 'L'),
            ('q4', 'X'): ('q0', 'X', 'R'),
            ('q2', '0'): ('q2', '0', 'R'),
            ('q2', '1'): ('q2', '1', 'R'),
            ('q2', '_'): ('q3', '_', 'L'),
            ('q3', '1'): ('q4', 'Y', 'L'),
            ('q4', 'Y'): ('q0', 'Y', 'R'),
            ('q0', 'X'): ('q0', 'X', 'R'),
            ('q0', 'Y'): ('q0', 'Y', 'R'),
            ('q0', '_'): ('q_accept', '_', 'S')
        }
        
        trans_nd = {
            ('q0', '0'): [('q0', '0', 'R'), ('q1', 'X', 'R')],
            ('q0', '1'): [('q0', '1', 'R'), ('q2', 'Y', 'R')],
            ('q1', '0'): [('q1', '0', 'R')],
            ('q1', '1'): [('q1', '1', 'R')],
            ('q1', '_'): [('q3', '_', 'L')],
            ('q3', '0'): [('q4', 'X', 'L')],
            ('q4', '0'): [('q4', '0', 'L')],
            ('q4', '1'): [('q4', '1', 'L')],
            ('q4', 'X'): [('q0', 'X', 'R')],
            ('q2', '0'): [('q2', '0', 'R')],
            ('q2', '1'): [('q2', '1', 'R')],
            ('q2', '_'): [('q3', '_', 'L')],
            ('q3', '1'): [('q4', 'Y', 'L')],
            ('q4', 'Y'): [('q0', 'Y', 'R')],
            ('q0', 'X'): [('q0', 'X', 'R')],
            ('q0', 'Y'): [('q0', 'Y', 'R')],
            ('q0', '_'): [('q_accept', '_', 'S')]
        }
        
        def input_gen(n):
            half = n//2
            return '01'*half + ('0' if n%2 else '')
    
    else:  # Mot aléatoire
        trans_d = {
            ('q0', '0'): ('q0', '0', 'R'),
            ('q0', '1'): ('q0', '1', 'R'),
            ('q0', '_'): ('q_accept', '_', 'S')
        }
        
        trans_nd = {
            ('q0', '0'): [('q0', '0', 'R'), ('q1', '0', 'R')],
            ('q0', '1'): [('q0', '1', 'R'), ('q1', '1', 'R')],
            ('q1', '0'): [('q1', '0', 'R')],
            ('q1', '1'): [('q1', '1', 'R')],
            ('q1', '_'): [('q_accept', '_', 'S')]
        }
        
        def input_gen(n):
            import random
            return ''.join(random.choice('01') for _ in range(n))
    
    if st.button("Lancer l'analyse"):
        with st.spinner("Calcul en cours..."):
            df = benchmark(trans_d, trans_nd, input_gen, max_len, step, trials)
            
            # Visualisation
            st.subheader("📈 Résultats d'analyse")
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
            
            # Graphique des temps
            ax1.plot(df['Length'], df['DT_time_ms'], 'b-', label='Déterministe')
            ax1.plot(df['Length'], df['ND_time_ms'], 'r-', label='Non-déterministe')
            ax1.set_yscale('log')
            ax1.set_title("Temps d'exécution (ms, échelle log)")
            ax1.legend()
            
            # Graphique des chemins
            ax2.plot(df['Length'], df['ND_paths'], 'g-')
            ax2.set_yscale('log')
            ax2.set_title("Chemins explorés (ND, échelle log)")
            
            st.pyplot(fig)
            
            # Données brutes
            st.subheader("📊 Données complètes")
            st.dataframe(df.style.format({
                'DT_time_ms': '{:.2f}',
                'ND_time_ms': '{:.2f}',
                'Time_ratio': '{:.1f}',
                'Paths_per_char': '{:.1e}'
            }))

if __name__ == "__main__":
    main()