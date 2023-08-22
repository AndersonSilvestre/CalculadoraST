from xml.dom import minidom
import tkinter as tk
from tkinter import ttk
# from tkinter.messagebox import showinfo
from tkinter import filedialog
# from tkinter.scrolledtext import ScrolledText
# from tkinter.filedialog import askopenfilename


class MainApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.geometry('790x250')
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        self.frames = {}

        for F in (Interface, Teste):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Interface)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


def seleciona_xml():
    filetypes = (('XML', '*.xml'), ('Todos os Arquivos', '*.*'))
    filename = filedialog.askopenfilename(filetypes=filetypes, title="Selecione o Arquivo")
    return filename


class Interface(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # Variaveis da classe

        # Ncm Nacional são os com Aliq de Icms de 12%
        self.ncm_nacional = {30021219: 1.8087, 30021229: 1.8087, 30021590: 1.8087, 34011190: 1.6356, 34029090: 1.5280,
                             38221940: 1.8087, 84716052: 1.4917, 84719012: 1.4702, 85392110: 1.9532, 85423190: 1.5239,
                             85444200: 1.5346, 90183119: 1.8087}
        # Ncm Importado são os com Aliq de Icms de 4%
        self.ncm_imp = {30021219: 1.9732, 30021229: 1.9732, 30021590: 1.9732, 34011190: 1.7843, 34029090: 1.6669,
                        38221940: 1.9732, 84716052: 1.6273, 84719012: 1.6039, 85423190: 1.6624, 85444200: 1.6741,
                        90183119: 1.9732}

        self.label = tk.Label(self, text='Calculadora ST')
        self.label.grid(column=2, row=1, columnspan=2)
        # Configura a tela
        # self.title('Calculo ST')
        # self.geometry('300x150')
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
        self.calculabtn = tk.Button(self, text='Grava Linha', command=self.cria_txt)
        self.calculabtn.grid(column=3, row=3, pady=5, padx=5, sticky='nsew')
        self.quit = tk.Button(self, text='Sair', command=self.quit)
        self.quit.grid(column=4, row=3, pady=5, padx=5, sticky='nsew')

    def abre_arquivo(self):
        self.produtos = []
        filename = seleciona_xml()
        xml = open(filename)

        # Cria variaveis das tags do xml
        parsed_xml = minidom.parse(xml)
        self.numero_nota = parsed_xml.getElementsByTagName('nNF')
        self.nat_op = parsed_xml.getElementsByTagName('natOp')
        self.cnpj = parsed_xml.getElementsByTagName('CNPJ')
        num_item = parsed_xml.getElementsByTagName('det')
        cod_prod = parsed_xml.getElementsByTagName('cProd')
        nome_item = parsed_xml.getElementsByTagName('xProd')
        xml_ncm = parsed_xml.getElementsByTagName('NCM')
        valor_total = parsed_xml.getElementsByTagName('vProd')
        valor_icms = parsed_xml.getElementsByTagName('vICMS')
        aliq_icms = parsed_xml.getElementsByTagName('pICMS')
        # valor_ipi = parsed_xml.getElementsByTagName('vIPI')

        # Cria a lista com os valores das tags
        self.nat_op = [str(nop.firstChild.data) for nop in self.nat_op]
        for nf in self.numero_nota:
            self.numero_nota = nf.firstChild.data
        lista_num_item = [int(n.attributes['nItem'].value) for n in num_item]
        lista_cod_prod = [int(cod.firstChild.data) for cod in cod_prod]
        lista_nome_item = [str(nome.firstChild.data) for nome in nome_item]
        lista_ncm = [int(ncm.firstChild.data) for ncm in xml_ncm]
        lista_valor_total = [float(valor.firstChild.data) for valor in valor_total]
        lista_valor_ncm = [float(vrncm.firstChild.data) for vrncm in valor_icms]
        lista_aliq_ncm = [float(aliq.firstChild.data) for aliq in aliq_icms]
        # lista_ipi = [float(ipi.firstChild.data) for ipi in valor_ipi]
        w=0
        for c in self.cnpj:
            if w < 1:
                self.cnpj = c.firstChild.data
                w+=1
            else:
                break

        lista_ipi = []
        for i in num_item:
            if i.getElementsByTagName("vIPI"):
                lista_ipi.append(float(i.getElementsByTagName('vIPI')[0].firstChild.data))
            else:
                lista_ipi.append(0)


        # for para gerar uma unica lista contendo as informações dos produtos da nota.
        w = 0
        for i in lista_num_item:
            listainterna = [lista_num_item[w], lista_cod_prod[w], lista_nome_item[w], lista_ncm[w], lista_valor_total[w],
                            lista_valor_ncm[w], lista_aliq_ncm[w], lista_ipi[w]]
            self.produtos.append(listainterna)
            w += 1

        self.calcula()

    def calcula(self):
        self.total = 0
        w = 0
        # Calculo do St dos produtos da nf
        for i in self.produtos:
            if i[6] == 12.00:
                if i[3] in self.ncm_nacional.keys():
                    item = round((((i[4]+i[7])*self.ncm_nacional[i[3]])*0.18)-i[5], 2)
                    self.produtos[w].append('R$ ' + str(item))
                    self.total += item
                    w += 1
                else:
                    self.produtos[w].append('Sem ST')
                    w += 1
            elif i[6] == 4.00:
                if i[3] in self.ncm_imp.keys():
                    item = round((((i[4]+i[7])*self.ncm_imp[i[3]])*0.18)-i[5], 2)
                    self.produtos[w].append('R$ ' + str(item))
                    self.total += item
                    w += 1
                else:
                    self.produtos[w].append('Sem ST')
                    w += 1


        self.total = round(self.total, 2)
        # Apresentacao do resultado
        self.label = tk.Label(self, text='Valor da ST')
        self.label.grid(column=1, row=4)

        self.totallabel = tk.Label(self, text='R$ ' + str(self.total), borderwidth=2, relief="groove", width=10)
        self.totallabel.grid(column=2, row=4, columnspan=2, ipadx=10, ipady=5)

        self.nota = tk.Label(self, text='Numero NF')
        self.nota.grid(column=4, row=4)
        self.nop = tk.Label(self, text=self.nat_op)
        self.nop.grid(column=2, row=5)
        self.numnota = tk.Label(self, text=self.numero_nota, borderwidth=2, relief='groove', width=10)
        self.numnota.grid(column=5, row=4)

        self.cria_tabela()

    def cria_tabela(self):
        colunas = ('linha', 'cod produto', 'nome', 'ncm', 'vlrUnitario', 'vlrNcm', 'aliq', 'ipi', 'st')
        self.tree = ttk.Treeview(self, height=5, columns=colunas, show='headings')
        self.tree.heading('linha', text='#0')
        self.tree.column('linha', width=30)
        self.tree.heading('cod produto', text='Cod Prod')
        self.tree.column('cod produto', width=80)
        self.tree.heading('nome', text='Descrição')
        self.tree.column('nome', width=250)
        self.tree.heading('ncm', text='NCM')
        self.tree.column('ncm', width=80)
        self.tree.heading('vlrUnitario', text='Vlr Un')
        self.tree.column('vlrUnitario', width=80)
        self.tree.heading('vlrNcm', text='Vlr NCM')
        self.tree.column('vlrNcm', width=80)
        self.tree.heading('aliq', text='Aliq')
        self.tree.column('aliq', width=40)
        self.tree.heading('ipi', text='IPI')
        self.tree.column('ipi', width=50)
        self.tree.heading('st', text='St')
        self.tree.column('st', width=80) 
        self.tree.grid(column=1, row=6, columnspan=6)

        scroll = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        scroll.grid(column=7, row=6, sticky='ns')

        self.pega_produto()

    def pega_produto(self):
        interno = self.produtos
        for itens in interno:
            self.tree.insert('', tk.END, values=itens)
        # print(interno)

    def cria_txt(self):
        linha_arquivo = str(self.numero_nota) + ";" + str(self.total) + '\n'
        # linha_arquivo = str(self.cnpj) + ";" + "08/2023" + ";" + "23/08/2023" + ";" + str(self.total) + ";" + "0" + '\n'
        with open('imposto.txt', 'a') as arquivo:
            arquivo.write(linha_arquivo)
        print(linha_arquivo)


class Teste(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # self.title("ScrolledText Widget")

        colunas = ('linha', 'cod produto', 'nome', 'ncm', 'vlrUnitario', 'vlrNcm')
        self.tree = ttk.Treeview(self, height=5, columns=colunas, show='headings')
        self.tree.heading('linha', text='#0')
        self.tree.column('linha', width=30)
        self.tree.heading('cod produto', text='Cod Prod')
        self.tree.column('cod produto', width=80)
        self.tree.heading('nome', text='Descrição')
        self.tree.column('nome', width=250)
        self.tree.heading('ncm', text='NCM')
        self.tree.column('ncm', width=80)
        self.tree.heading('vlrUnitario', text='Vlr Un')
        self.tree.column('vlrUnitario', width=80)
        self.tree.heading('vlrNcm', text='Vlr NCM')
        self.tree.column('vlrNcm', width=80)
        self.tree.grid(column=1, row=1)

        self.mostra = tk.Button(self, text='tabela', command=self.pega_produto)
        self.mostra.grid(column=1, row=4, pady=5, padx=5)
        self.volta = tk.Button(self, text='Sair', command=lambda: controller.show_frame(Interface))
        self.volta.grid(column=1, row=3, pady=5, padx=5)

        scroll = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        scroll.grid(row=1, column=2, sticky='ns')

    def pega_produto(self):
        interno = produtos
        for itens in interno:
            self.tree.insert('', tk.END, values=itens)
        print(interno)


gui = MainApp()
gui.mainloop()
