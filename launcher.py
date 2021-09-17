from tkinter import *
from pdf import *
from PyQt5.QtWidgets import QApplication
import sys
from functools import partial 
from summariser import Summarize
from os import system
from PIL import ImageTk,Image

def merge():
    app = QApplication(sys.argv)
    pdf = PDF()
    pdf.pdfmerger()
    del pdf

def split():
    app = QApplication(sys.argv)
    pdf = PDF()
    pdf.pdfsplitter()
    del pdf

def rotate_box():
    popup = Toplevel()
    popup.configure(bg='#9999ff')
    popup.title('Rotation Parameters')
    popup.geometry("400x400")

    number1 = IntVar()  
  
    rlabel = Label(popup,text='Degree to rotate -- Enter multiples of 90',bg='white',fg='blue')
    rlabel.grid(row=1,column=0,padx=10,pady=10)
    rot = Entry(popup,width=10,textvariable=number1)
    rot.grid(row=2,column=0,padx=10,pady=10)

    rlabel = Label(popup,text='Direction to Rotate ',bg='white',fg='blue')
    rlabel.grid(row=4,column=0,padx=10,pady=10)
    CheckVar1 = IntVar()

    C1 = Radiobutton(popup, text = 'Clockwise', variable = CheckVar1,
        value = 1).grid(row=5,column=0,padx=10,pady=10)

    C2 = Radiobutton(popup, text = 'CounterClockwise', variable = CheckVar1,
        value = 2).grid(row=6,column=0,padx=10,pady=10)

    rbutton = Button(popup,text='Done',command = partial(rotate,number1,popup,CheckVar1) ,width=50,bg='black',fg='blue')
    rbutton.grid(row=7,column=0,padx=10,pady=10)

def rotate(n1,pp,dir):
    app = QApplication(sys.argv)
    pdf = PDF()
    pp.destroy()
    if dir==1:
        pdf.rotatepdf(n1.get(),flag ='CW')
    else:
        pdf.rotatepdf(n1.get(),flag='CCW')
    
    del pdf
    
def summarise():
    popup = Toplevel()
    popup.configure(bg='#9999ff')
    popup.title('Save Confirmation')
    popup.geometry("400x400")

    CheckVar1 = IntVar()
    rlabel = Label(popup,text='Save',bg='white',fg='blue')
    rlabel.grid(row=1,column=0,padx=10,pady=10)

    C1 = Radiobutton(popup, text = 'Yes', variable = CheckVar1,
        value = 1).grid(row=1,column=0,padx=10,pady=10)
    C2 = Radiobutton(popup, text = 'No', variable = CheckVar1,
        value = 2).grid(row=2,column=0,padx=10,pady=10)

    rbutton = Button(popup,text='Done',command = partial(summa,popup,CheckVar1) ,width=50,bg='black',fg='blue')
    rbutton.grid(row=7,column=0,padx=10,pady=10)


def summa(pp,CheckVar1):
    app = QApplication(sys.argv)
    pdf = PDF()
    summ = Summarize()
    filelines =  summ.get_file_and_lines()
    pp.destroy()
    if filelines != None:
        summ.load_spacy_nlp(filelines)
        word_frequency = summ.word_frequency_count()
        sentence_scores = summ.sentence_score_computer(word_frequency)
        summary = summ.summariser(sentence_scores)
        fn = filelines.split(' ')
        sn = summary.split(' ')
        print()
        print(Fore.GREEN,f"Word count before summary: {len(fn)}")
        print()
        print(Fore.MAGENTA,"Summary:")
        print(Fore.YELLOW,f"{summary}")
        print()
        print(Fore.GREEN,f"Word count after summary: {len(sn)}")
        print()

        if CheckVar1 == 1:
            file = pdf.saveFileDialog()
            base = os.path.basename(file) + '.txt'
            path = os.path.join(os.path.dirname(file),base)
            with open(path,'w+') as file:
                file.write(summary)
                print(f'File written at {file}')
    del pdf
    
    
def convert():
    app = QApplication(sys.argv)
    pdf = PDF()
    pdf.doctopdf()
    del pdf



system('cls')
root = Tk()
root.configure(bg='#9999ff')
root.title('AstutePDF')
root.geometry("400x550")


label = Label(root,text='What would you like to do? ',bg='black',fg='white')
label.grid(row=1,column=0,padx=10,pady=10)
mbutton = Button(root,text='Merge',command = merge,width=50,bg='white',fg='blue')
mbutton.grid(row=2,column=0,padx=10,pady=10)

sbutton = Button(root,text='Split',command = split,width=50,bg='white',fg='blue')
sbutton.grid(row=3,column=0,padx=10,pady=10)

rbutton = Button(root,text='Rotate',command = rotate_box,width=50,bg='white',fg='blue')
rbutton.grid(row=6,column=0,padx=10,pady=10)

obutton = Button(root,text='Summarise',command = summarise,width=50,bg='white',fg='blue')
obutton.grid(row=7,column=0,padx=10,pady=10)

dbutton = Button(root,text='Convert Docx to PDF',command = convert,width=50,bg='white',fg='blue')
dbutton.grid(row=8,column=0,padx=10,pady=10)


img = Image.open('./Csclogo.png')
img = img.resize((250,250))
img = ImageTk.PhotoImage(img)
panel = Label(root, image = img)
panel.grid(row=10,column=0)

root.mainloop()