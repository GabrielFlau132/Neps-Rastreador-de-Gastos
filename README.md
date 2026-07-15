# 💰 Despesas CLI

CLI em Python para controle de despesas pessoais, com persistência em CSV, tabelas formatadas via **Rich** e comandos organizados com **Click**.

---

## ✨ Funcionalidades

| Comando  | Descrição |
|----------|-----------|
| `add`    | Cadastra uma nova despesa (data, descrição, valor e categoria) |
| `edit`   | Edita uma despesa existente campo a campo, mantendo o valor atual ao pressionar Enter |
| `delete` | Remove uma despesa pelo ID |
| `list`   | Lista despesas, com filtros opcionais por categoria e por mês/ano |
| `resume` | Exibe um resumo financeiro mensal, com total e percentual por categoria |

Recursos adicionais:

- ✅ Validação de data (`DD/MM/YYYY`), valor (numérico e positivo) e categoria (menu numerado).
- ✅ Leitura de CSV tolerante a cabeçalhos em maiúsculas ou minúsculas.
- ✅ Tabelas coloridas no terminal via `rich`.
- ✅ Persistência automática — nada é perdido entre execuções.

---

## 📦 Requisitos

- Python 3.9+
- [Click](https://click.palletsprojects.com/)
- [Rich](https://rich.readthedocs.io/)

---

## 🚀 Instalação

```bash
git clone <url-do-repositorio>
cd <pasta-do-projeto>
pip install click rich
```

> Opcional: crie um ambiente virtual antes de instalar as dependências.
>
> ```bash
> python -m venv venv
> source venv/bin/activate  # Windows: venv\Scripts\activate
> pip install click rich
> ```

---

## ▶️ Uso

O programa é executado via linha de comando, sempre a partir do arquivo principal:

```bash
python despesas.py <comando> [opções]
```

Na primeira execução, o arquivo `despesas.csv` é criado automaticamente no diretório atual, caso ainda não exista.

### `add` — Adicionar despesa

```bash
python despesas.py add
```

O comando solicita interativamente:

1. **Data** (`DD/MM/YYYY`) — revalidada até ser digitada corretamente.
2. **Descrição** — texto livre.
3. **Valor** — precisa ser numérico e positivo.
4. **Categoria** — escolhida a partir de um menu numerado:

   ```
   1. Alimentação
   2. Transporte
   3. Moradia
   4. Saúde
   5. Outros
   ```

Também é possível passar tudo via flags, sem prompts interativos:

```bash
python despesas.py add --data 14/07/2026 --descricao "Mercado" --valor 250.90
```
*(a categoria continua sendo escolhida pelo menu interativo)*

---

### `edit` — Editar despesa

```bash
python despesas.py edit <ID>
```

Cada campo é exibido com o valor atual; pressionar **Enter** sem digitar nada mantém o valor como está. Data, valor e categoria são revalidados — entradas inválidas são rejeitadas com nova tentativa.

```bash
python despesas.py edit 3
```

---

### `delete` — Remover despesa

```bash
python despesas.py delete <ID>
```

Exemplo:

```bash
python despesas.py delete 3
```

---

### `list` — Listar despesas

```bash
python despesas.py list
```

Filtros opcionais, combináveis entre si:

```bash
python despesas.py list --category Alimentação
python despesas.py list --month-year 07/2026
python despesas.py list --category Transporte --month-year 07/2026
```

A tabela final exibe uma linha **TOTAL** separada por uma divisória, com a soma de todos os valores filtrados.

---

### `resume` — Resumo mensal

```bash
python despesas.py resume <MM/YYYY>
```

Exemplo:

```bash
python despesas.py resume 07/2026
```

Mostra, por categoria, o valor gasto e o percentual sobre o total do mês, seguido de uma linha **TOTAL GERAL**.

---

## 🗂️ Estrutura do CSV

Arquivo: `despesas.csv`

| id | data       | descricao  | valor  | categoria    |
|----|------------|------------|--------|--------------|
| 1  | 14/07/2026 | Mercado    | 250.90 | Alimentação  |
| 2  | 15/07/2026 | Uber       | 32.50  | Transporte   |

- `id`: gerado automaticamente (incremental).
- `data`: formato `DD/MM/YYYY`.
- `valor`: número decimal, sempre positivo.
- `categoria`: uma das cinco categorias predefinidas.

O cabeçalho é aceito em maiúsculas ou minúsculas na leitura, mas sempre regravado em minúsculas pelo próprio programa.

---

## 🏷️ Categorias disponíveis

1. Alimentação
2. Transporte
3. Moradia
4. Saúde
5. Outros

---

## 📁 Estrutura do projeto

```
.
├── despesas.py       # CLI completa (comandos, persistência, validações)
├── despesas.csv      # Gerado automaticamente na primeira execução
└── README.md
```

---

## 🛠️ Possíveis melhorias futuras

- Exportar relatórios em PDF/Excel.
- Suporte a múltiplas moedas.
- Categorias customizáveis pelo usuário.
- Testes automatizados (pytest) para os fluxos de add/edit/delete.

---

## 📄 Licença

Uso livre para fins de estudo e portfólio.

---

## 📚 Créditos

Projeto do curso **Python Mastery Bootcamp** — [Neps Academy](https://neps.academy).
