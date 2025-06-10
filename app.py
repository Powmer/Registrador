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

de1a100 = [i + 1 for i in range(101)]
de50em100 = [50 * i for i in range(101)]
comanda_selecionada = None

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

def selecionar_arquivo_excel():
    global excel_file
    arquivo = filedialog.askopenfilename(title="Selecione um arquivo Excel", filetypes=[("Arquivos Excel", "*.xlsx")])
    if arquivo:
        excel_file = arquivo
        messagebox.showinfo("Arquivo Carregado", f"Arquivo carregado: {excel_file}")

def abrir_planilha():
    global excel_file
    if not excel_file:
        messagebox.showwarning("Atenção", "Nenhum arquivo Excel carregado.")
        return
    janela_planilha = tk.Toplevel(root)
    janela_planilha.title("Edição de Vendas")
    janela_planilha.configure(bg="#000000")
    style = ttk.Style()
    style.configure("Treeview", background="#000000", foreground="#FFA500", fieldbackground="#000000", rowheight=25)
    style.map("Treeview", background=[("selected", "#FFA500")], foreground=[("selected", "#000000")])

    tree = ttk.Treeview(janela_planilha)
    tree.pack(fill="both", expand=True)

    wb = openpyxl.load_workbook(excel_file)
    ws = wb.active
    colunas = [cell.value for cell in ws[1]]
    tree["columns"] = colunas
    tree["show"] = "headings"

    for col in colunas:
        tree.heading(col, text=col)
        tree.column(col, width=100, anchor="center")

    for row in ws.iter_rows(min_row=2, values_only=True):
        tree.insert("", "end", values=row)

    # CRUD: Editar e Excluir
    def editar_item():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Atenção", "Selecione uma linha para editar.")
            return
        item = tree.item(selected[0])
        valores = item["values"]

        edit_window = tk.Toplevel(janela_planilha)
        edit_window.title("Editar Registro")
        edit_window.configure(bg="#000000")

        entries = []
        for i, col in enumerate(colunas):
            ttk.Label(edit_window, text=col).grid(row=i, column=0)
            entry = ttk.Entry(edit_window)
            entry.grid(row=i, column=1)
            entry.insert(0, valores[i])
            entries.append(entry)

        def salvar_edicao():
            for idx, entry in enumerate(entries):
                valores[idx] = entry.get()
            tree.item(selected[0], values=valores)

            # Atualizar no Excel
            for i, row in enumerate(ws.iter_rows(min_row=2), start=2):
                if [cell.value for cell in row] == item["values"]:
                    for j, cell in enumerate(row):
                        cell.value = valores[j]
                    wb.save(excel_file)
                    break
            edit_window.destroy()
            messagebox.showinfo("Sucesso", "Registro atualizado.")

        ttk.Button(edit_window, text="Salvar", command=salvar_edicao).grid(row=len(colunas), column=0, columnspan=2, pady=5)

    def excluir_item():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Atenção", "Selecione uma linha para excluir.")
            return
        confirm = messagebox.askyesno("Confirmar", "Tem certeza que deseja excluir o registro?")
        if confirm:
            item = tree.item(selected[0])
            valores = item["values"]
            tree.delete(selected[0])

            # Excluir no Excel
            for i, row in enumerate(ws.iter_rows(min_row=2), start=2):
                if [cell.value for cell in row] == valores:
                    ws.delete_rows(i)
                    wb.save(excel_file)
                    break
            messagebox.showinfo("Sucesso", "Registro excluído.")

    ttk.Button(janela_planilha, text="Editar", command=editar_item).pack(side="left", padx=10, pady=5)
    ttk.Button(janela_planilha, text="Excluir", command=excluir_item).pack(side="left", padx=10, pady=5)

def powerby():
    global excel_file
    if not excel_file:
        messagebox.showwarning("Atenção", "Nenhum arquivo Excel carregado.")
        return
    wb = openpyxl.load_workbook(excel_file)
    ws = wb.active

    total_vendas = 0
    total_arrecadado = 0.0
    for row in ws.iter_rows(min_row=2, values_only=True):
        total_vendas += 1
        total_arrecadado += float(row[4])

    messagebox.showinfo("PowerBy", f"Total de vendas: {total_vendas}\nTotal arrecadado: R$ {round(total_arrecadado, 2)}")

def calcular_preco(produto, quantidade):
    if produto == "Combo Individual":
        return round(quantidade * 29.99, 2)
    elif produto == "Combo Família":
        return round(quantidade * 79.99, 2)
    elif produto == "Kilo":
        return round((quantidade / 1000) * 89.99, 2)
    return 0.0

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
    if not excel_file:
        messagebox.showwarning("Atenção", "Selecione ou crie um arquivo Excel antes.")
        return
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
    quantidade_var.set(0)
    quantidade_gramas_var.set(0)
    delivery_type_var.set("")

# ---------- Interface gráfica ----------
root = tk.Tk()
root.title("Sistema de Vendas e Comandas")
root.configure(bg="#000000")

style = ttk.Style()
style.theme_use("clam")
style.configure("TLabel", foreground="#FFA500", background="#000000")
style.configure("TButton", foreground="#FFFFFF", background="#FFA500", font=("Helvetica", 10, "bold"))
style.map("TButton", background=[("active", "#FF8C00")])
style.configure("TCombobox", foreground="#FFA500", fieldbackground="#000000", background="#000000")
style.configure("Treeview", background="#000000", foreground="#FFA500", fieldbackground="#000000", rowheight=25)
style.map("Treeview", background=[("selected", "#FFA500")], foreground=[("selected", "#000000")])

# Botão de Configurações
menu_button = ttk.Menubutton(root, text="Configurações", direction="below")
menu = tk.Menu(menu_button, tearoff=0, bg="#000000", fg="#FFA500")
menu.add_command(label="Abrir Planilha", command=abrir_planilha)
menu.add_command(label="PowerBy", command=powerby)
menu_button["menu"] = menu
menu_button.pack(side="top", anchor="nw", padx=5, pady=5)

# Frame de Vendas
frame_venda = ttk.LabelFrame(root, text="Venda")
frame_venda.configure(style="TLabel")
frame_venda.pack(side="left", padx=10, pady=10, fill="both")

ttk.Label(frame_venda, text="Produto").grid(row=0, column=0)
product_type_var = tk.StringVar()
ttk.Combobox(frame_venda, textvariable=product_type_var, values=["Combo Individual", "Combo Família", "Kilo"]).grid(row=0, column=1)

ttk.Label(frame_venda, text="Qtd Produtos").grid(row=1, column=0)
quantidade_var = tk.DoubleVar()
ttk.Combobox(frame_venda, textvariable=quantidade_var, values=de1a100).grid(row=1, column=1)

ttk.Label(frame_venda, text="Qtd (g)").grid(row=2, column=0)
quantidade_gramas_var = tk.DoubleVar()
ttk.Combobox(frame_venda, textvariable=quantidade_gramas_var, values=de50em100).grid(row=2, column=1)

ttk.Label(frame_venda, text="Entrega").grid(row=3, column=0)
delivery_type_var = tk.StringVar()
ttk.Combobox(frame_venda, textvariable=delivery_type_var, values=["Retirada", "Entrega"]).grid(row=3, column=1)

ttk.Button(frame_venda, text="Adicionar ao Carrinho", command=adicionar_ao_carrinho).grid(row=4, column=0, columnspan=2, pady=5)
ttk.Button(frame_venda, text="Finalizar Venda", command=registrar_carrinho).grid(row=5, column=0, columnspan=2, pady=5)
ttk.Button(frame_venda, text="Selecionar Pasta", command=selecionar_diretorio).grid(row=6, column=0, columnspan=2, pady=5)
ttk.Button(frame_venda, text="Carregar Arquivo Excel", command=selecionar_arquivo_excel).grid(row=7, column=0, columnspan=2, pady=5)

# Frame Carrinho
frame_carrinho = ttk.LabelFrame(root, text="Carrinho")
frame_carrinho.configure(style="TLabel")
frame_carrinho.pack(side="left", padx=10, pady=10, fill="both")

lista_carrinho = ttk.Treeview(frame_carrinho, columns=("Produto", "Qtd", "Preço", "Entrega"), show="headings", height=7)
for col in ("Produto", "Qtd", "Preço", "Entrega"):
    lista_carrinho.heading(col, text=col)
lista_carrinho.pack(padx=5, pady=5)

ttk.Label(frame_carrinho, text="Total:").pack()
preco_total_carrinho_var = tk.StringVar(value="R$ 0.0")
ttk.Label(frame_carrinho, textvariable=preco_total_carrinho_var, font=("Helvetica", 10, "bold")).pack()

root.mainloop()
