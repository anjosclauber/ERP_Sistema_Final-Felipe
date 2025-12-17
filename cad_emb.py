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

def cadastro_embalagem(frame_conteudo, dados=None, on_show_small_logo=None, on_show_big_logo=None):
    for widget in frame_conteudo.winfo_children():
        widget.destroy()
    if callable(on_show_small_logo):
        try: on_show_small_logo()
        except: pass
    frame_conteudo.configure(fg_color="#e1f1fd")

    main_frame = ctk.CTkFrame(
        frame_conteudo,
        fg_color="#eaf6ff",
        border_color="#1976d2",
        border_width=2,
        width=700,
        height=350,
    )
    main_frame.place(relx=0.5, rely=0.5, anchor="center")

    ctk.CTkLabel(
        main_frame,
        text="Cadastro de Embalagem",
        font=("Arial", 28, "bold"),
        text_color="#1976d2",
    ).place(relx=0.5, y=40, anchor="center")

    ctk.CTkLabel(
        main_frame,
        text="Nome da Embalagem",
        font=("Arial", 18, "bold"),
        text_color="#1976d2",
    ).place(x=75, y=100)

    entry_nome = ctk.CTkEntry(main_frame, width=400, height=32, placeholder_text="Digite o nome da embalagem")
    entry_nome.place(x=75, y=135)

    embalagem_id = None
    if dados:
        embalagem_id = dados.get("id")
        entry_nome.insert(0, dados["nome"])

    def gravar():
        nonlocal embalagem_id
        nome = entry_nome.get().strip()
        if not nome:
            messagebox.showwarning("Aviso", "Preencha o nome da embalagem!")
            return
        con = None
        try:
            con = conectar()
            cur = con.cursor()
            if embalagem_id:
                cur.execute("UPDATE embalagem SET nome=%s WHERE id=%s", (nome, embalagem_id))
                messagebox.showinfo("Atualizado", "Embalagem atualizada com sucesso!")
            else:
                cur.execute("SELECT id FROM embalagem WHERE nome=%s", (nome,))
                if cur.fetchone():
                    messagebox.showwarning("Aviso", "Esta embalagem já existe!")
                    return
                cur.execute("INSERT INTO embalagem (nome) VALUES (%s)", (nome,))
                messagebox.showinfo("Sucesso", "Embalagem cadastrada com sucesso!")
            con.commit()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gravar embalagem:\n{e}")
        finally:
            if con: con.close()

    def procurar():
        abrir_tela_procurar_embalagem(frame_conteudo, on_show_small_logo, on_show_big_logo)

    def limpar():
        nonlocal embalagem_id
        embalagem_id = None
        entry_nome.delete(0, "end")

    def sair():
        for widget in frame_conteudo.winfo_children():
            widget.destroy()
        if callable(on_show_big_logo):
            try: on_show_big_logo()
            except: pass

    # Botões em linha na base do main_frame
    def pack_button(text, cmd, color, xpos, hover_color="#0b60c9", width=None, height=None):
        btn = ctk.CTkButton(
            main_frame,
            text=text,
            width=width if width is not None else 120,
            height=height if height is not None else 32,
            fg_color=color,
            hover_color=hover_color,
            font=("Arial", 14, "bold"),
            command=cmd,
        )
        btn.place(x=xpos, y=250)

    pack_button("Gravar", gravar, "#1f80ff", 75)
    pack_button("Procurar", procurar, "#1f80ff", 205)
    pack_button("Limpar", limpar, "#1f80ff", 335)
    pack_button("Sair", sair, "#e53935", 465, hover_color="#cc0000")

def abrir_tela_procurar_embalagem(frame_conteudo, on_show_small_logo=None, on_show_big_logo=None):
    for widget in frame_conteudo.winfo_children():
        widget.destroy()
    if callable(on_show_small_logo):
        try: on_show_small_logo()
        except: pass
    frame_conteudo.configure(fg_color="#e1f1fd")

    main_frame = ctk.CTkFrame(
        frame_conteudo,
        fg_color="#eaf6ff",
        border_color="#1976d2",
        border_width=2,
        width=700,
        height=400,
    )
    main_frame.place(relx=0.5, rely=0.5, anchor="center")

    ctk.CTkLabel(
        main_frame,
        text="Buscar Embalagem",
        font=("Arial", 24, "bold"),
        text_color="#1976d2",
    ).place(relx=0.5, y=40, anchor="center")

    ctk.CTkLabel(
        main_frame,
        text="Nome",
        font=("Arial", 16, "bold"),
        text_color="#1976d2",
    ).place(x=75, y=90)

    entry_busca = ctk.CTkEntry(main_frame, width=320, height=28, placeholder_text="Digite o nome da embalagem")
    entry_busca.place(x=150, y=90)

    emoji_lbl = ctk.CTkLabel(main_frame, text="🔍", font=("Arial", 20))
    emoji_lbl.place(x=480, y=90)

    # Tabela
    table_frame = ctk.CTkFrame(
        main_frame,
        fg_color="#eaf6ff",
        width=550,
        height=180,
    )
    table_frame.place(x=75, y=130)

    style = ttk.Style()
    style.theme_use("default")
    style.configure("Treeview", font=("Arial", 12), rowheight=28)
    style.configure("Treeview.Heading", font=("Arial", 12, "bold"))

    tree = ttk.Treeview(table_frame, columns=("id", "nome"), show="headings", height=6)
    tree.heading("id", text="ID")
    tree.heading("nome", text="Nome")
    tree.column("id", width=60, anchor="center")
    tree.column("nome", width=400)
    tree.place(x=0, y=0, width=500, height=170)

    scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
    scrollbar.place(x=500, y=0, height=170)
    tree.configure(yscroll=scrollbar.set)
    tree.tag_configure("oddrow", background="#ffffff")
    tree.tag_configure("evenrow", background="#f5f7fb")

    def executar_busca(event=None):
        for i in tree.get_children():
            tree.delete(i)
        con = None
        try:
            con = conectar()
            cur = con.cursor()
            termo = entry_busca.get().strip()
            if termo == "":
                cur.execute("SELECT id, nome FROM embalagem ORDER BY nome")
            else:
                cur.execute("SELECT id, nome FROM embalagem WHERE nome LIKE %s ORDER BY nome", (f"%{termo}%",))
            registros = cur.fetchall()
            for idx, (id_, nome) in enumerate(registros):
                tag = "evenrow" if idx % 2 == 0 else "oddrow"
                tree.insert("", "end", values=(id_, nome), tags=(tag,))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao buscar embalagens:\n{e}")
        finally:
            if con: con.close()

    def abrir_embalagem_por_click(event):
        item = tree.identify_row(event.y) if event else tree.focus()
        if not item:
            return
        vals = tree.item(item, "values")
        dados = {"id": vals[0], "nome": vals[1]}
        cadastro_embalagem(frame_conteudo, dados, on_show_small_logo, on_show_big_logo)

    entry_busca.bind("<Return>", executar_busca)
    tree.bind("<Double-1>", abrir_embalagem_por_click)
    tree.bind("<ButtonRelease-1>", abrir_embalagem_por_click)
    executar_busca()

    # Botões em linha na base do main_frame
    def pack_button(text, cmd, color, xpos, hover_color="#0b60c9", width=None, height=None):
        btn = ctk.CTkButton(
            main_frame,
            text=text,
            width=width if width is not None else 120,
            height=height if height is not None else 32,
            fg_color=color,
            hover_color=hover_color,
            font=("Arial", 14, "bold"),
            command=cmd,
        )
        btn.place(x=xpos, y=340)

    pack_button("Abrir", lambda: abrir_embalagem_por_click(None), "#1f80ff", 75)
    pack_button("Buscar", executar_busca, "#1f80ff", 205)
    pack_button("Sair", lambda: cadastro_embalagem(frame_conteudo, None, on_show_small_logo, on_show_big_logo), "#e53935", 335, hover_color="#cc0000")
