import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import Menu
from tkinter import filedialog

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
            fram = app.notebook.tabs().index(app.notebook.select())
            (app.tablist[fram].canvans.itemconfig(
                app.tablist[fram].Renc[app.XY_position[0]][app.XY_position[1]], outline="#DCDCDC"))
            Len = len(app.tablist[fram].Mass)
            app.tablist[fram].Mass.append([0] * 3)
            app.tablist[fram].Mass[Len][0] = 4
            app.tablist[fram].Mass[Len][1] = self.x
            app.tablist[fram].Mass[Len][2] = self.y
            tp.destroy()

class Frame(tk.Frame):
    def __init__(self, parent, xy):
        super().__init__(parent)
        self.xy=xy
        self.Mass=[]
        self.Mass.append([xy])
        self.button_fr=[]
        self.config(width=self.winfo_screenwidth(), height=(self.winfo_screenheight()-110),
                    background='white')
        self.w=self.winfo_screenwidth()
        self.h=self.winfo_screenheight()-110
        self.Canvas_Button()
        self.canvans = tk.Canvas(self, width=self.h, height=self.h, background='white')
        self.canvans.bind('<Button-1>', self.print)
        self.canvans.bind('<Button-3>', self.Delete_print)
        self.canvans.grid(row=0, column=1, sticky='news')
        self.Renctangle_pole()

    def Renctangle_pole(self):
        self.Renc=[0]*self.xy
        rang=self.h//self.xy
        i=0
        g=0
        ren=None
        for i in range(self.xy):
            self.Renc[i]=[0]*self.xy
            for g in range(self.xy):
                self.Renc[i][g]=self.canvans.create_rectangle(i*rang-1, g*rang-1,(i+1)*rang,
                                                              (g+1)*rang, outline="#DCDCDC")
    def print(self, event):
        x=(app.winfo_pointerx()-(app.winfo_screenwidth()-self.h))//(self.h//self.xy)+1
        y=(app.winfo_pointery()-(app.winfo_screenheight()-self.h)+40)//(self.h//self.xy)+1
        self.canvans.itemconfig(self.Renc[x-1][y-1], outline="#99958C")
        self.button_fr[y-1][x-1].Function_Button()

    def Delete_print(self, event):
        fram = app.notebook.tabs().index(app.notebook.select())
        (app.tablist[fram].canvans.itemconfig(
            app.tablist[fram].Renc[app.XY_position[0]-1][app.XY_position[1]-1],
            outline="#DCDCDC"))
        app.XY_position[0]=0
        app.XY_position[1]=0

    def Canvas_Button(self):
        self.canvans_button = tk.Canvas(self, width=(self.w - self.h),
                                        height=self.h, background='black')
        self.canvans_button.grid(row=0, column=0, sticky='news')
        self.canvans_button.grid_rowconfigure(0, weight=1)
        self.canvans_button.grid_columnconfigure(0, weight=1)
        self.canvans_button.grid_propagate(False)
        self.frame_button = tk.Frame(self.canvans_button, width=(self.w - self.h),
                                     height=self.h, bg='white')
        self.frame_button.grid(row=0, column=0, sticky='news')
        self.scroll_x = ttk.Scrollbar(self.canvans_button, orient=HORIZONTAL,
                                      command=self.canvans_button.xview)
        self.scroll_x.grid(row=1, column=0, sticky='news')
        self.scroll_x.grid_columnconfigure(0, weight=1)
        self.scroll_y = ttk.Scrollbar(self.canvans_button, orient=VERTICAL,
                                      command=self.canvans_button.yview)
        self.scroll_y.grid(row=0, column=1, sticky='news')
        self.canvans_button.create_window(0, 0, window=self.frame_button)

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
        self.lab = Label(self, text="Размеры:").grid(row=1, column=0,
                                                     sticky=W, padx=5, pady=5)
        self.combobox.grid(row=1, column=1, sticky='news', columnspan=2, padx=10)
        self.butt = ttk.Button(self, text="Создать",
                               command=self.quit).grid(row=2, column=2, padx=10)
        self.mainloop()
        self.bk=self.Open()
        self.destroy()

    def Open(self):
        get = self.combobox.get()
        return get


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.Window_App()               #функция создания окна приложения
        self.XY_position=[0,0,0,0]
        self.Geometry=None
        self.Text_On=False
        self.Num_frame = 1
        self.Geometry_Num=0
        self.RB=0
        self.W=0        #параметры длинны поля
        self.H=0        #параметры ширины поля
        self.tablist = []
        self.notebook = ttk.Notebook(self)
        self.notebook.place(x=0, y=0)
        fram=tk.Frame(self.notebook)
        fram.config(width=self.winfo_screenwidth(),
                    height=self.winfo_screenheight()-110, background='white')
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
        self.new_item.add_command(label='Сохранить', command=self.save_file)
        self.new_item.add_command(label='Открыть', command=self.open_file)

    def Window_App(self):
        self.state('zoomed')
        self.geometry("{}x{}".format(self.winfo_screenwidth(),
                                     self.winfo_screenheight() - 40))
        self.title("KP_Kurs")
        self.iconbitmap("icons8-монитор-50.ico")
        self.config(background='grey1')

    def open_file(self):
        filepath = filedialog.askopenfilename(defaultextension="txt", filetypes=(('text file', 'txt'),),
                                              initialdir=("C:"))
        i=1
        if filepath != "":
            with open(filepath, "r") as file:
                text = file.read().splitlines()
            self.New_frame(int(text[0]))



    def save_file(self):
        filepath = filedialog.asksaveasfilename()
        fram = self.notebook.tabs().index(self.notebook.select())
        i=0
        g=0
        if filepath != "":
            with open(filepath, "a") as file:
                for i in range(len(self.tablist[fram].Mass)):
                    for g in range(len(self.tablist[fram].Mass[i])) :
                        file.write(str(self.tablist[fram].Mass[i][g]))
    def Draw_Geometry(self, x, y):
        fram = self.notebook.tabs().index(self.notebook.select())
        if(self.XY_position[0]==0):
            if self.Geometry != None:
                print(x, ' ', y)
                self.XY_position[0] = x
                self.XY_position[1] = y
                return
            else:

                self.tablist[fram].canvans.itemconfig(self.tablist[fram].Renc[x-1][y-1],
                                                      outline="#DCDCDC")
                print(self.XY_position[0],self.XY_position[1])
                self.XY_position[0] = 0
                self.XY_position[1] = 0
                return
        elif(self.XY_position[2]==0):
            print(x, ' ', y)
            W = self.W // (self.tablist[fram].xy)
            H = self.H // (self.tablist[fram].xy)
            self.XY_position[0]=self.XY_position[0]-1
            self.XY_position[1]=self.XY_position[1]-1
            self.XY_position[2]=x-1
            self.XY_position[3]=y-1
            if self.Geometry!=None:
                self.Geometry(self.XY_position[0]*W+W//2,self.XY_position[1]*H+H//2,
                              self.XY_position[2]*W+W//2,self.XY_position[3]*H+H//2)
                Len=len(self.tablist[fram].Mass)
                self.tablist[fram].Mass.append([0]*5)
                self.tablist[fram].Mass[Len][0]=self.Geometry_Num
                self.tablist[fram].Mass[Len][1]=self.XY_position[0]+1
                self.tablist[fram].Mass[Len][2]=self.XY_position[1]+1
                self.tablist[fram].Mass[Len][3]=self.XY_position[2]+1
                self.tablist[fram].Mass[Len][4]=self.XY_position[3]+1
        (self.tablist[fram].canvans.itemconfig(
            self.tablist[fram].Renc[self.XY_position[0]][self.XY_position[1]], outline="#DCDCDC"))
        (self.tablist[fram].canvans.itemconfig(
            self.tablist[fram].Renc[self.XY_position[2]][self.XY_position[3]], outline="#DCDCDC"))
        self.XY_position[0]=0
        self.XY_position[1]=0
        self.XY_position[2]=0
        self.XY_position[3]=0
        print(self.tablist[fram].Mass)

    def Text_Note(self):
        self.Text_On=True

    def Geometry_Rectangle(self):
        self.Text_On=False
        fram=self.notebook.tabs().index(self.notebook.select())
        self.Geometry_Num=2
        self.Geometry=self.tablist[fram].canvans.create_rectangle

    def Geometry_Line(self):
        self.Text_On=False
        fram = self.notebook.tabs().index(self.notebook.select())
        self.Geometry_Num=1
        self.Geometry = self.tablist[fram].canvans.create_line

    def Geometry_Oval(self):
        self.Text_On=False
        fram = self.notebook.tabs().index(self.notebook.select())
        self.Geometry_Num=3
        self.Geometry = self.tablist[fram].canvans.create_oval

    def New_frame(self, XY):
        fram=Frame(self.notebook, xy=XY)
        self.tablist.append(fram)
        self.tablist[self.Num_frame].config(width=self.winfo_screenwidth(),
                                            height=self.winfo_screenheight(), background='blue')
        self.notebook.add(self.tablist[self.Num_frame], text='Note ' + str(self.Num_frame))
        self.W=fram.h
        self.H=fram.h
        self.Num_frame+=1
        i = 0
        g = 0
        self.tablist[self.Num_frame - 1].button_fr = []
        for i in range(XY):
            self.tablist[self.Num_frame - 1].button_fr.append([0] * XY)
            for g in range(XY):
                self.tablist[self.Num_frame - 1].button_fr[i][g] = Button(
                    parent=self.tablist[self.Num_frame - 1].frame_button, y=i, x=g)
                self.tablist[self.Num_frame - 1].button_fr[i][g].grid(row=i, column=g, sticky='news')

    def open_windows(self):
        win = Win(self)
        self.RB=int(win.bk)
        print(self.RB)
        self.New_frame(self.RB)
        

app = App()
app.mainloop()