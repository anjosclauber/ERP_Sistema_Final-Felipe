# cad_produto.py
import customtkinter as ctk
from tkinter import ttk, messagebox

def cadastro_produto(frame_conteudo):

    for widget in frame_conteudo.winfo_children():
        widget.destroy()

    frame_conteudo.grid_rowconfigure(0, weight=1)
    frame_conteudo.grid_columnconfigure(0, weight=1)

    # Frame interno principal
    tela = ctk.CTkFrame(frame_conteudo)
    tela.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    # -------------------- TÍTULO --------------------
    titulo = ctk.CTkLabel(tela, text="Cadastro de Produto", font=("Segoe UI", 20, "bold"))
    titulo.grid(row=0, column=0, columnspan=6, pady=(5, 15))

    # -------------------- LINHA 1 --------------------
    ctk.CTkLabel(tela, text="Produto:").grid(row=1, column=0, sticky="e", padx=5)
    entry_produto = ctk.CTkEntry(tela, width=250)
    entry_produto.grid(row=1, column=1, sticky="w", padx=5)

    # -------------------- LINHA 2 --------------------
    ctk.CTkLabel(tela, text="Descrição:").grid(row=2, column=0, sticky="e", padx=5)
    entry_desc = ctk.CTkEntry(tela, width=400)
    entry_desc.grid(row=2, column=1, columnspan=3, sticky="w", padx=5)

    # -------------------- LINHA 3 --------------------
    ctk.CTkLabel(tela, text="Fabricante:").grid(row=3, column=0, sticky="e", padx=5)
    entry_fabricante = ctk.CTkEntry(tela, width=250)
    entry_fabricante.grid(row=3, column=1, sticky="w", padx=5)

    # -------------------- LINHA 4 --------------------
    ctk.CTkLabel(tela, text="CLM:").grid(row=4, column=0, sticky="e", padx=5)
    entry_clm = ctk.CTkEntry(tela, width=200)
    entry_clm.grid(row=4, column=1, sticky="w", padx=5)

    ctk.CTkLabel(tela, text="Cod.Barra:").grid(row=4, column=2, sticky="e", padx=5)
    entry_barra = ctk.CTkEntry(tela, width=200)
    entry_barra.grid(row=4, column=3, sticky="w", padx=5)

    # -------------------- LINHA 5 --------------------
    ctk.CTkLabel(tela, text="Emb:").grid(row=5, column=0, sticky="e", padx=5)
    entry_emb = ctk.CTkEntry(tela, width=200)
    entry_emb.grid(row=5, column=1, sticky="w", padx=5)

    # -------------------- LINHA 6 --------------------
    ctk.CTkLabel(tela, text="P. Custo:").grid(row=6, column=0, sticky="e", padx=5)
    entry_pcusto = ctk.CTkEntry(tela, width=150)
    entry_pcusto.grid(row=6, column=1, sticky="w", padx=5)

    ctk.CTkLabel(tela, text="Marg %:").grid(row=6, column=2, sticky="e", padx=5)
    entry_marg = ctk.CTkEntry(tela, width=150)
    entry_marg.grid(row=6, column=3, sticky="w", padx=5)

    ctk.CTkLabel(tela, text="P. Venda:").grid(row=6, column=4, sticky="e", padx=5)
    entry_pvenda = ctk.CTkEntry(tela, width=150)
    entry_pvenda.grid(row=6, column=5, sticky="w", padx=5)

    # -------------------- STATUS --------------------
    frame_status = ctk.CTkFrame(tela)
    frame_status.grid(row=7, column=0, columnspan=1, pady=10)

    ctk.CTkLabel(frame_status, text="Status:").grid(row=0, column=0, sticky="w")

    status_var = ctk.StringVar(value="Ativo")

    ctk.CTkRadioButton(frame_status, text="Ativo", variable=status_var, value="Ativo").grid(row=1, column=0, sticky="w")
    ctk.CTkRadioButton(frame_status, text="Inativo", variable=status_var, value="Inativo").grid(row=2, column=0, sticky="w")
    ctk.CTkRadioButton(frame_status, text="Excluido", variable=status_var, value="Excluido").grid(row=3, column=0, sticky="w")

    # -------------------- TIPO --------------------
    frame_tipo = ctk.CTkFrame(tela)
    frame_tipo.grid(row=7, column=1, pady=10)

    ctk.CTkLabel(frame_tipo, text="Tipo:").grid(row=0, column=0, sticky="w")

    tipo_var = ctk.StringVar(value="Venda")

    ctk.CTkRadioButton(frame_tipo, text="Venda", variable=tipo_var, value="Venda").grid(row=1, column=0, sticky="w")
    ctk.CTkRadioButton(frame_tipo, text="Interno", variable=tipo_var, value="Interno").grid(row=2, column=0, sticky="w")

    # -------------------- FRACIONADO --------------------
    frame_frac = ctk.CTkFrame(tela)
    frame_frac.grid(row=7, column=2, pady=10)

    ctk.CTkLabel(frame_frac, text="Fracionado:").grid(row=0, column=0, sticky="w")

    fracionado_var = ctk.StringVar(value="Não")

    ctk.CTkRadioButton(frame_frac, text="Sim", variable=fracionado_var, value="Sim").grid(row=1, column=0, sticky="w")
    ctk.CTkRadioButton(frame_frac, text="Não", variable=fracionado_var, value="Não").grid(row=2, column=0, sticky="w")

    # -------------------- BALANÇA --------------------
    frame_balanca = ctk.CTkFrame(tela)
    frame_balanca.grid(row=7, column=3, pady=10)

    ctk.CTkLabel(frame_balanca, text="Balança:").grid(row=0, column=0, sticky="w")

    balanca_var = ctk.StringVar(value="Não")

    ctk.CTkRadioButton(frame_balanca, text="Sim", variable=balanca_var, value="Sim").grid(row=1, column=0, sticky="w")
    ctk.CTkRadioButton(frame_balanca, text="Não", variable=balanca_var, value="Não").grid(row=2, column=0, sticky="w")

    # -------------------- ARMAZENAGEM --------------------
    frame_arm = ctk.CTkFrame(tela)
    frame_arm.grid(row=7, column=4, pady=10)

    ctk.CTkLabel(frame_arm, text="Armazenagem:").grid(row=0, column=0, sticky="w")

    arm_var = ctk.StringVar(value="Loja")

    ctk.CTkRadioButton(frame_arm, text="Loja", variable=arm_var, value="Loja").grid(row=1, column=0, sticky="w")
    ctk.CTkRadioButton(frame_arm, text="Deposito", variable=arm_var, value="Deposito").grid(row=2, column=0, sticky="w")

    # -------------------- BOTÕES --------------------
    frame_botoes = ctk.CTkFrame(tela)
    frame_botoes.grid(row=8, column=0, columnspan=6, pady=20)

    btn_gravar = ctk.CTkButton(frame_botoes, text="Gravar", width=120)
    btn_gravar.grid(row=0, column=0, padx=20)

    btn_cancelar = ctk.CTkButton(frame_botoes, text="Cancelar", width=120)
    btn_cancelar.grid(row=0, column=1, padx=20)

    btn_visualizar = ctk.CTkButton(frame_botoes, text="Visualizar", width=120)
    btn_visualizar.grid(row=0, column=2, padx=20)

    btn_sair = ctk.CTkButton(frame_botoes, text="Sair", width=120, command=lambda: frame_conteudo.destroy())
    btn_sair.grid(row=0, column=3, padx=20)
