import tkinter as tk

m = tk.Tk()
m.title('myFirstPythonTkinter')
btn = tk.Button(m, text='Stop', width=10, command=m.destroy)
btn.pack()
m.mainloop()
