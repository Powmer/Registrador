import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import openpyxl
from openpyxl import Workbook
from datetime import datetime
import os

# Variáveis globais
excel_file = ""
carrinho = []
comandas = {}
comanda_selecionada = None

# Excel e dados 
def criar_excel():
    global excel_file
    if not excel_file:
        return
    if not os.path.exists(excel_file):
        wb = Workbook()
        ws = wb.active
        ws.title = "Vendas"
        ws.append(["Comanda/Carrinho", "Data e Hora", "Produto", "Quantidade", "Preço", "Entrega", "Pagamento"])
        wb.save(excel_file)

def selecionar_diretorio():
    global excel_file
    pasta = filedialog.askdirectory(title="Selecione o diretório para salvar o arquivo Excel")
    if pasta:
        excel_file = os.path.join(pasta, "vendas.xlsx")
        criar_excel()
        messagebox.showinfo("Sucesso", f"Arquivo criado em: {excel_file}")

def calcular_preco(produto, quantidade):
    if produto == "Combo Individual":
        return round(quantidade * 29.99, 2)
    elif produto == "Combo Família":
        return round(quantidade * 79.99, 2)
    elif produto == "Kilo":
        return round((quantidade / 1000) * 89.99, 2)
    return 0.0

# Carrinho de vendas
def adicionar_ao_carrinho():
    produto = product_type_var.get()
    entrega = delivery_type_var.get()
    if produto == "Kilo":
        quantidade = quantidade_gramas_var.get()
    else:
        quantidade = quantidade_var.get()

    if not produto or not entrega or quantidade <= 0:
        messagebox.showwarning("Atenção", "Preencha produto, quantidade e entrega.")
        return

    preco = calcular_preco(produto, quantidade)
    carrinho.append({
        "produto": produto,
        "quantidade": quantidade,
        "preco": preco,
        "entrega": entrega
    })
    atualizar_lista_carrinho()
    atualizar_total_carrinho()
    limpar_campos_venda()

def atualizar_lista_carrinho():
    for i in lista_carrinho.get_children():
        lista_carrinho.delete(i)
    for item in carrinho:
        lista_carrinho.insert("", "end", values=(item["produto"], item["quantidade"], f"R$ {item['preco']}", item["entrega"]))

def atualizar_total_carrinho():
    total = sum(item["preco"] for item in carrinho)
    preco_total_carrinho_var.set(f"R$ {round(total, 2)}")

def registrar_carrinho():
    global excel_file
    pagamento = payment_method_var.get()
    if not pagamento:
        messagebox.showwarning("Atenção", "Informe o método de pagamento.")
        return
    if not carrinho:
        messagebox.showwarning("Atenção", "Carrinho vazio.")
        return

    data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    wb = openpyxl.load_workbook(excel_file)
    ws = wb.active
    for item in carrinho:
        ws.append(["Carrinho", data_hora, item["produto"], item["quantidade"], item["preco"], item["entrega"], pagamento])
    wb.save(excel_file)
    messagebox.showinfo("Sucesso", "Venda do carrinho registrada!")
    carrinho.clear()
    atualizar_lista_carrinho()
    atualizar_total_carrinho()

def limpar_campos_venda():
    product_type_var.set("")
    quantidade_var.set(0.0)
    quantidade_gramas_var.set(0.0)
    delivery_type_var.set("")

# Funções das comandas
def abrir_comanda():
    global comanda_selecionada
    nome = comanda_nome_var.get().strip()
    tipo_entrega = comanda_delivery_var.get()
    if not nome or not tipo_entrega:
        messagebox.showwarning("Atenção", "Informe nome e entrega.")
        return
    if nome not in comandas:
        comandas[nome] = {
            "itens": [],
            "entrega": tipo_entrega,
            "inicio": datetime.now(),
            "pagamento": ""
        }
    comanda_selecionada = nome
    atualizar_comandas()
    atualizar_lista_itens()
    atualizar_total_comanda()

def adicionar_item_comanda():
    global comanda_selecionada
    if not comanda_selecionada:
        messagebox.showwarning("Atenção", "Nenhuma comanda selecionada.")
        return
    produto = comanda_produto_var.get()
    if produto == "Kilo":
        quantidade = comanda_gramas_var.get()
    else:
        quantidade = comanda_qtd_var.get()
    if not produto or quantidade <= 0:
        messagebox.showwarning("Atenção", "Informe produto e quantidade.")
        return
    preco = calcular_preco(produto, quantidade)
    comandas[comanda_selecionada]["itens"].append({
        "produto": produto,
        "quantidade": quantidade,
        "preco": preco
    })
    atualizar_lista_itens()
    atualizar_total_comanda()
    limpar_campos_comanda()

def atualizar_comandas():
    lista_comandas.delete(0, tk.END)
    for nome in comandas:
        lista_comandas.insert(tk.END, nome)

def selecionar_comanda(evt):
    global comanda_selecionada
    selecao = lista_comandas.curselection()
    if selecao:
        comanda_selecionada = lista_comandas.get(selecao)
        atualizar_lista_itens()
        atualizar_total_comanda()

def atualizar_lista_itens():
    for i in lista_itens.get_children():
        lista_itens.delete(i)
    if comanda_selecionada:
        for item in comandas[comanda_selecionada]["itens"]:
            lista_itens.insert("", "end", values=(item["produto"], item["quantidade"], f"R$ {item['preco']}"))

def atualizar_total_comanda():
    if comanda_selecionada:
        total = sum(item["preco"] for item in comandas[comanda_selecionada]["itens"])
        preco_total_comanda_var.set(f"R$ {round(total, 2)}")
    else:
        preco_total_comanda_var.set("R$ 0.0")

def fechar_comanda():
    global excel_file
    if not comanda_selecionada:
        messagebox.showwarning("Atenção", "Nenhuma comanda selecionada.")
        return
    pagamento = comanda_pagamento_var.get()
    if not pagamento:
        messagebox.showwarning("Atenção", "Informe o pagamento.")
        return
    comanda = comandas[comanda_selecionada]
    data_hora = comanda["inicio"].strftime("%Y-%m-%d %H:%M:%S")
    wb = openpyxl.load_workbook(excel_file)
    ws = wb.active
    for item in comanda["itens"]:
        ws.append([comanda_selecionada, data_hora, item["produto"], item["quantidade"], item["preco"], comanda["entrega"], pagamento])
    wb.save(excel_file)
    messagebox.showinfo("Sucesso", f"Comanda '{comanda_selecionada}' fechada.")
    del comandas[comanda_selecionada]
    atualizar_comandas()
    atualizar_lista_itens()
    atualizar_total_comanda()

def limpar_campos_comanda():
    comanda_produto_var.set("")
    comanda_qtd_var.set(0.0)
    comanda_gramas_var.set(0.0)

# ---------- Interface gráfica ----------
root = tk.Tk()
root.title("Sistema de Vendas e Comandas")
root.option_add("*Font", "Helvetica 10")
style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"))
style.configure("TButton", padding=5)

# Frame de Vendas
frame_venda = ttk.LabelFrame(root, text="Venda")
frame_venda.pack(side="left", padx=10, pady=10, fill="both")

ttk.Label(frame_venda, text="Produto").grid(row=0, column=0)
product_type_var = tk.StringVar()
ttk.Combobox(frame_venda, textvariable=product_type_var, values=["Combo Individual", "Combo Família", "Kilo"]).grid(row=0, column=1)

ttk.Label(frame_venda, text="Qtd Produtos").grid(row=1, column=0)
quantidade_var = tk.DoubleVar()
ttk.Entry(frame_venda, textvariable=quantidade_var).grid(row=1, column=1)

ttk.Label(frame_venda, text="Qtd (g)").grid(row=2, column=0)
quantidade_gramas_var = tk.DoubleVar()
ttk.Entry(frame_venda, textvariable=quantidade_gramas_var).grid(row=2, column=1)

ttk.Label(frame_venda, text="Entrega").grid(row=3, column=0)
delivery_type_var = tk.StringVar()
ttk.Combobox(frame_venda, textvariable=delivery_type_var, values=["Retirada", "Entrega"]).grid(row=3, column=1)

ttk.Button(frame_venda, text="Adicionar ao Carrinho", command=adicionar_ao_carrinho).grid(row=4, column=0, columnspan=2, pady=5)

ttk.Label(frame_venda, text="Pagamento").grid(row=5, column=0)
payment_method_var = tk.StringVar()
ttk.Combobox(frame_venda, textvariable=payment_method_var, values=["Pix", "Cartão", "Dinheiro"]).grid(row=5, column=1)

ttk.Button(frame_venda, text="Finalizar Venda", command=registrar_carrinho).grid(row=6, column=0, columnspan=2, pady=5)
ttk.Button(frame_venda, text="Selecionar Pasta", command=selecionar_diretorio).grid(row=7, column=0, columnspan=2, pady=5)

# Frame Carrinho
frame_carrinho = ttk.LabelFrame(root, text="Carrinho")
frame_carrinho.pack(side="left", padx=10, pady=10, fill="both")

lista_carrinho = ttk.Treeview(frame_carrinho, columns=("Produto", "Qtd", "Preço", "Entrega"), show="headings", height=7)
for col in ("Produto", "Qtd", "Preço", "Entrega"):
    lista_carrinho.heading(col, text=col)
lista_carrinho.pack(padx=5, pady=5)

ttk.Label(frame_carrinho, text="Total:").pack()
preco_total_carrinho_var = tk.StringVar(value="R$ 0.0")
ttk.Label(frame_carrinho, textvariable=preco_total_carrinho_var, font=("Helvetica", 10, "bold")).pack()

# Janela Comandas
frame_comanda = ttk.LabelFrame(root, text="Comandas")
frame_comanda.pack(side="right", padx=10, pady=10, fill="both")

ttk.Label(frame_comanda, text="Nome").grid(row=0, column=0)
comanda_nome_var = tk.StringVar()
ttk.Entry(frame_comanda, textvariable=comanda_nome_var).grid(row=0, column=1)

ttk.Label(frame_comanda, text="Entrega").grid(row=1, column=0)
comanda_delivery_var = tk.StringVar()
ttk.Combobox(frame_comanda, textvariable=comanda_delivery_var, values=["Retirada", "Entrega"]).grid(row=1, column=1)

ttk.Button(frame_comanda, text="Abrir Comanda", command=abrir_comanda).grid(row=2, column=0, columnspan=2, pady=5)

ttk.Label(frame_comanda, text="Produto").grid(row=3, column=0)
comanda_produto_var = tk.StringVar()
ttk.Combobox(frame_comanda, textvariable=comanda_produto_var, values=["Combo Individual", "Combo Família", "Kilo"]).grid(row=3, column=1)

ttk.Label(frame_comanda, text="Qtd Produtos").grid(row=4, column=0)
comanda_qtd_var = tk.DoubleVar()
ttk.Entry(frame_comanda, textvariable=comanda_qtd_var).grid(row=4, column=1)

ttk.Label(frame_comanda, text="Qtd (g)").grid(row=5, column=0)
comanda_gramas_var = tk.DoubleVar()
ttk.Entry(frame_comanda, textvariable=comanda_gramas_var).grid(row=5, column=1)

ttk.Button(frame_comanda, text="Adicionar Item", command=adicionar_item_comanda).grid(row=6, column=0, columnspan=2, pady=5)

ttk.Label(frame_comanda, text="Pagamento").grid(row=7, column=0)
comanda_pagamento_var = tk.StringVar()
ttk.Combobox(frame_comanda, textvariable=comanda_pagamento_var, values=["Pix", "Cartão", "Dinheiro"]).grid(row=7, column=1)

ttk.Button(frame_comanda, text="Fechar Comanda", command=fechar_comanda).grid(row=8, column=0, columnspan=2, pady=5)

ttk.Label(frame_comanda, text="Comandas Abertas").grid(row=9, column=0, columnspan=2)
lista_comandas = tk.Listbox(frame_comanda, height=5)
lista_comandas.grid(row=10, column=0, columnspan=2, padx=5, pady=5)
lista_comandas.bind("<<ListboxSelect>>", selecionar_comanda)

ttk.Label(frame_comanda, text="Itens da Comanda").grid(row=11, column=0, columnspan=2)
lista_itens = ttk.Treeview(frame_comanda, columns=("Produto", "Qtd", "Preço"), show="headings", height=5)
for col in ("Produto", "Qtd", "Preço"):
    lista_itens.heading(col, text=col)
lista_itens.grid(row=12, column=0, columnspan=2, padx=5, pady=5)

ttk.Label(frame_comanda, text="Total:").grid(row=13, column=0)
preco_total_comanda_var = tk.StringVar(value="R$ 0.0")
ttk.Label(frame_comanda, textvariable=preco_total_comanda_var, font=("Helvetica", 10, "bold")).grid(row=13, column=1)

root.mainloop()
