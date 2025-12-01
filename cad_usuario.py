import customtkinter as ctk
from tkinter import messagebox, ttk
from PIL import Image
import mysql.connector
import os


# ================= CONEXÃO BANCO (separado, mantém seu conectar local) =================
def conectar():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="MAJu2022@",
        database="erp_sistema"
    )


# ================= TELA CADASTRO USUÁRIO =================
def cadastro_usuario(frame_conteudo, dados=None, on_show_small_logo=None, on_show_big_logo=None):
    """
    Observações:
    - assinatura aceita callbacks on_show_small_logo e on_show_big_logo (passadas pelo portal).
    - se forem None, o módulo apenas tenta funcionar sem controlar a logo.
    - 'dados' pode ser None ou um dict com keys id, nome, login, senha, email, perfil
    """

    # limpa conteúdo
    for widget in frame_conteudo.winfo_children():
        widget.destroy()

    # pedimos ao portal para diminuir a logo se callback foi passado
    if callable(on_show_small_logo):
        try:
            on_show_small_logo()
        except Exception:
            pass

    # layout base (muito similar ao que você forneceu)
    frame_conteudo.grid_propagate(False)
    frame_conteudo.configure(fg_color="#d9d9d9")

    # ---------- título ----------
    titulo = ctk.CTkLabel(
        frame_conteudo,
        text="Cadastro de Usuário",
        font=("Arial", 28, "bold")
    )
    titulo.place(relx=0.569, rely=0.3, anchor="center")

    frame_central = ctk.CTkFrame(frame_conteudo, fg_color="transparent")
    frame_central.place(relx=0.5, rely=0.5, anchor="center")

    # ---------- imagem ----------
    frame_img = ctk.CTkFrame(frame_central, fg_color="transparent")
    frame_img.grid(row=0, column=0, padx=(20, 40), pady=10)

    try:
        diretorio_base = os.path.dirname(os.path.abspath(__file__))
        caminho_img = os.path.join(diretorio_base, "imagens", "usuario_lock.png")
        img_user = ctk.CTkImage(light_image=Image.open(caminho_img), size=(200, 200))
        lbl_img = ctk.CTkLabel(frame_img, image=img_user, text="")
        lbl_img.pack()
    except Exception:
        lbl_img = ctk.CTkLabel(frame_img, text="(Imagem)", width=200, height=200)
        lbl_img.pack()

    # ---------- formulário ----------
    frame_form = ctk.CTkFrame(frame_central, fg_color="transparent")
    frame_form.grid(row=0, column=1, pady=10)

    entry_nome = ctk.CTkEntry(frame_form, placeholder_text="Nome", width=320)
    entry_nome.grid(row=0, column=0, pady=8)

    entry_login = ctk.CTkEntry(frame_form, placeholder_text="Login", width=320)
    entry_login.grid(row=1, column=0, pady=8)

    entry_senha = ctk.CTkEntry(frame_form, placeholder_text="Senha", show="*", width=320)
    entry_senha.grid(row=2, column=0, pady=8)

    entry_email = ctk.CTkEntry(frame_form, placeholder_text="Email", width=320)
    entry_email.grid(row=3, column=0, pady=8)

    combo_perfil = ctk.CTkOptionMenu(frame_form, values=["Master", "Administrador", "Usuário"], width=320)
    combo_perfil.set("Perfil")
    combo_perfil.grid(row=4, column=0, pady=8)

    usuario_id = None
    if dados:
        usuario_id = dados.get("id")
        entry_nome.insert(0, dados["nome"])
        entry_login.insert(0, dados["login"])
        entry_senha.insert(0, dados["senha"])
        entry_email.insert(0, dados.get("email", ""))
        combo_perfil.set(dados["perfil"])

    # ---------- FUNÇÕES ----------
    def gravar():
        nonlocal usuario_id
        nome = entry_nome.get().strip()
        login_val = entry_login.get().strip()
        senha_val = entry_senha.get().strip()
        email = entry_email.get().strip()
        perfil = combo_perfil.get()

        if not nome or not login_val or not senha_val or perfil == "Perfil":
            messagebox.showwarning("Aviso", "Preencha todos os campos!")
            return

        con = None
        try:
            con = conectar()
            cur = con.cursor()

            if usuario_id:
                cur.execute("""
                    UPDATE usuario
                    SET nome=%s, login=%s, senha=%s, email=%s, perfil=%s
                    WHERE id=%s
                """, (nome, login_val, senha_val, email, perfil, usuario_id))
                messagebox.showinfo("Atualizado", f"Usuário '{login_val}' atualizado com sucesso!")
            else:
                cur.execute("SELECT id FROM usuario WHERE login=%s", (login_val,))
                existente = cur.fetchone()
                if existente:
                    messagebox.showwarning("Aviso", "Este login já está cadastrado!")
                    return
                cur.execute("""
                    INSERT INTO usuario (nome, login, senha, email, perfil)
                    VALUES (%s, %s, %s, %s, %s)
                """, (nome, login_val, senha_val, email, perfil))
                messagebox.showinfo("Sucesso", f"Usuário '{nome}' cadastrado com sucesso!")

            con.commit()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gravar usuário:\n{e}")
        finally:
            if con:
                con.close()

    def procurar():
        # abre tela procurar reutilizando função local que está depois
        abrir_tela_procurar(frame_conteudo, on_show_small_logo, on_show_big_logo)

    def limpar():
        nonlocal usuario_id
        usuario_id = None
        entry_nome.delete(0, "end")
        entry_login.delete(0, "end")
        entry_senha.delete(0, "end")
        entry_email.delete(0, "end")
        combo_perfil.set("Perfil")

    def sair():
        # limpa a tela de conteúdo e pede ao portal para mostrar logo grande
        for widget in frame_conteudo.winfo_children():
            widget.destroy()
        if callable(on_show_big_logo):
            try:
                on_show_big_logo()
            except Exception:
                pass

    # ---------- botões ----------
    frame_botoes = ctk.CTkFrame(frame_form, fg_color="transparent")
    frame_botoes.grid(row=5, column=0, pady=(30, 10))

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


# ================= TELA PROCURAR =================
def abrir_tela_procurar(frame_conteudo, on_show_small_logo=None, on_show_big_logo=None):
    for widget in frame_conteudo.winfo_children():
        widget.destroy()

    # pedir logo pequena (se callback)
    if callable(on_show_small_logo):
        try:
            on_show_small_logo()
        except Exception:
            pass

    lbl = ctk.CTkLabel(frame_conteudo, text="Buscar Usuário", font=("Arial", 24, "bold"))
    lbl.pack(pady=10)

    # Contêiner para entrada de texto e emoji lado a lado
    container = ctk.CTkFrame(frame_conteudo)
    container.pack(pady=10)

    entry_busca = ctk.CTkEntry(container, placeholder_text="Digite o nome", width=320)
    entry_busca.pack(side="left")

    emoji_lbl = ctk.CTkLabel(container, text="🔍", font=("Arial", 20))
    emoji_lbl.pack(side="left", padx=(5, 0))

    frame_tree = ctk.CTkFrame(frame_conteudo)
    frame_tree.pack(expand=True, fill="both", pady=10)

    # ---------- Treeview ----------
    style = ttk.Style()
    style.theme_use("default")
    style.configure("Treeview", font=("Arial", 12), rowheight=30)
    style.configure("Treeview.Heading", font=("Arial", 12, "bold"))

    tree = ttk.Treeview(frame_tree, columns=("id", "nome", "login", "email", "perfil"), show="headings", height=10)
    tree.heading("id", text="ID")
    tree.heading("nome", text="Nome")
    tree.heading("login", text="Login")
    tree.heading("email", text="Email")
    tree.heading("perfil", text="Perfil")
    tree.column("id", width=40, anchor="center")
    tree.column("nome", width=180)
    tree.column("login", width=120)
    tree.column("email", width=180)
    tree.column("perfil", width=90, anchor="center")
    tree.pack(side="left", fill="both", expand=True)

    # ---------- Scrollbar ----------
    scrollbar = ttk.Scrollbar(frame_tree, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    # ---------- Tags para cores alternadas ----------
    tree.tag_configure("oddrow", background="white")
    tree.tag_configure("evenrow", background="#f0f0f0")  # cinza claro

    # ---------- buscar no banco ----------
    def executar_busca(event=None):
        for i in tree.get_children():
            tree.delete(i)

        con = None
        try:
            con = conectar()
            cur = con.cursor()
            termo = entry_busca.get().strip()
            if termo == "":
                cur.execute("SELECT id, nome, login, senha, email, perfil FROM usuario ORDER BY nome")
            else:
                cur.execute("""
                    SELECT id, nome, login, senha, email, perfil
                    FROM usuario
                    WHERE nome LIKE %s
                    ORDER BY nome
                """, (f"%{termo}%",))
            registros = cur.fetchall()
            for idx, (id_, nome, login, senha, email, perfil) in enumerate(registros):
                tag = "evenrow" if idx % 2 == 0 else "oddrow"
                tree.insert("", "end", values=(id_, nome, login, email, perfil), tags=(tag, senha))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao buscar usuários:\n{e}")
        finally:
            if con:
                con.close()

    # ---------- abrir usuário selecionado ----------
    def abrir_usuario_por_selecao():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("Aviso", "Selecione um usuário na lista!")
            return
        item = sel[0]
        vals = tree.item(item, "values")
        tags = tree.item(item, "tags")
        senha = tags[1] if len(tags) > 1 else ""
        dados = {
            "id": vals[0],
            "nome": vals[1],
            "login": vals[2],
            "senha": senha,
            "email": vals[3],
            "perfil": vals[4]
        }
        cadastro_usuario(frame_conteudo, dados, on_show_small_logo, on_show_big_logo)

    def abrir_usuario_por_click(event):
        item = tree.identify_row(event.y)
        if not item:
            return
        vals = tree.item(item, "values")
        tags = tree.item(item, "tags")
        senha = tags[1] if len(tags) > 1 else ""
        dados = {
            "id": vals[0],
            "nome": vals[1],
            "login": vals[2],
            "senha": senha,
            "email": vals[3],
            "perfil": vals[4]
        }
        cadastro_usuario(frame_conteudo, dados, on_show_small_logo, on_show_big_logo)

    entry_busca.bind("<Return>", executar_busca)
    tree.bind("<Double-1>", abrir_usuario_por_click)
    tree.bind("<ButtonRelease-1>", abrir_usuario_por_click)

    executar_busca()

    # ---------- botões ----------
    frame_botoes = ctk.CTkFrame(frame_conteudo, fg_color="transparent")
    frame_botoes.pack(pady=10)

    btn_abrir = ctk.CTkButton(frame_botoes, text="Abrir", command=abrir_usuario_por_selecao,
                              fg_color="#2e8bff", hover_color="#1c5fb8", width=120)
    btn_abrir.grid(row=0, column=0, padx=10)

    btn_buscar = ctk.CTkButton(frame_botoes, text="Buscar", command=executar_busca,
                               fg_color="#2e8bff", hover_color="#1c5fb8", width=120)
    btn_buscar.grid(row=0, column=1, padx=10)

    btn_sair = ctk.CTkButton(frame_botoes, text="Sair",
                             command=lambda: cadastro_usuario(frame_conteudo, None, on_show_small_logo, on_show_big_logo),
                             fg_color="red", hover_color="#cc0000", width=120)
    btn_sair.grid(row=0, column=2, padx=10)
    # pedir logo grande ao sair (se callback)
    def sair_procurar():
        for widget in frame_conteudo.winfo_children():
            widget.destroy()
        if callable(on_show_big_logo):
            try:
                on_show_big_logo()
            except Exception:
                pass        