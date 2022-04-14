import tkinter as tk
from turtle import color
from libsvm.svmutil import svm_train, svm_predict


class MainApplication(tk.Frame):
    def __init__(self, master, *args, **kwargs):

        tk.Frame.__init__(self, master, *args, **kwargs)
        self.width = 1000
        self.master = master
        self.frame = tk.Frame(self.master)
        self.canvas = tk.Canvas(self.frame, height=1000, width=self.width, bg = "white")

        self.draw_flag = False

        #Initail paramter values
        self.c = 100
        self.g = 0.001
        self.p = 0.0001

        #list of dot cooardinates
        self.x_list = []
        self.y_list = []

        #list for drawing the line (it's just a bunch of dots)
        #x_plot is alwas a list od values from 1-width(canvas)
        #y_plot is calculated by svr()
        self.x_plot = [[i] for i in range(self.width)]
        self.y_plot = []

        #Sliders, button, frame, canvas
        self.glabel = tk.Label(self.master, text = "gamma")
        self.glabel.grid(row=0,column=1, sticky="n")
        self.gslider = tk.Scale(self.master, from_=0.001, to=0.003,resolution = 0.0001, orient="vertical", length = 800, sliderlength = 60)
        self.gslider.bind("<ButtonRelease-1>", self.set)
        self.gslider.set(0.002)
        self.gslider.grid(row = 0, column=1)

        self.clabel = tk.Label(self.master, text = "C")
        self.clabel.grid(row=0,column=2, sticky="n")
        self.cslider = tk.Scale(self.master, from_=1, to=300, orient="vertical", length = 800, sliderlength = 60)
        self.cslider.bind("<ButtonRelease-1>", self.set)
        self.cslider.set(150)
        self.cslider.grid(row = 0, column=2)


        self.plabel = tk.Label(self.master, text = "epsilon")
        self.plabel.grid(row=0,column=3, sticky="n")
        self.pslider = tk.Scale(self.master, from_=0.0001, to=10,resolution = 1, orient="vertical", length = 800, sliderlength = 60)
        self.pslider.set(5)
        self.pslider.bind("<ButtonRelease-1>", self.set)
        self.pslider.grid(row = 0, column=3)

        self.canvas.bind('<Button-1>', self.dot)
        self.button1 = tk.Button(self.frame, text = 'Clear', command = self.clear, height = 4, width = 16)
        self.button1.grid(row = 1, column=0, sticky="s")
        
        self.frame.grid(row = 0, column=0)
        self.canvas.grid(row = 1, column=0)

        self.master.grid_columnconfigure([1,2,3], minsize=100)

    def set(self,event):
        """sets the values of parameter to slider values
        deltes everything on canvas
        calculates y_plot values with new paramas"""
        self.c=self.cslider.get()
        self.g=self.gslider.get()
        self.p=self.pslider.get()

        self.canvas.delete("all")
        self.show_dot()
        self.svr()


    def dot(self,event):
        """saves button1 click coordinates
        draws the dots
        when there is more than 1 dot svr() is called"""
        self.x_list.append([event.x])
        self.y_list.append(event.y)
        
        self.show_dot()

        if len(self.x_list) > 1:
            self.svr()


    
    def clear(self):
        """clears all the lists
        deletes clears the canvas"""
        self.x_list = []
        self.y_list = []
        self.y_plot = []

        self.canvas.delete("all")
    
    def show_dot(self):
        """draws dots from x/y_list"""
        for i in zip(self.x_list,self.y_list):
            x_dot = i[0][0]
            y_dot = i[1]
            self.canvas.create_oval((x_dot-1),(y_dot-1), (x_dot+1),(y_dot+1), fill="red", width=10)
        

    def show_line(self):
        """Deletes the line if there is one allready
        draw new line"""
        if self.draw_flag:
            self.canvas.delete("line")

        for i in zip(self.x_plot,self.y_plot):
            x = i[0][0]
            y = i[1][0]
            self.canvas.create_oval((x-1),(y-1), (x+1),(y+1), fill="red", tags="line")
                    
            

    def svr(self):
        """support vector regression
        trains model from drawn points
        predicts y values from x_plot"""
        params = '-s 3 -t 2 -h 1 -c {} -g {} -p {}'.format(self.c, self.g, self.p)
        model = svm_train(self.y_list,self.x_list,params)
        _,_,self.y_plot = svm_predict([],self.x_plot,model,'-q')

        self.show_line()
        self.draw_flag = True

    

if __name__ == "__main__":
    root = tk.Tk()
    MainApplication(root)
    root.mainloop()