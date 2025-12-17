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
from buscar_orcamento import buscar_orcamento

# Tenta importar pedido de venda
try:
    from cad_pedido_venda import cadastro_pedido_venda
except Exception:
    def cadastro_pedido_venda(frame=None):
        messagebox.showinfo("Aviso", "Tela de Pedido de Venda não implementada.")


# ================== CONFIGURAÇÕES DE LARGURA DE BOTÕES ==================
# Altere o valor abaixo para modificar a largura do botão de seleção do menu filho (submenu):
SUBMENU_BTN_WIDTH = 240  # <<<<<<<<<<<  MUDE AQUI A LARGURA DO BOTÃO DO SUBMENU  <<<<<<<<<<<


# ================== CONFIGURAÇÃO TAMANHO MARCA D'ÁGUA PEQUENA ==================
# Altere os valores abaixo para modificar o tamanho da marca d'água pequena (submenu):
MARCA_DAGUA_PEQUENA_WIDTH = 200  # largura
MARCA_DAGUA_PEQUENA_HEIGHT = 120  # altura

# Caminho padrão para a marca d'água (usado por várias telas)
PASTA_PROJETO = os.path.dirname(os.path.abspath(__file__))
DEFAULT_LOGO_PATH = os.path.join(PASTA_PROJETO, "imagens", "Marca_dagua.png")

# =====================================================================
#   FUNÇÕES DE MARCA D'ÁGUA
# =====================================================================

def mostrar_marca_dagua_grande(frame_conteudo):
    """Mostra a marca d’água grande centralizada (tela inicial)."""
    for w in frame_conteudo.winfo_children():
        w.destroy()

    if os.path.exists(DEFAULT_LOGO_PATH):
        try:
            img = Image.open(DEFAULT_LOGO_PATH)
            w, h = img.size

            ratio = min(
                (frame_conteudo.winfo_width() or 900) / w,
                (frame_conteudo.winfo_height() or 700) / h,
                1.2
            )

            new_size = (int(w * ratio), int(h * ratio))
            img = img.resize(new_size, Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)

            lbl = ctk.CTkLabel(frame_conteudo, image=photo, text="")
            lbl.image = photo
            lbl.place(relx=0.5, rely=0.5, anchor="center")
            return
        except:
            pass

    ctk.CTkLabel(
        frame_conteudo,
        text="NexusERP",
        font=("Arial", 72, "bold"),
        text_color="#1976d2",
    ).place(relx=0.5, rely=0.5, anchor="center")


def mostrar_marca_dagua_pequena(frame_conteudo):
    """Mostra a marca d’água pequena no canto inferior esquerdo."""
    if os.path.exists(DEFAULT_LOGO_PATH):
        try:
            img = Image.open(DEFAULT_LOGO_PATH)
            img = img.resize((180, 180), Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)

            lbl = ctk.CTkLabel(frame_conteudo, image=photo, text="")
            lbl.image = photo
            lbl.place(x=10, rely=1.0, anchor="sw")  # ⬅ canto inferior esquerdo
        except:
            pass        

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
        font=("Arial", 20, "bold")
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
# ===============================================================
def abrir_portal(usuario_logado, perfil):
    def recolher_submenu(event=None):
        nonlocal submenu_aberto, submenu_ativo_btn, pinned_menu
        # Só recolhe se não houver tela de conteúdo aberta
        if submenu_aberto and current_content_frame is None and current_toplevel is None:
            for widget in inner_submenu_container.winfo_children():
                widget.destroy()
            submenu_aberto = None
            submenu_ativo_btn = None
            pinned_menu = None
            restaurar_marca_dagua()


    # Aplicar capitalize
    usuario_formatado = str(usuario_logado).title()
    perfil_formatado = str(perfil).title()

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
    # SUBMENU_BTN_WIDTH agora está no topo do arquivo para fácil configuração

    # ===========================================================
    #   MENU LATERAL
    # ===========================================================
    frame_menu = ctk.CTkFrame(root, corner_radius=0, width=MENU_WIDTH, fg_color="#2F80C0")
    frame_menu.grid(row=0, column=0, sticky="ns")
    frame_menu.grid_propagate(False)

    frame_menu_buttons = ctk.CTkFrame(frame_menu, fg_color="#2F80C0")
    frame_menu_buttons.pack(side="top", fill="both", expand=True)

    pasta = os.path.dirname(os.path.abspath(__file__))
    logo_path = os.path.join(pasta, "imagens", "logo_small.png")

    try:
        img_logo = Image.open(logo_path).resize((160, 80), Image.Resampling.LANCZOS)
        img_logo_tk = ImageTk.PhotoImage(img_logo)
    except:
        img_logo_tk = None


    frame_logo = ctk.CTkFrame(frame_menu, fg_color="#2F80C0")
    frame_logo.pack(side="bottom", pady=10)

    lbl_logo = ctk.CTkLabel(frame_logo, text="", image=img_logo_tk)
    lbl_logo.pack()

    # Marca d'água pequena no menu lateral (escondida por padrão)
    try:
        img_marca_menu = Image.open(DEFAULT_LOGO_PATH).resize((MARCA_DAGUA_PEQUENA_WIDTH, MARCA_DAGUA_PEQUENA_HEIGHT), Image.LANCZOS)
        img_marca_menu_tk = ImageTk.PhotoImage(img_marca_menu)
    except:
        img_marca_menu_tk = None

    marca_menu_label = ctk.CTkLabel(frame_menu, text="", image=img_marca_menu_tk)
    marca_menu_label.image = img_marca_menu_tk
    marca_menu_label.place(relx=0.5, rely=1.0, anchor="s", y=-10)
    marca_menu_label.lower()  # Esconde inicialmente
    marca_menu_label.place_forget()

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
        img_small = bg_original.resize((MARCA_DAGUA_PEQUENA_WIDTH, MARCA_DAGUA_PEQUENA_HEIGHT), Image.Resampling.LANCZOS)
        _bg_small_photo = ImageTk.PhotoImage(img_small)

        fundo.grid_forget()
        fundo.configure(image=_bg_small_photo, text="")
        fundo.image = _bg_small_photo

        fundo.place(
            x=40,
            rely=2.0,
            y=-(MARCA_DAGUA_PEQUENA_HEIGHT + 40),
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

    lbl_bemvindo = criar_texto_boas_vindas(frame_conteudo, usuario_formatado)

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
            current_content_frame = None
            # Recolhe o submenu ao fechar a tela e reseta tudo
            for widget in inner_submenu_container.winfo_children():
                widget.destroy()
            # Some completamente com o menu filho
            frame_submenu.grid_remove()
            inner_submenu_container.place_forget()
            nonlocal submenu_aberto, submenu_ativo_btn, pinned_menu, menu_ativo, lbl_bemvindo
            submenu_aberto = None
            submenu_ativo_btn = None
            pinned_menu = None
            # Remove destaque de todos os menus pais
            for nome, b in arrow_btns.items():
                b.configure(fg_color="#2F80C0", text=f" {nome} ►")
            menu_ativo = None
            # Limpa o conteúdo e volta tela inicial
            for w in frame_conteudo.winfo_children():
                w.destroy()
            lbl_bemvindo = criar_texto_boas_vindas(frame_conteudo, usuario_formatado)
            restaurar_marca_dagua()
            marca_menu_label.place_forget()  # Esconde marca d'água pequena ao sair de qualquer tela

    def resetar_para_inicial():
        nonlocal submenu_aberto, menu_ativo, submenu_ativo_btn, pinned_menu
        for widget in inner_submenu_container.winfo_children():
            widget.destroy()
        submenu_aberto = None
        submenu_ativo_btn = None
        pinned_menu = None
        fechar_conteudo_aberto()
        restaurar_marca_dagua()
        marca_menu_label.place_forget()  # Esconde marca d'água pequena do menu lateral só ao voltar ao portal inicial

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
            marca_menu_label.place(relx=0.5, rely=1.0, anchor="s", y=-10)
            marca_menu_label.lift()

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
        s_btn.pack(fill="x", pady=3, padx=5)
        return s_btn

    def open_submenu(nome_menu, opcoes, btn, pin=False, from_hover=False):
        nonlocal submenu_aberto, pinned_menu, submenu_ativo_btn

        # Sempre mostra o menu filho ao abrir submenu
        frame_submenu.grid()
        if btn is not None:
            btn.update_idletasks()
            y_pai = btn.winfo_rooty() - btn.master.winfo_rooty() - 8  # Sobe 8 pixels
            inner_submenu_container.place_configure(y=y_pai)
        # Sempre que abrir o menu pai, marca d'água volta ao centro
        restaurar_marca_dagua()
        # Não esconde mais a marca d'água pequena do menu lateral aqui

        for w in inner_submenu_container.winfo_children():
            w.destroy()
        # Adiciona binding para recolher submenu ao clicar fora
        root.bind("<Button-1>", recolher_submenu, add='+')

        # Destaca todos os menus como normal
        for nome, b in arrow_btns.items():
            b.configure(text=f" {nome} ►", fg_color="#2F80C0")

        # Destaca o menu pai selecionado
        btn.configure(text=f" {nome_menu} ▼", fg_color="#1565C0")

        # Cria botões filhos alinhados e com destaque ao selecionar
        def criar_botao_filho_alinhado(inner_container, label, comando):
            s_btn = ctk.CTkButton(
                inner_container,
                text=label,
                fg_color="#2F80C0",
                hover_color="#1565C0",
                text_color="white",
                corner_radius=8,
                width=SUBMENU_BTN_WIDTH,
                anchor="center",
                font=("Arial", 15, "bold")
            )
            def cmd_wrap(c=comando, btn=s_btn):
                nonlocal submenu_ativo_btn, current_content_frame
                # Remove binding ao abrir tela
                root.unbind("<Button-1>")
                fechar_conteudo_aberto()
                mostrar_marca_dagua_pequena()  # Sempre que escolher menu filho, marca d'água vai para canto
                marca_menu_label.place(relx=0.5, rely=1.0, anchor="s", y=-10)
                marca_menu_label.lift()
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
                # Garante que a marca d'água pequena aparece após abrir a tela
                marca_menu_label.place(relx=0.5, rely=1.0, anchor="s", y=-10)
                marca_menu_label.lift()
                # Remove destaque do anterior
                if submenu_ativo_btn:
                    submenu_ativo_btn.configure(fg_color="#2F80C0")
                btn.configure(fg_color="#90CAF9")
                submenu_ativo_btn = btn
                # Mantém o menu pai destacado
                btn_menu_pai = arrow_btns.get(nome_menu)
                if btn_menu_pai:
                    btn_menu_pai.configure(fg_color="#1565C0")
            s_btn.configure(command=cmd_wrap)
            # Alinhar exatamente com o menu pai
            s_btn.pack(fill="x", pady=8, padx=8)
            return s_btn

        for label, comando in opcoes or []:
            criar_botao_filho_alinhado(inner_submenu_container, label, comando)

        submenu_aberto = nome_menu
        if pin:
            pinned_menu = nome_menu

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
            corner_radius=8,
            font=("Arial", 15, "bold")
        )
        btn.pack(fill="x", pady=8, padx=8)
        arrow_btns[nome] = btn

        btn.bind("<Enter>", lambda e, n=nome, o=opcoes, b=btn: open_submenu(n, o, b))
        btn.bind("<Button-1>", lambda e, n=nome, o=opcoes, b=btn: open_submenu(n, o, b, pin=True))
        # Alinhar o submenu exatamente ao botão pai
        if btn is not None:
            btn.update_idletasks()
            y_pai = btn.winfo_rooty() - btn.master.winfo_rooty()
            inner_submenu_container.place_configure(y=y_pai)

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
    #   RODAPÉ — (AQUI FOI FEITO O AJUSTE)
    # ===========================================================
    rodape = ctk.CTkFrame(root, height=36, corner_radius=0, fg_color="#2F80C0")
    rodape.grid(row=1, column=0, columnspan=3, sticky="ew")
    rodape.grid_propagate(False)

    # Marca
    ctk.CTkLabel(rodape, text="NexusERP", text_color="white").pack(side="left", padx=10)

    # Usuário com capitalize
    ctk.CTkLabel(
        rodape,
        text=f"🙍 Usuário: {usuario_formatado}",
        text_color="white"
    ).pack(side="left", expand=True)

    # Perfil com capitalize
    ctk.CTkLabel(
        rodape,
        text=f"Perfil: {perfil_formatado}",
        text_color="white"
    ).pack(side="right", padx=10)

    frame_conteudo.bind("<Button-1>", lambda e: resetar_para_inicial())
    # Evento virtual para permitir que telas filhas peçam para resetar o menu
    frame_conteudo.bind("<<ResetarMenu>>", lambda e: resetar_para_inicial())

    atualizar_fundo()
    root.mainloop()
