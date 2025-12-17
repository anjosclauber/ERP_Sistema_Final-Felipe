# === buscar_orcamento.py ===

import customtkinter as ctk
from tkinter import ttk, messagebox
import mysql.connector
import datetime
from tkcalendar import Calendar

DB_HOST = "127.0.0.1"
DB_USER = "root"
DB_PASSWORD = "MAJu2022@"
DB_NAME = "erp_sistema"

def get_connection():
    try:
        return mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
        )
    except mysql.connector.Error as e:
        messagebox.showerror("Erro MySQL", f"Conexão: {e}")
        return None

# ============================================================
#   TELA PRINCIPAL DE BUSCA DE ORÇAMENTOS
# ============================================================
def buscar_orcamento(master=None, callback=None, callback_voltar=None):
    colunas = ("id", "cliente", "data", "vendedor", "total")

    embed = master is not None

    if not embed:
        master = ctk.CTkToplevel()
        master.title("Buscar Orçamento")
        master.geometry("1400x900")

    for w in master.winfo_children():
        w.destroy()

    # ============ FUNDO ============
    master.configure(fg_color="#e1f1fd")

    # ============ FRAME PRINCIPAL COM BORDA ============
    main_frame = ctk.CTkFrame(
        master,
        fg_color="#eaf6ff",
        border_color="#1976d2",
        border_width=2,
        width=1200,
        height=800,
    )
    main_frame.place(relx=0.5, rely=0.5, anchor="center")

    # ==================== TÍTULO ====================
    ctk.CTkLabel(
        main_frame,
        text="Buscar Orçamento",
        font=("Arial", 32, "bold"),
        text_color="#1976d2",
    ).place(relx=0.5, y=40, anchor="center")

    # ================== FILTROS ==================
    ctk.CTkLabel(main_frame, text="Cliente", font=("Arial", 18, "bold"), text_color="#1976d2").place(x=75, y=100)
    entry_cliente = ctk.CTkEntry(main_frame, width=350, height=28, placeholder_text="Cliente")
    entry_cliente.place(x=75, y=125)

    # Campo N° Orçamento (30px de espaço após o campo Cliente)
    x_orc_label = 75 + 350 + 30  # 75 (x do cliente) + 350 (largura cliente) + 30 (espaço)
    ctk.CTkLabel(main_frame, text="N° Orçamento", font=("Arial", 18, "bold"), text_color="#1976d2").place(x=x_orc_label, y=100)
    entry_num_orc = ctk.CTkEntry(main_frame, width=140, height=28, placeholder_text="N° Orçamento")
    entry_num_orc.place(x=x_orc_label, y=125)

    ctk.CTkLabel(main_frame, text="Data Início", font=("Arial", 18, "bold"), text_color="#1976d2").place(x=630, y=100)

    entry_data_ini = ctk.CTkEntry(main_frame, width=140, height=28, placeholder_text="dd/mm/aaaa")
    entry_data_ini.place(x=630, y=125)
    ctk.CTkLabel(main_frame, text="Data Fim", font=("Arial", 18, "bold"), text_color="#1976d2").place(x=800, y=100)
    entry_data_fim = ctk.CTkEntry(main_frame, width=140, height=28, placeholder_text="dd/mm/aaaa")
    entry_data_fim.place(x=800, y=125)

    def abrir_calendario(entry):
        # Fecha outros calendários se abertos
        for widget in main_frame.winfo_children():
            if str(widget.winfo_class()) == 'Toplevel':
                widget.destroy()
        top = ctk.CTkToplevel(main_frame)
        top.geometry(f"250x230+{entry.winfo_rootx()}+{entry.winfo_rooty()+30}")
        top.overrideredirect(True)
        azul_bg = '#e3f0fb'
        azul_fg = '#1976d2'
        azul_header = '#b3d8f7'
        azul_select = '#90caf9'
        azul_border = '#90caf9'
        cal = Calendar(
            top,
            selectmode='day',
            date_pattern='dd/mm/yyyy',
            locale='pt_BR',
            background=azul_bg,
            foreground=azul_fg,
            selectbackground=azul_select,
            selectforeground=azul_fg,
            headersbackground=azul_header,
            headersforeground=azul_fg,
            weekendbackground=azul_bg,
            weekendforeground=azul_fg,
            othermonthbackground='#f0f6fa',
            othermonthwebackground='#f0f6fa',
            bordercolor=azul_border,
            disabledbackground='#e0e0e0',
            disabledforeground='#b0b0b0',
            normalbackground=azul_bg,
            normalforeground=azul_fg,
        )
        cal.pack(expand=True, fill='both')
        def escolher_data(event=None):
            entry.delete(0, 'end')
            entry.insert(0, cal.get_date())
            top.destroy()
        cal.bind("<Double-1>", escolher_data)
        cal.bind("<Return>", escolher_data)
        # Fecha ao perder foco
        top.focus_force()
        top.bind('<FocusOut>', lambda e: top.destroy())

    entry_data_ini.bind('<Button-1>', lambda e: abrir_calendario(entry_data_ini))
    entry_data_fim.bind('<Button-1>', lambda e: abrir_calendario(entry_data_fim))

    # (Removido: já criado acima)

    # Botão buscar
    def pesquisar():
        cliente = entry_cliente.get().strip()
        data_ini = entry_data_ini.get().strip()
        data_fim = entry_data_fim.get().strip()

        query = "SELECT id, cliente_nome, data, vendedor, valor_total FROM orcamento WHERE 1=1"
        params = []

        if cliente:
            query += " AND cliente_nome LIKE %s"
            params.append(cliente + "%")

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
        tabela.delete(*tabela.get_children())
        try:
            cur.execute(query, params)
            for idx, row in enumerate(cur.fetchall()):
                tag = "evenrow" if idx % 2 == 0 else "oddrow"
                tabela.insert("", "end", values=row, tags=(tag,))
        except mysql.connector.Error as e:
            messagebox.showerror("MySQL", f"Erro ao buscar orçamentos:\n{e}")
        finally:
            cur.close()
            conn.close()

    botao_buscar = ctk.CTkButton(
        main_frame,
        width=45,
        text="🔍",
        height=28,
        fg_color="#1f80ff",
        hover_color="#0b60c9",
        command=pesquisar,
    )
    botao_buscar.place(x=1000, y=125)

    # ================== TABELA ==================
    table_frame = ctk.CTkFrame(
        main_frame,
        fg_color="#eaf6ff",
        width=1100,
        height=300,
    )
    table_frame.place(x=75, y=180)
    tabela = ttk.Treeview(table_frame, columns=colunas, show="headings", height=11)
    tabela.tag_configure("oddrow", background="#ffffff")
    tabela.tag_configure("evenrow", background="#f5f7fb")

    tabela.heading("id", text="Orçamento")
    tabela.heading("cliente", text="Cliente")
    tabela.heading("data", text="Data Emissão")
    tabela.heading("vendedor", text="Vendedor")
    tabela.heading("total", text="Valor Total")

    tabela.column("id", width=120)
    tabela.column("cliente", width=350)
    tabela.column("data", width=150)
    tabela.column("vendedor", width=180)
    tabela.column("total", width=150)

    tabela.place(x=0, y=0, width=1050, height=300)

    scroll = ttk.Scrollbar(table_frame, orient="vertical", command=tabela.yview)
    scroll.place(x=1050, y=0, height=300)
    tabela.configure(yscrollcommand=scroll.set)

    # ================== OBSERVAÇÕES ==================
    ctk.CTkLabel(
        main_frame,
        text="Observação",
        font=("Arial", 14, "bold"),
        text_color="#1976d2",
    ).place(x=75, y=510)
    
    obs_frame = ctk.CTkFrame(
        main_frame,
        fg_color="#ffffff",
        border_color="#000000",
        border_width=1,
        width=500,
        height=100,
    )
    obs_frame.place(x=75, y=540)

    obs = ctk.CTkTextbox(
        obs_frame,
        width=480,
        height=80,
        fg_color="#ffffff",
        text_color="#000000",
    )
    obs.place(x=10, y=10)

    # ================== ITENS DO ORÇAMENTO ==================
    ctk.CTkLabel(
        main_frame,
        text="Itens do Orçamento",
        font=("Arial", 14, "bold"),
        text_color="#1976d2",
    ).place(x=625, y=510)
    
    itens_frame = ctk.CTkFrame(
        main_frame,
        fg_color="#eaf6ff",
        width=500,
        height=100,
    )
    itens_frame.place(x=625, y=540)

    col_itens = ("produto", "qtd")
    tabela_itens = ttk.Treeview(itens_frame, columns=col_itens, show="headings", height=5)

    # ===== Estilo e cores para tabela_itens =====
    style = ttk.Style()
    try:
        style.theme_use("default")
    except Exception:
        pass

    # Cores de fundo, texto e cabeçalho
    style.configure(
        "Treeview",
        background="#ffffff",
        foreground="#000000",
        fieldbackground="#ffffff",
        rowheight=24,
        font=("Arial", 10),
        bordercolor="#d9d9d9",
        relief="flat",
    )
    style.configure(
        "Treeview.Heading",
        background="#f0f0f0",
        foreground="#000000",
        font=("Arial", 10, "bold"),
        relief="raised",
        borderwidth=1,
    )
    # Mapeamento de estados: mantém a mesma cor ao passar o mouse (active)
    style.map(
        "Treeview",
        background=[("selected", "#b3d4ff"), ("active", "#f8fbff")],
        foreground=[("selected", "#000000"), ("active", "#000000")],
    )

    tabela_itens.heading("produto", text="Produto")
    tabela_itens.heading("qtd", text="Qtd")

    tabela_itens.column("produto", width=400)
    tabela_itens.column("qtd", width=80)

    # tags para linhas alternadas: branca / cinza claro
    tabela_itens.tag_configure("even", background="#ffffff")
    tabela_itens.tag_configure("odd", background="#f2f2f2")

    tabela_itens.place(x=0, y=0, width=480, height=100)

    scroll_itens = ttk.Scrollbar(itens_frame, orient="vertical", command=tabela_itens.yview)
    scroll_itens.place(x=480, y=0, height=100)
    tabela_itens.configure(yscrollcommand=scroll_itens.set)

    # ================== CARREGAR DETALHES ==================
    def carregar_detalhes(event=None):
        sel = tabela.selection()
        if not sel:
            return
        orcamento_id = tabela.item(sel[0])["values"][0]

        conn = get_connection()
        if not conn:
            return
        cur = conn.cursor(dictionary=True)
        try:
            cur.execute("SELECT observacao FROM orcamento WHERE id=%s", (orcamento_id,))
            res = cur.fetchone()
            obs.delete("1.0", "end")
            obs.insert("1.0", res["observacao"] if res and res["observacao"] else "")

            cur.execute(
                "SELECT produto_nome, quantidade FROM orcamento_itens WHERE orcamento_id=%s", (orcamento_id,)
            )
            tabela_itens.delete(*tabela_itens.get_children())
            itens = []
            for idx, row in enumerate(cur.fetchall()):
                tag = "evenrow" if idx % 2 == 0 else "oddrow"
                tabela_itens.insert("", "end", values=(row["produto_nome"], row["quantidade"]), tags=(tag,))
                itens.append({
                    "produto_nome": row["produto_nome"],
                    "quantidade": row["quantidade"],
                    "valor_unitario": 0,
                    "valor_total": 0
                })

            # Prepara dict do orçamento completo
            master._orcamento_selecionado = {
                "id": orcamento_id,
                "cliente_id": None,
                "itens": itens,
            }

        except mysql.connector.Error as e:
            messagebox.showerror("MySQL", f"Erro ao carregar detalhes:\n{e}")
        finally:
            cur.close()
            conn.close()

    tabela.bind("<<TreeviewSelect>>", carregar_detalhes)

    # ================== BOTÕES ==================
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

    def ok():
        if callback and hasattr(master, "_orcamento_selecionado"):
            callback(master._orcamento_selecionado)
        if not embed:
            master.destroy()

    pack_button("Ok", ok, "#1f80ff", 474)

    def sair():
        # Limpa todos os widgets do frame e volta para cad_orcamento
        for w in master.winfo_children():
            try:
                w.destroy()
            except:
                pass
        
        # Importa e chama novamente a tela de cadastro de orçamento
        from cad_orcamento import cadastro_orcamento
        cadastro_orcamento(master)

    pack_button("Voltar", sair, "#e53935", 618, hover_color="#cc0000")

    return master
