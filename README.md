# Simulação de Rotas Inteligentes em Grafos Dinâmicos 

Este projeto implementa uma simulação computacional em Python para otimização de rotas urbanas utilizando a **Teoria dos Grafos**. O sistema utiliza uma função de custo multiobjetivo (ponderando Tempo, Distância e Risco) e realiza análises de robustez via **Simulação de Monte Carlo**.

> Trabalho desenvolvido para a disciplina de Matemática Discreta da FGV.

## Estrutura do Projeto

O projeto segue uma arquitetura modular baseada no princípio de separação de responsabilidades:

- `main.py`: **Orquestrador.** Gerencia o fluxo da simulação, chamando as visualizações e a análise estatística.
- `funcoes.py`: **Lógica (Core).** Contém o algoritmo de Dijkstra, cálculos de custo e geração de gráficos.
- `cenario.py`: **Dados.** Define a topologia dos grafos, os parâmetros de simulação e os pesos dos perfis.

## Resultados

O sistema gera automaticamente:
1. Visualização de rotas em grafo didático.
2. Comparação de rotas em malha complexa (Grid 4x5).
3. Histograma estatístico de variância de tempo (Monte Carlo).

## Tecnologias
- Python 3.9+
- NetworkX
- Matplotlib
- Pandas
- NumPy

## Autor
**Lucas Oliveira** FGV - Escola de Matemática Aplicada
