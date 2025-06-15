import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import os

class ExcelMergerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("PyMerger - Unir Arquivos Excel")

        self.arquivos = []

        # Widgets
        ttk.Label(master, text="Arquivos Selecionados").pack(pady=5)

        self.lista_arquivos = tk.Listbox(master, width=60, height=8)
        self.lista_arquivos.pack(pady=5)

        frame_botoes = ttk.Frame(master)
        frame_botoes.pack()

        ttk.Button(frame_botoes, text="Selecionar Arquivos", command=self.selecionar_arquivos).grid(row=0, column=0, padx=5)
        ttk.Button(frame_botoes, text="Remover Selecionado", command=self.remover_arquivo).grid(row=0, column=1, padx=5)
        ttk.Button(frame_botoes, text="Mesclar Arquivos", command=self.mesclar_arquivos).grid(row=0, column=2, padx=5)

    def selecionar_arquivos(self):
        novos = filedialog.askopenfilenames(title="Selecione arquivos Excel", filetypes=[("Arquivos Excel", "*.xlsx")])
        for arquivo in novos:
            if arquivo not in self.arquivos:
                self.arquivos.append(arquivo)
                self.lista_arquivos.insert(tk.END, os.path.basename(arquivo))

    def remover_arquivo(self):
        selecao = self.lista_arquivos.curselection()
        if selecao:
            idx = selecao[0]
            self.lista_arquivos.delete(idx)
            del self.arquivos[idx]

    def mesclar_arquivos(self):
        if len(self.arquivos) < 2:
            messagebox.showwarning("Atenção", "Selecione ao menos dois arquivos para mesclar.")
            return

        try:
            df_merged = pd.DataFrame()
            for arquivo in self.arquivos:
                df = pd.read_excel(arquivo)
                df_merged = pd.concat([df_merged, df], ignore_index=True)

            save_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel", "*.xlsx")], title="Salvar arquivo mesclado")
            if save_path:
                df_merged.to_excel(save_path, index=False)
                messagebox.showinfo("Sucesso", f"Arquivo salvo em:\n{save_path}")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao mesclar os arquivos:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ExcelMergerApp(root)
    root.mainloop()
