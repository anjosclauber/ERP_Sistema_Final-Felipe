import customtkinter as ctk
from tkinter import messagebox, ttk
import mysql.connector
import os
from PIL import Image

def conectar():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="MAJu2022@",
        database="erp_sistema"
    )

def cadastro_cidade(frame_conteudo, dados=None, on_show_small_logo=None, on_show_big_logo=None):
    for widget in frame_conteudo.winfo_children():
        widget.destroy()
    if callable(on_show_small_logo):
        try: on_show_small_logo()
        except: pass
    frame_conteudo.grid_propagate(False)
    frame_conteudo.configure(fg_color="#d9d9d9")
    
    # Usando grid em todos os frames principais e internos
    titulo = ctk.CTkLabel(frame_conteudo, text="Cadastro de Cidade", font=("Arial", 28, "bold"))
    titulo.grid(row=0, column=0, columnspan=2, pady=(60, 15))
    
    frame_central = ctk.CTkFrame(frame_conteudo, fg_color="transparent")
    frame_central.grid(row=1, column=0, columnspan=2, pady=(30, 0))
    
    frame_form = ctk.CTkFrame(frame_central, fg_color="transparent")
    frame_form.grid(row=0, column=1, padx=(30, 0))
    
    entry_nome = ctk.CTkEntry(frame_form, placeholder_text="Nome da Cidade", width=320)
    entry_nome.grid(row=0, column=0, pady=8)
    
    estados = ["AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES",
               "GO", "MA", "MT", "MS", "MG", "PA", "PB", "PR",
               "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC",
               "SP", "SE", "TO"]
    combo_uf = ctk.CTkOptionMenu(frame_form, values=estados, width=320)
    combo_uf.set("UF")
    combo_uf.grid(row=1, column=0, pady=8)

    # Imagem sempre com grid
    frame_img = ctk.CTkFrame(frame_central, fg_color="transparent")
    frame_img.grid(row=0, column=0, padx=(20, 40), sticky="n")
    
    try:
        diretorio_base = os.path.dirname(os.path.abspath(__file__))
        caminho_img = os.path.join(diretorio_base, "imagens", "cidade.png")
        if os.path.isfile(caminho_img):
            img_user = ctk.CTkImage(light_image=Image.open(caminho_img), size=(200, 200))
            lbl_img = ctk.CTkLabel(frame_img, image=img_user, text="")
            lbl_img.grid(row=0, column=0, padx=10, pady=10)
        else:
            lbl_img = ctk.CTkLabel(frame_img, text="(Imagem não encontrada)", width=200, height=200)
            lbl_img.grid(row=0, column=0, padx=10, pady=10)
    except Exception as e:
        lbl_img = ctk.CTkLabel(frame_img, text=f"(Erro na imagem: {e})", width=200, height=200)
        lbl_img.grid(row=0, column=0, padx=10, pady=10)
    
    cidade_id = None
    if dados:
        cidade_id = dados.get("id")
        entry_nome.insert(0, dados["nome"])
        combo_uf.set(dados.get("uf", "UF"))
    
    def gravar():
        nonlocal cidade_id
        nome = entry_nome.get().strip()
        uf = combo_uf.get()
        if not nome or uf == "UF":
            messagebox.showwarning("Aviso", "Preencha o nome da cidade e selecione o estado!")
            return
        con = None
        try:
            con = conectar()
            cur = con.cursor()
            if cidade_id:
                cur.execute("UPDATE cidade SET nome=%s, uf=%s WHERE id=%s", (nome, uf, cidade_id))
                messagebox.showinfo("Atualizado", "Cidade atualizada com sucesso!")
            else:
                cur.execute("SELECT id FROM cidade WHERE nome=%s AND uf=%s", (nome, uf))
                if cur.fetchone():
                    messagebox.showwarning("Aviso", "Esta cidade já está cadastrada nesse estado!")
                    return
                cur.execute("INSERT INTO cidade (nome, uf) VALUES (%s, %s)", (nome, uf))
                messagebox.showinfo("Sucesso", "Cidade cadastrada com sucesso!")
            con.commit()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gravar cidade:\n{e}")
        finally:
            if con: con.close()

    def procurar():
        abrir_tela_procurar_cidade(frame_conteudo, on_show_small_logo, on_show_big_logo)

    def limpar():
        nonlocal cidade_id
        cidade_id = None
        entry_nome.delete(0, "end")
        combo_uf.set("UF")

    def sair():
        for widget in frame_conteudo.winfo_children():
            widget.destroy()
        if callable(on_show_big_logo):
            try: on_show_big_logo()
            except: pass

    frame_botoes = ctk.CTkFrame(frame_form, fg_color="transparent")
    frame_botoes.grid(row=2, column=0, pady=(30, 10))
    
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

def abrir_tela_procurar_cidade(frame_conteudo, on_show_small_logo=None, on_show_big_logo=None):
    for widget in frame_conteudo.winfo_children():
        widget.destroy()
    if callable(on_show_small_logo):
        try: on_show_small_logo()
        except: pass
    lbl = ctk.CTkLabel(frame_conteudo, text="Buscar Cidade", font=("Arial", 24, "bold"))
    lbl.grid(row=0, column=0, columnspan=2, pady=10)
    
    container = ctk.CTkFrame(frame_conteudo)
    container.grid(row=1, column=0, columnspan=2, pady=10)
    
    entry_busca = ctk.CTkEntry(container, placeholder_text="Digite o nome", width=320)
    entry_busca.grid(row=0, column=0)
    emoji_lbl = ctk.CTkLabel(container, text="🔍", font=("Arial", 20))
    emoji_lbl.grid(row=0, column=1, padx=(5, 0))
    
    frame_tree = ctk.CTkFrame(frame_conteudo)
    frame_tree.grid(row=2, column=0, columnspan=2, pady=10, sticky="nsew")
    
    style = ttk.Style()
    style.theme_use("default")
    style.configure("Treeview", font=("Arial", 12), rowheight=30)
    style.configure("Treeview.Heading", font=("Arial", 12, "bold"))
    tree = ttk.Treeview(frame_tree, columns=("id", "nome", "uf"), show="headings", height=10)
    tree.heading("id", text="ID")
    tree.heading("nome", text="Nome")
    tree.heading("uf", text="UF")
    tree.column("id", width=60, anchor="center")
    tree.column("nome", width=160)
    tree.column("uf", width=40, anchor="center")
    tree.grid(row=0, column=0, sticky="nsew")
    
    scrollbar = ttk.Scrollbar(frame_tree, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=0, column=1, sticky="ns")
    
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
                cur.execute("SELECT id, nome, uf FROM cidade ORDER BY nome")
            else:
                cur.execute("SELECT id, nome, uf FROM cidade WHERE nome LIKE %s ORDER BY nome", (f"%{termo}%",))
            registros = cur.fetchall()
            for idx, (id_, nome, uf) in enumerate(registros):
                tag = "evenrow" if idx % 2 == 0 else "oddrow"
                tree.insert("", "end", values=(id_, nome, uf), tags=(tag,))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao buscar cidades:\n{e}")
        finally:
            if con: con.close()
    def abrir_cidade_por_click(event):
        item = tree.identify_row(event.y)
        if not item:
            return
        vals = tree.item(item, "values")
        dados = {"id": vals[0], "nome": vals[1], "uf": vals[2]}
        cadastro_cidade(frame_conteudo, dados, on_show_small_logo, on_show_big_logo)
    entry_busca.bind("<Return>", executar_busca)
    tree.bind("<Double-1>", abrir_cidade_por_click)
    tree.bind("<ButtonRelease-1>", abrir_cidade_por_click)
    executar_busca()
    frame_botoes = ctk.CTkFrame(frame_conteudo, fg_color="transparent")
    frame_botoes.grid(row=3, column=0, columnspan=2, pady=10)
    btn_abrir = ctk.CTkButton(frame_botoes, text="Abrir", command=lambda: abrir_cidade_por_click(None),
                              fg_color="#2e8bff", hover_color="#1c5fb8", width=120)
    btn_abrir.grid(row=0, column=0, padx=10)
    btn_buscar = ctk.CTkButton(frame_botoes, text="Buscar", command=executar_busca,
                               fg_color="#2e8bff", hover_color="#1c5fb8", width=120)
    btn_buscar.grid(row=0, column=1, padx=10)
    btn_sair = ctk.CTkButton(frame_botoes, text="Sair",
                             command=lambda: cadastro_cidade(frame_conteudo, None, on_show_small_logo, on_show_big_logo),
                             fg_color="red", hover_color="#cc0000", width=120)
    btn_sair.grid(row=0, column=2, padx=10)
