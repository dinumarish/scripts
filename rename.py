
import os
from datetime import timedelta
from tinytag import TinyTag
from math import floor
import sys

def renameVideos(files,only_docfile=False):    

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

    with open('doc.txt', 'w') as fhand:
        fhand.seek(0,0)
        for item in sorted(lc.items())[1:]:
            fhand.write(str(item).replace('(','').replace(')','').replace(',',':')+"\n")
        fhand.write(content)

    if not only_docfile:
        print('Dateinamenänderungen, abgeschlossen!!')
    else:
        print(f"doc.txt-Datei im {os.getcwd()} mit den Videodauerangaben gespeichert")

def revertNames(files):
    for file in files:
        os.rename(file,file.split('.')[0]+'.mp4')
    print(f'Umkehrung von Dateinamen erfolgreich für Verzeichnis in')


arg = sys.argv
files = list(filter(lambda x: x.endswith('mp4'),os.listdir()))

if len(arg)==1:
    renameVideos(files,only_docfile=True)

elif len(arg)==2 and arg[1].lower()=='p':
    renameVideos(files)

elif len(arg)==2 and arg[1].lower()=='r':
    revertNames(files)

else:
    print("""
    Das Skript akzeptiert nur 'p' oder 'r'
    'p' für die Umbenennung von mp4-Dateien gemäß der pppv-Konvention und 
    'r' für die Umkehrung der pppv-Namen in ihre ursprünglichen Namen""")
