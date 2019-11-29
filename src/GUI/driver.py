# Sean Kunz

import tkinter as tk
from Conn import Conn

class Driver(tk.Frame):
    cn = Conn()
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_window()

    def newPage(self, top, retArr, pageNum):
        width = 6
        index = (1+pageNum)*20
        if index > len(retArr):
            return
        top.destroy()
        top = tk.Toplevel()
        for i in range(index, index+20): #Rows
            if i > len(retArr)-1:
                break
            for j in range(width): #Columns
                if j == 0:
                    ratext = retArr[i]['Name']
                elif j == 1:
                    ratext = retArr[i]['City']
                elif j == 2:
                    ratext = retArr[i]['State']
                elif j == 3:
                    ratext = retArr[i]['Address']
                elif j == 4:
                    ratext = retArr[i]['Num_Ratings']
                elif j == 5:
                    ratext = retArr[i]['Rating']
                b = tk.Label(top, text=ratext)
                b.grid(row=i+1, column=j)
        b = tk.Button(top, text="Load next", command= lambda : self.newPage(top, retArr, pageNum+1))
        b.grid(row=0, column=2)
        top.mainloop()

    def getChoice(self, value):
        top = tk.Toplevel()

        #top.geometry("750x250")
        width = 6
        retArr = self.cn.getStores(value)
        index = 0
        for i in range(index, index+20): #Rows
            if i > len(retArr)-1:
                break
            for j in range(width): #Columns
                if j == 0:
                    ratext = retArr[i]['Name']
                elif j == 1:
                    ratext = retArr[i]['City']
                elif j == 2:
                    ratext = retArr[i]['State']
                elif j == 3:
                    ratext = retArr[i]['Address']
                elif j == 4:
                    ratext = retArr[i]['Num_Ratings']
                elif j == 5:
                    ratext = retArr[i]['Rating']
                b = tk.Label(top, text=ratext)
                b.grid(row=i+1, column=j)
        butt = tk.Button(top, text="Load next", command= lambda : self.newPage(top, retArr, 0))
        butt.grid(row=0, column=2)
        top.mainloop()

    def create_window(self):
        storeOptions = self.cn.getCities()
        storeOptions.append("all")
        summaryOptions = self.cn.getCities()
        mapOptions = self.cn.getCities()
        default = tk.StringVar()
        default2 = tk.StringVar()
        default3 = tk.StringVar()
        default.set("---")
        default2.set("---")
        default3.set("---")
        self.see_stores = tk.OptionMenu(self, default, *storeOptions, command=self.getChoice)
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
