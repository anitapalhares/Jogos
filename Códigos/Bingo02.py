import tkinter as tk
import random

# Função para gerar números aleatórios para cada coluna de acordo com o intervalo do bingo
def gerar_numeros_bingo():
    # Criar uma lista de números para cada intervalo do bingo
    colunas = [
        random.sample(range(1, 16), 5),  # Números de 1 a 15
        random.sample(range(16, 31), 5), # Números de 16 a 30
        random.sample(range(31, 46), 5), # Números de 31 a 45
        random.sample(range(46, 61), 5), # Números de 46 a 60
        random.sample(range(61, 76), 5)  # Números de 61 a 75
    ]
    # Ordenar as colunas para garantir que os números na grid fiquem em ordem crescente
    for i in range(5):
        colunas[i].sort(reverse=True)
        
    return colunas

# Função para criar o grid
def criar_grid():
    global btns  # Referência aos botões para poder desabilitar depois
    btns = []  # Lista para armazenar os botões do grid
    colunas = gerar_numeros_bingo()
    
    for i in range(5):
        for j in range(5):
            # A posição central (2,2) será o botão BINGO
            if i == 2 and j == 2:
                btn = tk.Button(root, text="BINGO", width=9, height=3, state=tk.DISABLED, bg="yellow", fg="Black", font=("Arial",30))
            else:
                num = colunas[i].pop()  # Pega o próximo número da coluna correspondente (pop no final)
                btn = tk.Button(root, text=str(num), width=20, height=8, 
                                command=lambda n=num: marcar_numero(n))
            
            btn.grid(row=i, column=j, padx=5, pady=5)
            btns.append(btn)  # Armazenando o botão na lista

# Função para sortear números
def sorteio():
    numero = random.choice(range(1, 76))
    while numero in numeros_sorteados:
        numero = random.choice(range(1, 76))  # Continua sorteando até encontrar um número não sorteado
    
    numeros_sorteados.add(numero)
    sorteio_label.config(text=f"Sorteio: {numero}")
    
    # Atualiza a lista de números sorteados
    lista_sorteados.config(state=tk.NORMAL)  # Torna o Listbox editável
    lista_sorteados.insert(tk.END, f"{numero} ")  # Adiciona o número sorteado ao final
    lista_sorteados.config(state=tk.DISABLED)  # Torna o Listbox não editável
    
    # Faz a rolagem do Listbox para o último item
    lista_sorteados.see(tk.END)  # Faz a barra de rolagem descer até o último item

    # Desabilitar o botão correspondente ao número sorteado
    for aparato in root.grid_slaves():
        if aparato.winfo_class() == 'Button' and aparato.cget("text") == str(numero):
            aparato.config(state=tk.DISABLED, bg="green")
    
    # Verifica se o jogador completou o bingo
    verificar_bingo()

# Função para marcar o número na grid
def marcar_numero(numero):
    for aparato in root.grid_slaves():
        if aparato.winfo_class() == 'Button' and aparato.cget("text") == str(numero):
            aparato.config(bg="green", state=tk.DISABLED)  # Marca o botão como "clicado" (verde)
    
    # Verifica se o jogador completou o bingo
    verificar_bingo()

# Função para verificar se o jogador completou o bingo
def verificar_bingo():
    # Verifica se todos os botões foram desabilitados (se todas as células estão marcadas)
    todos_marcados = all(btn.cget("state") == tk.DISABLED for btn in btns)
    
    if todos_marcados:
        mostrar_mensagem_parabens()

# Função para mostrar a mensagem de parabéns e a opção de reiniciar
def mostrar_mensagem_parabens():
    mensagem = tk.Label(root, text="Parabéns, você ganhou o Bingo!", font=("Arial", 20), fg="green", bg="lightblue")
    mensagem.grid(row=5, column=0, columnspan=5, pady=10)
    
    # Botão para reiniciar o jogo
    reiniciar_button = tk.Button(root, text="Reiniciar Jogo", font=("Arial", 16), command=reiniciar_jogo, bg="lightblue")
    reiniciar_button.grid(row=6, column=0, columnspan=5, pady=10)

# Função para reiniciar o jogo
def reiniciar_jogo():
    global numeros_sorteados, btns
    # Limpa a lista de números sorteados e a grid
    numeros_sorteados = set()
    for btn in btns:
        btn.config(bg="lightblue", state=tk.NORMAL)
    
    sorteio_label.config(text="Sorteio: Nenhum")
    lista_sorteados.config(state=tk.NORMAL)
    lista_sorteados.delete(0, tk.END)
    lista_sorteados.config(state=tk.DISABLED)
    
    # Recria o grid de bingo
    for widget in root.grid_slaves():
        widget.grid_forget()
    criar_grid()

# Criando a janela principal
root = tk.Tk()
root.title("Bingo")
root.configure(bg="lightblue")

# Adicionando o quadrado para mostrar o número sorteado
numeros_sorteados = set()  # Para armazenar os números sorteados

# Label para mostrar o número sorteado
sorteio_label = tk.Label(root, text="Sorteio: Nenhum", font=("Arial", 16), bg="lightblue", width=15, height=2, relief="solid")
sorteio_label.grid(row=0, column=5, padx=10, pady=10)

# Frame para a lista de números sorteados e a barra de rolagem
frame_lista = tk.Frame(root)
frame_lista.grid(row=1, column=5, padx=10, pady=10)

# Listbox para exibir os números sorteados
lista_sorteados = tk.Listbox(frame_lista, font=("Arial", 14), height=10, width=15, selectmode=tk.SINGLE, bg="lightgray")
lista_sorteados.grid(row=0, column=0)

# Barra de rolagem
scrollbar = tk.Scrollbar(frame_lista, orient="vertical", command=lista_sorteados.yview)
scrollbar.grid(row=0, column=1, sticky="ns")

# Vincula a rolagem do Listbox com a barra de rolagem
lista_sorteados.config(yscrollcommand=scrollbar.set)

# Listbox inicializado como não editável
lista_sorteados.config(state=tk.DISABLED)

# Botão para sortear o próximo número
sorteio_button = tk.Button(root, text="Sortear Número", font=("Arial", 16), command=sorteio, bg="lightgreen")
sorteio_button.grid(row=2, column=5, padx=10, pady=10)

# Criando o grid de bingo
criar_grid()

# Iniciando o loop principal
root.mainloop()