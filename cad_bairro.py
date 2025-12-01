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

def cadastro_cliente(frame_conteudo, dados=None, on_show_small_logo=None, on_show_big_logo=None):
    for widget in frame_conteudo.winfo_children():
        widget.destroy()

    frame_conteudo.grid_propagate(False)
    frame_conteudo.configure(fg_color="#d9d9d9")
    
    #-------------------------------------------
class cadastro_bairro(ctk.CTkFrame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.place(relx=0.5, rely=0.52, anchor="center", relwidth=0.82, relheight=0.80)
        self.configure(fg_color="#e3f2fd")

        # Variáveis para fonte/personalização
        self.font_family = "Arial"
        self.font_size = 15
        self.font_color = "#000000"

        # Frame central para organizar o formulário
        frame_central = ctk.CTkFrame(self, fg_color="transparent")
        frame_central.place(relx=0.5, rely=0.5, anchor="center")

        # Título
        self.lbl_titulo = ctk.CTkLabel(
            frame_central,
            text="Cadastro de Bairro",
            font=("Arial", 28, "bold"),
            text_color="#1976D2"
        )
        self.lbl_titulo.grid(row=0, column=0, pady=(0, 20))

        # Frame do formulário
        self.frame_form = ctk.CTkFrame(frame_central, fg_color="transparent")
        self.frame_form.grid(row=1, column=0, pady=10)

        # Campo Bairro
        self.entry_bairro = ctk.CTkEntry(
            self.frame_form,
            placeholder_text="Bairro",
            font=(self.font_family, self.font_size),
            height=34
        )
        self.entry_bairro.grid(row=0, column=0, pady=6, sticky="ew")

        # Combo Cidade (puxa direto da tabela cidade)
        self.combo_cidade = ttk.Combobox(
            self.frame_form,
            font=(self.font_family, self.font_size),
            width=33,
            state="readonly"
        )
        self.combo_cidade.grid(row=1, column=0, pady=6, sticky="ew")
        self.combo_cidade.set("Cidade")
        self.combo_cidade.bind("<Button-1>", self.limpa_cidade_placeholder)
        self.combo_cidade.bind("<<ComboboxSelected>>", self.limpa_cidade_placeholder)

        # Carrega cidades diretamente da tabela cidade
        self.carregar_cidades()

        # Combo Estado (simulando placeholder)
        self.combo_estado = ttk.Combobox(
            self.frame_form,
            font=(self.font_family, self.font_size),
            width=33,
            state="readonly"
        )
        self.combo_estado.grid(row=2, column=0, pady=6, sticky="ew")
        self.combo_estado.set("Estado")
        self.combo_estado.bind("<Button-1>", self.limpa_estado_placeholder)
        self.combo_estado.bind("<<ComboboxSelected>>", self.limpa_estado_placeholder)

        self.carregar_estados()

        # Botões
        frame_botoes = ctk.CTkFrame(self.frame_form, fg_color="transparent")
        frame_botoes.grid(row=4, column=0, pady=(30, 10))

        btn_w = 110
        btn_h = 34
        style_btn = {
            "fg_color": "#1976D2",
            "text_color": "#fff",
            "font": ("Arial", 15),
            "width": btn_w,
            "height": btn_h
        }

        self.btn_gravar = ctk.CTkButton(frame_botoes, text="Gravar", command=self.gravar_bairro, **style_btn)
        self.btn_gravar.grid(row=0, column=0, padx=8)

        self.btn_procurar = ctk.CTkButton(frame_botoes, text="Procurar", command=self.abrir_consulta, **style_btn)
        self.btn_procurar.grid(row=0, column=1, padx=8)

        self.btn_limpar = ctk.CTkButton(frame_botoes, text="Limpar", command=self.limpar, **style_btn)
        self.btn_limpar.grid(row=0, column=2, padx=8)

        self.btn_sair = ctk.CTkButton(frame_botoes, text="Sair", fg_color="#E53935", text_color="#fff", command=self.sair,
                                      width=btn_w, height=btn_h, font=("Arial", 15))
        self.btn_sair.grid(row=0, column=3, padx=8)

    # Funções auxiliares e eventos

    def limpa_cidade_placeholder(self, event=None):
        if self.combo_cidade.get() == "Cidade":
            self.combo_cidade.set("")

    def limpa_estado_placeholder(self, event=None):
        if self.combo_estado.get() == "Estado":
            self.combo_estado.set("")

    def carregar_cidades(self):
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT nome FROM cidade ORDER BY nome")
            cidades = [row[0] for row in cursor.fetchall()]
            self.combo_cidade['values'] = cidades
            if cidades:
                self.combo_cidade.set(cidades[0])
            else:
                self.combo_cidade.set("Cidade")
            cursor.close()
            conn.close()
        except Exception as e:
            messagebox.showerror("Erro ao carregar cidades", str(e))

    def carregar_estados(self):
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT nome FROM estado ORDER BY nome")
            estados = [row[0] for row in cursor.fetchall()]
            self.combo_estado['values'] = estados
            cursor.close()
            conn.close()
        except Exception as e:
            messagebox.showerror("Erro ao carregar estados", str(e))

    def gravar_bairro(self):
        bairro = self.entry_bairro.get()
        cidade = self.combo_cidade.get()
        estado = self.combo_estado.get()
        if not bairro or not cidade or not estado or cidade == "Cidade" or estado == "Estado":
            messagebox.showwarning("Validação", "Preencha todos os campos para cadastrar!")
            return
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT c.id FROM cidade c INNER JOIN estado e ON c.id_estado=e.id WHERE c.nome=%s AND e.nome=%s", (cidade, estado))
            resultado = cursor.fetchone()
            if not resultado:
                messagebox.showerror("Cadastro", "Cidade/Estado não encontrados no banco.")
                cursor.close()
                conn.close()
                return
            id_cidade = resultado[0]
            cursor.execute("INSERT INTO bairro (nome, id_cidade) VALUES (%s,%s)", (bairro, id_cidade))
            conn.commit()
            cursor.close()
            conn.close()
            self.limpar()
            messagebox.showinfo("Sucesso", "Bairro cadastrado com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro ao gravar", str(e))

    def limpar(self):
        self.entry_bairro.delete(0, tk.END)
        self.combo_cidade.set("Cidade")
        self.combo_estado.set("Estado")
        
    def abrir_consulta(self):
        ConsultaBairro(self.master)

    def sair(self):
        self.destroy()


class ConsultaBairro(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Consulta de Bairros")
        self.geometry("950x450")
        self.configure(bg="#e3f2fd")

        lbl_titulo = ctk.CTkLabel(self, text="Bairro", font=("Arial", 32, "bold"), text_color="#1976D2")
        lbl_titulo.place(relx=0.5, rely=0.08, anchor="center")
        frame_grid = tk.Frame(self, bg="#e3f2fd")
        frame_grid.place(relx=0.5, rely=0.20, anchor="n", relwidth=0.91, height=240)

        style = ttk.Style()
        style.configure("Custom.Treeview.Heading", font=("Arial", 15, "bold"), background="#1976D2", foreground="#FFF")
        style.configure("Custom.Treeview", background="#e3f2fd", fieldbackground="#e3f2fd", font=("Arial", 14))
        style.map("Custom.Treeview", background=[("selected", "#90CAF9")])

        grid_bairros = ttk.Treeview(frame_grid, columns=("bairro", "cidade", "estado"), show="headings", style="Custom.Treeview")
        grid_bairros.heading("bairro", text="Bairro")
        grid_bairros.heading("cidade", text="Cidade")
        grid_bairros.heading("estado", text="Estado")
        grid_bairros.column("bairro", width=320, anchor="center")
        grid_bairros.column("cidade", width=310, anchor="center")
        grid_bairros.column("estado", width=260, anchor="center")
        grid_bairros.pack(fill="both", expand=True)

        btn_sair = ctk.CTkButton(self, text="Sair", 
                                 width=120, fg_color="#E53935", hover_color="#cc0000", command=lambda: cadastro_bairro(self, None, on_show_small_logo, on_show_big_logo),)
        btn_sair.place(relx=0.90, rely=0.92, anchor="center")

        self.carregar_bairros(grid_bairros)

    def carregar_bairros(self, treeview):
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT nome, c.nome, e.nome
                FROM bairro b
                INNER JOIN cidade c ON id_cidade = id
                INNER JOIN estado e ON id_estado = id
                ORDER BY nome
            """)
            for item in treeview.get_children():
                treeview.delete(item)
            for bairro, cidade, estado in cursor.fetchall():
                treeview.insert("", "end", values=(bairro, cidade, estado))
            cursor.close()
            conn.close()
        except Exception as e:
            messagebox.showerror("Erro ao carregar bairros", str(e))


if __name__ == "__main__":
    root = ctk.CTk()
    root.title("Cadastro de Bairro")
    root.after(10, lambda: root.state("zoomed"))
    root.configure(fg_color="#e3f2fd")
    cadastro_bairro(root)
    root.mainloop()
