
# ================== Cadastro de Cliente (Novo Layout) ====================
import customtkinter as ctk
from tkinter import ttk, messagebox
from PIL import Image
import os
from db import conectar

def cadastro_cliente(frame_conteudo, dados=None, on_show_small_logo=None, on_show_big_logo=None):
    for widget in frame_conteudo.winfo_children():
        widget.destroy()

    frame_conteudo.configure(fg_color="#e1f1fd")

    main_frame = ctk.CTkFrame(
        frame_conteudo,
        fg_color="#eaf6ff",
        border_color="#1976d2",
        border_width=2,
        width=1000,
        height=650,
    )
    main_frame.place(relx=0.5, rely=0.5, anchor="center")


    ctk.CTkLabel(
        main_frame,
        text="Cadastro de Cliente",
        font=("Arial", 32, "bold"),
        text_color="#1976d2",
    ).place(relx=0.5, y=70, anchor="center")

    # Centralizar tudo dentro do main_frame (borda azul)
    form_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
    form_frame.place(relx=0.5, rely=0.5, anchor="center")

    # Nome e CPF
    ctk.CTkLabel(form_frame, text="Nome", font=("Arial", 16, "bold"), text_color="#1976d2").grid(row=0, column=0, sticky="w", padx=(0,10), pady=(0,2))
    entry_nome = ctk.CTkEntry(form_frame, width=350, height=28, placeholder_text="Digite o nome")
    entry_nome.grid(row=1, column=0, sticky="w", padx=(0,10), pady=(0,10))
    ctk.CTkLabel(form_frame, text="CPF", font=("Arial", 16, "bold"), text_color="#1976d2").grid(row=0, column=1, sticky="w", padx=(0,10), pady=(0,2))
    entry_cpf = ctk.CTkEntry(form_frame, width=220, height=28, placeholder_text="CPF")
    entry_cpf.grid(row=1, column=1, sticky="w", padx=(0,10), pady=(0,10))

    # Endereço e Complemento
    ctk.CTkLabel(form_frame, text="Endereço", font=("Arial", 16, "bold"), text_color="#1976d2").grid(row=2, column=0, sticky="w", padx=(0,10), pady=(0,2))
    entry_endereco = ctk.CTkEntry(form_frame, width=350, height=28, placeholder_text="Endereço")
    entry_endereco.grid(row=3, column=0, sticky="w", padx=(0,10), pady=(0,10))
    ctk.CTkLabel(form_frame, text="Complemento", font=("Arial", 16, "bold"), text_color="#1976d2").grid(row=2, column=1, sticky="w", padx=(0,10), pady=(0,2))
    entry_complemento = ctk.CTkEntry(form_frame, width=220, height=28, placeholder_text="Complemento")
    entry_complemento.grid(row=3, column=1, sticky="w", padx=(0,10), pady=(0,10))

    # Bairro, Telefone, Cidade
    ctk.CTkLabel(form_frame, text="Bairro", font=("Arial", 16, "bold"), text_color="#1976d2").grid(row=4, column=0, sticky="w", padx=(0,10), pady=(0,2))
    entry_bairro = ctk.CTkEntry(form_frame, width=180, height=28, placeholder_text="Bairro")
    entry_bairro.grid(row=5, column=0, sticky="w", padx=(0,10), pady=(0,10))
    ctk.CTkLabel(form_frame, text="Telefone", font=("Arial", 16, "bold"), text_color="#1976d2").grid(row=4, column=1, sticky="w", padx=(0,10), pady=(0,2))
    entry_telefone = ctk.CTkEntry(form_frame, width=180, height=28, placeholder_text="Telefone")
    entry_telefone.grid(row=5, column=1, sticky="w", padx=(0,10), pady=(0,10))
    ctk.CTkLabel(form_frame, text="Cidade", font=("Arial", 16, "bold"), text_color="#1976d2").grid(row=4, column=2, sticky="w", padx=(0,10), pady=(0,2))
    entry_cidade = ctk.CTkEntry(form_frame, width=180, height=28, placeholder_text="Cidade")
    entry_cidade.grid(row=5, column=2, sticky="w", padx=(0,10), pady=(0,10))

    # Estado e Email
    ctk.CTkLabel(form_frame, text="Estado", font=("Arial", 16, "bold"), text_color="#1976d2").grid(row=6, column=0, sticky="w", padx=(0,10), pady=(0,2))
    try:
        con = conectar()
        cur = con.cursor()
        cur.execute("SELECT nome, sigla FROM estado ORDER BY nome")
        estados = cur.fetchall()
        con.close()
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao carregar estados:\n{e}")
        estados = []
    estados_formatados = [f"{nome} | {sigla}" for nome, sigla in estados]
    combobox_estado = ttk.Combobox(form_frame, values=estados_formatados, width=20, font=("Arial", 14))
    combobox_estado.grid(row=7, column=0, sticky="w", padx=(0,10), pady=(0,10))
    combobox_estado.set("Selecione o Estado")

    ctk.CTkLabel(form_frame, text="Email", font=("Arial", 16, "bold"), text_color="#1976d2").grid(row=6, column=1, sticky="w", padx=(0,10), pady=(0,2))
    entry_email = ctk.CTkEntry(form_frame, width=370, height=28, placeholder_text="Email")
    entry_email.grid(row=7, column=1, columnspan=2, sticky="w", padx=(0,10), pady=(0,10))

    # Variável de controle para edição
    cliente_id = None
    if dados:
        cliente_id = dados.get("id", None)
        entry_nome.insert(0, dados.get("nome", ""))
        entry_cpf.insert(0, dados.get("cpf", ""))
        entry_telefone.insert(0, dados.get("telefone", ""))
        entry_endereco.insert(0, dados.get("endereco", ""))
        entry_bairro.insert(0, dados.get("bairro", ""))
        entry_cidade.insert(0, dados.get("cidade", ""))
        estado_valor = dados.get("estado", "")
        if estado_valor:
            matches = [e for e in estados_formatados if estado_valor == e.split(" | ")[1]]
            combobox_estado.set(matches[0] if matches else estado_valor)
        entry_email.insert(0, dados.get("email", ""))

    # ====== BOTÕES (rodapé) ======
    def pack_button(text, cmd, color, xpos, hover_color="#0b60c9", width=None, height=None):
        btn = ctk.CTkButton(
            main_frame,
            text=text,
            width=width if width is not None else 110,
            height=height if height is not None else 28,
            fg_color=color,
            hover_color=hover_color,
            font=("Arial", 14, "bold"),
            command=cmd,
        )
        btn.place(x=xpos, y=380)

    def limpar():
        nonlocal cliente_id
        cliente_id = None
        entry_nome.delete(0, "end")
        entry_cpf.delete(0, "end")
        entry_telefone.delete(0, "end")
        entry_endereco.delete(0, "end")
        entry_bairro.delete(0, "end")
        entry_cidade.delete(0, "end")
        combobox_estado.set("Selecione o Estado")
        entry_email.delete(0, "end")

    def gravar():
        nonlocal cliente_id
        nome = entry_nome.get().strip()
        cpf = entry_cpf.get().strip()
        telefone = entry_telefone.get().strip()
        endereco = entry_endereco.get().strip()
        bairro = entry_bairro.get().strip()
        cidade = entry_cidade.get().strip()
        estado_completo = combobox_estado.get()
        email = entry_email.get().strip()
        if not nome or not cpf:
            messagebox.showwarning("Aviso", "Preencha pelo menos Nome e CPF!")
            return
        estado = ""
        if " | " in estado_completo:
            estado = estado_completo.split(" | ")[1]
        try:
            con = conectar()
            cur = con.cursor()
            if cliente_id:
                cur.execute("""
                    UPDATE cliente
                    SET nome=%s, cpf=%s, telefone=%s, endereco=%s, bairro=%s, cidade=%s, estado=%s, email=%s
                    WHERE id=%s
                """, (nome, cpf, telefone, endereco, bairro, cidade, estado, email, cliente_id))
                messagebox.showinfo("Atualizado", f"Cliente '{nome}' atualizado com sucesso!")
            else:
                cur.execute("SELECT id FROM cliente WHERE cpf=%s", (cpf,))
                existente = cur.fetchone()
                if existente:
                    messagebox.showwarning("Aviso", "Já existe um cliente cadastrado com este CPF!")
                    return
                cur.execute("""
                    INSERT INTO cliente (nome, cpf, telefone, endereco, bairro, cidade, estado, email)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (nome, cpf, telefone, endereco, bairro, cidade, estado, email))
                messagebox.showinfo("Sucesso", f"Cliente '{nome}' cadastrado com sucesso!")
            con.commit()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gravar cliente:\n{e}")
        finally:
            con.close()
        limpar()

    def procurar():
        from cad_cliente import abrir_tela_procurar_cliente
        abrir_tela_procurar_cliente(
            frame_conteudo,
            on_show_small_logo=on_show_small_logo,
            on_show_big_logo=on_show_big_logo
        )

    def sair():
        for widget in frame_conteudo.winfo_children():
            widget.destroy()

    # ====== BOTÕES ======
    # Botões alinhados com espaçamento de 30
    # Botões centralizados abaixo do formulário
    btn_x = 0
    btn_y = 380
    pack_button("Gravar", gravar, "#1f80ff", btn_x)
    pack_button("Procurar", procurar, "#1f80ff", btn_x + 140)
    pack_button("Limpar", limpar, "#1f80ff", btn_x + 280)
    pack_button("Sair", sair, "#e53935", btn_x + 420, hover_color="#cc0000")


# ================= TELA PROCURAR CLIENTE =================
def abrir_tela_procurar_cliente(frame_conteudo, on_show_small_logo=None, on_show_big_logo=None):
    for widget in frame_conteudo.winfo_children():
        widget.destroy()

    if callable(on_show_small_logo):
        try:
            on_show_small_logo()
        except Exception:
            pass

    lbl = ctk.CTkLabel(frame_conteudo, text="Buscar Cliente", font=("Arial", 24, "bold"))
    lbl.pack(pady=10)

    container = ctk.CTkFrame(frame_conteudo)
    container.pack(pady=10)

    entry_busca = ctk.CTkEntry(container, placeholder_text="Digite o nome do cliente", width=320)
    entry_busca.pack(side="left")

    emoji_lbl = ctk.CTkLabel(container, text="🔍", font=("Arial", 20))
    emoji_lbl.pack(side="left", padx=(5, 0))

    frame_tree = ctk.CTkFrame(frame_conteudo)
    frame_tree.pack(expand=True, fill="both", pady=10)

    style = ttk.Style()
    style.theme_use("default")
    style.configure("Treeview", font=("Arial", 12), rowheight=30)
    style.configure("Treeview.Heading", font=("Arial", 12, "bold"))

    columns = ("id", "nome", "cpf", "telefone", "endereco", "bairro", "cidade", "estado", "email")
    tree = ttk.Treeview(frame_tree, columns=columns, show="headings", height=10)
    for col, texto in zip(columns, ["ID", "Nome", "CPF", "Telefone", "Endereço", "Bairro", "Cidade", "Estado", "Email"]):
        tree.heading(col, text=texto)
    tree.column("id", width=40, anchor="center")
    tree.pack(side="left", fill="both", expand=True)

    scrollbar = ttk.Scrollbar(frame_tree, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    tree.tag_configure("oddrow", background="white")
    tree.tag_configure("evenrow", background="#f0f0f0")

    def executar_busca(event=None):
        for i in tree.get_children():
            tree.delete(i)
        try:
            con = conectar()
            cur = con.cursor()
            termo = entry_busca.get().strip()
            if termo == "":
                cur.execute("SELECT id, nome, cpf, telefone, endereco, bairro, cidade, estado, email FROM cliente ORDER BY nome")
            else:
                cur.execute("""
                    SELECT id, nome, cpf, telefone, endereco, bairro, cidade, estado, email 
                    FROM cliente WHERE nome LIKE %s ORDER BY nome
                """, (f"%{termo}%",))
            registros = cur.fetchall()
            for idx, linha in enumerate(registros):
                tag = "evenrow" if idx % 2 == 0 else "oddrow"
                tree.insert("", "end", values=linha, tags=(tag,))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao buscar clientes:\n{e}")
        finally:
            con.close()

    def abrir_cliente_por_click(event):
        item = tree.identify_row(event.y)
        if not item:
            return
        vals = tree.item(item, "values")
        dados = {
            "id": vals[0],
            "nome": vals[1],
            "cpf": vals[2],
            "telefone": vals[3],
            "endereco": vals[4],
            "bairro": vals[5],
            "cidade": vals[6],
            "estado": vals[7],
            "email": vals[8]
        }
        cadastro_cliente(frame_conteudo, dados, on_show_small_logo, on_show_big_logo)

    entry_busca.bind("<Return>", executar_busca)
    tree.bind("<Double-1>", abrir_cliente_por_click)
    tree.bind("<ButtonRelease-1>", abrir_cliente_por_click)

    executar_busca()

    frame_botoes = ctk.CTkFrame(frame_conteudo, fg_color="transparent")
    frame_botoes.pack(pady=10)

    btn_buscar = ctk.CTkButton(frame_botoes, text="Buscar", command=executar_busca,
                               fg_color="#2e8bff", hover_color="#1c5fb8", width=120)
    btn_buscar.grid(row=0, column=0, padx=10)

    btn_sair = ctk.CTkButton(frame_botoes, text="Sair",
                             command=lambda: cadastro_cliente(frame_conteudo, None, on_show_small_logo, on_show_big_logo),
                             fg_color="red", hover_color="#cc0000", width=120)
    btn_sair.grid(row=0, column=1, padx=10)
