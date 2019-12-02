# Sean Kunz

import tkinter as tk
from PIL import ImageTk, Image
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

    def getChoiceStores(self, value):
        top = tk.Toplevel()

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

    def getChoiceSummary(self, value):
        top = tk.Toplevel()
        retDict = self.cn.getSummary(value)
        nl = tk.Label(top, text=retDict['Name'], font=('Helvetica', 16))
        nl.pack(side=tk.TOP)
        arl = tk.Label(top, text="Average Rating: " + "{:.2f}".format(retDict['Average Rating']))
        nrl = tk.Label(top, text="Total Number of Ratings: " + str(retDict['Total Number of Ratings']))
        pfdl = tk.Label(top, text="Percent of the Population Living in a Food Desert: " + str(retDict['Percent Pop in Food Desert']) + "%")
        arl.pack(side=tk.LEFT)
        nrl.pack(side=tk.LEFT)
        pfdl.pack(side=tk.LEFT)

    def getChoiceMap(self, value):
        top = tk.Toplevel()
        retArr = self.cn.getMap(value)
        path = retArr[0]['Path']
        nl = tk.Label(top, text=value, font=('Helvetica', 16))
        nl.pack(side=tk.TOP)
        img = Image.open(path)
        img = img.resize((660,510), Image.ANTIALIAS)
        map = ImageTk.PhotoImage(img)
        mpl = tk.Label(top, image=map)
        mpl.pack(side=tk.TOP, expand=tk.YES)
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
        see_stores = tk.OptionMenu(self, default, *storeOptions, command=self.getChoiceStores)
        see_summary = tk.OptionMenu(self, default2, *summaryOptions, command=self.getChoiceSummary)
        see_map = tk.OptionMenu(self, default3, *mapOptions, command=self.getChoiceMap)
        see_stores.pack(side=tk.LEFT, padx=5, pady=10)
        see_summary.pack(side=tk.LEFT, padx=5, pady=20)
        see_map.pack(side=tk.LEFT, padx=5, pady=20)

def main():
    root = tk.Tk()
    #root.geometry("600x360+300+300")
    app = Driver(master = root)
    app.mainloop()
main()
