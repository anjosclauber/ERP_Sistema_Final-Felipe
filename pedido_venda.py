# pedido_venda.py
import os
import datetime
from decimal import Decimal, InvalidOperation

import customtkinter as ctk
from tkinter import ttk, messagebox, filedialog, Toplevel, END, Listbox
import mysql.connector

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib.utils import ImageReader

# Configuration - ajuste se necessário
DB_HOST = "127.0.0.1"
DB_USER = "root"
DB_PASSWORD = ""
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
    # Fundo igual orçamento
    frame_conteudo.configure(fg_color="#e1f1fd")

    main_frame = ctk.CTkFrame(
        frame_conteudo,
        fg_color="#eaf6ff",
        border_color="#1976d2",
        border_width=2,
        width=1200,
        height=800,
    )
    main_frame.place(relx=0.5, rely=0.5, anchor="center")

    # Título
    ctk.CTkLabel(
        main_frame,
        text="Pedido de Venda",
        font=("Arial", 32, "bold"),
        text_color="#1976d2",
    ).place(relx=0.5, y=40, anchor="center")

    # Campo Nº Pedido
    ctk.CTkLabel(
        main_frame,
        text="Nº Pedido:",
        font=("Arial", 16, "bold"),
        text_color="#1976d2",
    ).place(x=935, y=30)
    entry_num_pedido = ctk.CTkEntry(
        main_frame,
        fg_color="#eaf6ff",
        width=110,
        height=30,
        placeholder_text="",
        border_width=0,
    )
    entry_num_pedido.place(x=1010, y=25)


    # Cliente
    ctk.CTkLabel(main_frame, text="Cliente", font=("Arial", 18, "bold"), text_color="#1976d2").place(x=75, y=80)
    entry_cliente = ctk.CTkEntry(main_frame, width=470, height=28, placeholder_text="Digite o cliente")
    entry_cliente.place(x=75, y=105)
    btn_busca_cliente = ctk.CTkButton(
        main_frame,
        text="🔍",
        width=36,
        height=28,
        fg_color="#1f80ff",
        hover_color="#0b60c9",
        command=lambda: abrir_busca_cliente_overlay(),
    )
    btn_busca_cliente.place(x=570, y=105)
    # Data do pedido (igual orçamento)
    from datetime import date
    hoje = date.today().strftime("%d/%m/%Y")
    ctk.CTkLabel(main_frame, text="Data Pedido", font=("Arial", 16, "bold"), text_color="#1976d2").place(x=632, y=80)
    entry_data = ctk.CTkEntry(main_frame, width=120, height=28, justify="center")
    entry_data.insert(0, hoje)
    entry_data.place(x=632, y=105)
    listbox_cliente = Listbox(main_frame, height=5)
    listbox_cliente.place(x=75, y=135, width=470)
    listbox_cliente.place_forget()

    # Produto
    ctk.CTkLabel(main_frame, text="Produto", font=("Arial", 18, "bold"), text_color="#1976d2").place(x=75, y=140)
    entry_produto = ctk.CTkEntry(main_frame, width=470, height=28, placeholder_text="Digite o produto")
    entry_produto.place(x=75, y=165)
    btn_busca_produto = ctk.CTkButton(
        main_frame,
        text="🔍",
        width=36,
        height=28,
        fg_color="#1f80ff",
        hover_color="#0b60c9",
        command=lambda: abrir_busca_produto_overlay(),
    )

    btn_busca_produto.place(x=570, y=165)

    # Overlay de busca de cliente (igual orçamento)
    def abrir_busca_cliente_overlay():
        overlay = ctk.CTkFrame(
            frame_conteudo,
            fg_color="#eaf6ff",
            border_color="#1976d2",
            border_width=2,
            width=1200,
            height=800,
        )
        overlay.place(relx=0.5, rely=0.5, anchor="center")
        ctk.CTkLabel(overlay, text="Cliente", font=("Arial", 18, "bold"), text_color="#1976d2").place(x=75, y=80)
        entry_search = ctk.CTkEntry(overlay, width=470, height=28, placeholder_text="Digite o cliente")
        entry_search.place(x=75, y=105)
        btn_fechar = ctk.CTkButton(overlay, text="Fechar", width=90, height=28, fg_color="#e53935", hover_color="#cc0000", command=lambda: overlay.destroy())
        btn_fechar.place(x=995, y=105)
        cols = ("arrow", "id", "nome", "endereco", "cpf_cnpj", "telefone", "email")
        tree_cli = ttk.Treeview(overlay, columns=cols, show="headings", height=12)
        tree_cli.heading("arrow", text="")
        tree_cli.heading("id", text="ID")
        tree_cli.heading("nome", text="Nome")
        tree_cli.heading("endereco", text="Endereço")
        tree_cli.heading("cpf_cnpj", text="CPF/CNPJ")
        tree_cli.heading("telefone", text="Telefone")
        tree_cli.heading("email", text="Email")
        tree_cli.column("arrow", width=30, anchor="center")
        tree_cli.column("id", width=60, anchor="center")
        tree_cli.column("nome", width=250)
        tree_cli.column("endereco", width=250)
        tree_cli.column("cpf_cnpj", width=120, anchor="center")
        tree_cli.column("telefone", width=120, anchor="center")
        tree_cli.column("email", width=200)
        tree_cli.place(x=75, y=150, width=1050, height=420)
        vsb = ttk.Scrollbar(overlay, orient="vertical", command=tree_cli.yview)
        vsb.place(x=1125, y=150, height=420)
        tree_cli.configure(yscrollcommand=vsb.set)
        try:
            tree_cli.tag_configure("match", foreground="#1f80ff")
        except Exception:
            pass
        def pesquisar_overlay_cliente(event=None):
            q = entry_search.get().strip()
            for r in tree_cli.get_children():
                tree_cli.delete(r)
            if not q:
                return
            conn = get_connection()
            if not conn:
                return
            try:
                cur = conn.cursor()
                cur.execute(
                    "SELECT id, nome, endereco, cpf_cnpj, telefone, email FROM cliente WHERE nome LIKE %s ORDER BY nome LIMIT 200",
                    (q + "%",),
                )
                for row in cur.fetchall():
                    _id, nome, endereco, cpf, telefone, email = row
                    arrow = "→" if q.lower() in (nome or "").lower() else ""
                    tag = "match" if arrow else ""
                    tree_cli.insert("", "end", iid=str(_id), values=(arrow, _id, nome or "", endereco or "", cpf or "", telefone or "", email or ""), tags=(tag,))
            except Exception:
                pass
            finally:
                try:
                    cur.close()
                    conn.close()
                except:
                    pass
        def selecionar_cliente_overlay(event=None):
            sel = tree_cli.selection()
            if not sel:
                return
            iid = sel[0]
            vals = tree_cli.item(iid)["values"]
            nome = vals[2]
            entry_cliente.delete(0, END)
            entry_cliente.insert(0, nome)
            overlay.destroy()
        entry_search.bind("<KeyRelease>", pesquisar_overlay_cliente)
        tree_cli.bind("<<TreeviewSelect>>", selecionar_cliente_overlay)

    # Overlay de busca de produto (igual orçamento)
    def abrir_busca_produto_overlay():
        overlay = ctk.CTkFrame(
            frame_conteudo,
            fg_color="#eaf6ff",
            border_color="#1976d2",
            border_width=2,
            width=1200,
            height=800,
        )
        overlay.place(relx=0.5, rely=0.5, anchor="center")
        ctk.CTkLabel(overlay, text="Produto", font=("Arial", 18, "bold"), text_color="#1976d2").place(x=75, y=80)
        entry_search = ctk.CTkEntry(overlay, width=470, height=28, placeholder_text="Digite o produto")
        entry_search.place(x=75, y=105)
        btn_fechar = ctk.CTkButton(overlay, text="Fechar", width=90, height=28, fg_color="#e53935", hover_color="#cc0000", command=lambda: overlay.destroy())
        btn_fechar.place(x=995, y=105)
        cols = ("arrow", "id", "produto", "pvenda", "descricao")
        tree_prd = ttk.Treeview(overlay, columns=cols, show="headings", height=12)
        tree_prd.heading("arrow", text="")
        tree_prd.heading("id", text="ID")
        tree_prd.heading("produto", text="Produto")
        tree_prd.heading("pvenda", text="Preço")
        tree_prd.heading("descricao", text="Descrição")
        tree_prd.column("arrow", width=30, anchor="center")
        tree_prd.column("id", width=60, anchor="center")
        tree_prd.column("produto", width=320)
        tree_prd.column("pvenda", width=120, anchor="center")
        tree_prd.column("descricao", width=500)
        tree_prd.place(x=75, y=150, width=1050, height=420)
        vsb = ttk.Scrollbar(overlay, orient="vertical", command=tree_prd.yview)
        vsb.place(x=1125, y=150, height=420)
        tree_prd.configure(yscrollcommand=vsb.set)
        try:
            tree_prd.tag_configure("match", foreground="#1f80ff")
        except Exception:
            pass
        def pesquisar_overlay_produto(event=None):
            q = entry_search.get().strip()
            for r in tree_prd.get_children():
                tree_prd.delete(r)
            if not q:
                return
            conn = get_connection()
            if not conn:
                return
            try:
                cur = conn.cursor()
                cur.execute(
                    "SELECT id, produto, pvenda, descricao FROM produto WHERE produto LIKE %s ORDER BY produto LIMIT 200",
                    (q + "%",),
                )
                for row in cur.fetchall():
                    _id, produto, pvenda, descricao = row
                    arrow = "→" if q.lower() in (produto or "").lower() else ""
                    tag = "match" if arrow else ""
                    tree_prd.insert("", "end", iid=str(_id), values=(arrow, _id, produto or "", pvenda or "", descricao or ""), tags=(tag,))
            except Exception:
                pass
            finally:
                try:
                    cur.close()
                    conn.close()
                except:
                    pass
        def selecionar_produto_overlay(event=None):
            sel = tree_prd.selection()
            if not sel:
                return
            iid = sel[0]
            vals = tree_prd.item(iid)["values"]
            produto = vals[2]
            pvenda = vals[3]
            entry_produto.delete(0, END)
            entry_produto.insert(0, produto)
            try:
                entry_valor.delete(0, END)
                entry_valor.insert(0, str(pvenda))
            except Exception:
                pass
            overlay.destroy()
        entry_search.bind("<KeyRelease>", pesquisar_overlay_produto)
        tree_prd.bind("<<TreeviewSelect>>", selecionar_produto_overlay)
    ctk.CTkLabel(main_frame, text="Quantidade", font=("Arial", 16, "bold"), text_color="#1976d2").place(x=632, y=140)
    entry_qtd = ctk.CTkEntry(main_frame, width=120, height=28, placeholder_text="Quantidade")
    entry_qtd.place(x=632, y=165)
    ctk.CTkLabel(main_frame, text="Valor Unitário", font=("Arial", 16, "bold"), text_color="#1976d2").place(x=775, y=140)
    entry_valor = ctk.CTkEntry(main_frame, width=120, height=28, placeholder_text="Valor Unitário")
    entry_valor.place(x=775, y=165)
    btn_add_item = ctk.CTkButton(
        main_frame,
        text="Inserir Produto",
        font=("Arial", 14, "bold"),
        fg_color="#1f80ff",
        hover_color="#0b60c9",
        width=140,
        height=28,
        command=lambda: None,  # Implementar função
    )
    btn_add_item.place(x=920, y=165)
    listbox_produto = Listbox(main_frame, height=5)
    listbox_produto.place(x=75, y=195, width=470)
    listbox_produto.place_forget()

    # Tabela
    table_frame = ctk.CTkFrame(
        main_frame,
        fg_color="#eaf6ff",
        width=1100,
        height=320,
    )
    table_frame.place(x=75, y=210)
    tree = ttk.Treeview(
        table_frame,
        columns=("produto", "quantidade", "valor_unitario", "valor_total"),
        show="headings",
        height=11,
    )
    tree.tag_configure("oddrow", background="#ffffff")
    tree.tag_configure("evenrow", background="#f5f7fb")
    tree.heading("produto", text="Produto")
    tree.heading("quantidade", text="Quantidade")
    tree.heading("valor_unitario", text="Valor Unitário")
    tree.heading("valor_total", text="Valor Total")
    tree.column("produto", width=550)
    tree.column("quantidade", width=100, anchor="center")
    tree.column("valor_unitario", width=180, anchor="center")
    tree.column("valor_total", width=180, anchor="center")
    tree.place(x=0, y=0, width=1050, height=320)
    vsb = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
    vsb.place(x=1050, y=0, height=320)
    tree.configure(yscrollcommand=vsb.set)

    itens_mem = []
    cliente_selecionado_id = None
    produto_selecionado_id = None

    # Rodapé
    lbl_total = ctk.CTkLabel(
        main_frame,
        text="Valor Total: R$ 0.00",
        font=("Arial", 20, "bold"),
        text_color="#1976d2",
    )
    lbl_total.place(x=890, y=540)

    # Observação
    ctk.CTkLabel(
        main_frame,
        text="Observação",
        font=("Arial", 14, "bold"),
        text_color="#1976d2",
    ).place(x=75, y=560)
    obs_frame = ctk.CTkFrame(
        main_frame,
        fg_color="#ffffff",
        border_color="#000000",
        border_width=1,
        width=1050,
        height=100,
    )
    obs_frame.place(x=75, y=590)
    try:
        obs_text = ctk.CTkTextbox(
            obs_frame,
            width=1020,
            height=80,
            fg_color="#ffffff",
            text_color="#000000",
        )
        obs_text.place(x=15, y=10)
    except Exception:
        from tkinter import Text
        obs_text = Text(obs_frame, wrap="word", bd=0, bg="#ffffff", fg="#000000")
        obs_text.place(x=15, y=10, width=1020, height=80)

    # Função pack_button igual orçamento
    def pack_button(text, cmd, color, xpos, hover_color="#0b60c9", width=None, height=None):
        btn = ctk.CTkButton(
            main_frame,
            text=text,
            width=width if width is not None else 110,
            height=height if height is not None else 28,
            fg_color=color,
            hover_color=hover_color,
            font=("Arial", 14, "bold"),
            command=cmd,
        )
        btn.place(x=xpos, y=720)

    # Botões
    pack_button("Gravar", lambda: None, "#1f80ff", 265)

    # Overlay de busca de pedido igual buscar_orcamento
    def abrir_busca_pedido_overlay():
        colunas = ("id", "cliente", "data", "vendedor", "total")
        overlay = ctk.CTkToplevel() if not hasattr(frame_conteudo, 'winfo_children') else ctk.CTkFrame(
            frame_conteudo,
            fg_color="#eaf6ff",
            border_color="#1976d2",
            border_width=2,
            width=1200,
            height=800,
        )
        overlay.place(relx=0.5, rely=0.5, anchor="center")
        ctk.CTkLabel(
            overlay,
            text="Buscar Pedido de Venda",
            font=("Arial", 32, "bold"),
            text_color="#1976d2",
        ).place(relx=0.5, y=40, anchor="center")

        # Filtros
        ctk.CTkLabel(overlay, text="Cliente", font=("Arial", 18, "bold"), text_color="#1976d2").place(x=75, y=100)
        entry_cliente = ctk.CTkEntry(overlay, width=350, height=28, placeholder_text="Cliente")
        entry_cliente.place(x=75, y=125)

        x_ped_label = 75 + 350 + 30
        ctk.CTkLabel(overlay, text="N° Pedido", font=("Arial", 18, "bold"), text_color="#1976d2").place(x=x_ped_label, y=100)
        entry_num_ped = ctk.CTkEntry(overlay, width=140, height=28, placeholder_text="N° Pedido")
        entry_num_ped.place(x=x_ped_label, y=125)

        ctk.CTkLabel(overlay, text="Data Início", font=("Arial", 18, "bold"), text_color="#1976d2").place(x=630, y=100)
        entry_data_ini = ctk.CTkEntry(overlay, width=140, height=28, placeholder_text="dd/mm/aaaa")
        entry_data_ini.place(x=630, y=125)
        ctk.CTkLabel(overlay, text="Data Fim", font=("Arial", 18, "bold"), text_color="#1976d2").place(x=800, y=100)
        entry_data_fim = ctk.CTkEntry(overlay, width=140, height=28, placeholder_text="dd/mm/aaaa")
        entry_data_fim.place(x=800, y=125)

        # Botão buscar
        def pesquisar():
            cliente = entry_cliente.get().strip()
            num_ped = entry_num_ped.get().strip()
            data_ini = entry_data_ini.get().strip()
            data_fim = entry_data_fim.get().strip()

            query = "SELECT id, cliente_nome, data, vendedor, valor_total FROM pedido_venda WHERE 1=1"
            params = []
            if cliente:
                query += " AND cliente_nome LIKE %s"
                params.append(cliente + "%")
            if num_ped:
                query += " AND id LIKE %s"
                params.append(num_ped + "%")
            if data_ini:
                try:
                    d = datetime.datetime.strptime(data_ini, "%d/%m/%Y").date()
                    query += " AND data >= %s"
                    params.append(d)
                except ValueError:
                    messagebox.showerror("Erro", "Data Início inválida. Use dd/mm/aaaa.")
                    return
            if data_fim:
                try:
                    d = datetime.datetime.strptime(data_fim, "%d/%m/%Y").date()
                    query += " AND data <= %s"
                    params.append(d)
                except ValueError:
                    messagebox.showerror("Erro", "Data Fim inválida. Use dd/mm/aaaa.")
                    return
            conn = get_connection()
            if not conn:
                return
            cur = conn.cursor()
            tree.delete(*tree.get_children())
            try:
                cur.execute(query, params)
                for idx, row in enumerate(cur.fetchall()):
                    tag = "evenrow" if idx % 2 == 0 else "oddrow"
                    tree.insert("", "end", values=row, tags=(tag,))
            except mysql.connector.Error as e:
                messagebox.showerror("MySQL", f"Erro ao buscar pedidos:\n{e}")
            finally:
                cur.close()
                conn.close()

        botao_buscar = ctk.CTkButton(
            overlay,
            width=45,
            text="🔍",
            height=28,
            fg_color="#1f80ff",
            hover_color="#0b60c9",
            command=pesquisar,
        )
        botao_buscar.place(x=1000, y=125)

        # Tabela igual buscar_orcamento
        table_frame = ctk.CTkFrame(
            overlay,
            fg_color="#eaf6ff",
            width=1100,
            height=300,
        )
        table_frame.place(x=75, y=180)
        tree = ttk.Treeview(table_frame, columns=colunas, show="headings", height=11)
        tree.tag_configure("oddrow", background="#ffffff")
        tree.tag_configure("evenrow", background="#f5f7fb")
        tree.heading("id", text="Pedido")
        tree.heading("cliente", text="Cliente")
        tree.heading("data", text="Data Emissão")
        tree.heading("vendedor", text="Vendedor")
        tree.heading("total", text="Valor Total")
        tree.column("id", width=120)
        tree.column("cliente", width=350)
        tree.column("data", width=150)
        tree.column("vendedor", width=180)
        tree.column("total", width=150)
        tree.place(x=0, y=0, width=1050, height=300)
        scroll = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        scroll.place(x=1050, y=0, height=300)
        tree.configure(yscrollcommand=scroll.set)

        # Seleção
        def selecionar_pedido(event=None):
            sel = tree.selection()
            if not sel:
                return
            pedido_id = tree.item(sel[0])["values"][0]
            # Aqui pode-se carregar detalhes do pedido se desejar
            messagebox.showinfo("Pedido", f"Abrir pedido {pedido_id}")
            if hasattr(overlay, 'destroy'):
                overlay.destroy()

        tree.bind("<<TreeviewSelect>>", selecionar_pedido)

        # Botão fechar
        btn_fechar = ctk.CTkButton(overlay, text="Fechar", width=90, height=28, fg_color="#e53935", hover_color="#cc0000", command=lambda: overlay.destroy())
        btn_fechar.place(x=1100, y=720)


    def sair_pedido():
        for w in frame_conteudo.winfo_children():
            try:
                w.destroy()
            except:
                pass
        try:
            from portal import mostrar_marca_dagua_grande
            mostrar_marca_dagua_grande(frame_conteudo)
        except Exception:
            try:
                import portal
                portal.mostrar_marca_dagua_grande(frame_conteudo)
            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível retornar ao portal:\n{e}")

    pack_button("Procurar", lambda: abrir_busca_pedido_overlay(), "#1f80ff", 405)
    pack_button("Excluir", lambda: None, "#e53935", 545, hover_color="#cc0000")
    pack_button("Imprimir", lambda: None, "#1f80ff", 688)
    pack_button("Sair", sair_pedido, "#e53935", 828, hover_color="#cc0000")

