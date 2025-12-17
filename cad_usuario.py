import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from PIL import Image
import os


def conectar():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="",
        database="erp_sistema"
    )


def cadastro_usuario(root, dados=None):
    for widget in root.winfo_children():
        widget.destroy()

    root.configure(fg_color="#e1f1fd")


    main_frame = ctk.CTkFrame(
        root,
        fg_color="#eaf6ff",
        border_color="#1976d2",
        border_width=2,  # Borda mais grossa para mais destaque
        width=1200,
        height=800,
    )
    main_frame.place(relx=0.5, rely=0.5, anchor="center")

    ctk.CTkLabel(
        main_frame,
        text="Cadastro de Usuário",
        font=("Arial", 28, "bold"),
        text_color="#1976D2"
    ).place(relx=0.5, y=70, anchor="center")

    form_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
    form_frame.place(relx=0.5, rely=0.45, anchor="center")

    font_family = "Arial"
    font_size = 15


    # Nome
    ctk.CTkLabel(
        form_frame,
        text="Nome",
        font=(font_family, 16, "bold"),
        text_color="#1976D2"
    ).grid(row=0, column=0, sticky="w", pady=(0, 0), columnspan=2)
    entry_nome = ctk.CTkEntry(
        form_frame,
        font=(font_family, font_size),
        height=28,
        width=350
    )
    entry_nome.grid(row=1, column=0, pady=(0, 6), sticky="ew", columnspan=2)

    # Login
    ctk.CTkLabel(
        form_frame,
        text="Login",
        font=(font_family, 16, "bold"),
        text_color="#1976D2"
    ).grid(row=2, column=0, sticky="w", pady=(0, 0), columnspan=2)
    entry_login = ctk.CTkEntry(
        form_frame,
        font=(font_family, font_size),
        height=28,
        width=350
    )
    entry_login.grid(row=3, column=0, pady=(0, 6), sticky="ew", columnspan=2)

    # Senha
    ctk.CTkLabel(
        form_frame,
        text="Senha",
        font=(font_family, 16, "bold"),
        text_color="#1976D2"
    ).grid(row=4, column=0, sticky="w", pady=(0, 0), columnspan=2)
    entry_senha = ctk.CTkEntry(
        form_frame,
        font=(font_family, font_size),
        height=28,
        width=350,
        show="*"
    )
    entry_senha.grid(row=5, column=0, pady=(0, 6), sticky="ew", columnspan=2)

    # Email
    ctk.CTkLabel(
        form_frame,
        text="Email",
        font=(font_family, 16, "bold"),
        text_color="#1976D2"
    ).grid(row=6, column=0, sticky="w", pady=(0, 0), columnspan=2)
    entry_email = ctk.CTkEntry(
        form_frame,
        font=(font_family, font_size),
        height=28,
        width=350
    )
    entry_email.grid(row=7, column=0, pady=(0, 6), sticky="ew", columnspan=2)

    # Perfil
    ctk.CTkLabel(
        form_frame,
        text="Perfil",
        font=(font_family, 16, "bold"),
        text_color="#1976D2"
    ).grid(row=8, column=0, sticky="w", pady=(0, 0), columnspan=2)
    combo_perfil = ttk.Combobox(
        form_frame,
        font=(font_family, font_size),
        width=28,
        state="readonly",
        values=["Master", "Administrador", "Usuário"]
    )
    combo_perfil.grid(row=9, column=0, pady=(0, 6), sticky="ew", columnspan=2)
    combo_perfil.set("Perfil")

    usuario_id = None
    if dados:
        usuario_id = dados.get("id")
        entry_nome.delete(0, tk.END)
        entry_nome.insert(0, dados.get("nome", ""))
        entry_login.delete(0, tk.END)
        entry_login.insert(0, dados.get("login", ""))
        entry_senha.delete(0, tk.END)
        entry_senha.insert(0, dados.get("senha", ""))
        entry_email.delete(0, tk.END)
        entry_email.insert(0, dados.get("email", ""))
        combo_perfil.set(dados.get("perfil", "Perfil"))

    def limpar():
        nonlocal usuario_id
        usuario_id = None
        entry_nome.delete(0, tk.END)
        entry_login.delete(0, tk.END)
        entry_senha.delete(0, tk.END)
        entry_email.delete(0, tk.END)
        combo_perfil.set("Perfil")

    def gravar_usuario():
        nonlocal usuario_id
        nome = entry_nome.get().strip()
        login = entry_login.get().strip()
        senha = entry_senha.get().strip()
        email = entry_email.get().strip()
        perfil = combo_perfil.get()
        if not nome or not login or not senha or perfil == "Perfil":
            messagebox.showwarning("Validação", "Preencha todos os campos obrigatórios!")
            return
        try:
            conn = conectar()
            cursor = conn.cursor()
            if usuario_id:
                cursor.execute(
                    "UPDATE usuario SET nome=%s, login=%s, senha=%s, email=%s, perfil=%s WHERE id=%s",
                    (nome, login, senha, email, perfil, usuario_id)
                )
            else:
                cursor.execute("SELECT id FROM usuario WHERE login=%s", (login,))
                if cursor.fetchone():
                    messagebox.showwarning("Aviso", "Este login já está cadastrado!")
                    cursor.close()
                    conn.close()
                    return
                cursor.execute(
                    "INSERT INTO usuario (nome, login, senha, email, perfil) VALUES (%s, %s, %s, %s, %s)",
                    (nome, login, senha, email, perfil)
                )
            conn.commit()
            cursor.close()
            conn.close()
            limpar()
            messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro ao gravar", str(e))

    def abrir_consulta():
        for w in root.winfo_children():
            w.destroy()
        procurar_usuario(root)

    def sair_local():
        for w in root.winfo_children():
            try:
                w.destroy()
            except:
                pass

    x_inicial = 170  # 120 + 30 para mover todos os botões para a direita
    espaco = 110 + 30

    def pack_button(text, cmd, color, xpos, ypos=470, hover_color="#0b60c9", width=None, height=None):
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

    pack_button("Gravar", gravar_usuario, "#1976D2", x_inicial + 7, ypos=470)
    pack_button("Procurar", abrir_consulta, "#1976D2", x_inicial + espaco + 7, ypos=470)
    pack_button("Limpar", limpar, "#1976D2", x_inicial + espaco * 2 + 7, ypos=470)
    pack_button("Sair", sair_local, "#E53935", x_inicial + espaco * 3 + 7, ypos=470, hover_color="#cc0000")

    def capitalize_first_letter(event):
        widget = event.widget
        value = widget.get()
        if value:
            new_value = value[0].upper() + value[1:]
            if value != new_value:
                widget.delete(0, tk.END)
                widget.insert(0, new_value)

    entry_nome.bind("<KeyRelease>", capitalize_first_letter)
    entry_login.bind("<KeyRelease>", capitalize_first_letter)
    entry_email.bind("<KeyRelease>", capitalize_first_letter)


def procurar_usuario(root):
    root.configure(fg_color="#eaf6ff")
    main_frame = ctk.CTkFrame(
        root,
        fg_color="#eaf6ff",
        border_color="#1976d2",
        border_width=2,
        width=1200,
        height=800,
    )
    main_frame.place(relx=0.5, rely=0.5, anchor="center")


    ctk.CTkLabel(
        main_frame,
        text="Procurar Usuário",
        font=("Arial", 28, "bold"),
        text_color="#1976D2"
    ).place(relx=0.5, y=70, anchor="center")



    # Campo de busca alinhado à esquerda com label
    search_var = tk.StringVar()
    label_search = ctk.CTkLabel(
        main_frame,
        text="Usuário",
        font=("Arial", 16, "bold"),
        text_color="#1976D2"
    )
    label_search.place(x=70, y=110)
    entry_search = ctk.CTkEntry(
        main_frame,
        textvariable=search_var,
        placeholder_text="Digite o Usuário",
        width=300,
        font=("Arial", 15)
    )
    entry_search.place(x=70, y=140)

    # Desce a tabela 40px, alinhada com campo de busca
    frame_grid = ctk.CTkFrame(main_frame, fg_color="transparent", border_color="#1976D2", border_width=1)
    frame_grid.place(x=70, y=190, relwidth=0.9, relheight=0.6)


    style = ttk.Style()
    # Cabeçalho branco, azul escuro
    style.configure("Custom.Treeview.Heading", font=("Arial", 15, "bold"), background="#174a8b", foreground="#FFF")
    # Fundo linhas azul claro, borda azul fina
    style.configure("Custom.Treeview", background="#e3f0fd", fieldbackground="#e3f0fd", font=("Arial", 14), bordercolor="#1976D2", borderwidth=1, relief="solid")
    style.map("Custom.Treeview", background=[("selected", "#90CAF9")])
    style.layout("Custom.Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])

    style.map("Treeview", background=[('selected', '#90CAF9')])
    style.configure("Treeview", rowheight=28)
    style.configure("Treeview", background="#e3f0fd", fieldbackground="#e3f0fd", font=("Arial", 14), bordercolor="#1976D2", borderwidth=1, relief="solid")

    grid_usuarios = ttk.Treeview(
        frame_grid,
        columns=("id", "nome", "login", "email", "perfil"),
        show="headings",
        style="Custom.Treeview"
    )
    grid_usuarios.heading("id", text="ID")
    grid_usuarios.heading("nome", text="Nome")
    grid_usuarios.heading("login", text="Login")
    grid_usuarios.heading("email", text="Email")
    grid_usuarios.heading("perfil", text="Perfil")
    grid_usuarios.column("id", width=60, anchor="w")
    grid_usuarios.column("nome", width=180, anchor="w")
    grid_usuarios.column("login", width=120, anchor="w")
    grid_usuarios.column("email", width=180, anchor="w")
    grid_usuarios.column("perfil", width=120, anchor="w")
    grid_usuarios.pack(fill="both", expand=True)

    grid_usuarios.tag_configure("evenrow", background="#e3f0fd")
    grid_usuarios.tag_configure("oddrow", background="#d0e2fa")


    # Carrega todos os usuários para busca dinâmica
    usuarios_lista = []
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome, login, email, perfil FROM usuario ORDER BY nome")
        usuarios_lista = cursor.fetchall()
        cursor.close()
        conn.close()
    except Exception as e:
        messagebox.showerror("Erro ao carregar usuários", str(e))

    def atualizar_tabela(filtro_nome=None):
        grid_usuarios.delete(*grid_usuarios.get_children())
        filtro = (filtro_nome or '').strip().lower()
        achou = False
        for i, (id_, nome, login, email, perfil) in enumerate(usuarios_lista):
            tag = "evenrow" if i % 2 == 0 else "oddrow"
            display_nome = nome
            if filtro and filtro in nome.lower():
                if not achou:
                    display_nome = f"→ {nome}"
                    achou = True
            grid_usuarios.insert("", "end", iid=str(id_), values=(id_, display_nome, login, email, perfil), tags=(tag,))
        # Seleciona e foca o primeiro encontrado
        if filtro:
            for iid in grid_usuarios.get_children():
                if grid_usuarios.item(iid)['values'][1].startswith('→'):
                    grid_usuarios.selection_set(iid)
                    grid_usuarios.see(iid)
                    break

    # Atualiza tabela ao digitar
    def on_search(*args):
        atualizar_tabela(search_var.get())
    search_var.trace_add('write', on_search)

    atualizar_tabela()

    def on_select(event):
        selected = grid_usuarios.selection()
        if selected:
            id_usuario = selected[0]
            try:
                conn = conectar()
                cursor = conn.cursor(dictionary=True)
                cursor.execute("SELECT * FROM usuario WHERE id = %s", (id_usuario,))
                dados = cursor.fetchone()
                cursor.close()
                conn.close()
                cadastro_usuario(root, dados)
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao buscar usuário: {e}")

    grid_usuarios.bind("<<TreeviewSelect>>", on_select)



    # Botão Ok: seleciona usuário marcado na tabela
    def on_ok():
        selected = grid_usuarios.selection()
        if selected:
            id_usuario = selected[0]
            try:
                conn = conectar()
                cursor = conn.cursor(dictionary=True)
                cursor.execute("SELECT * FROM usuario WHERE id = %s", (id_usuario,))
                dados = cursor.fetchone()
                cursor.close()
                conn.close()
                messagebox.showinfo("Usuário Selecionado", f"ID: {dados['id']}\nNome: {dados['nome']}")
                # Aqui você pode chamar outra função ou fechar a tela, conforme desejado
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao buscar usuário: {e}")
        else:
            messagebox.showwarning("Seleção", "Selecione um usuário na tabela.")

    btn_ok = ctk.CTkButton(
        main_frame,
        text="Ok",
        width=110,
        fg_color="#1976D2",
        hover_color="#0b60c9",
        font=("Arial", 15, "bold"),
        command=on_ok
    )
    btn_ok.place(x=70, y=main_frame.winfo_height()-70)

    btn_voltar = ctk.CTkButton(
        main_frame,
        text="Voltar",
        width=110,
        fg_color="#E53935",
        hover_color="#cc0000",
        font=("Arial", 15, "bold"),
        command=lambda: cadastro_usuario(root)
    )
    btn_voltar.place(x=70+110+30, y=main_frame.winfo_height()-70)


# Exemplo de uso:
if __name__ == "__main__":
    root = ctk.CTk()
    root.title("Cadastro de Usuário")
    root.after(10, lambda: root.state("zoomed"))
    root.configure(fg_color="#e3f2fd")
    cadastro_usuario(root)
    root.mainloop()