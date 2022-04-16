import tkinter as tk

def main():
    gg=entry_string.get()
    ruts=foo(gg)
    r.insert(1.0, ruts)

root=tk.Tk()
root.geometry('800x600')
entry_string=tk.StringVar(root)
txt=tk.Entry(root, width=800, textvariable=entry_string)
txt.pack()
b1=tk.Button(root,text='решение',bg='green', height=5, width=25,command=main)
b1.pack()
r = tk.Text(root, width=800, height=600)
r.pack()

root.mainloop()

