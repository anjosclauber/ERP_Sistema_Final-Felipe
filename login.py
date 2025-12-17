import os
import customtkinter as ctk
from customtkinter import CTkImage
from PIL import Image
from tkinter import messagebox
import mysql.connector
import portal

# ---------- Configurações ----------
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

DB_CONFIG = {
    "host": "127.0.0.1",
    "user": "root",
    "password": "",
    "database": "erp_sistema"
}

# ---------- Conexão MySQL ----------
def get_db_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        messagebox.showerror("Erro MySQL", f"Erro ao conectar ao banco: {err}")
        return None

# ---------- Cancelar afters pendentes ----------
def cancel_all_after(win):
    try:
        info = win.tk.eval('after info')
        if info:
            ids = info.split()
            for job in ids:
                try:
                    win.after_cancel(job)
                except Exception:
                    pass
    except Exception:
        pass

# ---------- Janela de Login ----------
def abrir_login():
    # Variável para deslocar o placeholder (texto) para a direita
    deslocamento_placeholder = 30  # Altere este valor para ajustar o deslocamento (em pixels, só efeito visual)

    # Função para gerar espaços no placeholder
    def placeholder_com_espacos(texto, n_espacos=6):
        return (" " * n_espacos) + texto

    # Função para garantir que a primeira letra do usuário seja maiúscula e manter alinhamento
    def on_user_keyrelease(event=None):
        valor = entry_user.get()
        if valor:
            # Remove espaços à esquerda, capitaliza a primeira letra e reinsere os espaços do placeholder
            novo = valor.lstrip()
            novo = novo[:1].upper() + novo[1:]
            entry_user.delete(0, 'end')
            entry_user.insert(0, '      ' + novo)  # 6 espaços para alinhar
            # Mantém o cursor no final
            entry_user.icursor('end')

    # Função para alinhar a digitação da senha
    def on_pass_keyrelease(event=None):
        valor = entry_pass.get()
        if valor and not valor.startswith('      '):
            entry_pass.delete(0, 'end')
            entry_pass.insert(0, '      ' + valor)  # 6 espaços para alinhar
            entry_pass.icursor('end')
    # Carregar ícones coloridos para usuário e senha
    pasta = os.path.dirname(os.path.abspath(__file__))
    icone_usuario = CTkImage(
        light_image=Image.open(os.path.join(pasta, "imagens", "usuario.png")),
        dark_image=Image.open(os.path.join(pasta, "imagens", "usuario.png")),
        size=(22, 22)
    )
    icone_senha = CTkImage(
        light_image=Image.open(os.path.join(pasta, "imagens", "usuario_lock.png")),
        dark_image=Image.open(os.path.join(pasta, "imagens", "usuario_lock.png")),
        size=(22, 22)
    )
    conn = get_db_connection()
    if conn is None:
        return
    cursor = conn.cursor()

    root = ctk.CTk()
    root.overrideredirect(True)

    largura, altura = 570, 290
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    x = (sw // 2) - (largura // 2)
    y = (sh // 2) - (altura // 2)
    root.geometry(f"{largura}x{altura}+{x}+{y}")
    root.resizable(False, False)

    def sair_app():
        root.withdraw()
        cancel_all_after(root)
        try: cursor.close()
        except: pass
        try: conn.close()
        except: pass
        root.destroy()

    # ---------------------------
    #     FRAME PRINCIPAL
    # ---------------------------
    frame_bg = ctk.CTkFrame(root, width=550, height=270, corner_radius=10, fg_color="#d9d9d9")
    frame_bg.place(x=10, y=10)

    # ---------------------------
    #     LISTRA CINZA
    # ---------------------------
    frame_divisor = ctk.CTkFrame(frame_bg, width=3.5, height=242, fg_color="#b7b7b7")
    frame_divisor.place(x=265, y=15)

    # ---------------------------
    #     LOGO ESQUERDA
    # ---------------------------
    frame_left = ctk.CTkFrame(frame_bg, width=250, height=240, corner_radius=20, fg_color="#d9d9d9")
    frame_left.place(x=15, y=15)

    try:
        pasta = os.path.dirname(os.path.abspath(__file__))
        caminho_logo = os.path.join(pasta, "imagens", "Logo_Login.png")
        if os.path.exists(caminho_logo):
            img = Image.open(caminho_logo)
            logo_img = CTkImage(light_image=img, dark_image=img, size=(280, 245))
            ctk.CTkLabel(frame_left, image=logo_img, text="").place(x=-25, y=0)
    except Exception as e:
        print("Erro ao carregar logo:", e)

    # ---------------------------
    #     ÁREA DE LOGIN
    # ---------------------------
    ctk.CTkLabel(
        frame_bg,
        text="Bem-Vindo!\nFaça login para acessar o Sistema",
        font=("Arial", 16, "bold"),
        text_color="#2363c3"
    ).place(x=278, y=30)

    # Ícone de usuário dentro do campo (sobreposto)

    entry_user = ctk.CTkEntry(
        frame_bg,
        placeholder_text=placeholder_com_espacos("Usuário", n_espacos=6),
        width=250, height=32, corner_radius=10, font=("Arial", 15)
    )
    entry_user.place(x=283, y=100)
    # Intermitência do cursor: 600ms ligado, 600ms desligado
    try:
        entry_user.configure(insertontime=600, insertofftime=600)
    except Exception:
        pass
    entry_user.bind('<KeyRelease>', on_user_keyrelease)
    lbl_user_icon = ctk.CTkLabel(frame_bg, text="", image=icone_usuario, fg_color="white")
    lbl_user_icon.place(x=283+8, y=100+2)
    # Foco automático no campo Usuário
    entry_user.focus_set()
    # Destaca visualmente o campo selecionado
    def highlight_entry_user(event=None):
        entry_user.configure(border_color="#1976D2", border_width=2)
    def unhighlight_entry_user(event=None):
        entry_user.configure(border_color="#d9d9d9", border_width=1)
    entry_user.bind('<FocusIn>', highlight_entry_user)
    entry_user.bind('<FocusOut>', unhighlight_entry_user)
    # Garante cursor piscando ao clicar
    entry_user.bind('<Button-1>', lambda e: entry_user.focus_set())

    # Ícone de senha dentro do campo (sobreposto)

    entry_pass = ctk.CTkEntry(
        frame_bg,
        placeholder_text=placeholder_com_espacos("Senha", n_espacos=6),
        show="*",
        width=250, height=32, corner_radius=10, font=("Arial", 15)
    )
    entry_pass.place(x=283, y=146)
    # Intermitência do cursor: 600ms ligado, 600ms desligado
    try:
        entry_pass.configure(insertontime=600, insertofftime=600)
    except Exception:
        pass
    entry_pass.bind('<KeyRelease>', on_pass_keyrelease)
    lbl_pass_icon = ctk.CTkLabel(frame_bg, text="", image=icone_senha, fg_color="white")
    lbl_pass_icon.place(x=283+8, y=146+2)
    # Destaca visualmente o campo selecionado
    def highlight_entry_pass(event=None):
        entry_pass.configure(border_color="#1976D2", border_width=2)
    def unhighlight_entry_pass(event=None):
        entry_pass.configure(border_color="#d9d9d9", border_width=1)
    entry_pass.bind('<FocusIn>', highlight_entry_pass)
    entry_pass.bind('<FocusOut>', unhighlight_entry_pass)
    # Garante cursor piscando ao clicar
    entry_pass.bind('<Button-1>', lambda e: entry_pass.focus_set())

    # ---------------------------
    #   ÍCONES DE OLHO
    # ---------------------------
    pasta = os.path.dirname(os.path.abspath(__file__))
    eye_open = CTkImage(
        light_image=Image.open(os.path.join(pasta, "imagens", "eye_open.png")),
        dark_image=Image.open(os.path.join(pasta, "imagens", "eye_open.png")),
        size=(22, 13)
    )
    eye_closed = CTkImage(
        light_image=Image.open(os.path.join(pasta, "imagens", "eye_closed.png")),
        dark_image=Image.open(os.path.join(pasta, "imagens", "eye_closed.png")),
        size=(22, 13)
    )

    senha_visivel = False

    def toggle_show_password(event=None):
        nonlocal senha_visivel
        senha_visivel = not senha_visivel

        if senha_visivel:
            entry_pass.configure(show="")
            lbl_toggle.configure(image=eye_open)
        else:
            entry_pass.configure(show="*")
            lbl_toggle.configure(image=eye_closed)

    # Escolha a cor de fundo do olho: "white", "transparent" ou outra cor hex
    cor_fundo_olho = "white"  # Altere para "transparent" se quiser sem fundo
    lbl_toggle = ctk.CTkLabel(frame_bg, text="", image=eye_closed, cursor="hand2", fg_color=cor_fundo_olho)
    lbl_toggle.place(x=495, y=148)
    lbl_toggle.bind("<Button-1>", toggle_show_password)

    # ---------- Verificar Login ----------
    def verificar_login(event=None):
        usuario = entry_user.get().strip()
        senha = entry_pass.get().strip()

        if not usuario:
            messagebox.showwarning("Atenção", "Por favor, informe o usuário.")
            entry_user.focus_set()
            entry_user.select_range(0, "end")
            return

        if not senha:
            messagebox.showwarning("Atenção", "Por favor, informe a senha.")
            entry_pass.focus_set()
            entry_pass.select_range(0, "end")
            return

        try:
            cursor.execute(
                "SELECT ID, Login, Nome, Perfil FROM usuario WHERE Login=%s AND Senha=%s",
                (usuario, senha)
            )
            resultado = cursor.fetchone()
        except mysql.connector.Error as err:
            messagebox.showerror("Erro MySQL", f"Erro ao consultar o banco: {err}")
            return

        if resultado:
            usuario_login = resultado[1]
            usuario_nome = resultado[2]      # NOME COMPLETO
            perfil = resultado[3]

            root.withdraw()
            cancel_all_after(root)

            try: cursor.close()
            except: pass
            try: conn.close()
            except: pass
            try: root.destroy()
            except: pass

            # Agora envia o NOME COMPLETO
            portal.abrir_portal(usuario_nome, perfil)

        else:
            messagebox.showerror("Erro", "Usuário não cadastrado ou senha incorreta.")
            entry_pass.select_range(0, "end")
            entry_pass.focus_set()

    entry_pass.bind("<Return>", verificar_login)
    entry_pass.bind("<KP_Enter>", verificar_login)

    ctk.CTkButton(
        frame_bg, text="Entrar", command=verificar_login,
        width=110, height=32, fg_color="#1f80ff",
        hover_color="#0b60c9", corner_radius=8, font=("Arial", 17, "bold")
    ).place(x=287, y=205)

    ctk.CTkButton(
        frame_bg, text="Sair", command=sair_app,
        width=110, height=32, fg_color="#ff0000",
        hover_color="#cc0000", corner_radius=8, font=("Arial", 17, "bold")
    ).place(x=421, y=205)

    root.mainloop()


if __name__ == "__main__":
    abrir_login()
