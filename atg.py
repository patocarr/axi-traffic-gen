#!/usr/bin/env python3

# This Python/Tk script allows editing of data intended to be used by the
# Xilinx AXI Traffic Generator IP by generating .coe files from the input data.

import pickle
from tkinter import *

PROGRAM_NAME = 'AXI Traffic Generator'
MAX_ROWS = 25

class Application:
    def __init__(self, root):
        self.root = root
        self.root.title(PROGRAM_NAME)
        self.init_vars()
        self.createWidgets()
        self.root.grid()

    def init_vars(self):
        self.axi_lite_type = IntVar()
        self.rows = [ \
                { \
                'check': 0, \
                'is_read': 0, \
                'ok_next_addr': 0, \
                'err_next_addr': 0, \
                'address': 0, \
                'data': 0, \
                'expdata': 0, \
                'mask': 0 \
                } \
                for k in range(MAX_ROWS)]

    def callback(self, event):
        print (event)

    def createWidgets(self):
        type_frame = Frame(self.root, height=15, bd=5, relief=GROOVE, padx=5, pady=5)
        self.gentype = Radiobutton(type_frame, \
                text="System Init (only writes)", \
                variable=self.axi_lite_type, value=0).grid(sticky=W)
        self.gentype = Radiobutton(type_frame, \
                text="Test Mode (read and writes allowed)", \
                variable=self.axi_lite_type, value=1).grid(sticky=W)
        type_frame.grid(row=0, column=0)

        text_frame = Frame(self.root, bd=5, relief=GROOVE, padx=15, pady=15)
        Label(text_frame, text="Entry").grid(column=0,row=0)
        Label(text_frame, text="Address").grid(column=1,row=0)
        Label(text_frame, text="Data").grid(column=2,row=0)
        Label(text_frame, text="Read?").grid(column=3,row=0)
        Label(text_frame, text="Expected").grid(column=4,row=0)
        Label(text_frame, text="Mask").grid(column=5,row=0)

        for i in range(MAX_ROWS):
            Label(text_frame, text=i).grid(column=0,row=i+5)

            self.rows[i]['address'] = StringVar()
            addr = Entry(text_frame, \
                    textvariable=self.rows[i]['address'] \
                    ).grid(column=1,row=i+5)

            self.rows[i]['data'] = StringVar()
            data = Entry(text_frame,  \
                    textvariable=self.rows[i]['data'] \
                    ).grid(column=2,row=i+5)

            self.rows[i]['is_read'] = BooleanVar()
            read = Checkbutton(text_frame, \
                    variable=self.rows[i]['is_read'] \
                    ).grid(column=3,row=i+5)

            self.rows[i]['expdata'] = StringVar()
            data = Entry(text_frame,  \
                    textvariable=self.rows[i]['expdata'] \
                    ).grid(column=4,row=i+5)

            self.rows[i]['mask'] = StringVar()
            data = Entry(text_frame,  \
                    textvariable=self.rows[i]['mask'] \
                    ).grid(column=5,row=i+5)

        text_frame.grid(row=6, columnspan=5)

        buttons_frame = Frame(self.root, bd=5, relief=GROOVE, padx=5, pady=5)
        self.quitButton = Button(buttons_frame, text='Quit', command=quit)
        self.quitButton.grid(row=0, column=0, padx=20)
        self.loadButton = Button(buttons_frame, text='Load', command=self.loadFile)
        self.loadButton.grid(row=0, column=1, padx=20)
        self.saveButton = Button(buttons_frame, text='Save', command=self.saveFile)
        self.saveButton.grid(row=0, column=2, padx=20)
        self.dumpButton = Button(buttons_frame, text='Dump .coe', command=self.dumpCoe)
        self.dumpButton.grid(row=0, column=3, padx=20)
        buttons_frame.grid()

    def to_hex(self, string):
        if string == '':
            string = '0'
        try:
            int_val = int(string,16)
        except:
            print ("There was a problem translating a string to hex")
            int_val = 0
        hex_str = "{0:08x}".format(int_val)
        return hex_str

    def writeCoe(self, filetype, array):
        with open(filetype+'.coe', 'wb') as f:
            f.write('memory_initialization_radix = 16;\n'.encode())
            f.write('memory_initialization_vector =\n'.encode())
            for row in array:
                f.write(row.encode())
                f.write('\n'.encode())
            f.write(';\n'.encode())

    def dumpCoe(self):
        addr_db = []
        data_db = []
        mask_db = []
        expdata_db = []
        for i, row in enumerate(self.rows):
            addr_db.append(self.to_hex(row['address'].get()))
            data_db.append(self.to_hex(row['data'].get()))
            mask_db.append(self.to_hex(row['mask'].get()))
            expdata_db.append(self.to_hex(row['expdata'].get()))

        self.writeCoe('addr', addr_db)
        self.writeCoe('data', data_db)
        if self.axi_lite_type.get() > 0:
            self.writeCoe('mask', mask_db)
            self.writeCoe('expdata', expdata_db)

    def saveFile(self):
        sav = []
        for i in range(MAX_ROWS):
            sav.append({ \
                    'address': self.rows[i]['address'].get(), \
                    'data'   : self.rows[i]['data'].get(), \
                    'is_read': self.rows[i]['is_read'].get() \
                    } \
                    )
            with open('data.pkl', 'wb') as f:
                pickle.dump(sav, f)

    def loadFile(self):
        load_ok = False
        sav = []
        with open('data.pkl', 'rb') as f:
            sav = pickle.load(f)
            load_ok = True
        if load_ok:
            for i in range(MAX_ROWS):
                self.rows[i]['address'].set(sav[i]['address'])
                self.rows[i]['data'].set(sav[i]['data'])
                self.rows[i]['is_read'].set(sav[i]['is_read'])

if __name__ == '__main__':
    root = Tk()
    Application(root)
    root.mainloop()

