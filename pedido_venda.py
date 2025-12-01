# pedido_venda.py
import os
import datetime
from decimal import Decimal, InvalidOperation
import customtkinter as ctk
from tkinter import ttk, messagebox, filedialog, END
import mysql.connector
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib.utils import ImageReader

# Configurações de banco e logo
DB_HOST = "127.0.0.1"
DB_USER = "root"
DB_PASSWORD = "MAJu2022@"
DB_NAME = "erp_sistema"
DEFAULT_LOGO_PATH = r"C:\Users\Desktop\OneDrive - SENAC PA - EDU\Área de Trabalho\Atual\Python\ERP_SISTEMA_FINAL\imagens\Marca_dagua.png"


def get_connection():
    try:
        return mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            autocommit=False,
        )
    except mysql.connector.Error as e:
        messagebox.showerror("Erro MySQL", f"Conexão: {e}")
        return None


def pedido_venda(frame_conteudo):
    # Fundo geral
    frame_conteudo.configure(fg_color="#eaf6ff")  # azul bem claro

    # Painel central branco com borda azul
    main_frame = ctk.CTkFrame(
        frame_conteudo,
        fg_color="white",
        border_color="#1976d2",
        border_width=2,
        corner_radius=0,
    )
    main_frame.place(relx=0.5, rely=0.5, anchor="center", width=1200, height=650)

    # Título
    ctk.CTkLabel(
        main_frame,
        text="Orçamento",
        font=("Arial", 32, "bold"),
        text_color="#1976d2",
    ).place(relx=0.5, y=40, anchor="center")

    # FRAME CLIENTE
    cliente_frame = ctk.CTkFrame(main_frame, fg_color="white", corner_radius=0)
    cliente_frame.place(x=50, y=90, width=1100, height=54)

    ctk.CTkLabel(
        cliente_frame,
        text="Cliente",
        font=("Arial", 16),
        text_color="#1976d2",
    ).place(x=0, y=12)

    entry_cliente = ctk.CTkEntry(
        cliente_frame,
        width=600,
        height=36,
        placeholder_text="Digite o cliente",
    )
    entry_cliente.place(x=100, y=8)

    btn_busca_cliente = ctk.CTkButton(
        cliente_frame,
        text="🔍",
        width=36,
        height=36,
        fg_color="#1976d2",
        hover_color="#1565c0",
        font=("Arial", 16, "bold"),
        command=lambda: buscar_cliente(),
    )
    btn_busca_cliente.place(x=720, y=8)

    # FRAME PRODUTO
    produto_frame = ctk.CTkFrame(main_frame, fg_color="white", corner_radius=0)
    produto_frame.place(x=50, y=150, width=1100, height=54)

    ctk.CTkLabel(
        produto_frame,
        text="Produto",
        font=("Arial", 16),
        text_color="#1976d2",
    ).place(x=0, y=12)

    entry_produto = ctk.CTkEntry(
        produto_frame,
        width=360,
        height=36,
        placeholder_text="Digite o produto",
    )
    entry_produto.place(x=100, y=8)

    btn_busca_produto = ctk.CTkButton(
        produto_frame,
        text="🔍",
        width=36,
        height=36,
        fg_color="#1976d2",
        hover_color="#1565c0",
        font=("Arial", 16, "bold"),
        command=lambda: buscar_produto(),
    )
    btn_busca_produto.place(x=470, y=8)

    entry_qtd = ctk.CTkEntry(
        produto_frame,
        width=120,
        height=36,
        placeholder_text="Quantidade",
    )
    entry_qtd.place(x=530, y=8)

    entry_valor = ctk.CTkEntry(
        produto_frame,
        width=120,
        height=36,
        placeholder_text="Valor Unitário",
    )
    entry_valor.place(x=660, y=8)

    btn_add_item = ctk.CTkButton(
        produto_frame,
        text="Inserir Produto",
        fg_color="#1976d2",
        hover_color="#1565c0",
        width=140,
        height=36,
        font=("Arial", 14, "bold"),
        command=lambda: adicionar_item(),
    )
    btn_add_item.place(x=800, y=8)

    # TABELA DE ITENS
    table_frame = ctk.CTkFrame(main_frame, fg_color="white", corner_radius=0)
    table_frame.place(x=50, y=210, width=1100, height=320)

    style = ttk.Style()
    style.theme_use("default")
    style.configure(
        "Treeview",
        background="white",
        foreground="black",
        rowheight=24,
        fieldbackground="white",
        font=("Arial", 10),
    )
    style.configure(
        "Treeview.Heading",
        font=("Arial", 10, "bold"),
        background="#1976d2",
        foreground="white",
    )
    style.map("Treeview.Heading", background=[("active", "#1565c0")])

    tree = ttk.Treeview(
        table_frame,
        columns=("produto", "quantidade", "valor_unitario", "valor_total"),
        show="headings",
        height=11,
    )
    tree.heading("produto", text="Produto")
    tree.heading("quantidade", text="Quantidade")
    tree.heading("valor_unitario", text="Valor Unitário")
    tree.heading("valor_total", text="Valor Total")

    tree.column("produto", width=500, anchor="w")
    tree.column("quantidade", width=180, anchor="center")
    tree.column("valor_unitario", width=180, anchor="center")
    tree.column("valor_total", width=180, anchor="center")

    tree.place(x=0, y=0, width=1050, height=320)

    vsb = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
    vsb.place(x=1050, y=0, height=320)
    tree.configure(yscrollcommand=vsb.set)

    # MEMÓRIA E IDS
    itens_mem = []
    cliente_selecionado_id = None
    produto_selecionado_id = None

    # LABEL TOTAL
    lbl_total = ctk.CTkLabel(
        main_frame,
        text="Valor Tota:",
        font=("Arial", 20, "bold"),
        text_color="#1976d2",
    )
    lbl_total.place(x=880, y=540)

    # BOTÕES RODAPÉ
    def pack_button(text, cmd, color, xpos):
        ctk.CTkButton(
            main_frame,
            text=text,
            width=120,
            height=32,
            fg_color=color,
            hover_color="#0d47a1" if color in ("#1976d2", "#2196f3") else color,
            font=("Arial", 14, "bold"),
            corner_radius=4,
            command=cmd,
        ).place(x=xpos, y=600)

    pack_button("Gravar", lambda: gravar_pedido_venda(), "#1976d2", 380)
    pack_button("Procurar", lambda: procurar_pedido_venda(), "#2196f3", 510)
    pack_button("Excluir", lambda: excluir_item(), "#e53935", 640)
    pack_button("Imprimir", lambda: imprimir_pedido_venda(salvar=True), "#1976d2", 900)
    pack_button("Sair", lambda: sair(), "#e53935", 1030)

    # FUNÇÕES INTERNAS

    def buscar_cliente():
        # Implemente sua tela/popup de busca de cliente aqui
        pass

    def buscar_produto():
        # Implemente sua tela/popup de busca de produto aqui
        pass

    def atualizar_total_label():
        total = Decimal("0.00")
        for it in itens_mem:
            total += Decimal(str(it["valor_total"]))
        lbl_total.configure(text=f"Valor Tota: R$ {float(total):.2f}")
        return total

    def adicionar_item():
        nonlocal produto_selecionado_id

        nome = entry_produto.get().strip()
        qtd_text = entry_qtd.get().strip() or "1"
        v_text = entry_valor.get().strip() or "0"

        if not nome:
            messagebox.showwarning("Aviso", "Informe o produto.")
            return

        try:
            qtd = Decimal(qtd_text.replace(",", "."))
            v = Decimal(str(v_text).replace(",", "."))
        except InvalidOperation:
            messagebox.showerror("Erro", "Quantidade ou valor inválido.")
            return

        vtotal = (qtd * v).quantize(Decimal("0.01"))
        item = {
            "produto_id": int(produto_selecionado_id) if produto_selecionado_id else None,
            "produto_nome": nome,
            "quantidade": float(qtd),
            "valor_unitario": float(v),
            "valor_total": float(vtotal),
        }
        itens_mem.append(item)

        tree.insert(
            "",
            "end",
            values=(
                item["produto_nome"],
                str(item["quantidade"]),
                f"R$ {float(item['valor_unitario']):.2f}",
                f"R$ {float(item['valor_total']):.2f}",
            ),
        )

        atualizar_total_label()
        entry_produto.delete(0, END)
        entry_valor.delete(0, END)
        entry_qtd.delete(0, END)
        produto_selecionado_id = None

    def excluir_item():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("Aviso", "Selecione um item para excluir.")
            return
        idx = tree.index(sel[0])
        tree.delete(sel[0])
        del itens_mem[idx]
        atualizar_total_label()

    def gravar_pedido_venda():
        if not itens_mem:
            message
