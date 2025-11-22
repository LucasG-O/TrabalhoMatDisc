# ARQUIVO: cenario.py
import networkx as nx
import random

# --- PREFERÊNCIAS ---
CENARIOS = {
    "Mais Rápida":       {"w_d": 0.1, "w_t": 0.8, "w_r": 0.1},
    "Mais Segura":       {"w_d": 0.1, "w_t": 0.1, "w_r": 0.8},
    "Mais Curta (Base)": {"w_d": 0.8, "w_t": 0.1, "w_r": 0.1},
}

# --- PARÂMETROS GERAIS ---
SIMULACAO_PARAMS = {
    "fator_congest": 1.5,
    "risco_extra": 5
}

# --- CENÁRIO 1: DIDÁTICO (6 VÉRTICES) ---
def criar_cenario_didatico():
    """Retorna (Grafo, Posicoes, Aresta_Problema, Start, End)"""
    G = nx.DiGraph()
    nodes = ['A', 'B', 'C', 'D', 'E', 'F']
    G.add_nodes_from(nodes)

    edges_data = [
        ('A', 'B', {'distancia': 3.0, 'tempo_base': 5, 'risco_base': 1}),
        ('A', 'C', {'distancia': 7.0, 'tempo_base': 10, 'risco_base': 2}),
        ('B', 'D', {'distancia': 4.0, 'tempo_base': 6, 'risco_base': 1}),
        ('C', 'E', {'distancia': 6.0, 'tempo_base': 8, 'risco_base': 3}),
        ('D', 'F', {'distancia': 5.0, 'tempo_base': 7, 'risco_base': 1}),
        ('E', 'F', {'distancia': 2.0, 'tempo_base': 3, 'risco_base': 4}),
        ('B', 'E', {'distancia': 1.0, 'tempo_base': 2, 'risco_base': 1}),
        ('D', 'C', {'distancia': 3.0, 'tempo_base': 4, 'risco_base': 2})
    ]
    G.add_edges_from([(u, v, data) for u, v, data in edges_data])
    
    # Define layout específico para este grafo
    pos = nx.spring_layout(G, seed=42)
    
    return G, pos, ('B', 'D'), 'A', 'F'

# --- CENÁRIO 2: COMPLEXO (20+ VÉRTICES) ---
def criar_cenario_complexo(linhas=4, colunas=5):
    """Retorna (Grafo, Posicoes, Aresta_Problema, Start, End)"""
    grid = nx.grid_2d_graph(linhas, colunas)
    G = nx.DiGraph()
    
    # Renomear para números
    mapping = {node: i for i, node in enumerate(grid.nodes())}
    grid = nx.relabel_nodes(grid, mapping)
    
    for u, v in grid.edges():
        for origem, destino in [(u,v), (v,u)]:
            dist = random.uniform(0.5, 2.0)
            tempo = dist * random.uniform(1.5, 3.0)
            risco = random.randint(1, 3)
            G.add_edge(origem, destino, 
                       distancia=dist, tempo_base=tempo, tempo_atual=tempo, 
                       risco_base=risco, risco_atual=risco)
            
    # Define layout específico para grade 
    pos = nx.kamada_kawai_layout(G)
    
    # Define problema no meio da cidade (ex: aresta entre nó 7 e 8)
    # Em um grid 4x5, o meio é por volta do 7, 8, 12, 13.
    aresta_problema = (7, 8) 
    
    # Inicio e Fim (Canto a Canto)
    start = 0
    end = (linhas * colunas) - 1
    
    return G, pos, aresta_problema, start, end
