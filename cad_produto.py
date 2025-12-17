# cad_produto.py
import customtkinter as ctk
from tkinter import ttk, messagebox
import tkinter as tk


def capitalize_first_letter(event):
    widget = event.widget
    value = widget.get()
    if value:
        new_value = value[0].upper() + value[1:]
        if value != new_value:
            widget.delete(0, tk.END)
            widget.insert(0, new_value)


def cadastro_produto(frame_conteudo):

    for widget in frame_conteudo.winfo_children():
        widget.destroy()

    frame_conteudo.configure(fg_color="#e1f1fd")

    main_frame = ctk.CTkFrame(
        frame_conteudo,
        fg_color="#eaf6ff",
        border_color="#1976d2",
        border_width=2,
        width=1200,
        height=720,
    )
    main_frame.place(relx=0.5, rely=0.5, anchor="center")

    font_family = "Arial"

    # Título e código do produto
    titulo_frame = ctk.CTkFrame(main_frame, fg_color="#eaf6ff")
    titulo_frame.place(relx=0.5, y=40, anchor="center", relwidth=0.9)

    ctk.CTkLabel(
        titulo_frame,
        text="Cadastro de Produto",
        font=(font_family, 32, "bold"),
        text_color="#1976d2",
    ).pack(side="left")

    ctk.CTkLabel(
        titulo_frame,
        text="Cód. Produto:",
        font=(font_family, 16, "bold"),
        text_color="#1976d2",
    ).pack(side="right", padx=(0, 5))

    entry_cod = ctk.CTkEntry(titulo_frame, width=120, font=(font_family, 14))
    entry_cod.pack(side="right", padx=(0, 15))

    # =================== BLOCO PRINCIPAL ===================
    bloco_principal = ctk.CTkFrame(
        main_frame,
        fg_color="#eaf6ff",
        border_color="#90caf9",
        border_width=2,
    )
    bloco_principal.place(relx=0.5, rely=0.48, anchor="center",
                          relwidth=0.92, relheight=0.72)

    # Barra de título "Informações do Produto"
    barra_info = ctk.CTkFrame(bloco_principal, fg_color="#eaf6ff")
    barra_info.pack(fill="x", padx=10, pady=(10, 0))

    ctk.CTkLabel(
        barra_info,
        text="Informações do Produto",
        font=(font_family, 14, "bold"),
        text_color="#1976d2",
    ).pack(side="left", padx=5)

    # Linha superior com campos
    linha_superior = ctk.CTkFrame(bloco_principal, fg_color="#eaf6ff")
    linha_superior.pack(fill="x", padx=20, pady=(5, 10))

    # Produto / Fornecedor
    ctk.CTkLabel(linha_superior, text="Produto", font=(font_family, 13, "bold")).grid(
        row=0, column=0, sticky="w", padx=5, pady=4
    )
    entry_produto = ctk.CTkEntry(linha_superior, width=350, font=(font_family, 13))
    entry_produto.grid(row=1, column=0, sticky="w", padx=5, pady=2)

    ctk.CTkLabel(linha_superior, text="Fornecedor", font=(font_family, 13, "bold")).grid(
        row=0, column=1, sticky="w", padx=5, pady=4
    )
    entry_fabricante = ctk.CTkEntry(linha_superior, width=350, font=(font_family, 13))
    entry_fabricante.grid(row=1, column=1, sticky="w", padx=5, pady=2)

    # Classificação Mercadológica
    ctk.CTkLabel(
        linha_superior,
        text="Classificação Mercadológica",
        font=(font_family, 13, "bold"),
    ).grid(row=0, column=2, sticky="w", padx=5, pady=4)
    entry_clm = ctk.CTkEntry(linha_superior, width=280, font=(font_family, 13))
    entry_clm.grid(row=1, column=2, sticky="w", padx=5, pady=2)

    # Embalagem / Cod. Barras
    ctk.CTkLabel(linha_superior, text="Embalagem", font=(font_family, 13, "bold")).grid(
        row=2, column=0, sticky="w", padx=5, pady=(10, 4)
    )
    entry_emb = ctk.CTkEntry(linha_superior, width=250, font=(font_family, 13))
    entry_emb.grid(row=3, column=0, sticky="w", padx=5, pady=2)

    ctk.CTkLabel(
        linha_superior, text="Cod. Barras", font=(font_family, 13, "bold")
    ).grid(row=2, column=1, sticky="w", padx=5, pady=(10, 4))
    entry_barra = ctk.CTkEntry(linha_superior, width=250, font=(font_family, 13))
    entry_barra.grid(row=3, column=1, sticky="w", padx=5, pady=2)

    # Ajuste de colunas para expandir um pouco
    for col in range(3):
        linha_superior.grid_columnconfigure(col, weight=1)

    # =================== LINHA INFERIOR ===================
    linha_inferior = ctk.CTkFrame(bloco_principal, fg_color="#eaf6ff")
    linha_inferior.pack(fill="both", expand=True, padx=20, pady=(0, 10))

    # ---------- Bloco Status / Tipo / Fracionado / Balança / Armazenagem ----------
    bloco_status = ctk.CTkFrame(
        linha_inferior,
        fg_color="#eaf6ff",
        border_color="#90caf9",
        border_width=2,
    )
    bloco_status.grid(row=0, column=0, padx=5, pady=5, sticky="nw")

    # Status
    ctk.CTkLabel(
        bloco_status, text="Status", font=(font_family, 13, "bold"), text_color="#1976d2"
    ).grid(row=0, column=0, padx=10, pady=(5, 0), sticky="w")
    status_var = tk.StringVar(value="Ativo")
    ctk.CTkRadioButton(
        bloco_status, text="Ativo", variable=status_var, value="Ativo"
    ).grid(row=1, column=0, sticky="w", padx=10, pady=2)
    ctk.CTkRadioButton(
        bloco_status, text="Inativo", variable=status_var, value="Inativo"
    ).grid(row=2, column=0, sticky="w", padx=10, pady=2)
    ctk.CTkRadioButton(
        bloco_status, text="Excluído", variable=status_var, value="Excluido"
    ).grid(row=3, column=0, sticky="w", padx=10, pady=2)

    # Tipo
    ctk.CTkLabel(
        bloco_status, text="Tipo", font=(font_family, 13, "bold"), text_color="#1976d2"
    ).grid(row=0, column=1, padx=15, pady=(5, 0), sticky="w")
    tipo_var = tk.StringVar(value="Venda")
    ctk.CTkRadioButton(
        bloco_status, text="Venda", variable=tipo_var, value="Venda"
    ).grid(row=1, column=1, sticky="w", padx=15, pady=2)
    ctk.CTkRadioButton(
        bloco_status, text="Interno", variable=tipo_var, value="Interno"
    ).grid(row=2, column=1, sticky="w", padx=15, pady=2)

    # Fracionado
    ctk.CTkLabel(
        bloco_status,
        text="Fracionado",
        font=(font_family, 13, "bold"),
        text_color="#1976d2",
    ).grid(row=0, column=2, padx=15, pady=(5, 0), sticky="w")
    fracionado_var = tk.StringVar(value="Não")
    ctk.CTkRadioButton(
        bloco_status, text="Sim", variable=fracionado_var, value="Sim"
    ).grid(row=1, column=2, sticky="w", padx=15, pady=2)
    ctk.CTkRadioButton(
        bloco_status, text="Não", variable=fracionado_var, value="Não"
    ).grid(row=2, column=2, sticky="w", padx=15, pady=2)

    # Balança
    ctk.CTkLabel(
        bloco_status,
        text="Balança",
        font=(font_family, 13, "bold"),
        text_color="#1976d2",
    ).grid(row=0, column=3, padx=15, pady=(5, 0), sticky="w")
    balanca_var = tk.StringVar(value="Não")
    ctk.CTkRadioButton(
        bloco_status, text="Sim", variable=balanca_var, value="Sim"
    ).grid(row=1, column=3, sticky="w", padx=15, pady=2)
    ctk.CTkRadioButton(
        bloco_status, text="Não", variable=balanca_var, value="Não"
    ).grid(row=2, column=3, sticky="w", padx=15, pady=2)

    # Armazenagem
    ctk.CTkLabel(
        bloco_status,
        text="Armazenagem",
        font=(font_family, 13, "bold"),
        text_color="#1976d2",
    ).grid(row=0, column=4, padx=15, pady=(5, 0), sticky="w")
    arm_var = tk.StringVar(value="Loja")
    ctk.CTkRadioButton(
        bloco_status, text="Loja", variable=arm_var, value="Loja"
    ).grid(row=1, column=4, sticky="w", padx=15, pady=2)
    ctk.CTkRadioButton(
        bloco_status, text="Depósito", variable=arm_var, value="Deposito"
    ).grid(row=2, column=4, sticky="w", padx=15, pady=2)

    # ---------- Bloco Financeiro ----------
    bloco_fin = ctk.CTkFrame(
        linha_inferior,
        fg_color="#eaf6ff",
        border_color="#90caf9",
        border_width=2,
    )
    bloco_fin.grid(row=0, column=1, padx=10, pady=5, sticky="nw")

    ctk.CTkLabel(
        bloco_fin,
        text="Financeiro",
        font=(font_family, 13, "bold"),
        text_color="#1976d2",
    ).grid(row=0, column=0, columnspan=2, pady=(5, 0))

    ctk.CTkLabel(
        bloco_fin, text="Preço Custo", font=(font_family, 12, "bold")
    ).grid(row=1, column=0, sticky="w", padx=10, pady=3)
    entry_pcusto = ctk.CTkEntry(bloco_fin, width=120, font=(font_family, 12))
    entry_pcusto.grid(row=2, column=0, sticky="w", padx=10, pady=2)

    ctk.CTkLabel(
        bloco_fin, text="Margem", font=(font_family, 12, "bold")
    ).grid(row=1, column=1, sticky="w", padx=10, pady=3)
    entry_marg = ctk.CTkEntry(bloco_fin, width=80, font=(font_family, 12))
    entry_marg.grid(row=2, column=1, sticky="w", padx=10, pady=2)

    ctk.CTkLabel(
        bloco_fin, text="Preço Venda", font=(font_family, 12, "bold")
    ).grid(row=3, column=0, sticky="w", padx=10, pady=3)
    entry_pvenda = ctk.CTkEntry(bloco_fin, width=120, font=(font_family, 12))
    entry_pvenda.grid(row=4, column=0, sticky="w", padx=10, pady=2)

    # ---------- Bloco Tributação ----------
    bloco_trib = ctk.CTkFrame(
        linha_inferior,
        fg_color="#eaf6ff",
        border_color="#90caf9",
        border_width=2,
    )
    bloco_trib.grid(row=0, column=2, padx=10, pady=5, sticky="nw")

    ctk.CTkLabel(
        bloco_trib,
        text="Tributação",
        font=(font_family, 13, "bold"),
        text_color="#1976d2",
    ).grid(row=0, column=0, columnspan=2, pady=(5, 0))

    trib_var = tk.StringVar(value="Tributacao")
    ctk.CTkRadioButton(
        bloco_trib, text="Tributação", variable=trib_var, value="Tributacao"
    ).grid(row=1, column=0, sticky="w", padx=10, pady=4)
    ctk.CTkRadioButton(
        bloco_trib, text="Substituição", variable=trib_var, value="Substituicao"
    ).grid(row=2, column=0, sticky="w", padx=10, pady=4)

    # ---------- Bloco Imagem ----------
    bloco_img = ctk.CTkFrame(
        linha_inferior,
        fg_color="#f5f5f5",
        border_color="#90caf9",
        border_width=2,
        width=260,
        height=220,
    )
    bloco_img.grid(row=0, column=3, padx=(20, 0), pady=5, sticky="ne")
    bloco_img.grid_propagate(False)

    ctk.CTkLabel(
        bloco_img,
        text="Imagem do Produto",
        font=(font_family, 13, "bold"),
        text_color="#1976d2",
    ).place(relx=0.5, rely=0.05, anchor="n")

    # Distribuição das colunas inferiores
    for col in range(4):
        linha_inferior.grid_columnconfigure(col, weight=0)

    # =================== BOTÕES RODAPÉ ===================
    def pack_button(text, cmd, color, xpos, hover_color="#0b60c9"):
        btn = ctk.CTkButton(
            main_frame,
            text=text,
            width=120,
            height=30,
            fg_color=color,
            hover_color=hover_color,
            font=(font_family, 15, "bold"),
            command=cmd,
        )
        btn.place(x=xpos, y=660)

    def gravar():
        messagebox.showinfo("Gravar", "Produto gravado!")

    def buscar():
        messagebox.showinfo("Buscar", "Buscar produto!")

    def sair():
        for w in frame_conteudo.winfo_children():
            w.destroy()

    x_inicial = 300
    espaco = 150
    pack_button("Gravar", gravar, "#1f80ff", x_inicial)
    pack_button("Buscar", buscar, "#1f80ff", x_inicial + espaco)
    pack_button("Sair", sair, "#e53935", x_inicial + espaco * 2, hover_color="#cc0000")

    # Capitalização
    entry_produto.bind("<KeyRelease>", capitalize_first_letter)
    entry_fabricante.bind("<KeyRelease>", capitalize_first_letter)
    entry_clm.bind("<KeyRelease>", capitalize_first_letter)
    entry_barra.bind("<KeyRelease>", capitalize_first_letter)
    entry_emb.bind("<KeyRelease>", capitalize_first_letter)
