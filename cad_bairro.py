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

def cadastro_bairro(root, dados=None):
    # Limpa a tela
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
        text="Cadastro de Bairro",
        font=("Arial", 32, "bold"),
        text_color="#1976D2"
    ).place(relx=0.5, y=80, anchor="center")

    form_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
    form_frame.place(relx=0.5, rely=0.45, anchor="center")

    font_family = "Arial"
    font_size = 15

    entry_bairro = ctk.CTkEntry(
        form_frame,
        placeholder_text="Bairro",
        font=(font_family, font_size),
        height=28,
        width=350
    )
    entry_bairro.grid(row=0, column=0, pady=6, sticky="ew", columnspan=2)

    combo_cidade = ttk.Combobox(
        form_frame,
        font=(font_family, font_size),
        width=28,
        state="readonly"
    )
    combo_cidade.grid(row=1, column=0, pady=6, sticky="ew", columnspan=2)
    combo_cidade.set("Cidade")

    combo_estado = ttk.Combobox(
        form_frame,
        font=(font_family, font_size),
        width=28,
        state="readonly"
    )
    combo_estado.grid(row=2, column=0, pady=6, sticky="ew", columnspan=2)
    combo_estado.set("Estado")

    def limpa_cidade_placeholder(event=None):
        if combo_cidade.get() == "Cidade":
            combo_cidade.set("")

    def limpa_estado_placeholder(event=None):
        if combo_estado.get() == "Estado":
            combo_estado.set("")

    combo_cidade.bind("<Button-1>", limpa_cidade_placeholder)
    combo_cidade.bind("<<ComboboxSelected>>", limpa_cidade_placeholder)
    combo_estado.bind("<Button-1>", limpa_estado_placeholder)
    combo_estado.bind("<<ComboboxSelected>>", limpa_estado_placeholder)

    def carregar_cidades():
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT nome FROM cidade ORDER BY nome")
            cidades = [row[0] for row in cursor.fetchall()]
            combo_cidade['values'] = cidades
            if cidades:
                combo_cidade.set(cidades[0])
            else:
                combo_cidade.set("Cidade")
            cursor.close()
            conn.close()
        except Exception as e:
            messagebox.showerror("Erro ao carregar cidades", str(e))

    def carregar_estados():
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT nome, sigla FROM estado ORDER BY nome")
            estados = [row[0] for row in cursor.fetchall()]
            combo_estado['values'] = estados
            cursor.close()
            conn.close()
        except Exception as e:
            messagebox.showerror("Erro ao carregar estados", str(e))

    carregar_cidades()
    carregar_estados()

    def limpar():
        entry_bairro.delete(0, tk.END)
        combo_cidade.set("Cidade")
        combo_estado.set("Estado")

    def gravar_bairro():
        bairro = entry_bairro.get()
        cidade = combo_cidade.get()
        estado = combo_estado.get()
        if not bairro or not cidade or not estado or cidade == "Cidade" or estado == "Estado":
            messagebox.showwarning("Validação", "Preencha todos os campos para cadastrar!")
            return
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT c.id FROM cidade c INNER JOIN estado e ON c.id_estado = e.id WHERE c.cidade=%s AND e.estado=%s",
                (cidade, estado)
            )
            resultado = cursor.fetchone()
            if not resultado:
                messagebox.showerror("Cadastro", "Cidade/Estado não encontrados no banco.")
                cursor.close()
                conn.close()
                return
            id_cidade = resultado[0]
            if dados and "id" in dados:
                cursor.execute("UPDATE bairro SET bairro=%s, id_cidade=%s WHERE id=%s", (bairro, id_cidade, dados["id"]))
            else:
                cursor.execute("INSERT INTO bairro (bairro, id_cidade) VALUES (%s,%s)", (bairro, id_cidade))
            conn.commit()
            cursor.close()
            conn.close()
            limpar()
            messagebox.showinfo("Sucesso", "Bairro cadastrado com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro ao gravar", str(e))

    def abrir_consulta():
        for w in root.winfo_children():
            w.destroy()
        procurar_bairro(root)

    def sair_local():
        for w in root.winfo_children():
            try:
                w.destroy()
            except:
                pass
        try:
            from portal import mostrar_marca_dagua_grande
            mostrar_marca_dagua_grande(root)
        except Exception:
            try:
                import portal
                portal.mostrar_marca_dagua_grande(root)
            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível retornar ao portal:\n{e}")

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

    # Exemplo de uso:
    pack_button("Gravar", gravar_bairro, "#1976D2", x_inicial + 7, ypos=340)
    pack_button("Procurar", abrir_consulta, "#1976D2", x_inicial + espaco + 7, ypos=340)
    pack_button("Limpar", limpar, "#1976D2", x_inicial + espaco * 2 + 7, ypos=340)
    pack_button("Sair", sair_local, "#E53935", x_inicial + espaco * 3 + 7, ypos=340, hover_color="#cc0000")

    # Se vier dados para edição, preenche os campos
    if dados:
        entry_bairro.insert(0, dados.get("bairro", ""))
        # Buscar cidade e estado pelo id_cidade
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT c.cidade, e.estado FROM cidade c INNER JOIN estado e ON c.id_estado = e.id WHERE c.id = %s",
                (dados.get("id_cidade"),)
            )
            row = cursor.fetchone()
            if row:
                combo_cidade.set(row[0])
                combo_estado.set(row[1])
            cursor.close()
            conn.close()
        except Exception:
            pass

def procurar_bairro(root):
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
        text="Procurar Bairro",
        font=("Arial", 28, "bold"),
        text_color="#1976D2"
    ).place(relx=0.5, y=40, anchor="center")

    frame_grid = ctk.CTkFrame(main_frame, fg_color="transparent")
    frame_grid.place(relx=0.5, rely=0.45, anchor="center", relwidth=0.9, relheight=0.6)

    style = ttk.Style()
    style.configure("Custom.Treeview.Heading", font=("Arial", 15, "bold"), background="#1976D2", foreground="#FFF")
    style.configure("Custom.Treeview", background="#eaf6ff", fieldbackground="#eaf6ff", font=("Arial", 14))
    style.map("Custom.Treeview", background=[("selected", "#90CAF9")])
    style.layout("Custom.Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])

    # Striped rows
    style.map("Treeview", background=[('selected', "#63AEEB")])
    style.configure("Treeview", rowheight=28)
    style.configure("Treeview", background="#ffffff", fieldbackground="#ffffff")
    style.configure("Treeview", font=("Arial", 14))

    grid_bairros = ttk.Treeview(
        frame_grid,
        columns=("bairro", "cidade", "estado"),
        show="headings",
        style="Custom.Treeview"
    )
    grid_bairros.heading("bairro", text="Bairro")
    grid_bairros.heading("cidade", text="Cidade")
    grid_bairros.heading("estado", text="Estado")
    grid_bairros.column("bairro", width=220, anchor="center")
    grid_bairros.column("cidade", width=220, anchor="center")
    grid_bairros.column("estado", width=180, anchor="center")
    grid_bairros.pack(fill="both", expand=True)

    # Carregar bairros
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, bairro, cidade, estado
            FROM bairro
            ORDER BY bairro
        """)
        for i, (id_bairro, bairro, cidade, estado) in enumerate(cursor.fetchall()):
            tag = "evenrow" if i % 2 == 0 else "oddrow"
            grid_bairros.insert("", "end", iid=str(id_bairro), values=(bairro, cidade, estado), tags=(tag,))
        grid_bairros.tag_configure("evenrow", background="#eaf6ff")
        grid_bairros.tag_configure("oddrow", background="#e3f2fd")
        cursor.close()
        conn.close()
    except Exception as e:
        messagebox.showerror("Erro ao carregar bairros", str(e))

    def on_select(event):
        selected = grid_bairros.selection()
        if selected:
            id_bairro = selected[0]
            try:
                conn = conectar()
                cursor = conn.cursor(dictionary=True)
                cursor.execute("SELECT * FROM bairro WHERE id = %s", (id_bairro,))
                dados = cursor.fetchone()
                cursor.close()
                conn.close()
                cadastro_bairro(root, dados)
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao buscar bairro: {e}")

    grid_bairros.bind("<<TreeviewSelect>>", on_select)

    # Botão Sair
    ctk.CTkButton(
        main_frame,
        text="Voltar",
        width=110,
        fg_color="#E53935",
        hover_color="#cc0000",
        font=("Arial", 15, "bold"),
        command=lambda: cadastro_bairro(root)
    ).place(relx=0.9, y=360, anchor="center")

# Exemplo de uso:
if __name__ == "__main__":
    root = ctk.CTk()
    root.title("Cadastro de Bairro")
    root.after(10, lambda: root.state("zoomed"))
    root.configure(fg_color="#e3f2fd")
    cadastro_bairro(root)
    root.mainloop()

def capitalize_first_letter(event):
    widget = event.widget
    value = widget.get()
    if value:
        # Só altera se a primeira letra não for maiúscula
        new_value = value[0].upper() + value[1:]
        if value != new_value:
            widget.delete(0, tk.END)
            widget.insert(0, new_value)

