import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from collections import defaultdict

def ler_arquivo_csv(caminho):
    try:
        with open(caminho, 'r', encoding='utf-8') as f:
            return [linha.strip() for linha in f if linha.strip()]
    except FileNotFoundError:
        messagebox.showerror("Erro", f"Arquivo '{caminho}' não encontrado!")
        return []

def processar_linhas(linhas):
    dados_onibus = defaultdict(list)
    for linha in linhas:
        partes = linha.strip().split(',')
        if not partes or len(partes) < 2:
            continue
        numero_linha = partes[0]
        for item in partes[1:]:
            if ':' in item:
                try:
                    entrada, _ = map(int, item.split(':'))  # Ignora saída
                    dados_onibus[numero_linha].append(entrada)
                except ValueError:
                    continue
    return dados_onibus

def calcular_estatisticas(dados_onibus):
    resultados = []
    for linha, entradas in dados_onibus.items():
        total_entrada = sum(entradas)
        resultados.append({
            'linha': linha,
            'total_entrada': total_entrada,
            'numero_paradas': len(entradas)
        })
    return sorted(resultados, key=lambda x: x['total_entrada'], reverse=True)

def carregar_arquivo():
    caminho = filedialog.askopenfilename(filetypes=[("Arquivos CSV", "*.csv")])
    if not caminho:
        return
    linhas = ler_arquivo_csv(caminho)
    dados = processar_linhas(linhas)
    estatisticas = calcular_estatisticas(dados)
    exibir_resultados(estatisticas)

def exibir_resultados(resultados):
    for item in tree.get_children():
        tree.delete(item)
    for r in resultados:
        tree.insert('', 'end', values=(r['linha'], r['total_entrada'], r['numero_paradas']))

# Criar janela principal
janela = tk.Tk()
janela.title("Análise de Linhas de Ônibus")
janela.geometry("600x400")

# Tabela com resultados (definida antes de usar)
colunas = ("Linha", "Entradas", "Paradas")
tree = ttk.Treeview(janela, columns=colunas, show='headings')
for col in colunas:
    tree.heading(col, text=col)
    tree.column(col, anchor='center')
tree.pack(expand=True, fill='both')

# Botão de carregar arquivo
btn_carregar = tk.Button(janela, text="Carregar Arquivo CSV", command=carregar_arquivo)
btn_carregar.pack(pady=10)

# Rodar a interface
janela.mainloop()
