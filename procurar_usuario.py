import customtkinter as ctk
from tkinter import ttk
from conexao import conectar  # supondo que você tenha esse arquivo com a função conectar()


def abrir_tela_procurar(master, entry_nome, entry_login, entry_senha, combo_perfil, voltar_callback):
    """Abre a tela de procurar usuário"""

    frame_busca = ctk.CTkFrame(master)
    frame_busca.pack(expand=True, fill="both", padx=20, pady=20)

    lbl = ctk.CTkLabel(frame_busca, text="Buscar Usuário", font=("Arial", 24, "bold"))
    lbl.pack(pady=10)

    entry_busca = ctk.CTkEntry(frame_busca, placeholder_text="Digite o nome", width=320)
    entry_busca.pack(pady=10)

    # Frame para Treeview + Scrollbar
    frame_tree = ctk.CTkFrame(frame_busca)
    frame_tree.pack(expand=True, fill="both", pady=10)

    tree = ttk.Treeview(frame_tree, columns=("login", "perfil"), show="headings", height=10)
    tree.heading("login", text="Login")
    tree.heading("perfil", text="Perfil")

    # Ajustando largura e alinhamento das colunas
    tree.column("login", width=150, anchor="center")
    tree.column("perfil", width=120, anchor="center")

    tree.pack(side="left", fill="both", expand=True)

    # Scrollbar vertical
    scrollbar = ttk.Scrollbar(frame_tree, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    def executar_busca():
        # Limpa resultados anteriores
        for i in tree.get_children():
            tree.delete(i)

        con = conectar()
        try:
            cur = con.cursor()
            cur.execute(
                "SELECT nome, login, perfil, senha FROM usuario WHERE nome LIKE %s",
                (f"%{entry_busca.get()}%",)
            )
            for nome, login, perfil, senha in cur.fetchall():
                tree.insert("", "end", values=(login, perfil), tags=(nome, senha))
        finally:
            con.close()

    def selecionar_usuario(event):
        item = tree.selection()
        if not item:
            return

        login = tree.item(item, "values")[0]
        perfil = tree.item(item, "values")[1]
        nome = tree.item(item, "tags")[0]
        senha = tree.item(item, "tags")[1]

        # Preenche formulário
        entry_nome.delete(0, "end")
        entry_nome.insert(0, nome)
        entry_login.delete(0, "end")
        entry_login.insert(0, login)
        entry_senha.delete(0, "end")
        entry_senha.insert(0, senha)
        combo_perfil.set(perfil)

        # Fecha tela de busca e volta para tela de cadastro
        frame_busca.destroy()
        voltar_callback()

    tree.bind("<<TreeviewSelect>>", selecionar_usuario)

    btn_buscar = ctk.CTkButton(
        frame_busca,
        text="Procurar",
        command=executar_busca,
        fg_color="#2e8bff",
        hover_color="#1c5fb8"
    )
    btn_buscar.pack(pady=10)
