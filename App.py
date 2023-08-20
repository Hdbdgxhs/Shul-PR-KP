import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import Menu

class Button(ttk.Button):
    def __init__(self, parent, y, x):
        super().__init__(parent, width=3)
        self.x=x+1
        self.y=y+1
        self.text=''
        self.config(command=self.Function_Button)

    def Function_Button(self):
        if (app.Text_On==False):
            app.Draw_Geometry(self.x, self.y)
        else:
            tp = tk.Toplevel(app)
            tp.geometry("660x420")
            entry = tk.Text(tp, wrap="word")
            entry.insert(1.0, self.text)
            entry.grid(row=0, column=0)
            butt = ttk.Button(tp, text='quit', command=tp.quit)
            butt.grid(row=1, column=0)
            tp.mainloop()
            self.text = (entry.get(1.0, END))
            self.config(text='*')
            tp.destroy()

class Frame(tk.Frame):
    def __init__(self, parent, xy):
        super().__init__(parent)
        self.xy=xy
        self.config(width=self.winfo_screenwidth(), height=(self.winfo_screenheight()), background='white')
        self.w=self.winfo_screenwidth()
        self.h=self.winfo_screenheight()-100
        self.canvans_button=tk.Canvas(self, width=(self.w-self.h), height=self.h, background='black')
        self.canvans_button.grid(row=0, column=0, sticky='news')
        self.canvans_button.grid_rowconfigure(0, weight=1)
        self.canvans_button.grid_columnconfigure(0, weight=1)
        self.canvans_button.grid_propagate(False)
        self.frame_button=tk.Frame(self.canvans_button, width=(self.w-self.h), height=self.h, bg='white')
        self.frame_button.grid(row=0, column=0, sticky='news')
        scroll_x=ttk.Scrollbar(self.canvans_button, orient=HORIZONTAL, command=self.canvans_button.xview)
        scroll_x.grid(row=1, column=0, sticky='news')
        scroll_x.grid_columnconfigure(0, weight=1)
        scroll_y=ttk.Scrollbar(self.canvans_button, orient=VERTICAL, command=self.canvans_button.yview)
        scroll_y.grid(row=0, column=1, sticky='news')
        self.canvans_button.create_window(0,0, window=self.frame_button)
        self.canvans = tk.Canvas(self, width=self.h, height=self.h, background='white')
        self.canvans.bind('<Button-1>', self.print)
        self.canvans.grid(row=0, column=1, sticky='news')


    def print(self, event):
        x=(app.winfo_pointerx()-(app.winfo_screenwidth()-self.h))//(self.h//self.xy)+1
        y=(app.winfo_pointery()-(app.winfo_screenheight()-self.h)+32)//(self.h//self.xy)+1
        print(x, ' ', y)
        app.Draw_Geometry(x, y)

class Win(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.geometry("300x100")
        self.title("KP_Kurs")
        self.iconbitmap("icons8-монитор-50.ico")
        BoxWH = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
        self.combobox = ttk.Combobox(self, values=BoxWH, state="readonly")
        self.combobox.bind("<<ComboboxSelected>>")
        self.combobox.current(0)
        self.bk=0
        self.lab = Label(self, text="Размеры:").grid(row=1, column=0, sticky=W, padx=5, pady=5)
        self.combobox.grid(row=1, column=1, sticky='news', columnspan=2, padx=10)
        self.butt = ttk.Button(self, text="Создать", command=self.quit).grid(row=2, column=2, padx=10)
        self.mainloop()
        self.bk=self.Open()
        self.destroy()

    def Open(self):
        get = self.combobox.get()
        return get


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.state('zoomed')
        self.geometry("{}x{}".format(self.winfo_screenwidth(), self.winfo_screenheight()))
        self.title("KP_Kurs")
        self.iconbitmap("icons8-монитор-50.ico")
        self.config(background='grey1')
        self.XY_position=[0,0,0,0]
        self.Geometry=None
        self.Text_On=False
        self.Num_frame = 1
        self.RB=0
        self.W=0
        self.H=0
        self.notebook = ttk.Notebook(self)
        self.notebook.place(x=0, y=0)
        self.tablist = []
        fram=tk.Frame(self.notebook)
        fram.config(width=self.winfo_screenwidth(), height=self.winfo_screenheight(), background='white')
        fram.pack(fill=X)
        self.tablist.append(fram)
        self.notebook.add(fram, text='Hello')
        self.menu = Menu(self)
        self.config(menu=self.menu)
        self.new_item = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label='Файл', menu=self.new_item)
        self.menu.add_cascade(label='Линия', command=self.Geometry_Line)
        self.menu.add_cascade(label='Квадрат', command=self.Geometry_Rectangle, compound=tk.LEFT)
        self.menu.add_cascade(label='Овал', command=self.Geometry_Oval)
        self.menu.add_cascade(label='Заметка', command= self.Text_Note)
        self.new_item.add_command(label='Создать', command=self.open_windows)

    def Draw_Geometry(self, x, y):

        if(self.XY_position[0]==0):
            print(x, ' ', y)
            self.XY_position[0] = x
            self.XY_position[1] = y
            return
        elif(self.XY_position[2]==0):
            print(x, ' ', y)
            self.XY_position[0]=self.XY_position[0]-1
            self.XY_position[1]=self.XY_position[1]-1
            self.XY_position[2]=x-1
            self.XY_position[3]=y-1
            if self.Geometry!=None:
                self.Geometry(self.XY_position[0]*self.W+self.W//2,self.XY_position[1]*self.H+self.H//2,
                              self.XY_position[2]*self.W+self.W//2,self.XY_position[3]*self.H+self.H//2)
        self.XY_position[0]=0
        self.XY_position[1]=0
        self.XY_position[2]=0
        self.XY_position[3]=0

    def Text_Note(self):
        self.Text_On=True

    def Geometry_Rectangle(self):
        self.Text_On=False
        fram=self.notebook.tabs().index(self.notebook.select())
        self.Geometry=self.tablist[fram].canvans.create_rectangle

    def Geometry_Line(self):
        self.Text_On=False
        fram = self.notebook.tabs().index(self.notebook.select())
        self.Geometry = self.tablist[fram].canvans.create_line

    def Geometry_Oval(self):
        self.Text_On=False
        fram = self.notebook.tabs().index(self.notebook.select())
        self.Geometry = self.tablist[fram].canvans.create_oval

    def New_frame(self):
        fram=Frame(self.notebook, xy=self.RB)
        self.tablist.append(fram)
        self.tablist[self.Num_frame].config(width=self.winfo_screenwidth(), height=self.winfo_screenheight(), background='blue')
        self.notebook.add(self.tablist[self.Num_frame], text='Note ' + str(self.Num_frame))
        self.W=fram.h
        self.H=fram.h
        self.Num_frame+=1

    def open_windows(self):
        win = Win(self)
        self.RB=int(win.bk)
        print(self.RB)
        self.New_frame()
        self.W=self.W//(self.RB)
        self.H=self.H//(self.RB)
        i=0
        g=0
        for i in range(self.RB):
            for g in range(self.RB):
                button_fr=Button(parent=self.tablist[self.Num_frame-1].frame_button, y=i, x=g)
                button_fr.grid(row=i, column=g, sticky='news')
        

app = App()
app.mainloop()