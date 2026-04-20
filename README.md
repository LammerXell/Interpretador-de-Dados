# 📊 Análise de Municípios de Pernambuco com Dados do IBGE

Projeto em Python para leitura, tratamento e análise de dados de municípios a partir de arquivos CSV exportados do IBGE.

## 🚀 Objetivo

Processar dados populacionais dos municípios de Pernambuco e gerar um ranking das cidades mais populosas, lidando com inconsistências presentes no arquivo CSV exportado.

---

## ⚠️ Problema

Embora os dados do IBGE sejam bem estruturados para visualização no site, o CSV exportado apresenta desafios como:

- Linha extra antes do cabeçalho real
- Cabeçalhos com nomes não padronizados (ex: `Município [-]`)
- Presença de conteúdo HTML no final do arquivo
- Valores ausentes ou inválidos (ex: `-`)

Esses problemas fazem com que uma leitura simples com `csv.DictReader` falhe ou retorne dados incorretos.

---

## 🛠️ Solução

Foi implementado um parser robusto que:

- 🔍 Detecta automaticamente o cabeçalho correto
- 🔄 Normaliza nomes de colunas
- 🧹 Remove ruídos como HTML e caracteres especiais
- ✅ Valida registros com base no código do município
- ⚠️ Trata erros e registra inconsistências
- 📈 Gera ranking das cidades por população

---

## 📦 Tecnologias utilizadas

- Python 3
- Biblioteca padrão:
  - `csv`
  - `re`
  - `html`
  - `unicodedata`

---

## ▶️ Como executar

1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/seu-repo.git
Acesse a pasta:
cd seu-repo
Execute o script:
python Main.py
📊 Exemplo de saída
Top 5 cidades mais populosas de Pernambuco:

1. Recife - População: XXXXXXX
2. Jaboatão dos Guararapes - População: XXXXXXX
3. Petrolina - População: XXXXXXX
4. Caruaru - População: XXXXXXX
5. Paulista - População: XXXXXXX
