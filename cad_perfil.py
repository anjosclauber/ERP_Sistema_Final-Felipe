import customtkinter as ctk
from tkinter import messagebox, ttk
import mysql.connector

def conectar():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="MAJu2022@",
        database="erp_sistema"
    )

def cadastro_perfil(frame_conteudo, dados=None, on_show_small_logo=None, on_show_big_logo=None):
    for widget in frame_conteudo.winfo_children():
        widget.destroy()
    if callable(on_show_small_logo):
        try: on_show_small_logo()
        except: pass
    frame_conteudo.grid_propagate(False)
    frame_conteudo.configure(fg_color="#d9d9d9")
    titulo = ctk.CTkLabel(frame_conteudo, text="Cadastro de Perfil", font=("Arial", 28, "bold"))
    titulo.place(relx=0.5, rely=0.28, anchor="center")
    frame_central = ctk.CTkFrame(frame_conteudo, fg_color="transparent")
    frame_central.place(relx=0.5, rely=0.5, anchor="center")
    frame_form = ctk.CTkFrame(frame_central, fg_color="transparent")
    frame_form.pack()
    entry_nome = ctk.CTkEntry(frame_form, placeholder_text="Nome do Perfil", width=320)
    entry_nome.grid(row=0, column=0, pady=8)
    perfil_id = None
    if dados:
        perfil_id = dados.get("id")
        entry_nome.insert(0, dados["nome"])
    def gravar():
        nonlocal perfil_id
        nome = entry_nome.get().strip()
        if not nome:
            messagebox.showwarning("Aviso", "Preencha o nome do perfil!")
            return
        con = None
        try:
            con = conectar()
            cur = con.cursor()
            if perfil_id:
                cur.execute("UPDATE perfil SET nome=%s WHERE id=%s", (nome, perfil_id))
                messagebox.showinfo("Atualizado", "Perfil atualizado com sucesso!")
            else:
                cur.execute("SELECT id FROM perfil WHERE nome=%s", (nome,))
                if cur.fetchone():
                    messagebox.showwarning("Aviso", "Este perfil já existe!")
                    return
                cur.execute("INSERT INTO perfil (nome) VALUES (%s)", (nome,))
                messagebox.showinfo("Sucesso", "Perfil cadastrado com sucesso!")
            con.commit()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gravar perfil:\n{e}")
        finally:
            if con: con.close()
    def procurar():
        abrir_tela_procurar_perfil(frame_conteudo, on_show_small_logo, on_show_big_logo)
    def limpar():
        nonlocal perfil_id
        perfil_id = None
        entry_nome.delete(0, "end")
    def sair():
        for widget in frame_conteudo.winfo_children():
            widget.destroy()
        if callable(on_show_big_logo):
            try: on_show_big_logo()
            except: pass
    frame_botoes = ctk.CTkFrame(frame_form, fg_color="transparent")
    frame_botoes.grid(row=1, column=0, pady=(30, 10))
    btn_gravar = ctk.CTkButton(frame_botoes, text="Gravar", width=120, command=gravar,
                               fg_color="#2e8bff", hover_color="#1c5fb8")
    btn_gravar.grid(row=0, column=0, padx=6)
    btn_procurar = ctk.CTkButton(frame_botoes, text="Procurar", width=120, command=procurar,
                                 fg_color="#2e8bff", hover_color="#1c5fb8")
    btn_procurar.grid(row=0, column=1, padx=6)
    btn_limpar = ctk.CTkButton(frame_botoes, text="Limpar", width=120, command=limpar,
                               fg_color="#2e8bff", hover_color="#1c5fb8")
    btn_limpar.grid(row=0, column=2, padx=6)
    btn_sair = ctk.CTkButton(frame_botoes, text="Sair", width=120, command=sair,
                             fg_color="red", hover_color="#cc0000")
    btn_sair.grid(row=0, column=3, padx=6)

def abrir_tela_procurar_perfil(frame_conteudo, on_show_small_logo=None, on_show_big_logo=None):
    for widget in frame_conteudo.winfo_children():
        widget.destroy()
    if callable(on_show_small_logo):
        try: on_show_small_logo()
        except: pass
    lbl = ctk.CTkLabel(frame_conteudo, text="Buscar Perfil", font=("Arial", 24, "bold"))
    lbl.pack(pady=10)
    container = ctk.CTkFrame(frame_conteudo)
    container.pack(pady=10)
    entry_busca = ctk.CTkEntry(container, placeholder_text="Digite o nome", width=320)
    entry_busca.pack(side="left")
    emoji_lbl = ctk.CTkLabel(container, text="🔍", font=("Arial", 20))
    emoji_lbl.pack(side="left", padx=(5, 0))
    frame_tree = ctk.CTkFrame(frame_conteudo)
    frame_tree.pack(expand=True, fill="both", pady=10)
    style = ttk.Style()
    style.theme_use("default")
    style.configure("Treeview", font=("Arial", 12), rowheight=30)
    style.configure("Treeview.Heading", font=("Arial", 12, "bold"))
    tree = ttk.Treeview(frame_tree, columns=("id", "nome"), show="headings", height=10)
    tree.heading("id", text="ID")
    tree.heading("nome", text="Nome")
    tree.column("id", width=60, anchor="center")
    tree.column("nome", width=220)
    tree.pack(side="left", fill="both", expand=True)
    scrollbar = ttk.Scrollbar(frame_tree, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    tree.tag_configure("oddrow", background="white")
    tree.tag_configure("evenrow", background="#f0f0f0")
    def executar_busca(event=None):
        for i in tree.get_children():
            tree.delete(i)
        con = None
        try:
            con = conectar()
            cur = con.cursor()
            termo = entry_busca.get().strip()
            if termo == "":
                cur.execute("SELECT id, nome FROM perfil ORDER BY nome")
            else:
                cur.execute("SELECT id, nome FROM perfil WHERE nome LIKE %s ORDER BY nome", (f"%{termo}%",))
            registros = cur.fetchall()
            for idx, (id_, nome) in enumerate(registros):
                tag = "evenrow" if idx % 2 == 0 else "oddrow"
                tree.insert("", "end", values=(id_, nome), tags=(tag,))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao buscar perfis:\n{e}")
        finally:
            if con: con.close()
    def abrir_perfil_por_click(event):
        item = tree.identify_row(event.y)
        if not item:
            return
        vals = tree.item(item, "values")
        dados = {"id": vals[0], "nome": vals[1]}
        cadastro_perfil(frame_conteudo, dados, on_show_small_logo, on_show_big_logo)
    entry_busca.bind("<Return>", executar_busca)
    tree.bind("<Double-1>", abrir_perfil_por_click)
    tree.bind("<ButtonRelease-1>", abrir_perfil_por_click)
    executar_busca()
    frame_botoes = ctk.CTkFrame(frame_conteudo, fg_color="transparent")
    frame_botoes.pack(pady=10)
    btn_abrir = ctk.CTkButton(frame_botoes, text="Abrir", command=lambda: abrir_perfil_por_click(None),
                              fg_color="#2e8bff", hover_color="#1c5fb8", width=120)
    btn_abrir.grid(row=0, column=0, padx=10)
    btn_buscar = ctk.CTkButton(frame_botoes, text="Buscar", command=executar_busca,
                               fg_color="#2e8bff", hover_color="#1c5fb8", width=120)
    btn_buscar.grid(row=0, column=1, padx=10)
    btn_sair = ctk.CTkButton(frame_botoes, text="Sair",
                             command=lambda: cadastro_perfil(frame_conteudo, None, on_show_small_logo, on_show_big_logo),
                             fg_color="red", hover_color="#cc0000", width=120)
    btn_sair.grid(row=0, column=2, padx=10)
