import tkinter as tk
import os
import pandas as pd
import requests
import time
import datetime
import random
from bs4 import BeautifulSoup
import json
import numpy as np

path = r"C:\Users\hungy\Desktop"
file = os.path.join(path, 'Price.xlsx')
old = pd.ExcelFile(file)




## function
# def data_D():
#     names = Daily.names()
#     price = Daily.prices()
#     for i in range(len(names)):
#         namedata = tk.Label(window, text = names[i], bg = 'white')
#         namedata.grid(column = 0, row = 1+i,sticky = "W")
#         pricedata = tk.Label(window, text = prices[i], bg = 'white')
#         pricedata.grid(column = 1, row = 1+i,sticky = "W")



class Weee:
    def __init__(self, tag):
        self.tag = tag
        self.names = []
        self.prices = []
        #self.hisPrice= []
        self.urllist = []
        self.df1 = pd.read_excel(old, self.tag)
        self.hisPrice = list(self.df1["HistoryPrice"])

    def collect(self, url):
        
        response = requests.get(url, timeout=20)
        soup = BeautifulSoup(response.text, "html.parser")
        result = soup.find(type="application/ld+json")
        json_object = json.loads(result.contents[0])
        self.names += [json_object['name']]
        self.prices += [float(json_object['offers']["price"])]
        self.urllist +=[url]
        #print(self.hisPrice)
        
        ## Check price
        if len(self.names)!=len(self.hisPrice):
            self.hisPrice+= [ np.nan for i in range(len(self.names)-len(self.hisPrice))]
        if pd.isna(self.hisPrice[len(self.names)-1]) or float(self.hisPrice[len(self.names)-1])>float(json_object['offers']["price"]):
            self.hisPrice[len(self.names)-1] = float(json_object['offers']["price"])
            
#         else:
#             self.hisPrice_tem +=[float(self.hisPrice[len(self.names)-1])]
        
    def makingSheet(self):
#         print(len(self.names))
#         print(len(self.hisPrice))
#         print('url', len(self.urllist))
        df1 = pd.DataFrame({"Name":self.names, "Price":self.prices, "HistoryPrice": self.hisPrice, 'url':self.urllist})
        return df1
    
    def read(self):
        tagfile = pd.read_excel(old, self.tag)
        names = list(tagfile['Name'])
        prices = list(tagfile['Price'])
        urllist = list(tagfile['url'])
        self.names = names
        self.prices = prices
        self.urllist = urllist

    def data(self):
        j = 2
        if self.tag == 'Daily Necessary':
            j = 0
        for i in range(len(self.names)):
            namedata = tk.Label(window, text = self.names[i], bg = 'white')
            namedata.grid(column = 0+j, row = 2+i,sticky = "W")
            pricedata = tk.Label(window, text = self.prices[i], bg = 'white')
            pricedata.grid(column = 1+j, row = 2+i,sticky = "W", columnspan=2)
    def check(self):
        print("I'm good!!!")
    
    def updateData(self):
        self.names = []
        self.prices = []
        index = self.urllist
        self.urllist = []
        for i in range(len(index)):
            self.collect(index[i])
        l.config(text= 'Gotcha!')
        
        
Daily = Weee("Daily Necessary")
Special = Weee("Special")
Daily.read()
Special.read()

# DailyList = ["https://www.sayweee.com/zht/product/Nisshin-Canola-Oil-/95694",
#             'https://www.sayweee.com/zht/product/Sun-Right-Fortified-All-Purpose-Flour/15354',
#              'https://www.sayweee.com/zht/product/ChiaHe-Premium-All-Purpose-Flour/16087'
# ]    
# Speciallist = ['https://www.sayweee.com/zht/product/Kao-MegRhythm-Gentle-Steam-Eye-Mask--Rose-12pc/45775',
#                'https://www.sayweee.com/zht/product/Kao-MegRhythm-Gentle-Steam-Eye-Mask--Unscented/8129',
#                'https://www.sayweee.com/zht/product/Kao-MegRhythm-Gentle-Steam-Eye-Mask-Lavender-12ct/95025'
# ]    
    

def addnew():
    address = entry.get()
    if var.get() == "D":
        l.config(text= 'Gotcha\n Daily')
        #print(Daily.prices)
        Daily.collect(address)
        #print(Daily.names)
    else:
        l.config(text= 'Gotcha \n Special')
        Special.collect(address)
    export()


    
def export():
    writer = pd.ExcelWriter(file, engine='xlsxwriter')

    # Write each dataframe to a different worksheet.
    df1 = Daily.makingSheet()
    df1.to_excel(writer, sheet_name='Daily Necessary', index = False)
    width = df1['Name'].astype(str).map(len).max()
    writer.sheets['Daily Necessary'].set_column('A:A', width*2)
    df2 = Special.makingSheet()
    df2.to_excel(writer, sheet_name='Special', index = False)
    width = df1['Name'].astype(str).map(len).max()
    writer.sheets['Special'].set_column('A:A', width*2)
    writer.save()
    print('save')
    Daily.data()
    Special.data()
        
        
def update():
    Daily.read()
    Special.read()
    Daily.updateData()
    Special.updateData()
    export()
    
    
    
# tagfile = pd.read_excel(old, "Daily Necessary")
# names = list(tagfile['Name'])
# prices = list(tagfile['Price'])
# urllist = list(tagfile['url'])
# Daily.names = names
# Daily.prices = prices
# Daily.urllist = urllist
# print(Daily.prices)



    


window = tk.Tk()
window.title('Price App')
window.geometry('850x600')
window.configure(background='white')

#Main

title1 = tk.Label(window, text = 'Name', bg = '#EEEDE7')
title1.grid(column = 0, row = 1)
title2 = tk.Label(window, text = 'Price', bg = '#EEEDE7')
title2.grid(column = 1, row = 1, sticky = "W")
title3 = tk.Label(window, text = 'Name', bg = '#EEEDE7')
title3.grid(column = 2, row = 1)
title4 = tk.Label(window, text = 'Price', bg = '#EEEDE7')
title4.grid(column = 3, row = 1, sticky = "W")

Daily.data()
Special.data()


    
    

##Side
var = tk.StringVar() 
entry = tk.Entry(window, width=30)
entry.grid(column = 2, row = 0, sticky = "E", padx = 1, ipadx = 1)
Addbutton = tk.Button(window, text='Add New', command=addnew)
Addbutton.grid(column = 4, row=0, sticky = "W", ipadx = 1, padx = 8)
Dailybutton = tk.Radiobutton(window, text = 'DailyNeccessary', bg = 'white',variable=var, value='D')
Dailybutton.grid(column = 0, row = 0, sticky = 'W')
Specialbutton = tk.Radiobutton(window, text = 'Special', bg = 'white', variable=var, value='S')
Specialbutton.grid(column = 2, row = 0, sticky = "W")
updatebutton = tk.Button(window, text='Update', command=update)
updatebutton.grid(column = 4, row=1, sticky = "W", padx = 8)

l = tk.Label(window, bg='white', width=7)
l.grid(column = 4, row=2, sticky = "W", padx = 8)

window.mainloop()