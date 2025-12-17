import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

def conectar():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="MAJu2022@",
        database="erp_sistema"
    )

def cadastro_clm(root, dados=None):
    for widget in root.winfo_children():
        widget.destroy()

    root.configure(fg_color="#e1f1fd")

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
        text="Cadastro de CLM",
        font=("Arial", 28, "bold"),
        text_color="#1976D2"
    ).place(relx=0.5, y=40, anchor="center")

    form_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
    form_frame.place(relx=0.5, rely=0.45, anchor="center")

    entry_descricao = ctk.CTkEntry(
        form_frame,
        placeholder_text="Descrição",
        font=("Arial", 15),
        height=28,
        width=350
    )
    entry_descricao.grid(row=0, column=0, pady=8)

    clm_id = None
    if dados:
        clm_id = dados.get("id")
        entry_descricao.insert(0, dados["descricao"])

    def gravar():
        nonlocal clm_id
        descricao = entry_descricao.get().strip()
        if not descricao:
            messagebox.showwarning("Aviso", "Preencha a descrição!")
            return
        con = None
        try:
            con = conectar()
            cur = con.cursor()
            if clm_id:
                cur.execute("UPDATE clm SET descricao=%s WHERE id=%s", (descricao, clm_id))
                messagebox.showinfo("Atualizado", "CLM atualizado com sucesso!")
            else:
                cur.execute("SELECT id FROM clm WHERE descricao=%s", (descricao,))
                if cur.fetchone():
                    messagebox.showwarning("Aviso", "Esta descrição já existe!")
                    return
                cur.execute("INSERT INTO clm (descricao) VALUES (%s)", (descricao,))
                messagebox.showinfo("Sucesso", "CLM cadastrado com sucesso!")
            con.commit()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gravar CLM:\n{e}")
        finally:
            if con: con.close()

    def procurar():
        for widget in root.winfo_children():
            widget.destroy()
        procurar_clm(root)

    def limpar():
        nonlocal clm_id
        clm_id = None
        entry_descricao.delete(0, "end")

    def sair():
        for widget in root.winfo_children():
            widget.destroy()

    x_inicial = 120
    espaco = 110 + 30

    def pack_button(text, cmd, color, xpos, ypos=340, hover_color="#0b60c9", width=None, height=None):
        btn = ctk.CTkButton(
            main_frame,
            text=text,
            width=width if width is not None else 110,
            height=height if height is not None else 28,
            fg_color=color,
            hover_color=hover_color,
            font=("Arial", 15, "bold"),
            command=cmd,
        )
        btn.place(x=xpos, y=ypos)

    pack_button("Gravar", gravar, "#1976D2", x_inicial + 7, ypos=340)
    pack_button("Procurar", procurar, "#1976D2", x_inicial + espaco + 7, ypos=340)
    pack_button("Limpar", limpar, "#1976D2", x_inicial + espaco * 2 + 7, ypos=340)
    pack_button("Sair", sair, "#E53935", x_inicial + espaco * 3 + 7, ypos=340, hover_color="#cc0000")

    def capitalize_first_letter(event):
        widget = event.widget
        value = widget.get()
        if value:
            new_value = value[0].upper() + value[1:]
            if value != new_value:
                widget.delete(0, tk.END)
                widget.insert(0, new_value)

    entry_descricao.bind("<KeyRelease>", capitalize_first_letter)

def procurar_clm(root):
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
        text="Buscar CLM",
        font=("Arial", 28, "bold"),
        text_color="#1976D2"
    ).place(relx=0.5, y=40, anchor="center")

    frame_grid = ctk.CTkFrame(main_frame, fg_color="transparent")
    frame_grid.place(relx=0.5, rely=0.45, anchor="center", relwidth=0.9, relheight=0.6)

    style = ttk.Style()
    style.theme_use("default")
    style.configure("Treeview", font=("Arial", 14), rowheight=28)
    style.configure("Treeview.Heading", font=("Arial", 15, "bold"))
    style.configure("Treeview", background="#eaf6ff", fieldbackground="#eaf6ff")
    style.map("Treeview", background=[('selected', '#90CAF9')])

    tree = ttk.Treeview(
        frame_grid,
        columns=("id", "descricao"),
        show="headings",
        height=10
    )
    tree.heading("id", text="ID")
    tree.heading("descricao", text="Descrição")
    tree.column("id", width=60, anchor="center")
    tree.column("descricao", width=400)
    tree.pack(fill="both", expand=True)

    tree.tag_configure("oddrow", background="#e3f2fd")
    tree.tag_configure("evenrow", background="#eaf6ff")

    def executar_busca():
        for i in tree.get_children():
            tree.delete(i)
        con = None
        try:
            con = conectar()
            cur = con.cursor()
            cur.execute("SELECT id, descricao FROM clm ORDER BY descricao")
            registros = cur.fetchall()
            for idx, (id_, descricao) in enumerate(registros):
                tag = "evenrow" if idx % 2 == 0 else "oddrow"
                tree.insert("", "end", values=(id_, descricao), tags=(tag,))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao buscar CLMs:\n{e}")
        finally:
            if con: con.close()

    def abrir_clm_por_click(event):
        item = tree.identify_row(event.y)
        if not item:
            return
        vals = tree.item(item, "values")
        dados = {"id": vals[0], "descricao": vals[1]}
        cadastro_clm(root, dados)

    tree.bind("<Double-1>", abrir_clm_por_click)
    tree.bind("<ButtonRelease-1>", abrir_clm_por_click)
    executar_busca()

    ctk.CTkButton(
        main_frame,
        text="Voltar",
        width=120,
        fg_color="#E53935",
        hover_color="#cc0000",
        font=("Arial", 15, "bold"),
        command=lambda: cadastro_clm(root)
    ).place(relx=0.9, y=360, anchor="center")

# Exemplo de uso:
if __name__ == "__main__":
    root = ctk.CTk()
    root.title("Cadastro de CLM")
    root.after(10, lambda: root.state("zoomed"))
    root.configure(fg_color="#e3f2fd")
    cadastro_clm(root)
    root.mainloop()
