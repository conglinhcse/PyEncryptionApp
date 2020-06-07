import Encryption

from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import scrolledtext
from tkinter.messagebox import *
import tkinter as tk
import time


from Crypto.Cipher import DES3
from Crypto import Random
from Crypto.Util import Counter
import sys, os , struct
from Crypto.Hash import SHA 
import hashlib
 
class Root(Tk):
    def __init__(self):
        super(Root, self).__init__()
        self.title("Python Encryption Application")
        self.minsize(800, 450)
        self.key = ''
        self.filename = ''
        self.foldername = ''
 
        self.labelFrame = ttk.LabelFrame(self, text = "Open File")
        self.labelFrame.grid(column = 0, row = 1, padx = 20, pady = 20)
        
        self.makeEntry()
        self.makeProgressBar()
        self.button()
        self.scrolledTextCtrl()
        self.key = self.getKey()
        self.click()

    def makeProgressBar(self):
        self.progress = ttk.Progressbar(orient = HORIZONTAL, length = 600, mode = 'determinate')
        self.progress.place(x= 100, y = 350)
    
    def updateProgresBar(self, value):
        self.progress['value'] = value
        self.progress.update_idletasks() 

 
    def makeEntry(self):
        self.label1 = ttk.Label( text = 'Password')
        self.label1.place(x = 25, y = 10)
        self.entry = ttk.Entry(width = 60, show = '*')
        self.entry.place(x = 200, y = 10)

    def getKey(self):
        return self.entry.get()
 
    def button(self):
        self.button1 = ttk.Button( text = "Select A File ",command = self.fileDialog1)
        self.button1.place(x = 25, y = 60)
        self.button2 = ttk.Button( text = "Select A Folder ",command = self.fileDialog2)
        self.button2.place(x = 25, y = 100)
 
    def fileDialog1(self):

        self.filename = filedialog.askopenfilename(initialdir =  "/", title = "Select A File ")
        self.label1 = ttk.Label( text = "")
        # self.infile = self.filename
        self.label1.place(x = 200, y = 60)
        self.label1.configure(text = self.filename)

    def fileDialog2(self):

        self.foldername = filedialog.askdirectory(initialdir =  "/", title = "Select A Folder", mustexist=True)
        self.label2 = ttk.Label( text = "")
        # self.foldername = self.foldername
        self.label2.place(x = 200, y = 100)
        self.label2.configure(text = self.foldername)
    
    def scrolledTextCtrl(self):
        scroll_w = 92
        scroll_h  = 10
    
        self.scrollText = scrolledtext.ScrolledText(self, width = scroll_w, height = scroll_h)
        self.scrollText.place(x = 25, y = 150)
    
    def click(self):

        self.btn1 = ttk.Button( text="Encrypt", command=self.encryptFile)
        self.btn2 = ttk.Button(text="Decrypt", command=self.decryptFile)
        self.btn3 = ttk.Button( text="Encrypt All", command=self.encryptFolder)
        self.btn4 = ttk.Button( text="Decrypt All", command=self.decryptFolder)
        self.btn1.place(x=200, y=400)
        self.btn2.place(x=300, y=400)
        self.btn3.place(x=400, y=400)
        self.btn4.place(x=500, y=400)

    def encryptFile(self):
        self.key = self.getKey()
        infile = self.filename
        if os.path.exists(infile) and os.path.isfile(infile):
            self.scrollText.insert(tk.INSERT, '********************************************************************************************\n')
            self.scrollText.insert(tk.INSERT, '--------------------------------------------------------------------------------------------\n')
            self.encrypt(self.key, infile)
            self.scrollText.insert(tk.INSERT, '[DONE]:  Encrypt file successfully! Please check it!\n')
            self.scrollText.insert(tk.INSERT, '--------------------------------------------------------------------------------------------\n')
            self.scrollText.insert(tk.INSERT, '********************************************************************************************\n\n')
            showinfo(title='Encrypt A File', message='SUCCESSFULLY!\nEncrypt file {}'.format(infile))
        else: 
            self.scrollText.insert(tk.INSERT, '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n')
            self.scrollText.insert(tk.INSERT, '[FILE NOT EXIST]\n')
            self.scrollText.insert(tk.INSERT, 'Please choose your file again:   \n')
            self.scrollText.insert(tk.INSERT, '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n')
            showerror(title='Encrypt A File', message='ERROR! FILE NOT EXIST!\n{}'.format(infile))
        self.scrollText.configure() 
        return

    def encryptFolder(self):
        self.key = self.getKey()
        folder = self.foldername
        self.scrollText.insert(tk.INSERT, '********************************************************************************************\n')
        if os.path.exists(folder):
            for name in os.listdir(folder):
                infile = os.path.join(folder, name)
                if not os.path.isfile(infile):
                    continue   
                self.scrollText.insert(tk.INSERT, '--------------------------------------------------------------------------------------------\n')
                self.encrypt(self.key, infile)
                self.scrollText.insert(tk.INSERT, '--------------------------------------------------------------------------------------------\n')
                
            self.scrollText.insert(tk.INSERT, '[DONE]:  Encrypt folder successfully! Please check all!\n')
            self.scrollText.insert(tk.INSERT, '********************************************************************************************\n\n')
            showinfo(title='Encrypt A Folder', message='SUCCESSFULLY!\nEncrypt all file in {}'.format(folder))
        else:
            self.scrollText.insert(tk.INSERT, '[FOLDER NOT EXIST]\tPlease check again!\n')
            self.scrollText.insert(tk.INSERT, '********************************************************************************************\n\n')
            showerror(title='Encrypt A Folder', message='ERROR! FOLDER NOT EXIST!\n{}'.format(folder))
        self.scrollText.configure() 
        return


    def decryptFile(self):
        self.key = self.getKey()
        infile = self.filename
        if not os.path.isfile(infile):
            self.scrollText.insert(tk.INSERT, '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n')
            self.scrollText.insert(tk.INSERT, '[FILE NOT EXIST]\n')
            self.scrollText.insert(tk.INSERT, 'Please choose your file again:   \n')
            self.scrollText.insert(tk.INSERT, '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n')
            self.scrollText.configure() 
            showerror(title='Decrypt A File', message='ERROR! FILE NOT EXIST!\n{}'.format(infile))
            return
        if infile.split('.')[-1] != 'cyp':
            self.scrollText.insert(tk.INSERT, '********************************************************************************************\n')
            self.scrollText.insert(tk.INSERT, '--------------------------------------------------------------------------------------------\n')
            self.scrollText.insert(tk.INSERT, '[ERROR]: This is not encrypted file. Please choose file with ".cyp" at the end! \n')
            self.scrollText.insert(tk.INSERT, '--------------------------------------------------------------------------------------------\n')
            self.scrollText.insert(tk.INSERT, '********************************************************************************************\n\n')
            self.scrollText.configure() 
            showerror(title='Decrypt A File', message='ERROR! NON-ENCRYPTED FILE!\n{}'.format(infile))
            return

        if os.path.exists(infile):
            self.scrollText.insert(tk.INSERT, '********************************************************************************************\n')
            self.scrollText.insert(tk.INSERT, '--------------------------------------------------------------------------------------------\n')
            check = self.decrypt(self.key, infile)
            if not check:
                self.scrollText.insert(tk.INSERT, '[ERROR]\tWRONG PASSWORD!\n')
                self.scrollText.insert(tk.INSERT, 'Can not decrypt this file! Please check again!\n')
                self.scrollText.insert(tk.INSERT, '--------------------------------------------------------------------------------------------\n')
                self.scrollText.insert(tk.INSERT, '********************************************************************************************\n\n')
                showerror(title='Decrypt A File', message='     WRONG PASSWORD      ')
            else:
                self.scrollText.insert(tk.INSERT, '[DONE]:  Decrypt file successfully! Please check it!\n')
                self.scrollText.insert(tk.INSERT, '--------------------------------------------------------------------------------------------\n')
                self.scrollText.insert(tk.INSERT, '********************************************************************************************\n\n')
                showinfo(title='Decrypt A File', message='SUCCESSFULLY!\nDecrypt file {}'.format(infile))
        else:
            self.scrollText.insert(tk.INSERT, '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n')
            self.scrollText.insert(tk.INSERT, '[ERROR]\tCan not decrypt this file! Please check again!\n')
            self.scrollText.insert(tk.INSERT, '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n')
            showerror(title='Decrypt A File', message='ERROR! FILE NOT EXITS {}'.format(infile))
        self.scrollText.configure() 
        return

    def decryptFolder(self):
        self.key = self.getKey()
        folder = self.foldername
        self.scrollText.insert(tk.INSERT, '********************************************************************************************\n')
        self.scrollText.insert(tk.INSERT, '[NOTICE]: Only decrypting file with ".cyp" at the end!\n\n')
        showwarning(title='Decrypt A Folder', message='NOTICE! Only decrypting file with ".cyp" at the end')
        if os.path.exists(folder):
            for name in os.listdir(folder):
                infile = os.path.join(folder, name)
                if not os.path.isfile(infile):
                    continue
                if infile.split('.')[-1] != 'cyp':
                    continue   
                self.scrollText.insert(tk.INSERT, '--------------------------------------------------------------------------------------------\n')
                check = self.decrypt(self.key, infile)
                if not check:
                    self.scrollText.insert(tk.INSERT, '[ERROR]\tWRONG PASSWORD!\n')
                    self.scrollText.insert(tk.INSERT, 'This password is not suitable for this file!\n')
                    self.scrollText.insert(tk.INSERT, '{}\n'.format(infile))
                self.scrollText.insert(tk.INSERT, '--------------------------------------------------------------------------------------------\n')
                
            self.scrollText.insert(tk.INSERT, '[DONE]:  Decrypt folder successfully! Please check all!\n')
            self.scrollText.insert(tk.INSERT, '********************************************************************************************\n\n')
            showinfo(title='Decrypt A Folder', message='SUCCESSFULLY!\nDecrypt all file in {}'.format(folder))
        else:
            self.scrollText.insert(tk.INSERT, '[FOLDER NOT EXIST]\tPlease check again!\n')
            self.scrollText.insert(tk.INSERT, '********************************************************************************************\n\n')
            showerror(title='Decrypt A Folder', message='ERROR! FOLDER NOT EXIST!\n{}'.format(folder))
        self.scrollText.configure() 
        return

    def encrypt(self, key, infile, size_file = 4096):

        (fsz, size_file, outfile, count) = Encryption.encrypt(key, infile)
        self.scrollText.insert(tk.INSERT, '[File Name]:\t{}\n'.format(infile))
        progress =0
        while count > 0:
            progress += (size_file/fsz)*100
            self.updateProgresBar(progress)
            count -= 1
            time.sleep(0.0005)
        self.progress['value'] = 0
        self.scrollText.insert(tk.INSERT, '[SIZE OF FILE]:\t{}\n'.format(fsz))
        self.scrollText.insert(tk.INSERT, 'Encrypted file located:\t{}\n'.format(outfile))
        self.scrollText.configure() 
        return

    def decrypt(self, key, infile, size_file = 4096):
        key = self.getKey()
        (check, fsz, size_file, outfile, count) = Encryption.decrypt(key, infile)
        if not check:
            return check
        progress = 0
        while count > 0:
            progress+= (size_file/fsz)*100
            self.updateProgresBar(progress)                    
            count -= 1
            time.sleep(0.0005)
        self.scrollText.insert(tk.INSERT, '[SIZE OF FILE]:\t{}\n'.format(fsz))
        self.scrollText.insert(tk.INSERT, 'Decrypted file located:\t{}\n'.format(outfile))
        self.scrollText.configure() 
        self.progress['value'] = 0
        self.verifyFile(infile, outfile)
        return check

    def verifyFile(self, originalFile, outfile):
        (check, hashOriginalFile, hashOutFile) = Encryption.verifyFile(originalFile, outfile)
        self.scrollText.insert(tk.INSERT, '[PRE HASH]:\t{}\n'.format(hashOriginalFile))
        self.scrollText.insert(tk.INSERT, '[NET HASH]:\t{}\n'.format(hashOutFile))
        if check:
            self.scrollText.insert(tk.INSERT, '[AUTHEN]:\tThe integrity is ensured!\n')
        else:
            self.scrollText.insert(tk.INSERT, '[WARNING]:\tData had been changed! Please check again carefully!\n')
        self.scrollText.configure() 



if __name__ == "__main__":
    root = Root()
    root.mainloop()