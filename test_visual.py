from PIL import Image, ImageTk
from tkinter import *
from tkinter import ttk
# pil_image = Image.open(r"C:\Users\wolfw\Downloads\BeatnoteProcess7-321-25\456beattest.png")
# pil_image1 = Image.open(r"D:\Diego\git\6s7p\456beattest.png")
# pil_image2 = Image.open(r"D:\Diego\git\6s7p\894beattest.png")
# pil_image3 = Image.open(r".\Picture_template.png")
# pil_image.rotate(45).show()
# plot_w = 500
# plot_h = 300
# resized_image1 = pil_image1.resize((plot_w, plot_h), Image.LANCZOS)
# resized_image2 = pil_image2.resize((plot_w, plot_h), Image.LANCZOS)
# resized_image3 = pil_image3.resize((plot_w, plot_h), Image.LANCZOS)
# first = True
# temp = plots()
# if __name__ == '__main__':
#     root = tk.Tk()
#     if first:
#         temp.create_image()
#         first = False
#     notebook = ttk.Notebook(root)
#     notebook.pack(expand=True, fill="both")
#     tab1_frame = ttk.Frame(notebook)
#     tab2_frame = ttk.Frame(notebook)
#     notebook.add(tab1_frame, text="Tab 1")
#     notebook.add(tab2_frame, text="Tab 2")
#     # tk_image1 = ImageTk.PhotoImage(resized_image1)
#     # tk_image2 = ImageTk.PhotoImage(resized_image2)
#     # tk_image3 = ImageTk.PhotoImage(resized_image3)
#     temp.update_image('Pavg',r"D:\Diego\git\6s7p\456beattest.png")
#     label1 = tk.Label(tab1_frame, text = 'hello', image=temp.imagetk, compound=tk.TOP)
#     label2 = tk.Label(tab1_frame, image=temp.imagetk)
#     # label1.image = tk_image1
#     open_button = ttk.Button(tab1_frame, text="Open Folder", command= lambda: change_image(label1, temp.imagetk2))

#     # label1.pack()
#     # label2.pack()
#     label1.grid(column=0,row=0)
#     label2.grid(column=2, row=0)
#     open_button.grid(column=2, row=1)

# root = Tk()
# root.title("PanedWindow Example")

# paned_main = PanedWindow(root, orient=HORIZONTAL)
# paned_main.pack(fill=BOTH, expand=1)

# entry = Entry(paned_main, bd=5)
# paned_main.add(entry)

# paned_vertical = PanedWindow(paned_main, orient=VERTICAL)
# paned_main.add(paned_vertical)

# scale = Scale(paned_vertical, orient=HORIZONTAL)
# paned_vertical.add(scale)

# root.mainloop()

root = Tk()
root.title("PanedWindow Example")

note = ttk.Notebook(root)
note.pack(fill='both', expand=True)
tab1 = ttk.Frame(note)
tab2 = ttk.Frame(note)
note.add(tab1, text='Tab 1')
note.add(tab2, text='Tab 2')
note1 = ttk.Notebook(tab1)
note2 = ttk.Notebook(tab2)
note1.pack(fill='both', expand=True)
note2.pack(fill='both', expand=True)

tab11 = ttk.Frame(note)
tab12 = ttk.Frame(note)
note1.add(tab11, text='Tab 11')
note1.add(tab12, text='Tab 12')

tab11 = ttk.Frame(note)
tab12 = ttk.Frame(note)
note2.add(tab11, text='Tab 21')
note2.add(tab12, text='Tab 22')
root.mainloop()
