from tkinter import *
from tkinter import filedialog
import tkSimpleDialog

class ATG_Import(tkSimpleDialog.Dialog):

    def body(self, master):

        self.option = StringVar(master)
        self.option.set("Address")
        self.menu = OptionMenu(master, self.option, "Address", "Data", "Mask", "Control")
        self.menu.grid(row=0, sticky=E)

        self.file = StringVar(master)
        self.fileentry = Entry(master, textvariable=self.file)
        self.fileentry.grid(row=0, column=1)

        self.browse = Button(master, text='Browse...', command=self.browse_cb)
        self.browse.grid(row=0, column=2, padx=20)

        return self.menu

    def browse_cb(self):
        filename=filedialog.askopenfilename(defaultextension='.coe')
        self.file.set(filename)

    def apply(self):
        self.result = {'column': self.option.get().lower(), 'filename': self.file.get()}

if __name__ == '__main__':
    root = Tk()
    ATG_Import(root, 'File import')
    root.mainloop()

