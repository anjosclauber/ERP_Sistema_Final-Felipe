import customtkinter as ctk
from tkinter import messagebox, ttk
from PIL import Image
import mysql.connector
import os

# --------- Função de conexão ao MySQL ---------
def conectar():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="MAJu2022@",
        database="erp_sistema"
    )

# --------- Cadastro de fornecedor ---------
def cadastro_fornecedor(frame_conteudo, dados=None, on_show_small_logo=None, on_show_big_logo=None):
    for widget in frame_conteudo.winfo_children():
        widget.destroy()
    if callable(on_show_small_logo):
        try:
            on_show_small_logo()
        except Exception:
            pass
    frame_conteudo.configure(fg_color="#e1f1fd")

    main_frame = ctk.CTkFrame(
        frame_conteudo,
        fg_color="#eaf6ff",
        border_color="#1976d2",
        border_width=2,
        width=700,
        height=600,
    )
    main_frame.place(relx=0.5, rely=0.5, anchor="center")

    ctk.CTkLabel(
        main_frame,
        text="Cadastro de Fornecedor",
        font=("Arial", 28, "bold"),
        text_color="#1976d2",
    ).place(relx=0.5, y=40, anchor="center")

    # Centralizar tudo dentro do main_frame (borda azul)
    form_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
    form_frame.place(relx=0.5, rely=0.5, anchor="center")

    # Nome
    ctk.CTkLabel(form_frame, text="Nome", font=("Arial", 16, "bold"), text_color="#1976d2").grid(row=0, column=0, sticky="w", padx=(0,10), pady=(0,2))
    entry_nome = ctk.CTkEntry(form_frame, width=350, height=28, placeholder_text="Digite o nome")
    entry_nome.grid(row=1, column=0, sticky="w", padx=(0,10), pady=(0,10))

    # CPF
    ctk.CTkLabel(form_frame, text="CPF", font=("Arial", 16, "bold"), text_color="#1976d2").grid(row=2, column=0, sticky="w", padx=(0,10), pady=(0,2))
    entry_cpf = ctk.CTkEntry(form_frame, width=220, height=28, placeholder_text="CPF")
    entry_cpf.grid(row=3, column=0, sticky="w", padx=(0,10), pady=(0,10))

    # Endereço
    ctk.CTkLabel(form_frame, text="Endereço", font=("Arial", 16, "bold"), text_color="#1976d2").grid(row=4, column=0, sticky="w", padx=(0,10), pady=(0,2))
    entry_endereco = ctk.CTkEntry(form_frame, width=350, height=28, placeholder_text="Endereço")
    entry_endereco.grid(row=5, column=0, sticky="w", padx=(0,10), pady=(0,10))

    # Complemento
    ctk.CTkLabel(form_frame, text="Complemento", font=("Arial", 16, "bold"), text_color="#1976d2").grid(row=6, column=0, sticky="w", padx=(0,10), pady=(0,2))
    entry_complemento = ctk.CTkEntry(form_frame, width=220, height=28, placeholder_text="Complemento")
    entry_complemento.grid(row=7, column=0, sticky="w", padx=(0,10), pady=(0,10))

    # Bairro
    ctk.CTkLabel(form_frame, text="Bairro", font=("Arial", 16, "bold"), text_color="#1976d2").grid(row=8, column=0, sticky="w", padx=(0,10), pady=(0,2))
    entry_bairro = ctk.CTkEntry(form_frame, width=180, height=28, placeholder_text="Bairro")
    entry_bairro.grid(row=9, column=0, sticky="w", padx=(0,10), pady=(0,10))

    # Telefone
    ctk.CTkLabel(form_frame, text="Telefone", font=("Arial", 16, "bold"), text_color="#1976d2").grid(row=10, column=0, sticky="w", padx=(0,10), pady=(0,2))
    entry_telefone = ctk.CTkEntry(form_frame, width=180, height=28, placeholder_text="Telefone")
    entry_telefone.grid(row=11, column=0, sticky="w", padx=(0,10), pady=(0,10))

    # Cidade
    ctk.CTkLabel(form_frame, text="Cidade", font=("Arial", 16, "bold"), text_color="#1976d2").grid(row=12, column=0, sticky="w", padx=(0,10), pady=(0,2))
    entry_cidade = ctk.CTkEntry(form_frame, width=180, height=28, placeholder_text="Cidade")
    entry_cidade.grid(row=13, column=0, sticky="w", padx=(0,10), pady=(0,10))

    # Estado (Combobox igual ao exemplo)
    ctk.CTkLabel(form_frame, text="Estado", font=("Arial", 16, "bold"), text_color="#1976d2").grid(row=14, column=0, sticky="w", padx=(0,10), pady=(0,2))
    try:
        con = conectar()
        cur = con.cursor()
        cur.execute("SELECT nome, sigla FROM estado ORDER BY nome")
        estados = cur.fetchall()
        con.close()
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao carregar estados:\\n{e}")
        estados = []
    estados_formatados = [f"{nome} | {sigla}" for nome, sigla in estados]
    combobox_estado = ttk.Combobox(form_frame, values=estados_formatados, width=20, font=("Arial", 14))
    combobox_estado.grid(row=15, column=0, sticky="w", padx=(0,10), pady=(0,10))
    combobox_estado.set("Selecione o Estado")

    # Email
    ctk.CTkLabel(form_frame, text="Email", font=("Arial", 16, "bold"), text_color="#1976d2").grid(row=16, column=0, sticky="w", padx=(0,10), pady=(0,2))
    entry_email = ctk.CTkEntry(form_frame, width=370, height=28, placeholder_text="Email")
    entry_email.grid(row=17, column=0, sticky="w", padx=(0,10), pady=(0,10))

    fornecedor_id = None
    if dados:
        fornecedor_id = dados.get("id")
        entry_nome.insert(0, dados.get("nome", ""))
        entry_cpf.insert(0, dados.get("cnpj_cpf", ""))
        entry_telefone.insert(0, dados.get("telefone", ""))
        entry_endereco.insert(0, dados.get("endereco", ""))
        entry_bairro.insert(0, dados.get("bairro", ""))
        entry_cidade.insert(0, dados.get("cidade", ""))
        entry_estado.insert(0, dados.get("estado", ""))
        entry_email.insert(0, dados.get("email", ""))

    def gravar():
        nonlocal fornecedor_id
        nome = entry_nome.get().strip()
        cnpj_cpf = entry_cpf.get().strip()
        telefone = entry_telefone.get().strip()
        endereco = entry_endereco.get().strip()
        bairro = entry_bairro.get().strip()
        cidade = entry_cidade.get().strip()
        estado = entry_estado.get().strip()
        email = entry_email.get().strip()
        if not nome or not cnpj_cpf:
            messagebox.showwarning("Aviso", "Preencha os campos obrigatórios!")
            return
        con = None
        try:
            con = conectar()
            cur = con.cursor()
            if fornecedor_id:
                cur.execute("""
                    UPDATE fornecedor
                    SET nome=%s, cnpj_cpf=%s, telefone=%s, endereco=%s, bairro=%s,
                        cidade=%s, estado=%s, email=%s
                    WHERE id=%s
                """, (nome, cnpj_cpf, telefone, endereco, bairro, cidade, estado, email, fornecedor_id))
                messagebox.showinfo("Atualizado", "Fornecedor atualizado com sucesso!")
            else:
                cur.execute("""
                    INSERT INTO fornecedor (nome, cnpj_cpf, telefone, endereco, bairro, cidade, estado, email)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (nome, cnpj_cpf, telefone, endereco, bairro, cidade, estado, email))
                messagebox.showinfo("Sucesso", "Fornecedor cadastrado com sucesso!")
            con.commit()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gravar fornecedor:\n{e}")
        finally:
            if con:
                con.close()

    def procurar():
        abrir_tela_procurar_fornecedor(frame_conteudo, on_show_small_logo, on_show_big_logo)

    def limpar():
        nonlocal fornecedor_id
        fornecedor_id = None
        for entry in entries:
            entry.delete(0, "end")

    def sair():
        for widget in frame_conteudo.winfo_children():
            widget.destroy()
        if callable(on_show_big_logo):
            try:
                on_show_big_logo()
            except Exception:
                pass

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
        btn.place(x=xpos, y=520)

    pack_button("Gravar", gravar, "#1f80ff", 75)
    pack_button("Procurar", procurar, "#1f80ff", 205)
    pack_button("Limpar", limpar, "#1f80ff", 335)
    pack_button("Sair", sair, "#e53935", 465, hover_color="#cc0000")

def abrir_tela_procurar_fornecedor(frame_conteudo, on_show_small_logo=None, on_show_big_logo=None):
    for widget in frame_conteudo.winfo_children():
        widget.destroy()
    if callable(on_show_small_logo):
        try:
            on_show_small_logo()
        except Exception:
            pass
    frame_conteudo.configure(fg_color="#e1f1fd")

    main_frame = ctk.CTkFrame(
        frame_conteudo,
        fg_color="#eaf6ff",
        border_color="#1976d2",
        border_width=2,
        width=900,
        height=500,
    )
    main_frame.place(relx=0.5, rely=0.5, anchor="center")

    ctk.CTkLabel(
        main_frame,
        text="Buscar Fornecedor",
        font=("Arial", 24, "bold"),
        text_color="#1976d2",
    ).place(relx=0.5, y=40, anchor="center")

    ctk.CTkLabel(
        main_frame,
        text="Nome",
        font=("Arial", 16, "bold"),
        text_color="#1976d2",
    ).place(x=75, y=90)

    entry_busca = ctk.CTkEntry(main_frame, width=320, height=28, placeholder_text="Digite o nome do fornecedor")
    entry_busca.place(x=150, y=90)

    emoji_lbl = ctk.CTkLabel(main_frame, text="🔍", font=("Arial", 20))
    emoji_lbl.place(x=480, y=90)

    # Tabela
    table_frame = ctk.CTkFrame(
        main_frame,
        fg_color="#eaf6ff",
        width=750,
        height=250,
    )
    table_frame.place(x=75, y=130)

    style = ttk.Style()
    style.theme_use("default")
    style.configure("Treeview", font=("Arial", 12), rowheight=28)
    style.configure("Treeview.Heading", font=("Arial", 12, "bold"))

    tree = ttk.Treeview(table_frame, columns=(
        "id", "nome", "cnpj_cpf", "telefone", "endereco", "bairro", "cidade", "estado", "email"
    ), show="headings", height=8)
    for col, width in zip(
        ["id", "nome", "cnpj_cpf", "telefone", "endereco", "bairro", "cidade", "estado", "email"],
        [40, 140, 100, 100, 150, 90, 90, 60, 140]
    ):
        tree.heading(col, text=col.capitalize())
        tree.column(col, width=width, anchor="center" if col in ["id", "estado"] else "w")
    tree.place(x=0, y=0, width=700, height=220)

    scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
    scrollbar.place(x=700, y=0, height=220)
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
                cur.execute("SELECT id, nome, cnpj_cpf, telefone, endereco, bairro, cidade, estado, email FROM fornecedor ORDER BY nome")
            else:
                cur.execute("""
                    SELECT id, nome, cnpj_cpf, telefone, endereco, bairro, cidade, estado, email
                    FROM fornecedor WHERE nome LIKE %s ORDER BY nome
                """, (f"%{termo}%",))
            registros = cur.fetchall()
            for idx, row in enumerate(registros):
                tag = "evenrow" if idx % 2 == 0 else "oddrow"
                tree.insert("", "end", values=row, tags=(tag,))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao buscar fornecedores:\n{e}")
        finally:
            if con:
                con.close()

    def abrir_fornecedor_por_selecao():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("Aviso", "Selecione um fornecedor!")
            return
        item = sel[0]
        vals = tree.item(item, "values")
        dados = {
            "id": vals[0], "nome": vals[1], "cnpj_cpf": vals[2], "telefone": vals[3],
            "endereco": vals[4], "bairro": vals[5], "cidade": vals[6], "estado": vals[7], "email": vals[8]
        }
        cadastro_fornecedor(frame_conteudo, dados, on_show_small_logo, on_show_big_logo)

    def abrir_fornecedor_por_click(event):
        item = tree.identify_row(event.y)
        if not item:
            return
        vals = tree.item(item, "values")
        dados = {
            "id": vals[0], "nome": vals[1], "cnpj_cpf": vals[2], "telefone": vals[3],
            "endereco": vals[4], "bairro": vals[5], "cidade": vals[6], "estado": vals[7], "email": vals[8]
        }
        cadastro_fornecedor(frame_conteudo, dados, on_show_small_logo, on_show_big_logo)

    entry_busca.bind("<Return>", executar_busca)
    tree.bind("<Double-1>", abrir_fornecedor_por_click)
    tree.bind("<ButtonRelease-1>", abrir_fornecedor_por_click)
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
        btn.place(x=xpos, y=400)

    pack_button("Abrir", abrir_fornecedor_por_selecao, "#1f80ff", 75)
    pack_button("Buscar", executar_busca, "#1f80ff", 205)
    pack_button("Sair", lambda: cadastro_fornecedor(frame_conteudo, None, on_show_small_logo, on_show_big_logo), "#e53935", 335, hover_color="#cc0000")
