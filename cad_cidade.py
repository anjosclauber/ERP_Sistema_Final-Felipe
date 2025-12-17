import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
import os
from PIL import Image

def conectar():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="MAJu2022@",
        database="erp_sistema"
    )

def cadastro_cidade(root, dados=None):
    def limpa_uf_placeholder(event=None):
        if combo_uf.get() == "UF":
            combo_uf.set("")

    for widget in root.winfo_children():
        widget.destroy()

    root.configure(fg_color="#eaf6fd")

    main_frame = ctk.CTkFrame(
        root,
        fg_color="#eaf6ff",
        border_color="#1976d2",
        border_width=2,
        width=800,
        height=450,
    )
    main_frame.place(relx=0.5, rely=0.5, anchor="center")

    ctk.CTkLabel(
        main_frame,
        text="Cadastro de Cidade",
        font=("Arial", 32, "bold"),
        text_color="#1976d2"
    ).place(relx=0.5, y=90, anchor="center")

    # Frame do formulário centralizado (sem imagem)
    frame_form = ctk.CTkFrame(main_frame, fg_color="transparent")
    frame_form.place(relx=0.5, rely=0.45, anchor="center")

    entry_nome = ctk.CTkEntry(frame_form, placeholder_text="Nome da Cidade", width=350, height=28)
    entry_nome.grid(row=0, column=0, pady=(0, 20))

    # Buscar estados e siglas do banco de dados
    estados = []
    try:
        con = conectar()
        cur = con.cursor()
        cur.execute("SELECT nome, sigla FROM estado ORDER BY nome")
        estados = [f"{row[0]} | {row[1]}" for row in cur.fetchall()]
        cur.close()
        con.close()
    except Exception as e:
        print("Erro ao buscar estados UF:", e)
        estados = []
    combo_uf = ttk.Combobox(
        frame_form,
        font=("Arial", 13),
        width=28,
        state="readonly"
    )
    combo_uf.grid(row=1, column=0, pady=(0, 20), sticky="ew")
    combo_uf['values'] = estados
    combo_uf.set("UF")
    combo_uf.bind("<Button-1>", limpa_uf_placeholder)
    combo_uf.bind("<<ComboboxSelected>>", limpa_uf_placeholder)
    # Deixa o texto do placeholder UF igual ao do entry_nome (fonte e cor)
    try:
        combo_uf.configure(foreground="#a9a9a9")
    except Exception:
        pass

    cidade_id = None
    if dados:
        cidade_id = dados.get("id")
        # Compatível com dicionário vindo de SELECT id, cidade, uf
        entry_nome.insert(0, dados.get("cidade", dados.get("nome", "")))
        # Buscar a sigla do estado pelo id_estado
        try:
            con = conectar()
            cur = con.cursor()
            cur.execute("""
                SELECT RIGHT(e.nome, 2) as uf
                FROM cidade c
                INNER JOIN estado e ON c.id_estado = e.id
                WHERE c.id = %s
            """, (cidade_id,))
            row = cur.fetchone()
            if row:
                combo_uf.set(row[0])
            cur.close()
            con.close()
        except Exception:
            combo_uf.set("UF")

    def gravar():
        nonlocal cidade_id
        nome = entry_nome.get().strip()
        uf = combo_uf.get()
        if not nome or uf == "UF":
            messagebox.showwarning("Aviso", "Preencha o nome da cidade e selecione o estado!")
            return
        con = None
        try:
            con = conectar()
            cur = con.cursor()
            # Busca o id do estado pela sigla
            cur.execute("SELECT id FROM estado WHERE nome LIKE %s OR nome LIKE %s", (f"%{uf}", f"%| {uf}"))
            estado_row = cur.fetchone()
            if not estado_row:
                messagebox.showerror("Erro", "Estado não encontrado!")
                return
            id_estado = estado_row[0]
            if cidade_id:
                cur.execute("UPDATE cidade SET cidade=%s, id_estado=%s WHERE id=%s", (nome, id_estado, cidade_id))
                messagebox.showinfo("Atualizado", "Cidade atualizada com sucesso!")
            else:
                cur.execute("SELECT id FROM cidade WHERE cidade=%s AND id_estado=%s", (nome, id_estado))
                if cur.fetchone():
                    messagebox.showwarning("Aviso", "Esta cidade já está cadastrada nesse estado!")
                    return
                cur.execute("INSERT INTO cidade (cidade, id_estado) VALUES (%s, %s)", (nome, id_estado))
                messagebox.showinfo("Sucesso", "Cidade cadastrada com sucesso!")
            con.commit()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gravar cidade:\n{e}")
        finally:
            if con: con.close()

    def procurar():
        abrir_tela_procurar_cidade(root)

    def limpar():
        nonlocal cidade_id
        cidade_id = None
        entry_nome.delete(0, "end")
        combo_uf.set("UF")

    def sair():
        for widget in root.winfo_children():
            widget.destroy()

    # Botões centralizados na parte inferior
    x_inicial = 120
    espaco = 120 + 30

    def pack_button(text, cmd, color, xpos, ypos=340, hover_color="#0b60c9", width=None, height=None):
        btn_kwargs = {
            "text": text,
            "fg_color": color,
            "hover_color": hover_color,
            "font": ("Arial", 15, "bold"),
            "command": cmd,
            "master": main_frame,
        }
        if width is not None:
            btn_kwargs["width"] = width
        if height is not None:
            btn_kwargs["height"] = height
        btn = ctk.CTkButton(**btn_kwargs)
        btn.place(x=xpos, y=ypos)

    # Exemplo: ajuste os tamanhos dos botões aqui
    button_width = 120  # Altere conforme desejado
    button_height = 30  # Altere conforme desejado

    pack_button("Gravar", gravar, "#2e8bff", x_inicial + 7, ypos=340, width=button_width, height=button_height)
    pack_button("Procurar", procurar, "#2e8bff", x_inicial + espaco + 7, ypos=340, width=button_width, height=button_height)
    pack_button("Limpar", limpar, "#2e8bff", x_inicial + espaco * 2 + 7, ypos=340, width=button_width, height=button_height)
    pack_button("Sair", sair, "red", x_inicial + espaco * 3 + 7, ypos=340, hover_color="#cc0000", width=button_width, height=button_height)

    def capitalize_first_letter(event):
        widget = event.widget
        value = widget.get()
        if value:
            # Só altera se a primeira letra não for maiúscula
            new_value = value[0].upper() + value[1:]
            if value != new_value:
                widget.delete(0, tk.END)
                widget.insert(0, new_value)

    entry_nome.bind("<FocusOut>", capitalize_first_letter)
    combo_uf.bind("<FocusOut>", capitalize_first_letter)

def abrir_tela_procurar_cidade(root):
    for widget in root.winfo_children():
        widget.destroy()
    root.configure(fg_color="#eaf6ff")

    main_frame = ctk.CTkFrame(
        root,
        fg_color="#eaf6ff",
        border_color="#1976d2",
        border_width=2,
        width=800,
        height=400,
    )
    main_frame.place(relx=0.5, rely=0.5, anchor="center")

    ctk.CTkLabel(
        main_frame,
        text="Buscar Cidade",
        font=("Arial", 28, "bold"),
        text_color="#1976D2"
    ).place(relx=0.5, y=40, anchor="center")

    frame_grid = ctk.CTkFrame(main_frame, fg_color="transparent")
    frame_grid.place(relx=0.5, rely=0.45, anchor="center", relwidth=0.9, relheight=0.6)

    style = ttk.Style()
    style.theme_use("default")
    style.configure("Treeview", font=("Arial", 14), rowheight=28)
    style.configure("Treeview.Heading", font=("Arial", 15, "bold"))
    style.configure("Treeview", background="#ffffff", fieldbackground="#ffffff")
    style.map("Treeview", background=[('selected', '#90CAF9')])

    tree = ttk.Treeview(
        frame_grid,
        columns=("id", "nome", "uf"),
        show="headings",
        height=10
    )
    tree.heading("id", text="ID")
    tree.heading("nome", text="Nome")
    tree.heading("uf", text="UF")
    tree.column("id", width=60, anchor="center")
    tree.column("nome", width=220)
    tree.column("uf", width=60, anchor="center")
    tree.pack(fill="both", expand=True)

    tree.tag_configure("oddrow", background="#ffffff")  # branco
    tree.tag_configure("evenrow", background="#eaf6ff")  # azul claro

    def executar_busca():
        for i in tree.get_children():
            tree.delete(i)
        con = None
        try:
            con = conectar()
            cur = con.cursor()
            cur.execute("SELECT id, cidade, uf FROM cidade ORDER BY cidade")
            registros = cur.fetchall()
            for idx, (id_, cidade, uf) in enumerate(registros):
                tag = "evenrow" if idx % 2 == 0 else "oddrow"
                tree.insert("", "end", values=(id_, cidade, uf), tags=(tag,))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao buscar cidades:\n{e}")
        finally:
            if con: con.close()

    def abrir_cidade_por_click(event):
        item = tree.identify_row(event.y)
        if not item:
            return
        vals = tree.item(item, "values")
        cidade_id = vals[0]
        # Buscar dados completos da cidade pelo id
        try:
            con = conectar()
            cur = con.cursor()
            cur.execute("SELECT id, cidade, uf FROM cidade WHERE id = %s", (cidade_id,))
            row = cur.fetchone()
            if row:
                dados = {"id": row[0], "nome": row[1], "uf": row[2]}
                cadastro_cidade(root, dados)
            cur.close()
            con.close()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao buscar cidade selecionada:\n{e}")

    tree.bind("<Double-1>", abrir_cidade_por_click)
    tree.bind("<ButtonRelease-1>", abrir_cidade_por_click)
    executar_busca()

    # Botão Voltar
    ctk.CTkButton(
        main_frame,
        text="Voltar",
        width=120,
        fg_color="#E53935",
        hover_color="#cc0000",
        font=("Arial", 15, "bold"),
        command=lambda: cadastro_cidade(root)
    ).place(relx=0.9, y=360, anchor="center")

# Exemplo de uso:
if __name__ == "__main__":
    root = ctk.CTk()
    root.title("Cadastro de Cidade")
    root.after(10, lambda: root.state("zoomed"))
    root.configure(fg_color="#e3f2fd")
    cadastro_cidade(root)
    root.mainloop()
