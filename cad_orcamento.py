# cad_orcamento.py
import os
import datetime
from decimal import Decimal, InvalidOperation

import customtkinter as ctk
from tkinter import ttk, messagebox, filedialog, Toplevel, END, Listbox
import mysql.connector

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib.utils import ImageReader


# Configuration
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


def cadastro_orcamento(frame_conteudo):
    # Fundo
    frame_conteudo.configure(fg_color="#eaf6ff")

    main_frame = ctk.CTkFrame(
        frame_conteudo,
        fg_color="#e3f2fd",
        border_color="#1976d2",
        border_width=2,
        width=1200,
        height=650,
    )
    main_frame.place(relx=0.5, rely=0.5, anchor="center")

    # Título
    ctk.CTkLabel(
        main_frame,
        text="Orçamento",
        font=("Arial", 32, "bold"),
        text_color="#1976d2",
    ).place(relx=0.5, y=40, anchor="center")

    # --------- CLIENTE ----------
    cliente_frame = ctk.CTkFrame(
        main_frame,
        fg_color="#e3f2fd",
        width=1100,
        height=54,
    )
    cliente_frame.place(x=50, y=90)

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
        command=lambda: buscar_cliente_popup(),
    )
    btn_busca_cliente.place(x=720, y=8)

    # Listbox para autocomplete cliente
    listbox_cliente = Listbox(cliente_frame, height=5)
    listbox_cliente.place(x=100, y=44, width=600)
    listbox_cliente.place_forget()

    # --------- PRODUTO ----------
    produto_frame = ctk.CTkFrame(
        main_frame,
        fg_color="#e3f2fd",
        width=1100,
        height=54,
    )
    produto_frame.place(x=50, y=150)

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
        command=lambda: buscar_produto_popup(),
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
        command=lambda: adicionar_item(),
    )
    btn_add_item.place(x=800, y=8)

    # Listbox para autocomplete produto
    listbox_produto = Listbox(produto_frame, height=5)
    listbox_produto.place(x=100, y=44, width=360)
    listbox_produto.place_forget()

    # --------- TABELA ----------
    table_frame = ctk.CTkFrame(
        main_frame,
        fg_color="#e3f2fd",
        width=1100,
        height=320,
    )
    table_frame.place(x=50, y=210)

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
    tree.column("produto", width=500)
    tree.column("quantidade", width=180, anchor="center")
    tree.column("valor_unitario", width=180, anchor="center")
    tree.column("valor_total", width=180, anchor="center")
    tree.place(x=0, y=0, width=1050, height=320)

    vsb = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
    vsb.place(x=1050, y=0, height=320)
    tree.configure(yscrollcommand=vsb.set)

    itens_mem = []
    cliente_selecionado_id = None
    produto_selecionado_id = None

    # --------- RODAPÉ ----------
    lbl_total = ctk.CTkLabel(
        main_frame,
        text="Valor Tota:",
        font=("Arial", 20, "bold"),
        text_color="#1976d2",
    )
    lbl_total.place(x=740, y=540)

    def pack_button(text, cmd, color, xpos):
        btn = ctk.CTkButton(
            main_frame,
            text=text,
            width=120,
            height=36,
            fg_color=color,
            font=("Arial", 14),
            command=cmd,
        )
        btn.place(x=xpos, y=600)

    pack_button("Gravar", lambda: gravar_orcamento(), "#1976d2", 380)
    pack_button("Procurar", lambda: procurar_orcamento(), "#2196f3", 510)
    pack_button("Excluir", lambda: excluir_item(), "#e53935", 640)
    pack_button("Gerar P. Venda", lambda: gerar_pedido_venda(), "#1976d2", 770)
    pack_button("Imprimir", lambda: imprimir_orcamento(salvar=True), "#1976d2", 900)
    pack_button("Sair", lambda: sair(), "#e53935", 1030)

    # ---------- FUNÇÕES DE AUTOCOMPLETE / BUSCA BANCO ----------

    def buscar_cliente_sugestoes(prefixo):
        conn = get_connection()
        if not conn:
            return []
        try:
            cur = conn.cursor()
            cur.execute(
                "SELECT id, nome FROM cliente WHERE nome LIKE %s ORDER BY nome LIMIT 20",
                (prefixo + "%",),
            )
            dados = cur.fetchall()
            return dados  # [(id, nome), ...]
        except mysql.connector.Error as e:
            messagebox.showerror("MySQL", f"Erro ao buscar clientes:\n{e}")
            return []
        finally:
            try:
                cur.close()
                conn.close()
            except:
                pass

    def buscar_produto_sugestoes(prefixo):
        conn = get_connection()
        if not conn:
            return []
        try:
            cur = conn.cursor()
            cur.execute(
                "SELECT id, produto, pvenda FROM produto WHERE produto LIKE %s ORDER BY produto LIMIT 20",
                (prefixo + "%",),
            )
            dados = cur.fetchall()
            return dados  # [(id, produto, pvenda), ...]
        except mysql.connector.Error as e:
            messagebox.showerror("MySQL", f"Erro ao buscar produtos:\n{e}")
            return []
        finally:
            try:
                cur.close()
                conn.close()
            except:
                pass

    def mostrar_sugestoes_cliente(event=None):
        nonlocal cliente_selecionado_id
        texto = entry_cliente.get().strip()
        cliente_selecionado_id = None
        listbox_cliente.delete(0, END)
        if not texto:
            listbox_cliente.place_forget()
            return
        dados = buscar_cliente_sugestoes(texto)
        if not dados:
            listbox_cliente.place_forget()
            return
        for _id, nome in dados:
            listbox_cliente.insert(END, f"{_id} - {nome}")
        listbox_cliente.place(x=100, y=44, width=600)

    def selecionar_cliente(event=None):
        nonlocal cliente_selecionado_id
        if not listbox_cliente.curselection():
            return
        valor = listbox_cliente.get(listbox_cliente.curselection()[0])
        try:
            _id_str, nome = valor.split(" - ", 1)
            cliente_selecionado_id = int(_id_str)
            entry_cliente.delete(0, END)
            entry_cliente.insert(0, nome)
        except ValueError:
            pass
        listbox_cliente.place_forget()

    def mostrar_sugestoes_produto(event=None):
        nonlocal produto_selecionado_id
        texto = entry_produto.get().strip()
        produto_selecionado_id = None
        listbox_produto.delete(0, END)
        if not texto:
            listbox_produto.place_forget()
            return
        dados = buscar_produto_sugestoes(texto)
        if not dados:
            listbox_produto.place_forget()
            return
        for _id, nome, pvenda in dados:
            listbox_produto.insert(END, f"{_id} - {nome} | {pvenda}")
        listbox_produto.place(x=100, y=44, width=360)

    def selecionar_produto(event=None):
        nonlocal produto_selecionado_id
        if not listbox_produto.curselection():
            return
        valor = listbox_produto.get(listbox_produto.curselection()[0])
        try:
            parte_id_nome, pvenda_str = valor.rsplit("|", 1)
            _id_str, nome = parte_id_nome.split(" - ", 1)
            produto_selecionado_id = int(_id_str)
            entry_produto.delete(0, END)
            entry_produto.insert(0, nome.strip())
            entry_valor.delete(0, END)
            entry_valor.insert(0, pvenda_str.strip())
        except ValueError:
            pass
        listbox_produto.place_forget()

    # ---------- OUTRAS FUNÇÕES ----------

    def buscar_cliente_popup():
        # Se quiser manter um popup separado depois
        mostrar_sugestoes_cliente()

    def buscar_produto_popup():
        mostrar_sugestoes_produto()

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

    def gravar_orcamento():
        if not itens_mem:
            messagebox.showwarning("Orçamento vazio", "Adicione pelo menos um item.")
            return
        cliente_nome = entry_cliente.get().strip() or "Cliente Avulso"
        cliente_id = cliente_selecionado_id
        conn = get_connection()
        if not conn:
            return
        cur = conn.cursor()
        total = float(atualizar_total_label())
        data = datetime.datetime.now()
        try:
            cur.execute(
                "INSERT INTO orcamento (cliente_id, cliente_nome, data, valor_total) VALUES (%s,%s,%s,%s)",
                (cliente_id, cliente_nome, data, total),
            )
            orcamento_id = cur.lastrowid
            for it in itens_mem:
                cur.execute(
                    "INSERT INTO orcamento_itens "
                    "(orcamento_id, produto_id, produto_nome, quantidade, valor_unitario, valor_total) "
                    "VALUES (%s,%s,%s,%s,%s,%s)",
                    (
                        orcamento_id,
                        it.get("produto_id"),
                        it["produto_nome"],
                        it["quantidade"],
                        it["valor_unitario"],
                        it["valor_total"],
                    ),
                )
            conn.commit()
            messagebox.showinfo("Sucesso", f"Orçamento gravado (ID {orcamento_id}).")
            for row in tree.get_children():
                tree.delete(row)
            itens_mem.clear()
            atualizar_total_label()
            entry_cliente.delete(0, END)
            imprimir_orcamento(salvar=True)
        except mysql.connector.Error as err:
            conn.rollback()
            messagebox.showerror("Erro MySQL", f"Erro ao gravar orçamento:\n{err}")
        finally:
            try:
                cur.close()
                conn.close()
            except:
                pass

    def imprimir_orcamento(salvar=False):
        if not itens_mem:
            messagebox.showwarning("Imprimir", "Não há itens para imprimir.")
            return
        cliente = entry_cliente.get().strip() or "Cliente"
        now = datetime.datetime.now()
        nome_arquivo = f"Orcamento_{cliente}_{now.strftime('%Y%m%d_%H%M%S')}.pdf"
        if salvar:
            file_path = filedialog.asksaveasfilename(
                initialfile=nome_arquivo,
                defaultextension=".pdf",
                filetypes=[("PDF Files", "*.pdf")],
            )
            if not file_path:
                return
            nome_arquivo = file_path
        try:
            c = pdf_canvas.Canvas(nome_arquivo, pagesize=A4)
            width, height = A4
            if os.path.exists(DEFAULT_LOGO_PATH):
                c.drawImage(
                    ImageReader(DEFAULT_LOGO_PATH),
                    40,
                    height - 80,
                    width=120,
                    preserveAspectRatio=True,
                    mask="auto",
                )
            c.setFont("Helvetica-Bold", 18)
            c.drawString(200, height - 60, "ORÇAMENTO")
            c.setFont("Helvetica", 10)
            c.drawString(40, height - 100, f"Cliente: {cliente}")
            c.drawString(40, height - 120, f"Data: {now.strftime('%Y-%m-%d %H:%M:%S')}")
            y = height - 150
            c.setFont("Helvetica-Bold", 10)
            c.drawString(40, y, "Produto")
            c.drawString(360, y, "Quantidade")
            c.drawString(460, y, "Valor Unitário")
            c.drawString(540, y, "Valor Total")
            c.setFont("Helvetica", 10)
            y -= 18
            for it in itens_mem:
                c.drawString(40, y, str(it["produto_nome"])[:40])
                c.drawString(360, y, str(it["quantidade"]))
                c.drawString(460, y, f"R$ {it['valor_unitario']:.2f}")
                c.drawString(540, y, f"R$ {it['valor_total']:.2f}")
                y -= 16
                if y < 80:
                    c.showPage()
                    y = height - 60
            total = sum(Decimal(str(i["valor_total"])) for i in itens_mem)
            c.setFont("Helvetica-Bold", 12)
            c.drawString(40, y - 10, f"Valor Total: R$ {float(total):.2f}")
            c.save()
            messagebox.showinfo("PDF", f"Orçamento salvo como {nome_arquivo}")
        except Exception as e:
            messagebox.showerror("Erro PDF", f"Erro ao gerar PDF: {e}")

    def procurar_orcamento():
        # Implemente tela de busca
        pass

    def gerar_pedido_venda():
        # Mesma tela, lógica identica, mas dar baixa no estoque apenas na gravação da venda
        pass

    def sair():
        for w in frame_conteudo.winfo_children():
            try:
                w.destroy()
            except:
                pass

    # Teclas rápidas e binds de autocomplete
    entry_cliente.bind("<KeyRelease>", mostrar_sugestoes_cliente)
    listbox_cliente.bind("<<ListboxSelect>>", selecionar_cliente)
    entry_cliente.bind("<Return>", lambda e: selecionar_cliente())

    entry_produto.bind("<KeyRelease>", mostrar_sugestoes_produto)
    listbox_produto.bind("<<ListboxSelect>>", selecionar_produto)
    entry_produto.bind("<Return>", lambda e: selecionar_produto())
    entry_qtd.bind("<Return>", lambda e: adicionar_item())

    frame_conteudo._orc_itens = itens_mem

# end of file
