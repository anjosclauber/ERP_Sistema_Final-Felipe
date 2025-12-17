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

from buscar_orcamento import buscar_orcamento  # Import da tela de busca

# Configuration
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

def cadastro_orcamento(frame_conteudo):
    # Fundo
    frame_conteudo.configure(fg_color="#e1f1fd")

    main_frame = ctk.CTkFrame(
        frame_conteudo,
        fg_color="#eaf6ff",
        border_color="#1976d2",
        border_width=2,
        width=1230,
        height=800,
    )
    main_frame.place(relx=0.5, rely=0.5, anchor="center")

    # Título
    ctk.CTkLabel(
        main_frame,
        text="Orçamento",
        font=("Arial", 32, "bold"),
        text_color="#1976d2",
    ).place(relx=0.5, y=70, anchor="center")
    
    # ---------- CAMPO Nº PEDIDO ----------
    ctk.CTkLabel(
        main_frame,
        text="Nº Orç.:",
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
    entry_num_pedido.place(x=1005, y=25)

    # --------- CLIENTE (layout compacto em main_frame) ----------
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
    # posiciona o botão logo à direita do entry
    btn_busca_cliente.place(x=570, y=105)

    # --------- CAMPO DATA (após buscar_cliente) ----------
    from datetime import date
    hoje = date.today().strftime("%d/%m/%Y")
    ctk.CTkLabel(main_frame, text="Data Orcamento", font=("Arial", 16, "bold"), text_color="#1976d2").place(x=632, y=80)
    entry_data = ctk.CTkEntry(main_frame, width=120, height=28, justify="center")
    entry_data.insert(0, hoje)
    entry_data.place(x=632, y=105)

    # Listbox para autocomplete cliente (posicionado abaixo do entry)
    listbox_cliente = Listbox(main_frame, height=5)
    listbox_cliente.place(x=75, y=135, width=470)
    listbox_cliente.place_forget()

    # --------- PRODUTO (layout compacto em main_frame) ----------
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
        command=lambda: adicionar_item(),
    )
    btn_add_item.place(x=920, y=165)

    # Listbox para autocomplete produto (posicionado abaixo do entry)
    listbox_produto = Listbox(main_frame, height=5)
    listbox_produto.place(x=75, y=195, width=470)
    listbox_produto.place_forget()

    # --------- TABELA ----------
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
    # Striped rows
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

    # --------- RODAPÉ ----------
    lbl_total = ctk.CTkLabel(
        main_frame,
        text="Valor Total: R$ 0.00",
        font=("Arial", 20, "bold"),
        text_color="#1976d2",
    )
    lbl_total.place(x=890, y=540)

    # --------- OBSERVAÇÃO ----------
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

    # Campo de texto para observação
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
        # Fallback para tkinter.Text se CTkTextbox não existir
        from tkinter import Text
        obs_text = Text(obs_frame, wrap="word", bd=0, bg="#ffffff", fg="#000000")
        obs_text.place(x=15, y=10, width=1020, height=80)

    # ====== FUNÇÃO pack_button (agora com width/height opcionais) ======
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

    # Função sair: limpa o conteúdo e retorna ao portal mostrando a marca d'água grande
    def sair_local():
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

    # ====== BOTÕES ======
    # posicionamento com gap ~30px entre botões (considerando widths padrão/explicit)
    pack_button("Gravar", lambda: gravar_orcamento(), "#1f80ff", 175)
    pack_button("Procurar", lambda: procurar_orcamento(), "#1f80ff", 315)
    pack_button("Excluir", lambda: excluir_item(), "#e53935", 455, hover_color="#cc0000")
    pack_button(
        "Gerar P. Venda",
        lambda: gerar_pedido_venda(),
        "#1f80ff",
        595,
        hover_color="#0b60c9",
        width=160,
        height=28,
    )

    pack_button("Imprimir", lambda: imprimir_orcamento(salvar=True), "#1f80ff", 785)
    pack_button("Sair", lambda: sair_local(), "#e53935", 925, hover_color="#cc0000")

    # ---------- FUNÇÕES DE AUTOCOMPLETE / BUSCA BANCO ----------
    def buscar_cliente_sugestoes(prefixo):
        """Retorna lista de dicionários com id e nome do cliente cujo nome começa com prefixo."""
        conn = get_connection()
        if not conn:
            return []
        try:
            cur = conn.cursor(dictionary=True)
            # Prioriza resultados que começam com o prefixo (mais relevantes), depois ordena por nome
            cur.execute(
                "SELECT id, nome FROM cliente WHERE nome LIKE %s ORDER BY (nome LIKE %s) DESC, nome LIMIT 50",
                (prefixo + "%", prefixo + "%"),
            )
            dados = cur.fetchall()
            return dados
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
        """Retorna lista de dicionários com id, produto e pvenda."""
        conn = get_connection()
        if not conn:
            return []
        try:
            cur = conn.cursor(dictionary=True)
            # Prioriza resultados que começam com o prefixo (mais relevantes), depois ordena por produto
            cur.execute(
                "SELECT id, produto, pvenda FROM produto WHERE produto LIKE %s ORDER BY (produto LIKE %s) DESC, produto LIMIT 50",
                (prefixo + "%", prefixo + "%"),
            )
            dados = cur.fetchall()
            return dados
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
        # Autocomplete inline: responde a cada tecla, ignora navegação e permite apagar
        nonlocal cliente_selecionado_id
        # Ignore navigation keys so user can move cursor freely
        if event is not None:
            nav_keys = ("Left", "Right", "Up", "Down", "Home", "End", "Escape", "Tab")
            if getattr(event, "keysym", None) in nav_keys:
                return
        prefix = entry_cliente.get()
        cliente_selecionado_id = None
        # não sugerir para prefixos muito curtos
        if not prefix or len(prefix.strip()) < 2:
            return
        dados = buscar_cliente_sugestoes(prefix)
        if not dados:
            return
        first = dados[0]
        _id = first.get("id")
        nome = first.get("nome") or ""
        # só autocomplete se houver continuação
        if nome and nome.lower().startswith(prefix.lower()) and len(nome) > len(prefix):
            # Sugere apenas a próxima letra e seleciona essa sugestão
            next_piece = nome[len(prefix):len(prefix)+1]
            suggested = prefix + next_piece
            entry_cliente.delete(0, END)
            entry_cliente.insert(0, suggested)
            try:
                entry_cliente.selection_range(len(prefix), len(suggested))
                entry_cliente.icursor(len(prefix))
            except Exception:
                pass
            try:
                cliente_selecionado_id = int(_id)
            except Exception:
                cliente_selecionado_id = None

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
        # Autocomplete inline para produto: responde a cada tecla, ignora navegação
        nonlocal produto_selecionado_id
        if event is not None:
            nav_keys = ("Left", "Right", "Up", "Down", "Home", "End", "Escape", "Tab")
            if getattr(event, "keysym", None) in nav_keys:
                return
        prefix = entry_produto.get()
        produto_selecionado_id = None
        # não sugerir para prefixos muito curtos
        if not prefix or len(prefix.strip()) < 2:
            return
        dados = buscar_produto_sugestoes(prefix)
        if not dados:
            return
        first = dados[0]
        _id = first.get("id")
        nome = first.get("produto") or ""
        pvenda = first.get("pvenda")
        if nome and nome.lower().startswith(prefix.lower()) and len(nome) > len(prefix):
            # Sugere apenas a próxima letra do produto
            next_piece = nome[len(prefix):len(prefix)+1]
            suggested = prefix + next_piece
            entry_produto.delete(0, END)
            entry_produto.insert(0, suggested)
            try:
                entry_produto.selection_range(len(prefix), len(suggested))
                entry_produto.icursor(len(prefix))
            except Exception:
                pass
            try:
                produto_selecionado_id = int(_id)
            except Exception:
                produto_selecionado_id = None
            # não preencher preço automaticamente aqui; aguarda seleção completa

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

    def buscar_cliente_popup():
        mostrar_sugestoes_cliente()

    def buscar_produto_popup():
        mostrar_sugestoes_produto()

    # ====== OVERLAY DE BUSCA DE CLIENTE ======
    def abrir_busca_cliente_overlay():
        nonlocal cliente_selecionado_id
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
            nonlocal cliente_selecionado_id
            sel = tree_cli.selection()
            if not sel:
                return
            iid = sel[0]
            vals = tree_cli.item(iid)["values"]
            nome = vals[1]
            try:
                cliente_selecionado_id = int(iid)
            except Exception:
                cliente_selecionado_id = None
            entry_cliente.delete(0, END)
            entry_cliente.insert(0, nome)
            overlay.destroy()

        entry_search.bind("<KeyRelease>", pesquisar_overlay_cliente)
        tree_cli.bind("<<TreeviewSelect>>", selecionar_cliente_overlay)

    # ====== OVERLAY DE BUSCA DE PRODUTO ======
    def abrir_busca_produto_overlay():
        nonlocal produto_selecionado_id
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
            nonlocal produto_selecionado_id
            sel = tree_prd.selection()
            if not sel:
                return
            iid = sel[0]
            vals = tree_prd.item(iid)["values"]
            produto = vals[1]
            pvenda = vals[2]
            try:
                produto_selecionado_id = int(iid)
            except Exception:
                produto_selecionado_id = None
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

    def atualizar_total_label():
        total = Decimal("0.00")
        for it in itens_mem:
            total += Decimal(str(it["valor_total"]))
        lbl_total.configure(text=f"Valor Total: R$ {float(total):.2f}")
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
        idx = len(tree.get_children())
        tag = "evenrow" if idx % 2 == 0 else "oddrow"
        tree.insert(
            "",
            "end",
            values=(
                item["produto_nome"],
                str(item["quantidade"]),
                f"R$ {float(item['valor_unitario']):.2f}",
                f"R$ {float(item['valor_total']):.2f}",
            ),
            tags=(tag,)
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
        cliente = entry_cliente.get().strip() or "Cliente Avulso"
        cliente_id = cliente_selecionado_id
        conn = get_connection()
        if not conn:
            return
        cur = conn.cursor()
        total = float(atualizar_total_label())
        data_orcamento = datetime.datetime.now()
        try:
            cur.execute(
                "INSERT INTO orcamento (cliente_id, cliente, data_orcamento, valor_total) VALUES (%s,%s,%s,%s)",
                (cliente_id, cliente, data_orcamento, total),
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

    # ---------- FUNÇÃO DE BUSCA INTEGRADA ----------
    def carregar_orcamento(orcamento):
        nonlocal cliente_selecionado_id
        for row in tree.get_children():
            tree.delete(row)
        itens_mem.clear()

        cliente_selecionado_id = orcamento.get("cliente_id")
        entry_cliente.delete(0, END)
        entry_cliente.insert(0, f"Cliente {cliente_selecionado_id or ''}")

        for it in orcamento.get("itens", []):
            itens_mem.append(it)
            tree.insert(
                "",
                "end",
                values=(
                    it["produto_nome"],
                    str(it["quantidade"]),
                    f"R$ {float(it['valor_unitario']):.2f}",
                    f"R$ {float(it['valor_total']):.2f}",
                ),
            )
        atualizar_total_label()

    def procurar_orcamento():
        buscar_orcamento(frame_conteudo, callback=carregar_orcamento)

    def gerar_pedido_venda():
        pass
    # Eventos de teclas / bindings
    entry_cliente.bind("<KeyRelease>", mostrar_sugestoes_cliente)
    listbox_cliente.bind("<<ListboxSelect>>", selecionar_cliente)
    entry_cliente.bind("<Return>", lambda e: selecionar_cliente())

    entry_produto.bind("<KeyRelease>", mostrar_sugestoes_produto)
    listbox_produto.bind("<<ListboxSelect>>", selecionar_produto)
    entry_produto.bind("<Return>", lambda e: selecionar_produto())
    entry_qtd.bind("<Return>", lambda e: adicionar_item())

    # Guarda itens no frame para uso externo
    frame_conteudo._orc_itens = itens_mem
