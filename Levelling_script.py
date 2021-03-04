
from tkinter import *
from tkinter import filedialog as fd
from tkinter import messagebox as mb

import numpy as np
import pandas as pd
import math as m




'''
Todo:
    1.Add Gif file
    2. Entry background colors
    3. App borders |deep brown or grey| thick borders
'''

#instantiating 
win = Tk()

win.title('Level Survey')

canvas = Canvas(win, width = 400, height = 500)
canvas.grid(padx=0,pady=0)

# this is a gif image located in the directory. add it to right top corner of app
surveyor = PhotoImage(file= r"C:\Users\Kojo Justine\Desktop\Level App\survey.gif")

win.geometry("400x280+0+0")
win.resizable(width=False, height=False)



#Variables **********************************
itbm = DoubleVar()

ftbm = DoubleVar()

inputPath = StringVar()
outpath = StringVar()

message = "If no final benchmark is given, \n  Reduced levels = IRL in the output"


#Space 
Label(canvas, text= "").grid(column=0, row = 0)


ibmL = Label(canvas, text = 'Initial Benchmark',)
ibmL.grid(column = 0, row = 1,padx=10,pady=10)


ibmE = Entry(canvas, textvariable = itbm, width = 10)
ibmE.grid(column = 1, row= 1, padx=10,pady=10)

fbmL = Label(canvas, text = 'Final Benchmark')
fbmL.grid(column = 0, row = 2, padx=10,pady=10)

fbmE = Entry(canvas, textvariable = ftbm, width = 10)
fbmE.grid(column = 1, row= 2, padx=10,pady=10)


# warning = Label(canvas, text = '')
# warning.grid(column= 2, row = 2)

warning = Label(canvas, text = '')
warning.grid(column= 1, row = 4)

filepathL = Label(canvas, text = 'Input File')
filepathL.grid(column = 0, row = 5)

inpath = Entry(canvas, width = 25, )
inpath.grid(column = 1, row= 5)

def browse():
    global filename
    filename = fd.askopenfilename(filetypes =(("Excel files",".xlsx"),("CSV files" ,".csv" ),("All files","*.*")))
    inpath.insert(END, filename)
    return filename    


browseButton = Button(canvas, text="Browse",relief=RIDGE, command=browse, padx=5)
browseButton.grid(column=2, row=5, padx=10,pady=10)
# *******************************************************************************
# Level computations
def reduceLevel():
    # Level computations here <<=== 
    path = inpath.get()
    
    df = pd.read_excel(path)
    np.nan_to_num(df,0)
    #vairables

    bs = list(np.nan_to_num(df.BS,0))
    ints = list(np.nan_to_num(df.IS,0))
    fs = list(np.nan_to_num(df.FS,0))
    
    rise_falls = [0]
    itbm = 200
    ftbm = 200.280
    
    irl = [itbm, ]
    frls = []
    
    
    
    x=0
    while x< len(bs):
        
    #        condition 1: bs - ints
        if bs[x] != 0 and ints[x+1] !=0 and fs[x+1]==0:
    #        print("condition 1 : bs - ints ")
            
            do =round(bs[x] - ints[x+1],3)
            rise_falls.append(do)
    
    #        condition 2: bs - fs
        if bs[x] != 0 and ints[x+1] ==0 and fs[x+1]!=0:
    #        print("condition 2 : bs - fs ")
    
            do =round(bs[x] - fs[x+1],3)
            rise_falls.append(do)
    
    #        condition 3: ints - ints
        if bs[x] == 0 and ints[x] !=0 and ints[x+1] !=0 and fs[x+1] ==0:
    #        print("condition 3 : ints - ints")
            
            do =round(ints[x] - ints[x+1],3)
            rise_falls.append(do)
              
    #        condition 4: ints - fs
        if bs[x] == 0 and ints[x] !=0 and fs[x+1] !=0 :
    #        print("condition 4 : ints - fs")
            
            do =round(ints[x] - fs[x+1],3)
            rise_falls.append(do)
    
    # increamenting code for the while statement
        x+=1
        
    #        computing the initial reduced levels in the method
    y= 0
    while y < len(rise_falls):
        for value in rise_falls:
            rl = round(irl[y] + value,3)
            irl.append(rl)
            
            y +=1
    irl.remove(irl[0])
    
    #computing the number of stations
    stns =[]
    for b in bs:
        if b !=0:
            stns.append(b)
    stn_counts = len(stns)
    
    
    
    total_error = irl[-1] - ftbm
    error_per_stn = round(total_error/stn_counts,5)
    
    
    #now apply the error per station
    #first identify change points
    #2nd multiply error by its index
    
    corr = [0,error_per_stn]
    q = 0
    
    
    while q < len(bs):
    
        for b in bs:
            if b != 0: 
                q +=1
                corr.append(corr[1]*q) 
            
        
            if b ==0:
                corr.append(corr[-1])   
    
        if q == stn_counts:
                    corr.remove(corr[1])
                    corr.remove(corr[2])
    
                    break
                
    for rl, c in zip(irl, corr):
        flevel = round(rl - c,3)
        frls.append(flevel)
            
                    
    # creating a dataframe for all columns in the sheet
    
    d = {"BS":bs, "IS":ints, "FS":fs, "RISE_FALL": rise_falls, "IRL":irl,"ERROR_PER_STN": corr, "FRL":frls}
    dd = pd.DataFrame(d)
    
    try:
        outpath = "{}_computed.xlsx".format(inpath.get())
        export = dd.to_excel(outpath )
        print("\n This is the filepath ======>>>>> {} <<<<========\n".format(outpath))
    except:"Error  here <<<========"
    Label(canvas, text="Check input file directory for output file").grid(column=1, row=9)

    
   

# *******************************************************************************
submitButton = Button(canvas, text= 'Compute', command=reduceLevel)
submitButton.grid(column = 1, row = 8)



feedback = Label(canvas, text = message)
feedback.grid(column= 1, row= 3)

win.mainloop()



    
            
        

        
