import pandas as pd
import matplotlib.pyplot as plt
import os
import matplotlib as plt

excel_file = os.path.join(os.path.dirname(__file__), "vendas.xlsx")

def processar_vendas():
    if not os.path.exists(excel_file):
        print("Arquivo de vendas não encontrado.")
        return

    # Lê o Excel
    df = pd.read_excel(excel_file)

    # Agrupa por produto
    agrupado = df.groupby("Produto").agg({
        "Quantidade": "sum",
        "Preço": "sum"
    }).reset_index()

    # Exibe gráfico de pizza
    plt.figure(figsize=(6, 6))
    plt.pie(agrupado["Quantidade"], labels=agrupado["Produto"], autopct="%1.1f%%", startangle=140)
    plt.title("Participação nas Vendas por Produto")
    plt.axis("equal")
    plt.show()

    print("\nResumo de Vendas por Produto:")
    print(agrupado)

if __name__ == "__main__":
    processar_vendas()
