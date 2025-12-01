import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import traceback

# =========== IMPORTAÇÃO DOS MÓDULOS DE CADASTRO ===========
from cad_produto import cadastro_produto
from cad_cliente import cadastro_cliente
from cad_fornecedor import cadastro_fornecedor
from cad_perfil import cadastro_perfil
from cad_usuario import cadastro_usuario
from cad_vendedor import cadastro_vendedor
from cad_emb import cadastro_embalagem
from cad_clm import cadastro_clm
from cad_bairro import cadastro_bairro
from cad_cidade import cadastro_cidade
from pedido_venda import pedido_venda
from cad_orcamento import cadastro_orcamento

# Tenta importar pedido de venda
try:
    from cad_pedido_venda import cadastro_pedido_venda
except Exception:
    def cadastro_pedido_venda(frame=None):
        messagebox.showinfo("Aviso", "Tela de Pedido de Venda não implementada.")


# ===============================================================
#       AUTENTICAÇÃO
# ===============================================================
def autenticar_usuario(usuario, senha):
    usuarios_mock = {
        "orlando": {"nome": "Orlando", "perfil": "Administrador"},
        "maria": {"nome": "Maria Silva", "perfil": "Vendedor"},
        "joao": {"nome": "João Souza", "perfil": "Estoquista"},
        "clauber": {"nome": "Clauber", "perfil": "Administrador"},
    }
    usuario = usuario.lower()
    if usuario in usuarios_mock and senha == "123":
        return usuarios_mock[usuario]
    return None


# ===============================================================
#       TEXTO BOAS VINDAS
# ===============================================================
def criar_texto_boas_vindas(frame_conteudo, usuario_logado):
    texto_completo = f"Bem-vindo, {usuario_logado}, ao sistema NexusERP"

    lbl_bemvindo = ctk.CTkLabel(
        frame_conteudo,
        text="",
        text_color="#1976D2",
        font=("Arial", 18, "bold")
    )
    lbl_bemvindo.place(relx=0.5, rely=0.05, anchor="center")

    def animar(i=0):
        if i <= len(texto_completo):
            lbl_bemvindo.configure(text=texto_completo[:i])
            lbl_bemvindo.after(40, animar, i + 1)

    animar()
    return lbl_bemvindo


# ===============================================================
#                   PORTAL PRINCIPAL
#                CONFIGURAÇÃO DO TEMA
# ===============================================================
def abrir_portal(usuario_logado, perfil):

    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.title("Portal NexusERP")

    root.after(10, lambda: root.state("zoomed"))
    root.minsize(1024, 600)

    root.grid_rowconfigure(0, weight=1)
    root.grid_rowconfigure(1, weight=0)
    root.grid_columnconfigure(0, weight=0)
    root.grid_columnconfigure(1, weight=0)
    root.grid_columnconfigure(2, weight=1)

    MENU_WIDTH = 240
    SUBMENU_WIDTH = 240

    # ===========================================================
    #   MENU LATERAL (COM LOGO NO RODAPÉ)
    # ===========================================================
    frame_menu = ctk.CTkFrame(root, corner_radius=0, width=MENU_WIDTH, fg_color="#2F80C0")
    frame_menu.grid(row=0, column=0, sticky="ns")
    frame_menu.grid_propagate(False)

    # --- container interno que empurra os botões para cima
    frame_menu_buttons = ctk.CTkFrame(frame_menu, fg_color="#2F80C0")
    frame_menu_buttons.pack(side="top", fill="both", expand=True)

    # --- LOGO FIXA NA PARTE INFERIOR
    pasta = os.path.dirname(os.path.abspath(__file__))
    logo_path = os.path.join(pasta, "imagens", "logo_small.png")  # <<< AJUSTE AQUI SUA LOGO

    try:
        img_logo = Image.open(logo_path).resize((160, 80), Image.Resampling.LANCZOS)
        img_logo_tk = ImageTk.PhotoImage(img_logo)
    except:
        img_logo_tk = None

    frame_logo = ctk.CTkFrame(frame_menu, fg_color="#2F80C0")
    frame_logo.pack(side="bottom", pady=10)

    lbl_logo = ctk.CTkLabel(frame_logo, text="", image=img_logo_tk)
    lbl_logo.pack()

    # ===========================================================
    #   SUBMENU
    # ===========================================================
    frame_submenu = ctk.CTkFrame(root, corner_radius=0, width=SUBMENU_WIDTH, fg_color="#2F80C0")
    frame_submenu.grid(row=0, column=1, sticky="ns")
    frame_submenu.grid_propagate(False)

    inner_submenu_container = ctk.CTkFrame(frame_submenu, fg_color="#2F80C0")
    inner_submenu_container.place(x=0, y=0, relwidth=1)

    # ===========================================================
    #   CONTEÚDO
    # ===========================================================
    frame_conteudo = ctk.CTkFrame(root, fg_color="#E6F0FA")
    frame_conteudo.grid(row=0, column=2, sticky="nsew")
    frame_conteudo.grid_rowconfigure(0, weight=1)
    frame_conteudo.grid_columnconfigure(0, weight=1)

    # ===========================================================
    #   MARCA D'ÁGUA
    # ===========================================================
    pasta_atual = os.path.dirname(os.path.abspath(__file__))
    caminho_img = os.path.join(pasta_atual, "imagens", "Marca_dagua.png")

    fundo = ctk.CTkLabel(frame_conteudo, text="")
    fundo.grid(row=0, column=0, sticky="nsew")

    bg_original = None
    if os.path.exists(caminho_img):
        try:
            bg_original = Image.open(caminho_img)
        except:
            fundo.configure(text="Erro ao abrir Marca_dagua.png", font=("Arial", 16))
    else:
        fundo.configure(text="Marca_dagua.png não encontrada", font=("Arial", 20))

    _bg_full_photo = None
    _bg_small_photo = None

    def atualizar_fundo(event=None):
        nonlocal _bg_full_photo
        if not bg_original:
            return
        w = frame_conteudo.winfo_width()
        h = frame_conteudo.winfo_height()
        if w <= 0 or h <= 0:
            return
        img = bg_original.resize((w, h), Image.Resampling.LANCZOS)
        _bg_full_photo = ImageTk.PhotoImage(img)
        fundo.configure(image=_bg_full_photo, text="")
        fundo.image = _bg_full_photo

    frame_conteudo.bind("<Configure>", atualizar_fundo)

    def mostrar_marca_dagua_pequena():
        nonlocal _bg_small_photo
        if not bg_original:
            return
        img_small = bg_original.resize((200, 120), Image.Resampling.LANCZOS)
        _bg_small_photo = ImageTk.PhotoImage(img_small)

        fundo.grid_forget()
        fundo.configure(image=_bg_small_photo, text="")
        fundo.image = _bg_small_photo

        fundo.place(
            x=15,
            rely=1.0,
            y=-(120 + 20),
            anchor="sw"
        )

    def mostrar_marca_dagua_grande():
        fundo.place_forget()
        fundo.grid(row=0, column=0, sticky="nsew")
        atualizar_fundo()

    def minimizar_marca_dagua():
        mostrar_marca_dagua_grande()
        root.after(80, mostrar_marca_dagua_pequena)

    def restaurar_marca_dagua():
        mostrar_marca_dagua_grande()

    # ===========================================================
    #   TEXTO DE BOAS-VINDAS
    # ===========================================================
    lbl_bemvindo = criar_texto_boas_vindas(frame_conteudo, usuario_logado)

    # ===========================================================
    #   VARIÁVEIS DE CONTROLE
    # ===========================================================
    menu_ativo = None
    submenu_aberto = None
    submenu_ativo_btn = None
    pinned_menu = None
    current_content_frame = None
    current_toplevel = None

    def fechar_conteudo_aberto():
        nonlocal current_content_frame, current_toplevel
        try:
            if current_toplevel:
                current_toplevel.destroy()
        except:
            pass
        current_toplevel = None
        try:
            if current_content_frame:
                current_content_frame.destroy()
        except:
            pass
        current_content_frame = None
        restaurar_marca_dagua()

    def resetar_para_inicial():
        nonlocal submenu_aberto, menu_ativo, submenu_ativo_btn, pinned_menu
        for widget in inner_submenu_container.winfo_children():
            widget.destroy()
        submenu_aberto = None
        submenu_ativo_btn = None
        pinned_menu = None
        fechar_conteudo_aberto()
        restaurar_marca_dagua()

    # ===========================================================
    #   SUBMENU
    # ===========================================================
    arrow_btns = {}

    def criar_botao_filho(inner_container, label, comando):
        s_btn = ctk.CTkButton(
            inner_container,
            text=label,
            fg_color="#2F80C0",
            hover_color="#1565C0",
            text_color="white",
            corner_radius=6
        )

        def cmd_wrap(c=comando, btn=s_btn):
            nonlocal submenu_ativo_btn, current_content_frame
            fechar_conteudo_aberto()
            minimizar_marca_dagua()

            current_content_frame = ctk.CTkFrame(frame_conteudo, fg_color="white")
            current_content_frame.grid(row=0, column=0, sticky="nsew")

            try:
                c(current_content_frame)
            except TypeError:
                current_content_frame.destroy()
                current_content_frame = None

                top = ctk.CTkToplevel(root)
                top.title(label)
                try:
                    c(top)
                except Exception as e:
                    messagebox.showerror("Erro", str(e))

            if submenu_ativo_btn:
                submenu_ativo_btn.configure(fg_color="#2F80C0")
            btn.configure(fg_color="#90CAF9")
            submenu_ativo_btn = btn

        s_btn.configure(command=cmd_wrap)
        s_btn.pack(fill="x", pady=3, padx=8)
        return s_btn

    def open_submenu(nome_menu, opcoes, btn, pin=False, from_hover=False):
        nonlocal submenu_aberto, pinned_menu, submenu_ativo_btn

        for w in inner_submenu_container.winfo_children():
            w.destroy()

        for nome, b in arrow_btns.items():
            b.configure(text=f" {nome} ►")

        btn.configure(text=f" {nome_menu} ▼")

        for label, comando in opcoes or []:
            criar_botao_filho(inner_submenu_container, label, comando)

        submenu_aberto = nome_menu
        if pin:
            pinned_menu = nome_menu

    # ===========================================================
    #   BOTÕES DO MENU LATERAL (AGORA NO frame_menu_buttons)
    # ===========================================================
    def criar_botao_menu(nome, opcoes):
        if nome == "Sair":
            btn = ctk.CTkButton(
                frame_menu_buttons,
                text="Sair",
                fg_color="#E53935",
                hover_color="#C62828",
                text_color="white",
                corner_radius=8,
                command=root.destroy
            )
            btn.pack(fill="x", padx=8, pady=8)
            return

        btn = ctk.CTkButton(
            frame_menu_buttons,
            text=f" {nome} ►",
            fg_color="#2F80C0",
            hover_color="#1565C0",
            text_color="white",
            corner_radius=8
        )
        btn.pack(fill="x", pady=8, padx=8)
        arrow_btns[nome] = btn

        btn.bind("<Enter>", lambda e, n=nome, o=opcoes, b=btn: open_submenu(n, o, b))
        btn.bind("<Button-1>", lambda e, n=nome, o=opcoes, b=btn: open_submenu(n, o, b, pin=True))

    menus = [
        ("Cadastro", [
            ("Bairro", cadastro_bairro),
            ("Cidade", cadastro_cidade),
            ("CLM", cadastro_clm),
            ("Cliente", cadastro_cliente),
            ("Embalagem", cadastro_embalagem),
            ("Fornecedor", cadastro_fornecedor),
            ("Perfil", cadastro_perfil),
            ("Produto", cadastro_produto),
            ("Usuário", cadastro_usuario),
            ("Vendedor", cadastro_vendedor),
        ]),
        ("Vendas", [
            ("Orçamento", cadastro_orcamento),
            ("Pedido de Venda", pedido_venda),
        ]),
        ("Relatórios", [
            ("Histórico Entrada", lambda f=None: messagebox.showinfo("Info", "Histórico Entrada")),
            ("Histórico Produto", lambda f=None: messagebox.showinfo("Info", "Histórico Produto")),
            ("Histórico Venda", lambda f=None: messagebox.showinfo("Info", "Histórico Venda")),
        ]),
        ("Manutenção", [
            ("Alterar Dados do Usuário", lambda f=None: messagebox.showinfo("Info", "Alterar Dados")),
            ("Alterar Perfil", lambda f=None: messagebox.showinfo("Info", "Alterar Perfil")),
        ]),
        ("Configuração", [
            ("Tema Claro", lambda f=None: ctk.set_appearance_mode("light")),
            ("Tema Escuro", lambda f=None: ctk.set_appearance_mode("dark")),
        ]),
        ("Utilitários", [
            ("Alterar Embalagem", lambda f=None: messagebox.showinfo("Info", "Alterar Embalagem")),
            ("Alterar Estoque", lambda f=None: messagebox.showinfo("Info", "Alterar Estoque")),
            ("Alterar Preço", lambda f=None: messagebox.showinfo("Info", "Alterar Preço")),
            ("Alterar Status", lambda f=None: messagebox.showinfo("Info", "Alterar Status")),
        ]),
        ("Sair", None),
    ]

    for nome, opcoes in menus:
        criar_botao_menu(nome, opcoes)

    # ===========================================================
    #   RODAPÉ
    # ===========================================================
    rodape = ctk.CTkFrame(root, height=36, corner_radius=0, fg_color="#2F80C0")
    rodape.grid(row=1, column=0, columnspan=3, sticky="ew")
    rodape.grid_propagate(False)

    ctk.CTkLabel(rodape, text="NexusERP", text_color="white").pack(side="left", padx=10)
    ctk.CTkLabel(rodape, text=f"🙍 Usuário: {usuario_logado}", text_color="white").pack(side="left", expand=True)
    ctk.CTkLabel(rodape, text=f"Perfil: {perfil}", text_color="white").pack(side="right", padx=10)

    # Clique na área central fecha submenus
    frame_conteudo.bind("<Button-1>", lambda e: resetar_para_inicial())

    atualizar_fundo()
    root.mainloop()
