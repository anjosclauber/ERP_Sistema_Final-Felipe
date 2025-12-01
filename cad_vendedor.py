import customtkinter as ctk
from tkinter import messagebox, ttk
from PIL import Image
import mysql.connector
import os

def conectar():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="MAJu2022@",
        database="erp_sistema"
    )

def cadastro_vendedor(frame_conteudo, dados=None, on_show_small_logo=None, on_show_big_logo=None):
    for widget in frame_conteudo.winfo_children():
        widget.destroy()

    if callable(on_show_small_logo):
        try:
            on_show_small_logo()
        except Exception:
            pass

    frame_conteudo.grid_propagate(False)
    frame_conteudo.configure(fg_color="#d9d9d9")

    titulo = ctk.CTkLabel(
        frame_conteudo,
        text="Cadastro de Vendedor",
        font=("Arial", 28, "bold")
    )
    titulo.place(relx=0.56, rely=0.32, anchor="center")

    frame_central = ctk.CTkFrame(frame_conteudo, fg_color="transparent")
    frame_central.place(relx=0.5, rely=0.5, anchor="center")

    frame_img = ctk.CTkFrame(frame_central, fg_color="transparent")
    frame_img.grid(row=0, column=0, padx=(20,40), pady=10)
    try:
        diretorio_base = os.path.dirname(os.path.abspath(__file__))
        caminho_img = os.path.join(diretorio_base, "imagens", "vendedor.png")
        img_vend = ctk.CTkImage(light_image=Image.open(caminho_img), size=(200,200))
        lbl_img = ctk.CTkLabel(frame_img, image=img_vend, text="")
        lbl_img.pack()
    except Exception:
        lbl_img = ctk.CTkLabel(frame_img, text="(Imagem)", width=200, height=200)
        lbl_img.pack()

    frame_form = ctk.CTkFrame(frame_central, fg_color="transparent")
    frame_form.grid(row=0, column=1, pady=10)

    entry_nome = ctk.CTkEntry(frame_form, placeholder_text="Nome", width=320)
    entry_nome.grid(row=0, column=0, pady=8)
    entry_cpf = ctk.CTkEntry(frame_form, placeholder_text="CPF", width=320)
    entry_cpf.grid(row=1, column=0, pady=8)
    entry_telefone = ctk.CTkEntry(frame_form, placeholder_text="Telefone", width=320)
    entry_telefone.grid(row=2, column=0, pady=8)
    entry_email = ctk.CTkEntry(frame_form, placeholder_text="Email", width=320)
    entry_email.grid(row=3, column=0, pady=8)

    vendedor_id = None
    if dados:
        vendedor_id = dados.get("id")
        entry_nome.insert(0, dados.get("nome", ""))
        entry_cpf.insert(0, dados.get("cpf", ""))
        entry_telefone.insert(0, dados.get("telefone", ""))
        entry_email.insert(0, dados.get("email", ""))

    def gravar():
        nonlocal vendedor_id
        nome = entry_nome.get().strip()
        cpf = entry_cpf.get().strip()
        telefone = entry_telefone.get().strip()
        email = entry_email.get().strip()
        if not nome or not cpf:
            messagebox.showwarning("Aviso", "Preencha os campos obrigatórios!")
            return
        con = None
        try:
            con = conectar()
            cur = con.cursor()
            if vendedor_id:
                cur.execute("""
                    UPDATE vendedor SET nome=%s, cpf=%s, telefone=%s, email=%s WHERE id=%s
                """, (nome, cpf, telefone, email, vendedor_id))
                messagebox.showinfo("Atualizado", "Vendedor atualizado com sucesso!")
            else:
                cur.execute("""
                    INSERT INTO vendedor (nome, cpf, telefone, email) VALUES (%s, %s, %s, %s)
                """, (nome, cpf, telefone, email))
                messagebox.showinfo("Sucesso", "Vendedor cadastrado com sucesso!")
            con.commit()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gravar vendedor:\n{e}")
        finally:
            if con:
                con.close()

    def procurar():
        abrir_tela_procurar_vendedor(frame_conteudo, on_show_small_logo, on_show_big_logo)

    def limpar():
        nonlocal vendedor_id
        vendedor_id = None
        entry_nome.delete(0, "end")
        entry_cpf.delete(0, "end")
        entry_telefone.delete(0, "end")
        entry_email.delete(0, "end")

    def sair():
        for widget in frame_conteudo.winfo_children():
            widget.destroy()
        if callable(on_show_big_logo):
            try:
                on_show_big_logo()
            except Exception:
                pass

    frame_botoes = ctk.CTkFrame(frame_form, fg_color="transparent")
    frame_botoes.grid(row=4, column=0, pady=(30, 10))
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

def abrir_tela_procurar_vendedor(frame_conteudo, on_show_small_logo=None, on_show_big_logo=None):
    for widget in frame_conteudo.winfo_children():
        widget.destroy()
    if callable(on_show_small_logo):
        try:
            on_show_small_logo()
        except Exception:
            pass
    lbl = ctk.CTkLabel(frame_conteudo, text="Buscar Vendedor", font=("Arial", 24, "bold"))
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
    tree = ttk.Treeview(frame_tree, columns=(
        "id", "nome", "cpf", "telefone", "email"
    ), show="headings", height=10)
    tree.heading("id", text="ID")
    tree.heading("nome", text="Nome")
    tree.heading("cpf", text="CPF")
    tree.heading("telefone", text="Telefone")
    tree.heading("email", text="Email")
    tree.column("id", width=40, anchor="center")
    tree.column("nome", width=140)
    tree.column("cpf", width=100)
    tree.column("telefone", width=100)
    tree.column("email", width=180)
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
                cur.execute("SELECT id, nome, cpf, telefone, email FROM vendedor ORDER BY nome")
            else:
                cur.execute("""
                    SELECT id, nome, cpf, telefone, email
                    FROM vendedor WHERE nome LIKE %s ORDER BY nome
                """, (f"%{termo}%",))
            registros = cur.fetchall()
            for idx, row in enumerate(registros):
                tag = "evenrow" if idx % 2 == 0 else "oddrow"
                tree.insert("", "end", values=row, tags=(tag,))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao buscar vendedores:\n{e}")
        finally:
            if con:
                con.close()

    def abrir_vendedor_por_selecao():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("Aviso", "Selecione um vendedor!")
            return
        item = sel[0]
        vals = tree.item(item, "values")
        dados = {
            "id": vals[0], "nome": vals[1], "cpf": vals[2], "telefone": vals[3], "email": vals[4]
        }
        cadastro_vendedor(frame_conteudo, dados, on_show_small_logo, on_show_big_logo)

    def abrir_vendedor_por_click(event):
        item = tree.identify_row(event.y)
        if not item:
            return
        vals = tree.item(item, "values")
        dados = {
            "id": vals[0], "nome": vals[1], "cpf": vals[2], "telefone": vals[3], "email": vals[4]
        }
        cadastro_vendedor(frame_conteudo, dados, on_show_small_logo, on_show_big_logo)

    entry_busca.bind("<Return>", executar_busca)
    tree.bind("<Double-1>", abrir_vendedor_por_click)
    tree.bind("<ButtonRelease-1>", abrir_vendedor_por_click)
    executar_busca()
    frame_botoes = ctk.CTkFrame(frame_conteudo, fg_color="transparent")
    frame_botoes.pack(pady=10)
    btn_abrir = ctk.CTkButton(frame_botoes, text="Abrir", command=abrir_vendedor_por_selecao,
                              fg_color="#2e8bff", hover_color="#1c5fb8", width=120)
    btn_abrir.grid(row=0, column=0, padx=10)
    btn_buscar = ctk.CTkButton(frame_botoes, text="Buscar", command=executar_busca,
                               fg_color="#2e8bff", hover_color="#1c5fb8", width=120)
    btn_buscar.grid(row=0, column=1, padx=10)
    btn_sair = ctk.CTkButton(frame_botoes, text="Sair",
        command=lambda: cadastro_vendedor(frame_conteudo, None, on_show_small_logo, on_show_big_logo),
        fg_color="red", hover_color="#cc0000", width=120)
    btn_sair.grid(row=0, column=2, padx=10)
