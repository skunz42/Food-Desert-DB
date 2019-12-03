# Sean Kunz

import tkinter as tk
from PIL import ImageTk, Image
from Conn import Conn

class Driver(tk.Frame):
    cn = Conn()
    # Constructor
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_window()

    '''***********************************************
                        newPage
        purpose:
            similar to summary window, but works as a new page
        parameters:
            top - window object
            retArr - the list of stores
            pageNum - which page the user is on
        return:
            None
    ***********************************************'''
    def newPage(self, top, retArr, pageNum):
        # Number of columns
        width = 6
        # Calculate index by page number
        index = (1+pageNum)*20
        # recursive base case
        if index > len(retArr):
            return
        # delete old window
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
        # via stack overflow
        b = tk.Button(top, text="Load next", command= lambda : self.newPage(top, retArr, pageNum+1))
        b.grid(row=0, column=2)
        top.mainloop()

    '''***********************************************
                        getChoiceStores
        purpose:
            displays the stores window
        parameters:
            value - City name from the drop down menu
        return:
            None
    ***********************************************'''
    def getChoiceStores(self, value):
        top = tk.Toplevel()

        width = 6 # number of columns
        retArr = self.cn.getStores(value)
        index = 0
        # creates grid
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

    '''***********************************************
                        getChoiceSummary
        purpose:
            displays the summary window
        parameters:
            value - City name from the drop down menu
        return:
            None
    ***********************************************'''
    def getChoiceSummary(self, value):
        top = tk.Toplevel()
        retDict = self.cn.getSummary(value)
        nl = tk.Label(top, text=retDict['Name'], font=('Helvetica', 16))
        nl.pack(side=tk.TOP)
        nsl = tk.Label(top, text="Number of Stores: " + str(retDict['Number of Stores']))
        arl = tk.Label(top, text="Average Rating: " + "{:.2f}".format(retDict['Average Rating']))
        nrl = tk.Label(top, text="Total Number of Ratings: " + str(retDict['Total Number of Ratings']))
        pfdl = tk.Label(top, text="Percent of the Population Living in a Food Desert: " + str(retDict['Percent Pop in Food Desert']) + "%")
        nsl.pack(side=tk.LEFT)
        arl.pack(side=tk.LEFT)
        nrl.pack(side=tk.LEFT)
        pfdl.pack(side=tk.LEFT)

    '''***********************************************
                        getChoiceMap
        purpose:
            displays the map window
        parameters:
            value - City name from the drop down menu
        return:
            None
    ***********************************************'''
    def getChoiceMap(self, value):
        top = tk.Toplevel()
        retArr = self.cn.getMap(value)
        path = retArr[0]['Path']
        nl = tk.Label(top, text=value, font=('Helvetica', 16))
        pfdl = tk.Label(top, text="Percent of Population Living in a Food Desert: " + str(retArr[0]['Percent Food Desert']))
        popl = tk.Label(top, text="City Population: " + str(retArr[0]['Population']))
        nl.pack(side=tk.TOP)
        pfdl.pack(side=tk.TOP)
        popl.pack(side=tk.TOP)
        img = Image.open(path)
        img = img.resize((765,450), Image.ANTIALIAS)
        map = ImageTk.PhotoImage(img)
        mpl = tk.Label(top, image=map)
        mpl.pack(side=tk.TOP, expand=tk.YES)
        top.mainloop()

    '''***********************************************
                        create_window
        purpose:
            creates the main window
        parameters:
            None
        return:
            None
    ***********************************************'''
    def create_window(self):
        # Gets drop down menu options
        storeOptions = self.cn.getCities()
        storeOptions.append("all")
        summaryOptions = self.cn.getCities()
        mapOptions = self.cn.getMapOptions()

        # Sets up drop down menus
        default = tk.StringVar()
        default2 = tk.StringVar()
        default3 = tk.StringVar()
        default.set("Stores")
        default2.set("Summary")
        default3.set("Map")
        see_stores = tk.OptionMenu(self, default, *storeOptions, command=self.getChoiceStores)
        see_summary = tk.OptionMenu(self, default2, *summaryOptions, command=self.getChoiceSummary)
        see_map = tk.OptionMenu(self, default3, *mapOptions, command=self.getChoiceMap)
        see_stores.pack(side=tk.LEFT, padx=5, pady=10)
        see_summary.pack(side=tk.LEFT, padx=5, pady=20)
        see_map.pack(side=tk.LEFT, padx=5, pady=20)

'''***********************************************
                    Main
***********************************************'''
def main():
    root = tk.Tk()
    app = Driver(master = root)
    app.mainloop()
main()
