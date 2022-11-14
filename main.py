import os
from datetime import timedelta
from tinytag import TinyTag
from math import floor
from tkinter import *


root = Tk()
root.title("Digi-Post-Prozessor")
root.geometry("720x280")
root.iconbitmap('mfix.ico')
result =Label(root,font=10)
result.grid(row=2, column=0,columnspan=3,sticky='nsew')

def renameVideos(path,only_docfile=False):    

    global result  
    result.grid_forget()
    
    current = path.get()
    try:
        os.chdir(current)
        
    except:
        result['text'] ="Bitte geben Sie einen gültigen Pfad ein"
        result.grid(row=2, column=0, columnspan=3)
        return
        
    files = list(filter(lambda x: x.endswith('mp4'),os.listdir()))
    files.sort(key=lambda x:int(x.split('_')[0]))

    excesslength = {
                    range(0,94):'',
                    range(94,184):'Ü1',
                    range(184,244):'Ü2',
                    range(244,304):'Ü3',
                    range(304,364):'Ü4',
                    range(364,50000):'Ü5'
                   }
    lc = {}
    title = os.getcwd().split("\\")[-1]
    fhand = open('doc.txt','w')
    fhand.write(title+'\n'+'Re:\n')

    for file in files:
        video = TinyTag.get(file)
        duration = floor(video.duration)
        duration = timedelta(seconds=duration)
        category = duration.seconds//60
        
        for k,v in excesslength.items():
            if category in k:
                category = v
                lc[v] = lc.get(v,0) + 1
                break
        
        fhand.write('#'+file.split('_')[0]+' vereizeilt leichte BS '+category+'\n')

        if not only_docfile:
            h,m,s=str(duration).split(':')
            if len(h)==1:
                h='0'+h
            os.rename(file,file.split('.')[0]+'.'+h+m+s+'.mp4')

        #os.system(f"copy {file} {file.split('.')[0]+'.'+h+m+s+'.mp4'}")
        #print(file.split('.')[0]+'.'+h+m+s+'.mp4')
    
    fhand.close()

    with open('doc.txt','r') as fhand:
        content = fhand.read()
    try:
        lc['Ü4']+=lc['Ü5']
        lc = sorted(lc.items())[1:]

    except:
        lc = sorted(lc.items())[1:]

    with open('doc.txt', 'w') as fhand:
        fhand.seek(0,0)
        for item in lc:
            fhand.write(str(item).replace('(','').replace(')','').replace(',',':')+"\n")
        fhand.write(content)

    if not only_docfile:
        
        result['text']="Dateinamenänderungen, abgeschlossen!!"
        result.grid(row=2,column=0,columnspan=3)
    else:
        
        result['text']=f"doc.txt-Datei im {os.getcwd()} \n mit den Videodauerangaben gespeichert"
        result.grid(row=2,column=0,columnspan=3)
    

def revertNames(path):
    global result
    result.grid_forget()   
    current = path.get()
    try:
        os.chdir(current)
    except:
        result['text'] ="Bitte geben Sie einen gültigen Pfad ein"
        result.grid(row=2,column=0, columnspan=3)
        return 
    files = list(filter(lambda x: x.endswith('mp4'),os.listdir()))
    files.sort(key=lambda x:int(x.split('_')[0]))
    for file in files:
        os.rename(file,file.split('.')[0]+'.mp4')
    
    result['text']="Umkehrung von Dateinamen erfolgreich für Verzeichnis"
    result.grid(row=2,column=0,columnspan=3)
    return



#create an entry box for getting directory path
path = Entry(root, width=50, borderwidth=5)
path.grid(row=0, column=0, columnspan=3,padx=10, pady=10,sticky='nsew')
path.insert(0, 'Ordnerpfad eingeben')

button_doc = Button(root, width=10,text="Doc", command=lambda: renameVideos(path, only_docfile=True)).grid(row=1,column=0, padx=15, pady=15,sticky='nsew')
button_pppv = Button(root, width=10,text="PPPV", command=lambda: renameVideos(path)).grid(row=1,column=1, padx=15, pady=15,sticky='nsew')
button_revert = Button(root, width=10,text="Umkehrung", command=lambda: revertNames(path)).grid(row=1,column=2, padx=15, pady=15,sticky='nsew')

root.rowconfigure([0,1],weight=1)
root.columnconfigure([0,1,2],weight=1)
root.mainloop()

