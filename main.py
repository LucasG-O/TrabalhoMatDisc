import matplotlib.pyplot as plt
import funcoes
import cenario

def executar_simulacao_visual(titulo, dados_cenario):
    """
    Executa uma rodada única e mostra o mapa (Gráfico de Rede).
    """
    # Desempacota os dados que vieram do cenario
    G, pos, aresta_caos, start, end = dados_cenario
    
    print(f"\n=== RODANDO VISUALIZAÇÃO: {titulo} ===")
    
    # 1. Aplica o Caos (Uma única instância de 'dia ruim')
    G_dinamico = funcoes.atualizar_pesos_dinamicamente(
        G.copy(), 
        cenario.SIMULACAO_PARAMS['fator_congest'],
        cenario.SIMULACAO_PARAMS['risco_extra'],
        aresta_critica=aresta_caos
    )
    
    resultados = []
    
    # 2. Roda para cada perfil
    for nome_perfil, pesos in cenario.CENARIOS.items():
        rota, custo = funcoes.encontrar_rota_otima(
            G_dinamico, start, end, 
            pesos['w_d'], pesos['w_t'], pesos['w_r']
        )
        
        if rota:
            # Coleta métricas
            tempo_real = sum(G_dinamico[u][v]['tempo_atual'] for u, v in zip(rota[:-1], rota[1:]))
            dist_real = sum(G_dinamico[u][v]['distancia'] for u, v in zip(rota[:-1], rota[1:]))
            risco_real = sum(G_dinamico[u][v]['risco_atual'] for u, v in zip(rota[:-1], rota[1:]))

            resultados.append({
                "Cenário": nome_perfil,
                "Rota": str(rota) if len(rota) < 10 else "Rota Longa...",
                "Tempo": tempo_real,
                "Distancia": dist_real,
                "Risco": risco_real
            })
            
            # Plota apenas se for solicitado (para não abrir 1000 janelas na Monte Carlo)
            mostrar_lbl = (G_dinamico.number_of_nodes() < 10)
            funcoes.plotar_rota(G_dinamico, pos, rota, f"{titulo} - {nome_perfil}", mostrar_rotulos=mostrar_lbl)
            
    # 3. Gera Tabela LaTeX desta rodada única
    funcoes.gerar_tabela_latex(resultados)


def executar_analise_monte_carlo(dados_cenario, n_simulacoes=1000):
    """
    Roda a simulação N vezes variando aleatoriamente o trânsito.
    Gera um histograma estatístico.
    """
    G_base, _, aresta_caos, start, end = dados_cenario
    
    print(f"\n=== INICIANDO MONTE CARLO ({n_simulacoes} iterações) ===")
    print("Isso pode levar alguns segundos...")
    
    tempos_rapida = []
    tempos_segura = []
    
    # Loop de Simulação Estocástica
    for i in range(n_simulacoes):
        # A cada iteração, o 'core' gera uma variação aleatória (0.9 a 1.1) nos pesos
        # simulando dias diferentes com o mesmo problema estrutural (acidente)
        G_sim = funcoes.atualizar_pesos_dinamicamente(
            G_base.copy(),
            cenario.SIMULACAO_PARAMS['fator_congest'],
            cenario.SIMULACAO_PARAMS['risco_extra'],
            aresta_critica=aresta_caos
        )
        
        # 1. Calcula para Perfil "Mais Rápida"
        pesos_r = cenario.CENARIOS["Mais Rápida"]
        rota_r, _ = funcoes.encontrar_rota_otima(G_sim, start, end, pesos_r['w_d'], pesos_r['w_t'], pesos_r['w_r'])
        
        if rota_r:
            t_r = sum(G_sim[u][v]['tempo_atual'] for u, v in zip(rota_r[:-1], rota_r[1:]))
            tempos_rapida.append(t_r)
            
        # 2. Calcula para Perfil "Mais Segura"
        pesos_s = cenario.CENARIOS["Mais Segura"]
        rota_s, _ = funcoes.encontrar_rota_otima(G_sim, start, end, pesos_s['w_d'], pesos_s['w_t'], pesos_s['w_r'])
        
        if rota_s:
            t_s = sum(G_sim[u][v]['tempo_atual'] for u, v in zip(rota_s[:-1], rota_s[1:]))
            tempos_segura.append(t_s)

    # --- PLOTAGEM DO HISTOGRAMA ---
    plt.figure(figsize=(10, 6))
    
    # Histograma Rápido (Vermelho)
    plt.hist(tempos_rapida, bins=30, alpha=0.6, color='salmon', label='Perfil Rápido (Arriscado)')
    
    # Histograma Seguro (Azul/Verde)
    plt.hist(tempos_segura, bins=30, alpha=0.6, color='skyblue', label='Perfil Seguro (Conservador)')
    
    # Linhas de Média
    media_r = sum(tempos_rapida) / len(tempos_rapida)
    media_s = sum(tempos_segura) / len(tempos_segura)
    plt.axvline(media_r, color='red', linestyle='dashed', linewidth=1.5, label=f'Média Rápida: {media_r:.1f}m')
    plt.axvline(media_s, color='blue', linestyle='dashed', linewidth=1.5, label=f'Média Segura: {media_s:.1f}m')
    
    plt.title(f"Simulação de Monte Carlo (N={n_simulacoes}): Variabilidade do Tempo de Viagem")
    plt.xlabel("Tempo Total de Viagem (minutos)")
    plt.ylabel("Frequência (Número de Simulações)")
    plt.legend()
    plt.grid(axis='y', alpha=0.3)
    
    print("Gerando gráfico de Monte Carlo...")
    plt.show() # Salve esta imagem


def main():
    # --- ETAPA 1: Análise Visual (Gera os mapas de rotas) ---
    # Cenário Didático
    dados_didatico = cenario.criar_cenario_didatico()
    executar_simulacao_visual("Cenário Didático", dados_didatico)
    
    # Cenário Complexo (Grade)
    dados_complexo = cenario.criar_cenario_complexo(4, 5)
    executar_simulacao_visual("Cenário Complexo", dados_complexo)
    
    # --- ETAPA 2: Análise Estatística (Gera o Histograma) ---
    # Usamos o cenário complexo para ter mais variabilidade
    executar_analise_monte_carlo(dados_complexo, n_simulacoes=1000)

if __name__ == "__main__":
    main()
