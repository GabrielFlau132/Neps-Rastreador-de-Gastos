import click
import csv
import os
from rich.console import Console
from rich.table import Table
from datetime import datetime

console = Console()
ID = 1
despesas = []

def carregar_despesas():
    global despesas, ID

    if os.path.exists("despesas.csv"):
        with open("despesas.csv", mode="r", newline="", encoding="utf-8") as arquivo:
            leitor = csv.DictReader(arquivo)
            for linha in leitor:
                despesas.append({
                    "id": int(linha["id"]),
                    "data": linha["data"],
                    "descricao": linha["descricao"],
                    "valor": float(linha["valor"]),
                    "categoria": linha["categoria"]
                })
            if despesas:
                ID = max(d["id"] for d in despesas) + 1

    else:
        with open("despesas.csv", mode="w", newline="", encoding="utf-8") as arquivo:
            writer = csv.DictWriter(arquivo, fieldnames=["id", "data", "descricao", "valor", "categoria"])
            writer.writeheader()
            ID = 1
def salvar_despesa(despesa):
    with open("despesas.csv", mode="a", newline="", encoding="utf-8") as arquivo:
        writer = csv.DictWriter(arquivo, fieldnames=["id", "data", "descricao", "valor", "categoria"])
        writer.writerow({
            "id": despesa["id"],
            "data": despesa["data"],
            "descricao": despesa["descricao"],
            "valor": despesa["valor"],
            "categoria": despesa["categoria"]
        })
def atualizar_despesas():
    with open("despesas.csv", mode="w", newline="", encoding="utf-8") as arquivo:
        writer = csv.DictWriter(arquivo, fieldnames=["id", "data", "descricao", "valor", "categoria"])
        writer.writeheader()
        for d in despesas:
            writer.writerow(d)

@click.group()
def comandos():
    pass

#===================================================================================================================================================
@click.command(help="Adicionar uma nova despesa.")
@click.option('--data', prompt="Digite a data (DD/MM/YYYY)", help="Data da despesa no formato DD/MM/YYYY")
@click.option('--descricao', prompt="Digite a descrição", help="Um texto curto que descreva a despesa.")
@click.option('--valor', prompt="Digite o valor", help="Um número positivo representando o valor da despesa.")
def add(data, descricao, valor):
    global ID

    while True:
        try:
            data = datetime.strptime(data, '%d/%m/%Y')
            break
        except ValueError:
            click.echo('A data deve estar no formato DD/MM/YYYY e ser válida.')
            data = click.prompt('Data (DD/MM/YYYY)', type=str)

    while float(valor) <= 0:
        click.echo('O valor deve ser um número positivo.')
        valor = click.prompt('Valor', type=float)

    categorias_dict = {
        1: "Alimentação",
        2: "Transporte",
        3: "Moradia",
        4: "Saúde",
        5: "Outros"
    }

    tabela = Table(title="Escolha a categoria:")
    tabela.add_column("Categorias", justify="left")
    for numero, nome in categorias_dict.items():
        tabela.add_row(f"{numero}. {nome}")
    console.print(tabela)

    while True:
        try:
            categoria = int(click.prompt("Digite o número da categoria"))
            if categoria in categorias_dict:
                categoria_nome = categorias_dict[categoria]
                break
            else:
                click.echo("Número de categoria inválido.")
        except ValueError:
            click.echo("Digite um número válido.")


    despesas.append({
        "id": ID,
        "data": data.strftime('%d/%m/%Y'),
        "descricao": descricao,
        "valor": float(valor),
        "categoria": categoria_nome
    })

    salvar_despesa(despesas[-1])

    click.echo(f"Despesa com ID {ID} adicionada com sucesso! ")
    ID += 1

@click.command(help="Editar uma despesa existente.")
@click.argument('idedit', type=int)
def edit(idedit):
    despesa = next((i for i in despesas if i["id"] == idedit), None)
    if despesa:
        click.echo(f"Editando despesa com ID: {idedit}")

        nova_data = click.prompt(f"Data atual: {despesa['data']}. Digite a nova data (DD/MM/YYYY) ou pressione Enter para manter", default=despesa["data"], show_default=False)
        try:
            datetime.strptime(nova_data, "%d/%m/%Y")
        except ValueError:
            click.echo("A data deve estar no formato DD/MM/YYYY e ser válida.")
            return
        nova_descricao = click.prompt(f"Descrição atual: {despesa['descricao']}. Digite a nova descrição ou pressione Enter para manter", default=despesa["data"], show_default=False)

        while True:
            novo_valor = click.prompt(f"Valor atual: {despesa['valor']:.2f}. Digite o novo valor ou pressione Enter para manter",
                default=despesa["valor"], show_default=False)
            try:
                novo_valor_float = float(novo_valor)
                if novo_valor_float > 0:
                    novo_valor = novo_valor_float
                    break
                else:
                    click.echo("Valor inválido! Digite um número positivo.")
            except ValueError:
                click.echo("Valor inválido! Digite um número positivo.")

        categorias_dict = {
            1: "Alimentação",
            2: "Transporte",
            3: "Moradia",
            4: "Saúde",
            5: "Outros"
        }
        click.echo(f"Categoria atual: {despesa['categoria']}. Escolha uma nova categoria ou pressione Enter para manter:")
        tabela = Table(title="Categorias")
        tabela.add_column("ID", justify="center")
        tabela.add_column("Nome", justify="left")
        for numero, nome in categorias_dict.items():
            tabela.add_row(str(numero), nome)
        console.print(tabela)
        categoria_input = click.prompt("Digite o número correspondente", default=despesa["categoria"], show_default=False)
        if categoria_input.isdigit() and int(categoria_input) in categorias_dict:
            nova_categoria = categorias_dict[int(categoria_input)]
        else:
            nova_categoria = despesa["categoria"]

        despesa["data"] = nova_data
        despesa["descricao"] = nova_descricao
        despesa["valor"] = novo_valor
        despesa["categoria"] = nova_categoria

        atualizar_despesas()
        click.echo("Despesa editada com sucesso!")

    else:
        click.echo("Nenhuma despesa encontrada com o ID fornecido.")

@click.command(help="Deletar uma despesa existente.")
@click.argument('idlet', type=int)
def delete(idlet):
    despesa = next((i for i in despesas if i["id"] == idlet), None)
    if despesa:
        despesas.remove(despesa)
        atualizar_despesas()
        click.echo(f"Despesa com ID {idlet} removida com sucesso!")
    else:
        click.echo("Nenhuma despesa encontrada com o ID fornecido.")

@click.command(help="Exibe todas as despesas registradas no sistema.\nVocê pode usar os filtros opcionais abaixo:\n--category TEXT     Filtra as despesas por categoria.\n--month-year TEXT   Filtra as despesas de um mês/ano específico (formato MM/YYYY).\n")
@click.option('--category', type=str, help='Filtra as despesas por categoria.')
@click.option('--month-year', type=str, help='Filtra as despesas por mês e ano (formato MM/YYYY).')
def list(category, month_year):
    categorias = ["Alimentação", "Transporte", "Moradia", "Saúde", "Outros"]
    despesasFiltradas = despesas

    if category:
        if category not in categorias:
            click.echo("Categoria inválida! Escolha uma das opções: " + ", ".join(categorias))
            return
        despesasFiltradas = [d for d in despesas if d["categoria"] == category]

    if month_year:
        try:
            filtro_data = datetime.strptime(month_year, "%m/%Y")
        except ValueError:
            click.echo("Formato de data inválido! Use MM/YYYY.")
            return

        despesasFiltradas = [d for d in despesasFiltradas if datetime.strptime(d["data"], "%d/%m/%Y").month == filtro_data.month and datetime.strptime(d["data"], "%d/%m/%Y").year == filtro_data.year]

    tabela = Table(title="Lista de Despesas")
    tabela.add_column("ID", justify="center")
    tabela.add_column("Data", justify="left")
    tabela.add_column("Descrição", justify="left")
    tabela.add_column("Valor (R$)", justify="left")
    tabela.add_column("Categoria", justify="left")
    Total = 0
    for despesa in despesasFiltradas:
        tabela.add_row(str(despesa.get("id")), despesa.get("data"), despesa.get("descricao"), str(despesa.get("valor")), despesa.get("categoria"))
        Total += despesa.get("valor")
    tabela.add_row("TOTAL", "", "", f"{Total:.2f}", "")
    console.print(tabela)

@click.command(help="Exibir o resumo financeiro mensal.")
@click.argument('mes', type=str)
def resume(mes):
    despesasFiltradas = despesas
    categorias = {"Alimentação": 0, "Transporte": 0, "Moradia": 0, "Saúde": 0, "Outros": 0}
    total = 0

    try:
        mes = datetime.strptime(mes, '%m/%Y')
    except ValueError:
        click.echo('Formato inválido! Use o formato MM/YYYY.')
        return

    despesasFiltradas = [d for d in despesasFiltradas if datetime.strptime(d["data"], "%d/%m/%Y").month == mes.month and datetime.strptime(d["data"], "%d/%m/%Y").year == mes.year]
    for despesa in despesasFiltradas:
        categorias[despesa["categoria"]] += despesa["valor"]
        total += despesa["valor"]

    NomeMes = mes.strftime('%B').capitalize()
    ano = mes.strftime('%Y')

    tabela = Table(title=f"Resumo Financeiro: {NomeMes}/{ano}")
    tabela.add_column("Categoria")
    tabela.add_column("Valor (R$)", justify="right")
    tabela.add_column("Percentual (%)", justify="right")

    for categoria in categorias:
        val = categorias[categoria]
        if total > 0:
            percentual = (val / total) * 100
        else:
            percentual = 0
        if val > 0:
            tabela.add_row(categoria, f"R$ {val:.2f}", f"{percentual:.2f}%")

    console.print(tabela)

#===================================================================================================================================================

comandos.add_command(add)
comandos.add_command(edit)
comandos.add_command(delete)
comandos.add_command(list)
comandos.add_command(resume)

carregar_despesas()
comandos()

