import random
import tkinter as tk

root = tk.Tk() 
root.title("My Bingo Program")
root.geometry("600x600")
    
root.configure(bg='#267326')  # Cor de fundo da janela principal, ctrl + shift + L

label = tk.Label(root, text="Bem-vindo ao Bingo!", bg='white', font=("Arial", 16))
label.grid(row=0, column=0, columnspan=5, rowspan=1, sticky="nsew")

def gerar_numeros():
    numeros = [] 
    for col in range(5):
        inicio = col * 15 +1
        fim = inicio + 14
        numeros.append(random.sample(range(inicio, fim + 1),5))
    return numeros

# Gerar os números para a cartela
numeros_cartela = gerar_numeros()

# Criar a grade de 5x5
for row in range(5):
    for col in range(5):
        if row == 2 and col == 2:
            bnt = tk.Button(root, text="BINGO", width=8, height=3, bg="#f2f20d", state="disabled")#, font=("Arial", 10, "bold")
        else:
            numero = numeros_cartela[col][row]
            # Criar botões para cada célula
            btn = tk.Button(root, text="", width=8, height=3, bg="lightgray")
            btn.grid(row=row+1, column=col, padx=5, pady=5)  # Adicionar o botão ao grid
            
        #Responsividade dos botoes (ignorar por agora):
# for row in range(6):  # Incluímos a linha do título
#     root.grid_rowconfigure(row, weight=1)
# for col in range(5):
#     root.grid_columnconfigure(col, weight=1)

root.mainloop()