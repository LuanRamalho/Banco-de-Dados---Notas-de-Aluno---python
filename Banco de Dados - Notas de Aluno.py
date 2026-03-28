import tkinter as tk
from tkinter import messagebox, ttk
import json
import os

# Configuração do "Banco de Dados" JSON
ARQUIVO_DB = 'cadastro_notas.json'

def carregar_dados():
    if not os.path.exists(ARQUIVO_DB):
        return [] # Retorna lista para manter compatibilidade com seu arquivo
    try:
        with open(ARQUIVO_DB, 'r', encoding='utf-8') as f:
            conteudo = json.load(f)
            return conteudo if isinstance(conteudo, list) else []
    except (json.JSONDecodeError, IOError):
        return []

def salvar_dados(dados):
    try:
        with open(ARQUIVO_DB, 'w', encoding='utf-8') as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)
    except IOError:
        messagebox.showerror("Erro", "Não foi possível salvar os dados no arquivo JSON.")

def adicionar_aluno():
    matricula = entry_matricula.get().strip()
    nome = entry_nome.get().strip()
    
    try:
        n1 = float(entry_nota1.get())
        n2 = float(entry_nota2.get())
        n3 = float(entry_nota3.get())
        n4 = float(entry_nota4.get())
        media = (n1 + n2 + n3 + n4) / 4
        situacao = "APROVADO" if media >= 6 else "REPROVADO"
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira notas válidas.")
        return

    if not matricula or not nome:
        messagebox.showerror("Erro", "Todos os campos são obrigatórios.")
        return

    dados = carregar_dados()
    
    # Verifica se a matrícula já existe na lista
    if any(aluno.get("Matricula") == matricula for aluno in dados):
        messagebox.showerror("Erro", "Matrícula já cadastrada.")
        return

    novo_aluno = {
        "Matricula": matricula,
        "Nome": nome,
        "Nota1": round(n1, 1),
        "Nota2": round(n2, 1),
        "Nota3": round(n3, 1),
        "Nota4": round(n4, 1),
        "Media": round(media, 1),
        "Situacao": situacao
    }
    
    dados.append(novo_aluno)
    salvar_dados(dados)
    messagebox.showinfo("Sucesso", "Aluno adicionado com sucesso!")
    exibir_resultados()
    limpar_campos()

def exibir_resultados(filtro_nome=None):
    for row in tree.get_children():
        tree.delete(row)

    dados = carregar_dados()

    for aluno in dados:
        nome_aluno = aluno.get('Nome', '')
        
        if filtro_nome and filtro_nome.lower() not in nome_aluno.lower():
            continue
            
        # Formatando os valores para 1 casa decimal na exibição
        n1 = f"{float(aluno.get('Nota1', 0)):.1f}"
        n2 = f"{float(aluno.get('Nota2', 0)):.1f}"
        n3 = f"{float(aluno.get('Nota3', 0)):.1f}"
        n4 = f"{float(aluno.get('Nota4', 0)):.1f}"
        media = f"{float(aluno.get('Media', 0)):.1f}"
        
        tree.insert('', 'end', values=(
            aluno.get('Matricula'), 
            nome_aluno, 
            n1, n2, n3, n4, media,
            aluno.get('Situacao')
        ))

def excluir_aluno():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Erro", "Selecione um aluno para excluir.")
        return
        
    matricula = str(tree.item(selected_item)['values'][0])
    dados = carregar_dados()
    
    # Filtra a lista removendo o aluno selecionado
    novos_dados = [a for a in dados if str(a.get("Matricula")) != matricula]
    
    if len(novos_dados) < len(dados):
        salvar_dados(novos_dados)
        messagebox.showinfo("Sucesso", "Aluno excluído com sucesso!")
        exibir_resultados()

def iniciar_edicao():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Erro", "Selecione um aluno para editar.")
        return
    
    global aluno_original_matricula
    valores = tree.item(selected_item)['values']
    aluno_original_matricula = str(valores[0])
    
    limpar_campos()
    entry_matricula.insert(0, valores[0])
    entry_nome.insert(0, valores[1])
    entry_nota1.insert(0, valores[2])
    entry_nota2.insert(0, valores[3])
    entry_nota3.insert(0, valores[4])
    entry_nota4.insert(0, valores[5])

def salvar_edicao():
    if aluno_original_matricula is None:
        return
        
    nova_matricula = entry_matricula.get().strip()
    nome = entry_nome.get().strip()
    
    try:
        n1 = float(entry_nota1.get())
        n2 = float(entry_nota2.get())
        n3 = float(entry_nota3.get())
        n4 = float(entry_nota4.get())
        media = (n1 + n2 + n3 + n4) / 4
        situacao = "APROVADO" if media >= 6 else "REPROVADO"
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira notas válidas.")
        return

    dados = carregar_dados()
    
    for aluno in dados:
        if str(aluno.get("Matricula")) == aluno_original_matricula:
            aluno["Matricula"] = nova_matricula
            aluno["Nome"] = nome
            aluno["Nota1"] = round(n1, 1)
            aluno["Nota2"] = round(n2, 1)
            aluno["Nota3"] = round(n3, 1)
            aluno["Nota4"] = round(n4, 1)
            aluno["Media"] = round(media, 1)
            aluno["Situacao"] = situacao
            break
    
    salvar_dados(dados)
    messagebox.showinfo("Sucesso", "Aluno atualizado com sucesso!")
    exibir_resultados()
    limpar_campos()

def buscar_aluno():
    exibir_resultados(entry_busca.get().strip())

def limpar_campos():
    entry_matricula.delete(0, tk.END)
    entry_nome.delete(0, tk.END)
    entry_nota1.delete(0, tk.END)
    entry_nota2.delete(0, tk.END)
    entry_nota3.delete(0, tk.END)
    entry_nota4.delete(0, tk.END)

# --- Interface Gráfica ---
root = tk.Tk()
root.title("Cadastro de Notas - JSON NoSQL")
root.geometry("800x650")
root.configure(bg="#f4f4f9")

frame = tk.Frame(root, bg="#f4f4f9")
frame.pack(pady=10)

labels = ["Matrícula:", "Nome:", "Nota 1:", "Nota 2:", "Nota 3:", "Nota 4:"]
entries = []

for i, texto in enumerate(labels):
    tk.Label(frame, text=texto, bg="#f4f4f9").grid(row=i, column=0, sticky="e", padx=5)
    ent = tk.Entry(frame)
    ent.grid(row=i, column=1, pady=2)
    entries.append(ent)

entry_matricula, entry_nome, entry_nota1, entry_nota2, entry_nota3, entry_nota4 = entries

tk.Button(frame, text="Adicionar Aluno", command=adicionar_aluno, bg="#4CAF50", fg="white", width=20).grid(row=6, columnspan=2, pady=5)
tk.Button(frame, text="Excluir Aluno", command=excluir_aluno, bg="#f44336", fg="white", width=20).grid(row=7, columnspan=2, pady=5)
tk.Button(frame, text="Iniciar Edição", command=iniciar_edicao, bg="#00acc1", fg="white", width=20).grid(row=8, columnspan=2, pady=5)
tk.Button(frame, text="Salvar Edição", command=salvar_edicao, bg="#00796b", fg="white", width=20).grid(row=9, columnspan=2, pady=5)

busca_frame = tk.Frame(root, bg="#f4f4f9")
busca_frame.pack(pady=10)
tk.Label(busca_frame, text="Buscar por Nome:", bg="#f4f4f9").pack(side="left")
entry_busca = tk.Entry(busca_frame)
entry_busca.pack(side="left", padx=5)
tk.Button(busca_frame, text="Buscar", command=buscar_aluno, bg="#4CAF50", fg="white").pack(side="left")

tree = ttk.Treeview(root, columns=("mat", "nom", "n1", "n2", "n3", "n4", "med", "sit"), show='headings')
colunas = [("mat", "Matrícula"), ("nom", "Nome"), ("n1", "N1"), ("n2", "N2"), ("n3", "N3"), ("n4", "N4"), ("med", "Média"), ("sit", "Situação")]
for id_col, texto in colunas:
    tree.heading(id_col, text=texto)
    tree.column(id_col, width=90, anchor="center")

tree.pack(expand=True, fill='both', padx=20, pady=10)

aluno_original_matricula = None
exibir_resultados()
root.mainloop()
