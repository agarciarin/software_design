#import os.path 
import os

import matplotlib.pyplot as plt
import matplotlib.widgets as widg
#print (dir(widg))
from matplotlib.widgets import TextBox 
import json
import PIL
from tkinter import filedialog as tkFileDialog
from tkinter import *

from fortran import  generate_diagrams as generate_diagrams_fortran
from python  import  generate_diagrams as generate_diagrams_python
from cpp     import  generate_diagrams as generate_diagrams_cpp

from pathlib import Path


class Interface(object):
    def __init__(self):   
        fname = Path("sources", "configuration.ini") 
        with open(fname, 'r') as file:
            self.filedir = json.load(file)
            print (self.filedir)
        try: 
            fname = Path("sources", "excludes.ini") 
            with open(fname, 'r') as fich:
                self.lstExcludes = json.load(fich)
                print ("lstexcludes LOADED")
                print (self.lstExcludes)
                for Exc in self.lstExcludes:
                    self.listExcludes.insert(END,Exc)
                
        except:
            pass

        self.main_window = plt.figure(figsize=(6.,3.), dpi=70)
        butfile_pos = plt.axes([0., 0., 0.25, 0.2])
        self.butfile = widg.Button(butfile_pos, 'Select folder...')
        self.butfile.on_clicked(self.select_dir)

        butdir_pos = plt.axes([0.25, 0., 0.25, 0.2])
        self.butdir = widg.Button(butdir_pos, 'Select main file...')
        self.butdir.on_clicked(self.select_file)

        butupdt_pos = plt.axes([0.5, 0., 0.25, 0.2])
        self.butupdt = widg.Button(butupdt_pos, 'Refresh graphs...')
        self.butupdt.on_clicked(self.update)

        butexc_pos=plt.axes([0.75,0.,0.25,0.2])
        self.butexc=widg.Button(butexc_pos, 'USES excluded')
        self.butexc.on_clicked(self.excludes)
   
        plt.show()
       
        
    def excludes(self,event):
        fname = Path("sources", "excludes.ini") 
        os.startfile(fname)
        
    def select_file(self, event):
        fname = Path("sources", "configuration.ini") 
        with open(fname, mode='r') as fich:
            try:
                filename = tkFileDialog.askopenfilename(
                            title = "Select file to analyze",
                            filetypes=[("FORTRAN files", ".f90"),
                                       ("PYTHON files", ".py"),
                                       ("C++ files", ".cpp"),
                                       ("All files",".*")],
                                       initialdir = self.filedir['dirname'])#json.load(fich)["dirname"])
            except:
                filename = tkFileDialog.askopenfilename(
                            title = "Select file to analyze",
                            filetypes=[("FORTRAN files", ".f90"),
                                       ("PYTHON files", ".py"),
                                       ("All files",".*")])
        try:
            filename = os.path.relpath(filename)
        except:
            pass
            
        if filename:
            self.filedir['filename'] = filename
            fname = Path("sources", "configuration.ini") 
            with open(fname, mode='w') as fich:
                json.dump(self.filedir, fich, indent = 2)

    def select_dir(self, event):
        fname = Path("sources", "configuration.ini") 
        with open(fname, mode='r') as fich:
            try:
                dirname = tkFileDialog.askdirectory(
                                    initialdir = self.filedir['dirname'],#json.load(fich)["dirname"],
                                    title = "Seleccione el directorio de busqueda")
            except:
                dirname = tkFileDialog.askdirectory(
                                    title = "Seleccione el directorio de busqueda")
        try:
            filename = os.path.relpath(dirname)
        except:
            pass
            
        if dirname:
            self.filedir['dirname'] = dirname
            fname = Path("sources", "configuration.ini") 
            with open(fname, mode='w') as fich:
                json.dump(self.filedir, fich, indent = 2)

    #def __grafselect_click(self, label):
    #    self.selected_diagram = label
    #   self.update_diagram()

    def update(self, event):
        
        try: 
            fname = Path("sources", "excludes.ini") 
            with open(fname, 'r') as fich:
                self.lstExcludes = json.load(fich)
                print ("lstexcludes LOADED")
                print (self.lstExcludes)
               
                
        except:
            self.lstExcludes=[]
            print ("lstexcludes EMPTY")
        
        if self.filedir['filename'].lower().endswith(".f90"):
            print("a")
            #generate_diagrams_fortran(self.filedir['filename'], self.filedir['dirname'], self.lstExcludes)

        elif self.filedir['filename'].lower().endswith(".py"):
            generate_diagrams_python(self.filedir['filename'], self.filedir['dirname'], self.lstExcludes)

        elif self.filedir['filename'].lower().endswith(".cpp"):
            generate_diagrams_cpp(self.filedir['filename'], self.filedir['dirname'], self.lstExcludes)

        self.update_diagram()

    def update_diagram(self):
       #img = plt.imread(self.diagrams_dicc[self.selected_diagram])

       fname = "doc" + os.sep +  "graphs" + os.sep + "uses_simplediagram.pdf" 

       
       os.system(fname)
      

    
class Excludes():
    def __init__(self):
        ventana=Tk()
        #~ if  'normal' != ventana.state():
        ventana.geometry("400x350+0+0")
        ventana.title("USES excluded")
        lblExcludes=Label(ventana, text="USES excluded").place(x=20,y=100)
        
        self.listExcludes=Listbox(ventana,width=50)
        self.listExcludes.place(x=20,y=120)
        lblExc=Label(ventana,text="USE ").place(x=20,y=20)
        self.entrada=StringVar()
        self.txtExclude=Entry(ventana,textvariable=self.entrada).place(x=50,y=20)
        
        btnExclude=Button(ventana,text="Exclude",height=2,width=20,command=self.addEx).place(x=200,y=20)
        btnClearAll=Button(ventana,text="Clear list", height=2,width=20, command=self.clearall).place(x=200,y=60)
            
        #~ lstExcludes=[]
            
        try: 
            with open("excludes.ini", 'r') as fich:
                self.lstExcludes = json.load(fich)
                print ("lstexcludes LOADED")
                print (self.lstExcludes)
                for Exc in self.lstExcludes:
                    self.listExcludes.insert(END,Exc)
                
        except:
            self.lstExcludes=[]
            print ("lstexcludes EMPTY")
            
    
        ventana.mainloop()
        #~ interfaz = Interface()
        
    def addEx(self):
        #~ print self.entrada
        print (self.entrada.get())
        self.listExcludes.insert(END,self.entrada.get())
        #~ self.listExcludes.update_idletasks()
        print (self.listExcludes)
        self.lstExcludes=self.listExcludes.get(0, END)
        print (self.lstExcludes)    
        print (self.listExcludes.get(0, END))
        #~ data=json.dumps(self.lstEx
        
        #~ os.system("pause")
        fname = Path("sources", "excludes.ini") 
        with open(fname, mode='w') as fich:
            json.dump(self.lstExcludes, fich)
            print ("SAVED in excludes.ini")
    
    def clearall(self):
        self.listExcludes.delete(0,END)
        self.lstExcludes=[]
        print (self.lstExcludes)
        fname = Path("sources", "excludes.ini") 
        with open(fname, mode='w') as fich:
            json.dump(self.lstExcludes, fich)
            print ("SAVED in excludes.ini")
        
            
if __name__ == '__main__':
    #~ exclude=Excludes()
    interfaz = Interface()
    #interfaz.update_diagram()
    #plt.show()

