import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

# Configuração do banco de dados SQLite
conn = sqlite3.connect('cadastro_notas.db')
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS alunos (
        matricula TEXT PRIMARY KEY,
        nome TEXT NOT NULL,
        nota1 REAL NOT NULL,
        nota2 REAL NOT NULL,
        nota3 REAL NOT NULL,
        nota4 REAL NOT NULL
    )
''')
conn.commit()

def adicionar_aluno():
    matricula = entry_matricula.get()
    nome = entry_nome.get()
    try:
        nota1 = float(entry_nota1.get())
        nota2 = float(entry_nota2.get())
        nota3 = float(entry_nota3.get())
        nota4 = float(entry_nota4.get())
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira notas válidas.")
        return

    if not matricula or not nome:
        messagebox.showerror("Erro", "Todos os campos são obrigatórios.")
        return

    try:
        c.execute('INSERT INTO alunos (matricula, nome, nota1, nota2, nota3, nota4) VALUES (?, ?, ?, ?, ?, ?)',
                  (matricula, nome, nota1, nota2, nota3, nota4))
        conn.commit()
        messagebox.showinfo("Sucesso", "Aluno adicionado com sucesso!")
        exibir_resultados()
        limpar_campos()
    except sqlite3.IntegrityError:
        messagebox.showerror("Erro", "Matrícula já cadastrada.")

def exibir_resultados(filtro_nome=None):
    for row in tree.get_children():
        tree.delete(row)

    query = 'SELECT * FROM alunos'
    params = ()

    if filtro_nome:
        query += ' WHERE nome LIKE ?'
        params = (f'%{filtro_nome}%',)

    c.execute(query, params)
    for aluno in c.fetchall():
        media = (aluno[2] + aluno[3] + aluno[4] + aluno[5]) / 4
        situacao = "APROVADO" if media >= 6 else "REPROVADO"
        tree.insert('', 'end', values=(aluno[0], aluno[1], aluno[2], aluno[3], aluno[4], aluno[5], f"{media:.1f}", situacao))

def limpar_campos():
    entry_matricula.delete(0, tk.END)
    entry_nome.delete(0, tk.END)
    entry_nota1.delete(0, tk.END)
    entry_nota2.delete(0, tk.END)
    entry_nota3.delete(0, tk.END)
    entry_nota4.delete(0, tk.END)

def excluir_aluno():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Erro", "Selecione um aluno para excluir.")
        return
    matricula = tree.item(selected_item)['values'][0]
    c.execute('DELETE FROM alunos WHERE matricula = ?', (matricula,))
    conn.commit()
    messagebox.showinfo("Sucesso", "Aluno excluído com sucesso!")
    exibir_resultados()

def iniciar_edicao():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Erro", "Selecione um aluno para editar.")
        return
    global aluno_editando
    aluno_editando = tree.item(selected_item)['values']
    entry_matricula.delete(0, tk.END)
    entry_nome.delete(0, tk.END)
    entry_nota1.delete(0, tk.END)
    entry_nota2.delete(0, tk.END)
    entry_nota3.delete(0, tk.END)
    entry_nota4.delete(0, tk.END)
    entry_matricula.insert(0, aluno_editando[0])
    entry_nome.insert(0, aluno_editando[1])
    entry_nota1.insert(0, aluno_editando[2])
    entry_nota2.insert(0, aluno_editando[3])
    entry_nota3.insert(0, aluno_editando[4])
    entry_nota4.insert(0, aluno_editando[5])

def salvar_edicao():
    if aluno_editando is None:
        return
    matricula = entry_matricula.get()
    nome = entry_nome.get()
    try:
        nota1 = float(entry_nota1.get())
        nota2 = float(entry_nota2.get())
        nota3 = float(entry_nota3.get())
        nota4 = float(entry_nota4.get())
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira notas válidas.")
        return

    c.execute('UPDATE alunos SET matricula = ?, nome = ?, nota1 = ?, nota2 = ?, nota3 = ?, nota4 = ? WHERE matricula = ?',
              (matricula, nome, nota1, nota2, nota3, nota4, aluno_editando[0]))
    conn.commit()
    messagebox.showinfo("Sucesso", "Aluno atualizado com sucesso!")
    exibir_resultados()
    limpar_campos()

def buscar_aluno():
    filtro_nome = entry_busca.get()
    exibir_resultados(filtro_nome)

# Configuração da interface gráfica
root = tk.Tk()
root.title("Cadastro de Notas do Aluno")
root.geometry("800x600")
root.configure(bg="#f4f4f9")

frame = tk.Frame(root, bg="#f4f4f9")
frame.pack(pady=20)

tk.Label(frame, text="Matrícula:", bg="#f4f4f9").grid(row=0, column=0)
entry_matricula = tk.Entry(frame)
entry_matricula.grid(row=0, column=1)

tk.Label(frame, text="Nome:", bg="#f4f4f9").grid(row=1, column=0)
entry_nome = tk.Entry(frame)
entry_nome.grid(row=1, column=1)

tk.Label(frame, text="Nota 1:", bg="#f4f4f9").grid(row=2, column=0)
entry_nota1 = tk.Entry(frame)
entry_nota1.grid(row=2, column=1)

tk.Label(frame, text="Nota 2:", bg="#f4f4f9").grid(row=3, column=0)
entry_nota2 = tk.Entry(frame)
entry_nota2.grid(row=3, column=1)

tk.Label(frame, text="Nota 3:", bg="#f4f4f9").grid(row=4, column=0)
entry_nota3 = tk.Entry(frame)
entry_nota3.grid(row=4, column=1)

tk.Label(frame, text="Nota 4:", bg="#f4f4f9").grid(row=5, column=0)
entry_nota4 = tk.Entry(frame)
entry_nota4.grid(row=5, column=1)

tk.Button(frame, text="Adicionar Aluno", command=adicionar_aluno, bg="#4CAF50", fg="white").grid(row=6, columnspan=2, pady=10)
tk.Button(frame, text="Excluir Aluno", command=excluir_aluno, bg="#f44336", fg="white").grid(row=7, columnspan=2, pady=10)
tk.Button(frame, text="Iniciar Edição", command=iniciar_edicao, bg="#00acc1", fg="white").grid(row=8, columnspan=2, pady=10)
tk.Button(frame, text="Salvar Edição", command=salvar_edicao, bg="#00796b", fg="white").grid(row=9, columnspan=2, pady=10)

# Campo de busca
tk.Label(root, text="Buscar por Nome:", bg="#f4f4f9").pack(pady=10)
entry_busca = tk.Entry(root)
entry_busca.pack(pady=5)
tk.Button(root, text="Buscar", command=buscar_aluno, bg="#4CAF50", fg="white").pack(pady=5)

# Configuração da tabela
tree = ttk.Treeview(root, columns=("matricula", "nome", "nota1", "nota2", "nota3", "nota4", "media", "situacao"), show='headings')
tree.heading("matricula", text="Matrícula")
tree.heading("nome", text="Nome")
tree.heading("nota1", text="Nota 1")
tree.heading("nota2", text="Nota 2")
tree.heading("nota3", text="Nota 3")
tree.heading("nota4", text="Nota 4")
tree.heading("media", text="Média")
tree.heading("situacao", text="Situação Final")

# Adicionando a barra de rolagem horizontal
scroll_x = ttk.Scrollbar(root, orient="horizontal", command=tree.xview)
scroll_x.pack(side='bottom', fill='x')
tree.configure(xscrollcommand=scroll_x.set)

# Adicionando a tabela ao layout
tree.pack(expand=True, fill='both', padx=20, pady=20)

# Iniciar o programa
aluno_editando = None
exibir_resultados()
root.mainloop()

# Fechar a conexão com o banco de dados
conn.close()
