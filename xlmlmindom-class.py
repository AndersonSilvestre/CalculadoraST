from xml.dom import minidom
import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import filedialog
# from tkinter.messagebox import showinfo
# from tkinter.filedialog import askopenfilename

ncms = [30021229, 30021590, 34029090, 90183119, 90183219, 30021219, 34011190, 84181000, 84716052, 84719012,
        84733019, 84733041, 84733042, 85285200, 85392110, 85423190, 85444200]


class MainApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)

        #self.geometry('700x200')
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        # container.grid_rowconfigure(0, weight = 1)
        # container.grid_columnconfigure(0, weight = 1)
        self.frames = {}
        for F in (PaginaInicial, CalculoArquivo, CalculoItem, Interface):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(PaginaInicial)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class PaginaInicial(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # label of frame Layout 2
        label = ttk.Label(self, text="Calculo ST Siemens")
        label.grid(row=0, column=2, columnspan=2, padx=10, pady=10)

        button1 = ttk.Button(self, text="Por Arquivo", command=lambda: controller.show_frame(CalculoArquivo))
        button1.grid(row=1, column=1, padx=10, pady=10)

        # button to show frame 2 with text layout2
        button2 = ttk.Button(self, text="Calculo por Item", command=lambda: controller.show_frame(CalculoItem))
        button2.grid(row=1, column=2, padx=10, pady=10)

        button3 = ttk.Button(self, text="interface", command=lambda: controller.show_frame(Interface))
        button3.grid(row=1, column=3, padx=10, pady=10)

        button4 = ttk.Button(self, text="Sair", command=self.quit)
        button4.grid(row=1, column=4, padx=10, pady=10)


# second window frame page1
class CalculoArquivo(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.produtos = []

        self.frame = tk.Frame(self, width=600, height=50, borderwidth=2, relief="groove")
        self.frame.grid(column=0, row=3, columnspan=6, sticky='nsew')
        self.frame.grid_propagate(False)
        # self.label = tk.Label(self, text='Importe o XML')
        # self.label.grid(column=2, row=2, columnspan=3)
        self.label = tk.Label(self, text='Selecione\no Arquivo Xml')
        self.label.grid(column=1, row=3)

        # buttons
        self.abre = tk.Button(self, text='Arquivo', command=self.abre_arquivo)
        self.abre.grid(column=2, row=3, ipady=5)
        self.abre.grid_propagate(False)
        # self.calculabtn = tk.Button(self, text='calcula', command=self.calcula)
        # self.calculabtn.grid(column=3, row=3, pady=5, padx=5, sticky='nsew')
        self.quit = tk.Button(self, text='Sair', command=self.quit)
        self.quit.grid(column=4, row=3, pady=5, padx=5, sticky='nsew')
        # self.mostra = tk.Button(self, text='tabela', command=lambda: controller.show_frame(Teste))
        # self.mostra.grid(column=6, row=3, pady=5, padx=5)

    def seleciona_xml(self):
        filetypes = (('XML', '*.xml'), ('Todos os Arquivos', '*.*'))
        filename = filedialog.askopenfilename(filetypes=filetypes, title="Selecione o Arquivo")
        return filename

    def abre_arquivo(self):

        filename = self.seleciona_xml()
        # filename = askopenfilename()
        xml = open(filename)
        # print(filename)
        parsed_xml = minidom.parse(xml)
        self.numero_nota = parsed_xml.getElementsByTagName('nNF')
        num_item = parsed_xml.getElementsByTagName('det')
        cod_prod = parsed_xml.getElementsByTagName('cProd')
        nome_item = parsed_xml.getElementsByTagName('xProd')
        xml_ncm = parsed_xml.getElementsByTagName('NCM')
        valor_total = parsed_xml.getElementsByTagName('vProd')
        valor_icms = parsed_xml.getElementsByTagName('vICMS')

        self.numero_nota = [str(nota.firstChild.data) for nota in self.numero_nota]
        print(self.numero_nota)
        lista_num_item = [int(n.attributes['nItem'].value) for n in num_item]
        lista_cod_prod = [int(cod.firstChild.data) for cod in cod_prod]
        lista_nome_item = [str(nome.firstChild.data) for nome in nome_item]
        lista_ncm = [int(ncm.firstChild.data) for ncm in xml_ncm]
        lista_valor_total = [float(valor.firstChild.data) for valor in valor_total]
        lista_valor_ncm = [float(vrncm.firstChild.data) for vrncm in valor_icms]
        w = 0
        # for para gerar uma unica lista contendo as informações dos produtos da nota.
        for i in lista_num_item:
            listainterna = [lista_num_item[w], lista_cod_prod[w], lista_nome_item[w], lista_ncm[w], lista_valor_total[w],
                            lista_valor_ncm[w]]
            self.produtos.append(listainterna)
            w += 1
            # print(self.produtos)
        self.calcula()

    def calcula(self):
        total = 0
        w = 0
        # Calculo do St dos produtos da nf
        for i in self.produtos:
            if i[3] in ncms:
                item = round(((i[4]*1.8087)*0.18)-i[5], 2)
                self.produtos[w].append('R$ ' + str(item))
                print(self.produtos)
                # total += ((i[4]*1.8087)*0.18)-i[5]
                total += item
                # print(total)
                w += 1
            else:
                self.produtos[w].append('Sem ST')
                w += 1
        total = round(total, 2)
        # Apresentacao do resultado
        self.label = tk.Label(self, text='Valor da ST')
        self.label.grid(column=1, row=4)

        totallabel = tk.Label(self, text='R$ ' + str(total), borderwidth=2, relief="groove", width=10)
        totallabel.grid(column=2, row=4, columnspan=2, ipadx=10, ipady=5)

        nota = tk.Label(self, text='Numero NF')
        nota.grid(column=4, row=4)
        numnota = tk.Label(self, text=self.numero_nota, borderwidth=2, relief='groove', width=10)
        numnota.grid(column=5, row=4)

        self.cria_tabela()

    def cria_tabela(self):
        colunas = ('linha', 'cod produto', 'nome', 'ncm', 'vlrUnitario', 'vlrNcm', 'st')
        tree = ttk.Treeview(self, height=5, columns=colunas, show='headings')
        tree.heading('linha', text='#0')
        tree.column('linha', width=30)
        tree.heading('cod produto', text='Cod Prod')
        tree.column('cod produto', width=80)
        tree.heading('nome', text='Descrição')
        tree.column('nome', width=250)
        tree.heading('ncm', text='NCM')
        tree.column('ncm', width=80)
        tree.heading('vlrUnitario', text='Vlr Un')
        tree.column('vlrUnitario', width=80)
        tree.heading('vlrNcm', text='Vlr NCM')
        tree.column('vlrNcm', width=80)
        tree.heading('st', text='Vlr ST')
        tree.column('st', width=80)
        tree.grid(column=1, row=5, columnspan=6, pady=10)

        scroll = ttk.Scrollbar(self, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scroll.set)
        scroll.grid(column=7, row=5, sticky='ns')

        # Pegar os produtos e inserilos na tabela
        interno = self.produtos
        for itens in interno:
            tree.insert('', tk.END, values=itens)
        print(interno)


class CalculoItem(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # Vars
        mvaajust = IntVar()
        # Labels
        tk.Label(self, text="Calculo por item").grid(row=0, column=2, padx=10, pady=10)
        tk.Label(self, text="Insira o MVA Ajustado").grid(row=0, column=0)
        # Entrys
        tk.Entry(self, textvariable=mvaajust).grid(row=1, column=0, padx=5, pady=5)

        # Buttons
        ttk.Button(self, text="Inicio", command=lambda: controller.show_frame(PaginaInicial))\
            .grid(row=4, column=2, padx=10, pady=10)
        ttk.Button(self, text="Não utilizar", command=lambda: controller.show_frame(StartPage))\
            .grid(row=4, column=1, padx=10, pady=10)


class Interface(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        button1 = ttk.Button(self, text="Pagina Inicial", command=lambda: controller.show_frame(PaginaInicial))
        button1.grid(row=4, column=1, padx=10, pady=10)


# Driver Code
app = MainApp()
app.mainloop()
