######################################
## PBM-Editor (c)2020 Johannes Harz ##
######################################

from tkinter import *
from tkinter import filedialog as fd
from tkinter import simpledialog as sd
import math
import io



root = Tk()
root.title("PBM Creator")

def bitstring_to_bytes(s):
    return int(s, 2).to_bytes(len(s) // 8, byteorder='big')

def changeSize():
    global h,mx,my,w,pixels
    ht = sd.askinteger("Pixelbreite eingeben","Pixelbreite (1-3")
    if not type(ht) is int:
        ht = 1
    if ht >3:
        ht =3
    if ht<0:
        ht=0
    h = ht
    w = math.ceil(3*h)
    for y in range(my-1,-1,-1):
        for x in range(mx-1,-1,-1):
            b = pixels[y][x]
            b.config(height=h,width=w)

def reset():
    global mx
    global my
    global pixels,w,h
    for y in range(my-1,-1,-1):
        for x in range(mx-1,-1,-1):
            b = pixels[y][x]
            b.destroy()
    
    xt = sd.askinteger("Breite eingeben","x=")
    if not type(xt) is int:
        xt = 10
    mx = min(xt,50)
    yt = sd.askinteger("Höhe eingeben","y=")
    if not type(yt) is int:
        yt = 10
    my = min(yt,50)
    
    pixels = []           
    for y in range(0,my):
        rows = []
        pixels.append(rows)
        for x in range(0,mx):
            button = Button(bg='white',text='', relief=RIDGE,width=w, height=h, command= lambda x=x,y=y: changeColor(x,y))
            button.grid(row=y,column=x)
            rows.append(button) 
            

def printfile():
    filename = fd.asksaveasfilename(defaultextension=".pbm", initialdir = "/",title = "Select file",filetypes = (("PBM Dateien","*.pbm"),("all files","*.*")))
    if filename!="":
        file = open(filename,"w")
        #file = open("test.pbm","w") 
        file.write("P1\n") 
        file.write(str(mx)+" "+str(my)+"\n")
        for y in range(0,my):
            r=""
            for x in range(0,mx):
                b = pixels[y][x]
                if b["bg"]=="white":
                    p="0"
                else:
                    p="1"
                r=r+p
            file.write(r)
            if y!= my:
                file.write("\n")
        file.close()

def printfile4():
    filename = fd.asksaveasfilename(defaultextension=".pbm", initialdir = "/",title = "Select file",filetypes = (("PBM Dateien","*.pbm"),("all files","*.*")))
    if filename!="":
        file = io.open(filename,"w",encoding = 'ANSI', newline='\n')
        #file = open("test.pbm","w") 
        file.write("P4\n") 
        file.write(str(mx)+" "+str(my)+"\n")
        rowlength = math.ceil(mx/8)
        file.close()
        file=io.open(filename,"ab")
        result=""
        for y in range(0,my):
            binary=""
            for x in range(0,mx):
                cur=x%8 
                b = pixels[y][x]
                if b["bg"]=="white":
                    p="0"
                else:
                    p="1"
                binary=binary+p
                if cur==7 or x==mx-1:
                    for i in range(cur,7):
                        binary=binary+"0"
                    byte = bitstring_to_bytes(binary)
                    #print(binary)
                    #binary = int(binary,2)
                    #print(binary)
                    #binary = hex(binary)[2:]
                    #print(binary[2:])
                    #byte = bytes.fromhex(binary)
                    file.write(byte)
                    binary=""
        #length = math.ceil(len(binary)/8)
        #print(result)
        #print(length)
        #result = ""
        #for i in range(0,length):
            #part = i*8
            #byte = binary[part:part+7]
            #result = result+chr(int(byte,2))     
        file.close()


def showCode():
    
    def showImage(data):
        #print(data.split())
        lines = data.split()
        global mx
        global my
        global pixels,w,h
        for y in range(my-1,-1,-1):
            for x in range(mx-1,-1,-1):
                b = pixels[y][x]
                b.destroy() 
        
        mx = int(lines[0])
        my = int(lines[1])
        
        pixels = []  
        for y in range(0,my):
            rows = []
            pixels.append(rows)
            for x in range(0,mx):
                button = Button(bg='white',text='', relief=RIDGE,width=w, height=h, command= lambda x=x,y=y: changeColor(x,y))
                button.grid(row=y,column=x)
                rows.append(button) 
    
        for y in range(2,my+2):
                for x in range(0,mx):
                    b = pixels[y-2][x]
                    if lines[y][x]=="1":
                        b.config(bg="black")
                    else:
                        b.config(bg="white")
    
    def checkImage(data):
        lines = data.split()
        ix = int(lines[0])
        iy = int(lines[1])
        if ix>0 and iy>0:
            
            if iy == len(lines)-2:
                b = True
                for y in range(2,iy+2):
                    if len(lines[y])!=ix:
                        b = False      
                    if b:
                        for x in range(0,ix):
                            if lines[y][x] not in ["0","1"]:
                                b = False
                if b:
                    showImage(data)
    
    code = "P1\n"
    code = code + str(mx)+" "+str(my)+"\n"
    for y in range(0,my):
            r=""
            for x in range(0,mx):
                b = pixels[y][x]
                if b["bg"]=="white":
                    p="0"
                else:
                    p="1"
                r=r+p
            code = code+r
            if y!= my:
                code = code+"\n"

    #print(code)
    cwin = Tk()
    cwin.title("Codierung")
    codetext = Text(cwin)
    codetext.insert(INSERT,code)
    codetext.pack()
    b = Button(cwin,text="Codierung ausblenden",command=cwin.destroy)
    b.pack()
    b2 = Button(cwin,text="Bild aus Codierung erzeugen",command=lambda codetext=codetext: checkImage(codetext.get("2.0","end-1c")))
    b2.pack()
    
    cwin.mainloop()
    

def readfile():
    global mx
    global my
    global pixels,h,w
    
    filename = fd.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("PBM Dateien","*.pbm"),("all files","*.*")))
    if filename!="":
        for y in range(my-1,-1,-1):
            for x in range(mx-1,-1,-1):
                b = pixels[y][x]
                b.destroy()
            
    
        file = open(filename,"r",encoding = 'ANSI')
        lines = file.readlines()
        fileformat = lines[0].split()
        size = lines[1].split()
        mx = int(size[0])
        my = int(size[1])
    
        pixels = []           
        for y in range(0,my):
            rows = []
            pixels.append(rows)
            for x in range(0,mx):
                button = Button(bg='white',text='', relief=RIDGE,width=w, height=h, command= lambda x=x,y=y: changeColor(x,y))
                button.grid(row=y,column=x)
                rows.append(button)
        print (fileformat[0])
        if fileformat[0] == "P1":
            y = 0
            for line in lines:
                if y>1:
                    for x in range(0,mx):
                        b = pixels[y-2][x]
                        if line[x]=="1":
                            b.config(bg="black")
                        else:
                            b.config(bg="white")
                y=y+1
        
        if fileformat[0] == "P4":
            file.close()
            bpl = (mx//8)+1 #bytes per line
            print("Bytes per Line: "+ str(bpl))
            with open(filename,"rb") as f:
                byte = f.read(1)
                start=0
                line=0
                cb=0
                while byte:
                    if start>1:
                        b = "{:08b}".format(int(byte.hex(),16))
                        for x in range(0,8):
                            if (cb*8+x)<mx:
                                button = pixels[line][cb*8+x]
                                if b[x]=="1":
                                    button.config(bg="black")
                                else:
                                    button.config(bg="white")
                        cb=(cb+1)%bpl
                        print(cb)
                        if (cb==0):
                            line=line+1
                            
                    if byte==b"\n":
                        start=start+1
                    byte = f.read(1)

def about():
    ab = Tk()
    ab.title("Über dieses Programm")
    l = Label(ab,text="Geschrieben von Johannes Harz, (c)2020")
    l.pack()
    b = Button(ab,text="Schließen",command=ab.destroy)
    b.pack()
    ab.mainloop()


menu= Menu(root)
root.config(menu=menu)
filemenu=Menu(menu)
menu.add_cascade(label="Datei", menu=filemenu)
filemenu.add_command(label="Neu", command=reset)
filemenu.add_command(label="Öffnen", command=readfile)
filemenu.add_command(label="Zeige Codierung", command=showCode)
filemenu.add_command(label="Speichern (ASCII)", command=printfile)
filemenu.add_command(label="Speichern (binär)", command=printfile4)
filemenu.add_command(label="Pixelgröße ändern",command=changeSize)
filemenu.add_command(label="Über dieses Programm",command=about)
filemenu.add_command(label="Schließen", command=root.quit)

def changeColor(x,y):
    global pixels
    b = pixels[y][x]
    if b["bg"]=="white":
        b.config(bg="black")
    else:
        b.config(bg="white")


mx = 6
my = 4
h=2
w=5
pixels = []           
for y in range(0,my):
    rows = []
    pixels.append(rows)
    for x in range(0,mx):
        button = Button(bg='white',text='', relief=RIDGE,width=w, height=h, command= lambda x=x,y=y: changeColor(x,y))
        button.grid(row=y,column=x)
        rows.append(button)
root.resizable(False,False)
root.mainloop()