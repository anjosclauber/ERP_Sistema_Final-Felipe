import os
import customtkinter as ctk
from customtkinter import CTkImage
from PIL import Image
from tkinter import messagebox
import mysql.connector
import portal as portal  # Seu portal

# Configurações globais
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# Conexão MySQL
try:
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="MAJu2022@",
        database="erp_sistema"
    )
    cursor = conn.cursor()
except mysql.connector.Error as err:
    messagebox.showerror("Erro MySQL", f"Erro ao conectar ao banco: {err}")
    exit()

def abrir_login():

    root = ctk.CTk()

    # REMOVE A BARRA SUPERIOR (minimizar, maximizar e fechar)
    root.overrideredirect(True)

    root.title("🔐Login - Sistema")

    # ======================
    #     NOVO TAMANHO
    # ======================
    largura, altura = 570, 290
    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()
    x = (screen_w // 2) - (largura // 2)
    y = (screen_h // 2) - (altura // 2)
    root.geometry(f"{largura}x{altura}+{x}+{y}")
    root.resizable(False, False)

    # =====================================================
    #   FUNÇÃO PARA MOVER A JANELA (já que a borda foi removida)
    # =====================================================
    def iniciar_movimento(event):
        root.x = event.x
        root.y = event.y

    def mover_janela(event):
        dx = event.x - root.x
        dy = event.y - root.y
        root.geometry(f"+{root.winfo_x() + dx}+{root.winfo_y() + dy}")

    root.bind("<Button-1>", iniciar_movimento)
    root.bind("<B1-Motion>", mover_janela)

    # Botão de sair alternativo
    def sair_app():
        root.destroy()

    # ============================
    #     FRAME PRINCIPAL
    # ============================
    frame_bg = ctk.CTkFrame(
        root,
        width=550,
        height=270,
        corner_radius=10,
        fg_color="#d9d9d9"
    )
    frame_bg.place(x=10, y=10)

    # # BOTÃO DE FECHAR CUSTOMIZADO (já que removemos a barra)
    # btn_fechar = ctk.CTkButton(
    #     frame_bg,
    #     text="X",
    #     width=25,
    #     height=20,
    #     fg_color="#ff0000",
    #     hover_color="#cc0000",
    #     command=sair_app,
    #     corner_radius=8,
    #     font=("Arial", 14, "bold")
    # )
    # btn_fechar.place(x=510, y=5)

    # ============================
    #     LADO ESQUERDO (LOGO)
    # ============================
    frame_left = ctk.CTkFrame(
        frame_bg,
        width=250,
        height=240,
        corner_radius=20,
        fg_color="#d9d9d9"
    )
    frame_left.place(x=15, y=28)

    try:
        pasta = os.path.dirname(os.path.abspath(__file__))
        caminho_logo = os.path.join(pasta, "imagens", "Logo_Login.png")
        img_logo = Image.open(caminho_logo)
        logo_img = CTkImage(light_image=img_logo, dark_image=img_logo, size=(280, 245))
        lbl_logo = ctk.CTkLabel(frame_left, image=logo_img, text="")
        lbl_logo.place(x=-35, y=5)
    except Exception as e:
        print("Erro ao carregar logo:", e)

    # ============================
    #     LADO DIREITO (LOGIN)
    # ============================
    lbl_titulo = ctk.CTkLabel(
        frame_bg,
        text="Bem-Vindo!\nFaça login para acessar o Sistema",
        font=("Arial", 16, "bold"),
        text_color="#2363c3"
    )
    lbl_titulo.place(x=270, y=30)

    entry_user = ctk.CTkEntry(
        frame_bg,
        placeholder_text="🧑‍💻Usuário",
        width=250,
        height=30,
        corner_radius=10,
        font=("Arial", 15)
    )
    entry_user.place(x=275, y=100)

    entry_pass = ctk.CTkEntry(
        frame_bg,
        placeholder_text="🔐Senha",
        show="*",
        width=250,
        height=30,
        corner_radius=10,
        font=("Arial", 15)
    )
    entry_pass.place(x=275, y=145)
    entry_pass.bind("<Return>", lambda e: verificar_login())
    entry_pass.bind("<KP_Enter>", lambda e: verificar_login())

    # --- Função Login ---
    def verificar_login(event=None):
        usuario = entry_user.get()
        senha = entry_pass.get()
        cursor.execute("SELECT * FROM usuario WHERE Login=%s AND Senha=%s", (usuario, senha))
        resultado = cursor.fetchone()

        if resultado:
            usuario_logado = resultado[1]
            perfil = resultado[5]
            root.destroy()
            portal.abrir_portal(usuario_logado, perfil)
        else:
            messagebox.showerror("Erro", "Usuário não cadastrado ou senha incorreta.")

    btn_entrar = ctk.CTkButton(
        frame_bg,
        text="Entrar",
        command=verificar_login,
        width=110,
        height=28,
        fg_color="#1f80ff",
        hover_color="#0b60c9",
        corner_radius=8,
        font=("Arial", 17, "bold")
    )
    btn_entrar.place(x=280, y=210)

    btn_sair = ctk.CTkButton(
        frame_bg,
        text="Sair",
        command=sair_app,
        width=110,
        height=28,
        fg_color="#ff0000",
        hover_color="#cc0000",
        corner_radius=8,
        font=("Arial", 17, "bold")
    )
    btn_sair.place(x=410, y=210)

    root.mainloop()


if __name__ == "__main__":
    abrir_login()
