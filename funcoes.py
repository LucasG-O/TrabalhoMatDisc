import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd

# --- LÓGICA MATEMÁTICA (UNIVERSAL) ---
def calcular_custo(distancia, tempo, risco, w_d, w_t, w_r):
    """
    Calcula o custo escalar da aresta com base nos pesos de prioridade.
    w_d + w_t + w_r deve ser idealmente igual a 1 para normalização.
    """
    soma = w_d + w_t + w_r
    if soma != 1.0 and soma != 0:
        w_d, w_t, w_r = w_d/soma, w_t/soma, w_r/soma
    return (distancia * w_d) + (tempo * w_t) + (risco * w_r)

def atualizar_pesos_dinamicamente(G, fator_congest, fator_risco, aresta_critica=None):
    """
    Percorre qualquer grafo G e atualiza os pesos 'tempo_atual' e 'risco_atual'.
    """
    for u, v, data in G.edges(data=True):
        # Simula variação natural (90% a 110%)
        variacao = np.random.uniform(0.9, 1.1)
        data['tempo_atual'] = data['tempo_base'] * fator_congest * variacao
        data['risco_atual'] = data['risco_base']
        
        # Aplica evento de caos se a aresta bater com a crítica
        if aresta_critica and (u, v) == aresta_critica:
            data['risco_atual'] += fator_risco
            data['tempo_atual'] *= 1.5 
            
    return G

# --- ALGORITMO DE BUSCA (UNIVERSAL) ---
def encontrar_rota_otima(G, start, end, w_d, w_t, w_r):
    # 1. Calcula custos nas arestas
    for u, v, data in G.edges(data=True):
        data['custo_final'] = calcular_custo(
            data['distancia'], data['tempo_atual'], data['risco_atual'], w_d, w_t, w_r
        )
    
    # 2. Executa Dijkstra
    try:
        rota = nx.dijkstra_path(G, start, end, weight='custo_final')
        custo = nx.dijkstra_path_length(G, start, end, weight='custo_final')
        return rota, custo
    except nx.NetworkXNoPath:
        return None, float('inf')

# --- VISUALIZAÇÃO (GENÉRICA) ---
def plotar_rota(G, pos, rota, titulo, mostrar_rotulos=True):
    """
    Agora recebe 'pos'. O core não decide mais como desenhar,
    ele apenas desenha onde mandaram.
    """
    plt.figure(figsize=(10, 6))
    
    # Desenha nós e arestas base
    nx.draw(G, pos, with_labels=True, node_color='lightgray', edge_color='gray', 
            node_size=500, font_size=9, arrows=True)
    
    # Desenha a rota destacada
    if rota:
        path_edges = list(zip(rota, rota[1:]))
        nx.draw_networkx_nodes(G, pos, nodelist=rota, node_color='orange', node_size=500)
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=3, arrows=True)
    
    # Rótulos (opcional, pois em grafos grandes polui)
    if mostrar_rotulos:
        edge_labels = { (u,v): f"{d['tempo_atual']:.1f}" for u,v,d in G.edges(data=True) if 'tempo_atual' in d}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)
    
    plt.title(titulo)
    plt.show()

# --- RELATÓRIOS (GENÉRICOS) ---
def plotar_comparacao(resultados):
    df = pd.DataFrame(resultados)
    
    # Se não houver dados, não plota
    if df.empty:
        return

    # Configurar gráfico de barras agrupadas
    labels = df["Cenário"]
    x = np.arange(len(labels))
    width = 0.25

    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Barras (Verifica se as colunas existem antes de plotar)
    if "Tempo" in df.columns:
        rects1 = ax.bar(x - width, df["Tempo"], width, label='Tempo (min)', color='salmon')
        ax.bar_label(rects1, padding=3, fmt='%.1f')
        
    if "Distancia" in df.columns:
        rects2 = ax.bar(x, df["Distancia"], width, label='Distância (km)', color='skyblue')
        ax.bar_label(rects2, padding=3, fmt='%.1f')
        
    if "Risco" in df.columns:
        rects3 = ax.bar(x + width, df["Risco"], width, label='Risco', color='lightgreen')
        ax.bar_label(rects3, padding=3, fmt='%.1f')

    ax.set_ylabel('Valores')
    ax.set_title('Comparativo de Trade-offs por Cenário')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    fig.tight_layout()
    print("Gráfico de comparação gerado.")
    plt.show()

def gerar_tabela_latex(resultados):
    df = pd.DataFrame(resultados)
    cols = ["Cenário", "Rota", "Tempo", "Distancia", "Risco"]
    # Filtra colunas se elas existirem
    cols_existentes = [c for c in cols if c in df.columns]
    
    print("\n--- CÓDIGO LATEX ---")
    print(df[cols_existentes].to_latex(index=False, float_format="%.2f"))
    print("--------------------\n")