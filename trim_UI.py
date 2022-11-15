import os
from tkinter import *
from tkinter import filedialog
root = Tk()
root.geometry("720x320")
root.title('mp4-Trimmer')
root.iconbitmap('mfix.ico')

root.rowconfigure([0,1,2],weight=1)
root.columnconfigure([0,1,2,3,4,5],weight=1)

def file_select():
    root.filename = filedialog.askopenfilename(title="Datei auswählen")
    path.delete(0,END)
    path.insert(0,root.filename)

def validate_entry():
    file = path.get()
    try:
        os.chdir(os.path.dirname(file))
        hh = int(float(h.get()))
        mm = int(float(m.get()))
        ss = int(float(s.get()))
        if ss <0 or ss>59 or mm<0 or mm>59 or hh<0:
            return False
        else:
            return hh,mm,ss
    except:
        return False       

def trim_video():
    file = path.get() 
    status.grid_forget()
    try:
        hh,mm,ss = validate_entry()
        cmd = f"echo Y|ffmpeg -i {file} -ss 00:00:00 -t {hh}:{mm}:{ss} -c:v copy -c:a copy {file.split('.')[0]}_edited.mp4"
        os.system(cmd)      
        status['text'] = "Erfolgreich abgeschlossen!"
        status.grid(row=3,column=0)
        
    except:
        status['text'] = "Bitte überprüfen Sie die übergebenen Parameter"
        status.grid(row=3,column=0)
    return

path = Entry(root, width=20,borderwidth=5,border=2)
path.grid(row=0,column=0,columnspan=6,rowspan=1,padx=10,pady=10,sticky='ew')
path.insert(0, 'Wählen Sie die mp4-Datei')

file_button = Button(root, text="browse", command=file_select)
file_button.grid(row=0, column=6, padx=5,pady=5,columnspan=2,sticky='ew')

h_label =Label(root,text="HH")
h_label.grid(row=1,column=0,padx=2,pady=2,sticky='ew')

h = Entry(root,width=2, borderwidth=5)
h.grid(row=1, column=1, padx=2, pady=2, sticky='ew')
h.insert(0,'00')

m_label =Label(root,text="MM")
m_label.grid(row=1,column=2,padx=2,pady=2,sticky='ew')

m = Entry(root,width=2, borderwidth=5)
m.grid(row=1, column=3, padx=5, pady=2, sticky='ew')
m.insert(0,'00')

s_label =Label(root,text="SS")
s_label.grid(row=1,column=4,padx=2,pady=2,sticky='ew')

s = Entry(root,width=2, borderwidth=5)
s.grid(row=1, column=5, padx=2, pady=2, sticky='ew')
s.insert(0,'00')

trim_button = Button(root, text = 'trim video', command=trim_video)
trim_button.grid(row=2,column=2, padx=5,pady=5, sticky='ew',rowspan=2)

status= Label(root)
status.grid(row=3,column=0,sticky='nsew')

root.mainloop()