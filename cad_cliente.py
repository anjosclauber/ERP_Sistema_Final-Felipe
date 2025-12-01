import customtkinter as ctk
from tkinter import messagebox, ttk
from PIL import Image
import os
from db import conectar


# ================== Cadastro de Cliente ====================
def cadastro_cliente(frame_conteudo, dados=None, on_show_small_logo=None, on_show_big_logo=None):
    for widget in frame_conteudo.winfo_children():
        widget.destroy()

    frame_conteudo.grid_propagate(False)
    frame_conteudo.configure(fg_color="#d9d9d9")

    # ---------- título ----------
    titulo = ctk.CTkLabel(
        frame_conteudo,
        text="Cadastro de Cliente",
        font=("Arial", 28, "bold")
    )
    titulo.place(relx=0.559, rely=0.1, anchor="center")

    frame_central = ctk.CTkFrame(frame_conteudo, fg_color="transparent")
    frame_central.place(relx=0.5, rely=0.5, anchor="center")

    # -------- imagem --------
    frame_img = ctk.CTkFrame(frame_central, fg_color="transparent")
    frame_img.grid(row=0, column=0, padx=(20, 40), pady=10, sticky="n")
    try:
        diretorio_base = os.path.dirname(os.path.abspath(__file__))
        caminho_img = os.path.join(diretorio_base, "imagens", "cliente.png")
        img = ctk.CTkImage(light_image=Image.open(caminho_img), size=(200, 200))
        lbl_img = ctk.CTkLabel(frame_img, image=img, text="")
        lbl_img.pack()
    except:
        lbl_img = ctk.CTkLabel(frame_img, text="(Imagem)", width=200, height=200)
        lbl_img.pack()

    # -------- formulário --------
    frame_form = ctk.CTkFrame(frame_central, fg_color="transparent")
    frame_form.grid(row=0, column=1, pady=10, sticky="n")

    entry_nome = ctk.CTkEntry(frame_form, placeholder_text="Nome", width=320)
    entry_nome.grid(row=0, column=0, pady=6, sticky="ew")

    entry_cpf = ctk.CTkEntry(frame_form, placeholder_text="CPF", width=320)
    entry_cpf.grid(row=1, column=0, pady=6, sticky="ew")

    entry_telefone = ctk.CTkEntry(frame_form, placeholder_text="Telefone", width=320)
    entry_telefone.grid(row=2, column=0, pady=6, sticky="ew")

    entry_endereco = ctk.CTkEntry(frame_form, placeholder_text="Endereço", width=320)
    entry_endereco.grid(row=3, column=0, pady=6, sticky="ew")

    entry_bairro = ctk.CTkEntry(frame_form, placeholder_text="Bairro", width=320)
    entry_bairro.grid(row=4, column=0, pady=6, sticky="ew")

    entry_cidade = ctk.CTkEntry(frame_form, placeholder_text="Cidade", width=320)
    entry_cidade.grid(row=5, column=0, pady=6, sticky="ew")

    # -------- Combobox Estado --------
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
    combobox_estado = ttk.Combobox(frame_form, values=estados_formatados, width=38, font=("Arial", 14))
    combobox_estado.grid(row=6, column=0, pady=6, sticky="ew")
    combobox_estado.set("Selecione o Estado")

    entry_email = ctk.CTkEntry(frame_form, placeholder_text="Email", width=320)
    entry_email.grid(row=7, column=0, pady=6, sticky="ew")

    # Variável de controle para edição
    cliente_id = None

    # Preenche dados se for edição
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

    # ================= FUNÇÕES =================
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
        abrir_tela_procurar_cliente(
            frame_conteudo,
            on_show_small_logo=on_show_small_logo,
            on_show_big_logo=on_show_big_logo
        )

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

    def sair():
        for widget in frame_conteudo.winfo_children():
            widget.destroy()

    # -------- botões --------
    frame_botoes = ctk.CTkFrame(frame_form, fg_color="transparent")
    frame_botoes.grid(row=8, column=0, pady=(50, 20))

    btn_gravar = ctk.CTkButton(frame_botoes, text="Gravar", width=120, command=gravar,
                               fg_color="#2e8bff", hover_color="#1c5fb8")
    btn_gravar.grid(row=0, column=0, padx=8)

    btn_procurar = ctk.CTkButton(frame_botoes, text="Procurar", width=120, command=procurar,
                                 fg_color="#2e8bff", hover_color="#1c5fb8")
    btn_procurar.grid(row=0, column=1, padx=8)

    btn_limpar = ctk.CTkButton(frame_botoes, text="Limpar", width=120, command=limpar,
                               fg_color="#2e8bff", hover_color="#1c5fb8")
    btn_limpar.grid(row=0, column=2, padx=8)

    btn_sair = ctk.CTkButton(frame_botoes, text="Sair", width=120, command=sair,
                             fg_color="red", hover_color="#cc0000")
    btn_sair.grid(row=0, column=3, padx=8)


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
