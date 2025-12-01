import os
import customtkinter as ctk
from PIL import Image

import login as login  # Importa login

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

def abrir_login():
    global fade_job
    if fade_job:
        splash.after_cancel(fade_job)
        fade_job = None

    try:
        splash.destroy()
    except:
        pass

    login.abrir_login()


# ================= Criar splash ================= #
splash = ctk.CTk()
splash.overrideredirect(True)
largura, altura = 550, 320

# Centralizar splash
screen_width = splash.winfo_screenwidth()
screen_height = splash.winfo_screenheight()
x = (screen_width // 2) - (largura // 2)
y = (screen_height // 2) - (altura // 2)
splash.geometry(f"{largura}x{altura}+{x}+{y}")
splash.attributes('-alpha', 0)

# Imagem do splash usando CTkImage
try:
    pasta_atual = os.path.dirname(os.path.abspath(__file__))
    caminho_img = os.path.join(pasta_atual, "imagens", "splash.png")
    img = Image.open(caminho_img)
    img = img.resize((largura, altura), Image.Resampling.LANCZOS)
    ctk_img = ctk.CTkImage(light_image=img, size=(largura, altura))
    ctk.CTkLabel(splash, image=ctk_img, text="").place(x=0, y=0)
except Exception as e:
    print("Erro splash:", e)

progress = ctk.CTkProgressBar(splash, width=largura-40)
progress.place(x=20, y=altura-40)

fade_job = None

# ================= Função fade-in + barra ================= #
def fade_in(alpha=0, value=0):
    global fade_job
    alpha += 0.02
    value += 1
    if alpha > 1: alpha = 1
    if value > 100: value = 100

    try:
        splash.attributes('-alpha', alpha)
        progress.set(value/100)
    except:
        return  # evita erro se a janela já foi destruída

    if value < 100:
        fade_job = splash.after(30, lambda: fade_in(alpha, value))
    else:
        abrir_login()


fade_in()
splash.mainloop()
