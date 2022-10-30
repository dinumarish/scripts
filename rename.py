
import os
from datetime import timedelta
from tkinter import N
from tinytag import TinyTag
from math import floor
import sys

def renameVideos(files):    

    excesslength = {
                    range(1,15):'',
                    range(15,31):'Ü1',
                    range(31,70):'Ü2',
                    range(71,121):'Ü3',
                    range(121,500):'Ü4',
                    range(500,50000):'Ü5'
                   }
    lc = {}
    title = os.getcwd().split("\\")[-1]
    fhand = open('doc.txt','w')
    fhand.write(title+'\n'+'Re:\n')

    for file in files:
        video = TinyTag.get(file)
        duration = floor(video.duration)
        duration = timedelta(seconds=duration)
        category = duration.seconds
        
        for k,v in excesslength.items():
            if category in k:
                category = v
                lc[v] = lc.get(v,0) + 1
        h,m,s=str(duration).split(':')
        if len(h)==1:
            h='0'+h
        
        os.rename(file,file.split('.')[0]+'.'+h+m+s+'.mp4')
        fhand.write(file.split('_')[0]+' vereizeilt leichte BS '+category+'\n')

        #os.system(f"copy {file} {file.split('.')[0]+'.'+h+m+s+'.mp4'}")
        #print(file.split('.')[0]+'.'+h+m+s+'.mp4')
    
    fhand.write(str(lc))
    fhand.close()
    print('Dateinamenänderungen, abgeschlossen!!')
    

def revertNames(files):
    for file in files:
        os.rename(file,file.split('.')[0]+'.mp4')
    print(f'Umkehrung von Dateinamen erfolgreich für Verzeichnis in')

arg = sys.argv
files = list(filter(lambda x: x.endswith('mp4'),os.listdir()))

if len(arg)==1:
    renameVideos(files)

elif len(arg)==2 and arg[1].lower()=='p':
    renameVideos(files)

elif len(arg)==2 and arg[1].lower()=='r':
    revertNames(files)

else:
    print("""
    Das Skript akzeptiert nur 'p' oder 'r'
    'p' für die Umbenennung von mp4-Dateien gemäß der pppv-Konvention und 
    'r' für die Umkehrung der pppv-Namen in ihre ursprünglichen Namen""")
   

