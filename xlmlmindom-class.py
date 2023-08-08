from xml.dom import minidom
import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter.messagebox import showinfo
from tkinter.filedialog import askopenfilename

ncms = [30021229, 30021590, 34029090, 90183119, 90183219, 30021219, 34011190, 84181000, 84716052, 84719012,
        84733019, 84733041, 84733042, 85285200, 85392110, 85423190, 85444200]

LARGEFONT = ("Verdana", 35)


class tkinterApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)

        self.geometry('500x200')
        # creating a container
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        # container.grid_rowconfigure(0, weight = 1)
        # container.grid_columnconfigure(0, weight = 1)

        # initializing frames to an empty array
        self.frames = {}

        # iterating through a tuple consisting
        # of the different page layouts
        for F in (PaginaInicial, CalculoArquivo, CalculoItem, Interface):
            frame = F(container, self)

            # initializing frame of that object from
            # startpage, page1, page2 respectively with
            # for loop
            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(PaginaInicial)

        # to display the current frame passed as
        # parameter

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


# first window frame startpage

class PaginaInicial(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # label of frame Layout 2
        label = ttk.Label(self, text="Calculo ST Siemens")
        label.grid(row=0, column=2, columnspan=2, padx=10, pady=10)

        button1 = ttk.Button(self, text="Por Arquivo", command=lambda: controller.show_frame(CalculoArquivo))
        button1.grid(row=1, column=1, padx=10, pady=10)

        ## button to show frame 2 with text layout2
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

        # Labels
        label = tk.Label(self, text='Calculadora ST')
        label.grid(column=2, row=1, columnspan=2)
        label = tk.Label(self, text='Importe o XML')
        label.grid(column=1, row=2, columnspan=2)

        # Buttons
        button1 = ttk.Button(self, text="StartPage", command=lambda: controller.show_frame(PaginaInicial))
        button1.grid(row=4, column=1, padx=10, pady=10)
        # button2 = ttk.Button(self, text="Page 2", command=lambda: controller.show_frame(Page2))
        # button2.grid(row=2, column=1, padx=10, pady=10)
        abre = ttk.Button(self, text='arquivo', command=self.abre_arquivo)
        abre.grid(column=1, row=3, pady=5, padx=5)
        calculabtn = ttk.Button(self, text='calcula', command=self.calcula)
        calculabtn.grid(column=3, row=3, pady=5, padx=5)
        quit = ttk.Button(self, text='Quit', command=self.quit)
        quit.grid(column=5, row=3, pady=5, padx=5)

    def abre_arquivo(self):
        self.produtos = []
        filename = askopenfilename()
        xml = open(filename)
        parsedXML = minidom.parse(xml)
        print(filename)
        numItem = parsedXML.getElementsByTagName('det')
        codProd = parsedXML.getElementsByTagName('cProd')
        nomeItem = parsedXML.getElementsByTagName('xProd')
        NCM = parsedXML.getElementsByTagName('NCM')
        valorTotal = parsedXML.getElementsByTagName('vProd')
        valorICM = parsedXML.getElementsByTagName('vICMS')

        listaNumItem = [int(n.attributes['nItem'].value) for n in numItem]
        listaCodProd = [int(cod.firstChild.data) for cod in codProd]
        listaNomeItem = [str(nome.firstChild.data) for nome in nomeItem]
        listaNCM = [int(ncm.firstChild.data) for ncm in NCM]
        listaValorTotal = [float(valor.firstChild.data) for valor in valorTotal]
        listaValorNCM = [float(vrncm.firstChild.data) for vrncm in valorICM]
        w = 0
        # for para gerar uma unica lista contendo as informações dos produtos da nota.
        for i in listaNumItem:
            listainterna = [listaNumItem[w], listaCodProd[w], listaNomeItem[w], listaNCM[w], listaValorTotal[w],
                            listaValorNCM[w]]
            self.produtos.append(listainterna)
            w += 1
        # print(self.produtos)

    def calcula(self):

        total = 0
        for i in self.produtos:
            if i[3] in ncms:
                total += ((i[4] * 1.8087) * 0.18) - i[5]
        self.total = tk.Label(self, text=total, anchor=W, justify=LEFT)
        self.total.grid(column=1, row=5, columnspan=3)


# third window frame page2
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
app = tkinterApp()
app.mainloop()
