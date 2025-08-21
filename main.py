import csv
from collections import defaultdict #É como um dicionário normal, mas quando você acessa uma chave que não existe, 
                                    #ele cria automaticamente um valor padrão

def analisar_dados_onibus():
    try:
        with open('out.csv', 'r', encoding='utf-8') as arquivo:
            linhas = arquivo.readlines() #Lê todas as linhas do arquivo e as armazena como uma lista de strings em linhas
    except FileNotFoundError:
        print("Arquivo 'out.csv' não encontrado!")
        return

    capacidade_maxima = 50
    dados_onibus = defaultdict(list) #Cria um dicionário que mapeia cada número de linha de ônibus a uma lista de tuplas 
                                     #(entrada, saída) por parada. Como é defaultdict(list), se você acessar uma chave 
                                     #que não existe, ele automaticamente cria uma lista vazia. 
    for linha in linhas:
        linha = linha.strip()        #Remove espaços, quebras de linha e tabulações no início e fim da linha.
        if not linha:                #Se a linha estiver vazia (após o strip()), pula para a próxima linha.
            continue

        partes = linha.split(',')    #Divide a linha em partes usando a vírgula como separador.
        numero_linha = partes[0]     #O primeiro item da lista é o número da linha de ônibus.

        for item in partes[1:]:      #Itera pelos demais itens da linha (depois do número da linha), que representam as paradas com entrada e saída de passageiros
            if ':' in item:          #¬ que representam as paradas com entrada e saída de passageiros.
                try:                                                    
                    entrada, saida = map(int, item.split(':'))          # item.split(':') divide "10:2" em ['10', '2'], map(int, ...) converte esses valores para inteiros.
                    dados_onibus[numero_linha].append((entrada, saida)) # Atribui entrada:saída
                except ValueError:                                      
                    print(f"Erro ao processar parada: {item}")          #
                    continue                                            #Se houver erro na conversão para inteiro (ex: se o dado for "abc:def"), imprime um aviso e pula esse item.

    resultados = []                  #Lista vazia que armazenará dicionários com os resultados calculados para cada linha.

    for linha, paradas in dados_onibus.items():      #Itera sobre cada linha de ônibus (linha) e sua lista de paradas com (entrada, saída)
        total_entrada = sum(e for e, _ in paradas)   #Soma todas as entradas de passageiros naquela linha. O _ ignora a saída.
        total_saida = sum(s for _, s in paradas)     #Soma todas as saídas de passageiros.
        fluxo_liquido = total_entrada - total_saida  #Calcula o fluxo líquido (quantos passageiros entraram a mais do que saíram). 

        lotacao_atual = 0
        lotacao_maxima = 0

        for entrada, saida in paradas:
            lotacao_atual += entrada - saida                                #Adiciona passageiros que entram e subtrai os que saem
            lotacao_atual = max(0, min(lotacao_atual, capacidade_maxima))   #limita a lotação ao máximo permitido
            lotacao_maxima = max(lotacao_maxima, lotacao_atual)             #Atualiza o valor máximo.

        porcentagem_lotacao = (lotacao_maxima / capacidade_maxima) * 100

        resultados.append({                                 #Adiciona um dicionário com todos os dados calculados para essa linha à lista resultados. 
            'linha': linha,
            'total_entrada': total_entrada,
            'total_saida': total_saida,
            'fluxo_liquido': fluxo_liquido,
            'lotacao_maxima': lotacao_maxima,
            'porcentagem_lotacao': porcentagem_lotacao,
            'numero_paradas': len(paradas)
        })

    if not resultados:  #Se nenhuma linha foi processada com sucesso (ex: arquivo vazio ou mal formatado), exibe mensagem e encerra. 
        print("Nenhum dado válido encontrado no arquivo.")
        return

    resultados.sort(key=lambda x: x['total_entrada'], reverse=True) #Ordena a lista resultados em ordem decrescente de total_entrada (mais passageiros primeiro).
    linha_menos_utilizada = min(resultados, key=lambda x: x['numero_paradas']) #Encontra a linha com menor número de paradas (menos utilizada em termos de extensão). 
    linha_menor_fluxo = min(resultados, key=lambda x: x['total_entrada']) # Encontra a linha com menor número total de entradas (menor fluxo de passageiros). 

    print("=" * 30)
    print("ANÁLISE DE LINHAS DE ÔNIBUS".center(30))
    print("=" * 30)
    print(f"{'Linha':<10} {'Usuários':<10} {'Paradas':<15}")
    print("-" * 30)

    for r in resultados:    #Imprime cada linha com seus dados formatados.
        print(f"{r['linha']:<10} {r['total_entrada']:<10} {r['numero_paradas']:<10}")

    print("-" * 30)
    print("\nLINHAS COM MAIOR VOLUME DE PASSAGEIROS:")
    for i, r in enumerate(resultados[:3]):
        print(f"{i+1}º Lugar: Linha {r['linha']} - {r['total_entrada']} passageiros")

    print(f"\nLINHA COM MENOR FLUXO:\nLinha {linha_menor_fluxo['linha']} - {linha_menor_fluxo['total_entrada']} passageiros")
    print(f"\nLINHA MENOS UTILIZADA:\nLinha {linha_menos_utilizada['linha']} - {linha_menos_utilizada['numero_paradas']} paradas")
    print(f"\nCAPACIDADE MÁXIMA DOS ÔNIBUS: {capacidade_maxima} passageiros")

# Executar
if __name__ == "__main__":  #Verifica se o script está sendo executado diretamente (não importado como módulo). 
    analisar_dados_onibus() #Se sim, chama a função analisar_dados_onibus(). 
