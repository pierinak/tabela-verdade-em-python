import itertools
import tkinter as tk
import tkinter.messagebox as messagebox

# Função para gerar a tabela verdade


def generate_truth_table(variables, expression):
    num_variables = len(variables)
    truth_table = []

    # Substitui os operadores lógicos por suas representações em Python
    expression = expression.replace("~", " not ")
    expression = expression.replace("/\\", " and ")
    expression = expression.replace("\\/", " or ")
    expression = expression.replace("^", " ^ ")
    expression = expression.replace("#", " # ")
    expression = expression.replace("==", " == ")
    #expression = expression.replace("*", " * ")

    # Define as funções para os operadores lógicos
    def xor(a, b):
        return a != b
    globals()["^"] = xor

    def implication(a, b):
        return (not a) or b
    globals()["#"] = implication

    def negation(a, b):
        return ((not a) or (not b))
    globals()["~"] = negation

    def XNOR(a, b):
        return a == b
    globals()["=="] = XNOR

    # def NAND(a, b):
    #    if a != b:
    #        return 0
    #    else:
    #        return 1
    # globals()["*"] = NAND

    # Gera todas as combinações possíveis de valores verdade para as variáveis
    for combination in itertools.product([0, 1], repeat=num_variables):
        row = list(combination)
        truth_table_row = {}
        for i in range(num_variables):
            truth_table_row[variables[i]] = row[i]
        subs = dict(zip(variables, row))
        truth_table_row["Resultado"] = eval(expression, subs)
        truth_table.append(truth_table_row)

    # Adiciona os operadores à tabela verdade
    operator_row = {"": "", "Operadores": ""}
    operator_row.update({var: "" for var in variables})
    operator_row.update({"Resultado": ""})
    truth_table.insert(50, operator_row)
    operator_row = {"": "", "Operadores": expression}
    operator_row.update({var: "" for var in variables})
    operator_row.update({"Resultado": ""})
    truth_table.insert(50, operator_row)

    return truth_table

# Função para verificar se uma expressão é uma tautologia


def is_tautology(expression):
    variables = []
    for char in expression:
        if char.isalpha() and char not in variables:
            variables.append(char)

    truth_table = generate_truth_table(variables, expression)

    for row in truth_table:
        if row["Resultado"] == 0 or row["Resultado"] == "False":
            return "Não é uma tautologia"

    for row in truth_table:
        if row["Resultado"] == 1 or row["Resultado"] == "True":
            return "É uma tautologia"

# Função para gerar a tabela verdade na interface gráfica


def generate_table():
    try:
        expression = expr_entry.get()
        valid_operators = ["~", "&", "\\/", "^", "#", "=="]

        if not expression:
            show_error("Insira uma expressão")
            return
        # elif not set(expression).issubset(set(valid_operators + list("() abcdefghijklmnopqrstuvwxyz"))):
         #   show_error("Expressão inválida")
           # return

        variables = []
        for char in expression:
            if char.isalpha() and char not in variables:
                variables.append(char)
        table = generate_truth_table(variables, expression)
    except Exception as e:
        show_error(f"Ocorreu um erro: {str(e)}")
        return

    # Limpa a tabela anterior
    for widget in table_frame.winfo_children():
        widget.destroy()

    # Cria o cabeçalho da tabela
    header = [""] + variables + ["Resultado"]
    for i, col in enumerate(header):
        label = tk.Label(table_frame, text=col, width=15, relief="solid")
        label.grid(row=0, column=i)

    # Preenche a tabela com os valores verdade
    for i, row in enumerate(table):
        label = tk.Label(table_frame, text=str(i), width=15, relief="solid")
        label.grid(row=i+1, column=0)
        label = tk.Label(table_frame, text=str(
            row["Resultado"]), width=15, relief="solid")
        label.grid(row=i+1, column=len(variables)+1)

        for j, var in enumerate(variables):
            label = tk.Label(table_frame, text=str(
                row[var]), width=15, relief="solid")
            label.grid(row=i+1, column=j+1)

    # Adiciona os operadores à tabela
    label = tk.Label(table_frame, text="", width=15, relief="solid")
    label.grid(row=len(table), column=0)
    label = tk.Label(table_frame, text="Operadores", width=15, relief="solid")
    label.grid(row=len(table), column=1)
    label = tk.Label(table_frame, text=expression,
                     width=15*len(variables), relief="solid")
    label.grid(row=len(table), column=2, columnspan=len(variables)+1)

    return table


# Cria a janela principal
root = tk.Tk()
root.title("Tabela Verdade")
root.attributes("-fullscreen", True)

# Função para exibir mensagens de erro


def show_error(message):
    messagebox.showerror("Erro", message)

# Funções para alternar entre tela cheia e janela normal


def toggle_fullscreen(event=None):
    root.attributes('-fullscreen', not root.attributes('-fullscreen'))


root.bind("<Escape>", toggle_fullscreen)
root.bind("<F11>", toggle_fullscreen)

# Cria os frames principais
main_frame = tk.Frame(root)
main_frame.pack(padx=10, pady=10)

Comand = tk.Frame(main_frame)
Comand.pack(side="left", padx=20, pady=50)

# Cria o texto com as instruções
comment_text = tk.Text(Comand, height=11, width=32)
comment_text.pack()

comment_text.insert(tk.END, "|      Truth Table Generator   |\n")
comment_text.insert(tk.END, "|------------------------------|\n")
comment_text.insert(tk.END, "|Operadores lógicos:           |\n")
comment_text.insert(tk.END, "|------------------------------|\n")
comment_text.insert(tk.END, "|And = /\                      |\n")
comment_text.insert(tk.END, "|Not = ~                       |\n")
comment_text.insert(tk.END, "|Or  = \/                      |\n")
comment_text.insert(tk.END, "|Xor = ^                       |\n")
comment_text.insert(tk.END, "|------------------------------|\n")

comment_text.config(state=tk.DISABLED)

# Cria o frame para a tabela verdade
table_frame = tk.Frame(root)
table_frame.pack(padx=10, pady=10)

frame = tk.Frame(main_frame)
frame.pack(side="left", padx=10, pady=5)

# Cria o campo para inserir a expressão
expr_label = tk.Label(frame, text="Expressão:", width=20, relief="solid")
expr_label.grid(row=0, column=0)
expr_entry = tk.Entry(frame)
expr_entry.grid(row=0, column=1)

# Cria o botão para gerar a tabela verdade
button = tk.Button(frame, text="Gerar Tabela",
                   command=generate_table, width=20)
button.grid(row=1, column=0, columnspan=2)

# Cria o label para o resultado da verificação de tautologia
result_label = tk.Label(frame, text="", width=20)
result_label.grid(row=3, column=0, columnspan=2)

# Cria o botão para verificar se a expressão é uma tautologia
button = tk.Button(frame, text="Verificar Tautologia",
                   command=lambda: result_label.config(text=str(is_tautology(expr_entry.get()))), width=20)
button.grid(row=2, column=0, columnspan=2)

# Inicia o loop da janela
root.mainloop()
