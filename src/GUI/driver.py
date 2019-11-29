# Sean Kunz

import tkinter as tk
from Conn import Conn

class Driver(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_window()

    def create_window(self):
        cn = Conn()
        storeOptions = cn.getCities()
        storeOptions.append("all")
        summaryOptions = cn.getCities()
        mapOptions = cn.getCities()
        default = tk.StringVar()
        default2 = tk.StringVar()
        default3 = tk.StringVar()
        default.set("---")
        default2.set("---")
        default3.set("---")
        self.see_stores = tk.OptionMenu(self, default, *storeOptions)
        self.see_summary = tk.OptionMenu(self, default2, *summaryOptions)
        self.see_map = tk.OptionMenu(self, default3, *mapOptions)
        self.see_stores.pack(side=tk.LEFT, padx=5, pady=10)
        self.see_summary.pack(side=tk.LEFT, padx=5, pady=20)
        self.see_map.pack(side=tk.LEFT, padx=5, pady=20)

def main():
    root = tk.Tk()
    #root.geometry("600x360+300+300")
    app = Driver(master = root)
    app.mainloop()
main()
