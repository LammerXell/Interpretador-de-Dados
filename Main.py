import csv

dados = []
with open('dados.csv',newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        row['População'] = int(row['População'])
        dados.append(row)

#Ordena do maior para o menor com base na população
dados.sort(key=lambda x: x['População'], reverse=True)

n=int(input("Quantas cidades deseja exibir? (Digite um número): "))
print(f'Top {n} cidades mais populosas de Pernambuco:')
for i, cidade in enumerate(dados[:n], start=1):
    print(f"{i}. {cidade['Cidade']} - População: {cidade['População']}\n\n")

resposta=input("Deseja exibir o ranking completo? (S/N): ").strip().upper()
if resposta == 'S':
    print('Ranking completo das cidades de Pernambuco por população:')
    for i, cidade in enumerate(dados, start=1):
        print(f"{i}. {cidade['Cidade']} - População: {cidade['População']}\n\n")
