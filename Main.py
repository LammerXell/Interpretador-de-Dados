import csv
import html
import re
import unicodedata

#essa funcao tem a funcao de normalizar o texto, ou seja, remover acentos, espaços com o .strip() caracteres especiais e deixar tudo em minusculo cm o .lower() para facilitar a comparação e a busca das colunas no CSV, ja que os nomes das colunas podem variar em formato e acentos.
#eu troquei a função replace por re.sub para remover as tags HTML e os colchetes, pois o re.sub é mais flexível e pode lidar com padrões mais complexos, como tags HTML que podem conter atributos ou colchetes que podem conter texto. 
# O uso de expressões regulares permite uma limpeza mais robusta do texto, garantindo que apenas o conteúdo relevante seja mantido para a comparação e análise dos dados.
def normalizar_texto(texto):
    texto = html.unescape((texto or "").strip())
    texto = re.sub(r"<[^>]+>", " ", texto)
    texto = re.sub(r"\[[^\]]*\]", "", texto)
    texto = unicodedata.normalize("NFKD", texto)
    texto = texto.encode("ascii", "ignore").decode("ascii")
    texto = re.sub(r"\s+", " ", texto) # Substitui multiplos espacos por um unico espaco
    return texto.strip().lower()


def limpar_texto(texto):
    return html.unescape((texto or "").strip())


def encontrar_cabecalho(linhas):
    for indice, linha in enumerate(linhas):
        cabecalho = [normalizar_texto(coluna) for coluna in linha]
        if "municipio" in cabecalho and "codigo" in cabecalho:
            return indice, linha
    raise ValueError("Nao foi possivel localizar o cabecalho do CSV.")


def obter_indices(cabecalho):
    indices = {}
    cabecalho_normalizado = {
        normalizar_texto(coluna): posicao for posicao, coluna in enumerate(cabecalho)
    }

    indices["municipio"] = cabecalho_normalizado.get("municipio")
    indices["codigo"] = cabecalho_normalizado.get("codigo")
    indices["pop_estimada"] = cabecalho_normalizado.get("populacao estimada - pessoas")
    indices["pop_censo"] = cabecalho_normalizado.get("populacao no ultimo censo - pessoas")

    obrigatorios = ("municipio", "codigo")
    faltando = [campo for campo in obrigatorios if indices[campo] is None]
    if faltando:
        raise ValueError(f"Colunas obrigatorias ausentes: {', '.join(faltando)}")

    if indices["pop_estimada"] is None and indices["pop_censo"] is None:
        raise ValueError("Nenhuma coluna de populacao foi encontrada no CSV.")

    return indices


def obter_valor(linha, indice):
    if indice is None or indice >= len(linha):
        return ""
    return linha[indice].strip()


def converter_populacao(valor):
    valor = limpar_texto(valor)
    if not valor or valor == "-":
        raise ValueError("Populacao nao encontrada")

    apenas_digitos = re.sub(r"\D", "", valor)
    if not apenas_digitos:
        raise ValueError("Populacao invalida")

    return int(apenas_digitos)


def carregar_dados(caminho_csv):
    with open(caminho_csv, newline="", encoding="utf-8") as csvfile:
        linhas = list(csv.reader(csvfile))

    indice_cabecalho, cabecalho = encontrar_cabecalho(linhas)
    indices = obter_indices(cabecalho)

    dados = []
    lista_erros = []

    for numero_linha, linha in enumerate(linhas[indice_cabecalho + 1 :], start=indice_cabecalho + 2):
        if not any(coluna.strip() for coluna in linha):
            continue

        codigo = obter_valor(linha, indices["codigo"])
        if not codigo.isdigit():
            lista_erros.append((numero_linha, "Linha ignorada por nao representar um municipio valido"))
            continue

        try:
            cidade = limpar_texto(obter_valor(linha, indices["municipio"]))
            if not cidade:
                raise ValueError("Municipio vazio")

            bruto_populacao = obter_valor(linha, indices["pop_estimada"])
            if not bruto_populacao or bruto_populacao == "-":
                bruto_populacao = obter_valor(linha, indices["pop_censo"])

            populacao = converter_populacao(bruto_populacao)

            dados.append({
                "Cidade": cidade,
                "Populacao": populacao,
            })
        except Exception as erro:
            lista_erros.append((numero_linha, str(erro)))

    dados.sort(key=lambda item: item["Populacao"], reverse=True)
    return dados, lista_erros


def main():
    dados, lista_erros = carregar_dados("dados.csv")
    erros = len(lista_erros)

    n = input("Quantas cidades deseja exibir? (Digite um numero): ")
    if not n.isdigit():
        print("Entrada invalida. Exibindo as 10 cidades mais populosas por padrao.")
        n = 10
    else:
        n = int(n)

    if n > len(dados):
        print(f"Existem apenas {len(dados)} cidades no ranking. Exibindo todas as cidades.")
        n = len(dados)

    print(f"Top {n} cidades mais populosas de Pernambuco:")
    for i, cidade in enumerate(dados[:n], start=1):
        print(f"{i}. {cidade['Cidade']} - Populacao: {cidade['Populacao']}\n")

    resposta = input("Deseja exibir o ranking completo? (S/N): ").strip().upper()
    if resposta == "S":
        print("Ranking completo das cidades de Pernambuco por populacao:")
        for i, cidade in enumerate(dados, start=1):
            print(f"{i}. {cidade['Cidade']} - Populacao: {cidade['Populacao']}\n")

    print(f"Total de erros encontrados: {erros}")
    if erros > 0:
        print("Lista de erros encontrados:")
        for erro in lista_erros[:5]:
            print(erro)


if __name__ == "__main__":
    main()
