import os
import subprocess
import json
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import time

extensions = {}
extension_selected = []
filepath = os.path.dirname(os.path.realpath(__file__))
config_path = os.environ['LOCALAPPDATA'] + "\outil_de_recherche\config.json"
icon_path = filepath + "\icon.ico"

def search(*args):
    if not os.path.exists(current_dir.get()):  #vérification de la conformité du chemin d'accès
        messagebox.showerror('Erreur', 'Erreur: Aucun dossier sélectionné')
        return
    research = str(word.get()) #récupération du mot que l'on souhaite rechercher
    results_window, results_frame = open_resuts_window()
    tree = create_tree(results_window, results_frame)
    x = StringVar() # variable of Progressbar
    label_loading = ttk.Label(results_window, text = "Recherche en cours ...")
    label_loading.pack(side=TOP)
    progress_bar = ttk.Progressbar(results_window,orient = HORIZONTAL,length = 300, mode = 'determinate',variable=x)
    progress_bar.pack(side=TOP)
    results_window.update()
    results_window.focus_set()
    nb_file = get_nb_file()
    progress_step = 100 / nb_file
    percentage = StringVar()
    label_percentage = ttk.Label(results_window, textvariable = percentage)
    x.trace('w', lambda *_,value = x : percentage.set(str(int(float(value.get()))) + '%'))
    label_percentage.pack(side=TOP)
    result = _search(research,results_window,tree,progress_bar,progress_step)
    if result > 0 :
        tree.focus_set()
        row_id = tree.get_children()[0]
        tree.focus(row_id)
        tree.selection_set(row_id)
    progress_bar.destroy()
    label_loading.destroy()
    label_percentage.destroy()
    label_title = ttk.Label(results_window, text = str(result) + " occurences trouvées").pack(side=TOP)
    label_shortcut = ttk.Label(results_window, text = "Double clic / Entrée pour ouvrir dans l'explorateur de fichier").pack(side=TOP)
    results_window.update()
    
def _search(research,window,tree,progress_bar,progress_step):
    found  = 0
    for path in os.listdir(current_dir.get()):
        if "log" in path:        #ignorer les logs
            continue
        if os.path.isfile(os.path.join(current_dir.get(), path)) and os.path.splitext(path)[1] in extension_selected:
            try:
                with open(os.path.join(current_dir.get(), path),'r') as f:
                    i = 1
                    for line in f.readlines():
                        if research in line:
                            found+=1
                            tree.insert('', 'end', values=(path, str(i)))
                        i+=1
            except:
                continue
        progress_bar.step(progress_step)
        window.update()
    return found

def search_rec(*args):
    if not os.path.exists(current_dir.get()):
        messagebox.showerror('Erreur', 'Erreur: Aucun dossier sélectionné')
        return
    research = str(word.get())
    results_window, results_frame = open_resuts_window()
    tree = create_tree(results_window, results_frame)
    x = StringVar() # variable of Progressbar
    label_loading = ttk.Label(results_window, text = "Recherche en cours ...")
    label_loading.pack(side=TOP)
    progress_bar = ttk.Progressbar(results_window,orient = HORIZONTAL,length = 300, mode = 'determinate',variable=x)
    progress_bar.pack(side=TOP)
    results_window.update()
    results_window.focus_set()
    nb_file = get_nb_file()
    progress_step = 100 / nb_file
    percentage = StringVar()
    label_percentage = ttk.Label(results_window, textvariable = percentage)
    x.trace('w', lambda *_,value = x : percentage.set(str(int(float(value.get()))) + '%'))
    label_percentage.pack(side=TOP)
    result = _search_rec(research, results_window, tree, progress_bar, progress_step)
    if result > 0 :
        tree.focus_set()
        row_id = tree.get_children()[0]
        tree.focus(row_id)
        tree.selection_set(row_id)
    progress_bar.destroy()
    label_loading.destroy()
    label_percentage.destroy()
    label_title = ttk.Label(results_window, text = str(result) + " occurences trouvées").pack(side=TOP)
    label_shortcut = ttk.Label(results_window, text = "Double clic / Entrée pour ouvrir dans l'explorateur de fichier").pack(side=TOP)
    results_window.update()

def _search_rec(research, window, tree, progress_bar, progress_step, addpath = ""):
    curpath = os.path.join(current_dir.get(),addpath)
    found = 0
    for path in os.listdir(curpath):
        relative_path = os.path.join(addpath,path)
        if "log" in path:        #ignorer les logs
            progress_bar.step(progress_step)
            window.update()
            continue
        if os.path.isfile(os.path.join(curpath, path)) and os.path.splitext(path)[1] in extension_selected:
            try:
                with open(os.path.join(curpath, path),'r') as f:
                    i = 1
                    for line in f.readlines():
                        if research in line:
                            found+=1
                            tree.insert('', 'end', values=(relative_path, str(i)))
                        i+=1
            except:
                progress_bar.step(progress_step)
                window.update()
                continue
            progress_bar.step(progress_step)
            window.update()
        elif os.path.isdir(os.path.join(curpath,path)):
            found += _search_rec(research, window, tree, progress_bar, progress_step, relative_path)
        else:
            progress_bar.step(progress_step)
            window.update()
    return found

def ask_for_directory(*args):
    dir = filedialog.askdirectory(mustexist = True)
    if (dir == ""):
        current_dir.set("Aucun dossier sélectionné")
    else:
        current_dir.set(dir)
        word_entry.focus()

def quit_window(*args,window):
    window.destroy()

def update_extension_selected(ext):
    dict = {}
    if ext in extension_selected:
        extension_selected.remove(ext)
    else:
        extension_selected.append(ext)
    load_extentions()

def open_resuts_window():
    results_window = Toplevel(takefocus = True)
    results_window.iconbitmap(icon_path)
    results_window.title("Résultats de la recherche")
    results_window.bind("<Escape>", lambda args : quit_window(args,window = results_window))
    results_frame = ttk.Frame(results_window)
    results_frame.pack( side = BOTTOM, expand=True, fill = BOTH)
    return results_window,results_frame

def create_tree(window, frame):
    window.geometry("600x500")
    tree = ttk.Treeview(frame, column=("path", "line"), show='headings')
    tree.pack(fill=BOTH, side = LEFT, expand=True, padx=10, pady=10)
    tree.column("# 1", anchor=CENTER)
    tree.heading("# 1", text="chemin d'accès")
    tree.column("# 2", anchor=CENTER)
    tree.heading("# 2", text="ligne")
    scrollbar = Scrollbar(frame)
    scrollbar.pack(side = RIGHT, fill = BOTH)
    tree.config(yscrollcommand = scrollbar.set)
    scrollbar.config(command = tree.yview)
    tree.bind("<Double-Button-1>", lambda event, tree = tree: open_path(event,tree))
    tree.bind("<Return>", lambda event, tree = tree: open_path(event,tree))
    return tree
    
def open_path(event, tree):
    selected_item = tree.focus()
    item_details = tree.item(selected_item)
    fp = item_details.get("values")[0]
    path = os.path.join(current_dir.get(),fp).replace('/','\\')
    subprocess.Popen(f'explorer /select,{path}')

def get_nb_file():
    count = 0
    for _, _, files in os.walk(current_dir.get()):
        count += len(files)
    return count
    
def load_default_state_extentions():
    for child in subframe.winfo_children():
        child.destroy()
    with open(config_path,'r') as config_file:
        dict = json.load(config_file)
        i = 0
        for ext,enable in dict.items():
            checkbox = Checkbutton(subframe, text = ext,onvalue=1, offvalue=0, command=lambda ext=ext: update_extension_selected(ext))
            checkbox.grid(column=i, row=1, sticky=W)
            if enable:
                checkbox.select()
                if not ext in extension_selected:
                    extension_selected.append(ext)
            else:
                if ext in extension_selected:
                    extension_selected.remove(ext)
            i+=1
        edit_ext_button = ttk.Button(subframe, text="Modifier", command=edit_config)
        edit_ext_button.grid(column=i, row=1, sticky=W)
        reset_ext_button = ttk.Button(subframe, text="Restaurer par défaut", command=load_default_state_extentions)
        reset_ext_button.grid(column=i+1, row=1, sticky=W)
        
    root.update()

def load_extentions():
    for child in subframe.winfo_children():
        child.destroy()
    with open(config_path,'r') as config_file:
        dict = json.load(config_file)
        i = 0
        for ext in dict.keys():
            checkbox = Checkbutton(subframe, text = ext,onvalue=1, offvalue=0, command=lambda ext=ext: update_extension_selected(ext))
            checkbox.grid(column=i, row=1, sticky=W)
            if ext in extension_selected:
                checkbox.select()
            i+=1
        edit_ext_button = ttk.Button(subframe, text="Modifier", command=edit_config)
        edit_ext_button.grid(column=i, row=1, sticky=W)
        reset_ext_button = ttk.Button(subframe, text="Restaurer par défaut", command=load_default_state_extentions)
        reset_ext_button.grid(column=i+1, row=1, sticky=W)
        
    root.update()


def addext(ext_var,ext_entry,tree):
    if ext_var.get() == "" or ext_var.get()[0] != '.':
        messagebox.showerror('Erreur', "Erreur: format de l'extension invalide.")
        return
    dict = {}
    with open(config_path,'r') as config_file:
        dict = json.load(config_file)
        
    if ext_var.get() in dict.keys():
        messagebox.showerror('Erreur', 'Erreur: cette extension a déjà été ajoutée.')
        return
    tree.insert('', 'end', values=(ext_var.get(), "Oui"))
    dict.update({ext_var.get():True})
    extension_selected.append(ext_var.get())
    ext_var.set(".")
    with open(config_path,'w') as config_file:
        json.dump(dict,config_file)
        
    load_extentions()
    
def rmext(tree):
    selected_items = tree.selection()
    ext_to_remove = []
    for item in selected_items:
        item_details = tree.item(item)
        ext = item_details.get("values")[0]
        ext_to_remove.append(ext)
        if ext in extension_selected:
            extension_selected.remove(ext)
        tree.delete(item)
    dict = {}
    with open(config_path,'r') as config_file:
        dict = json.load(config_file)
    
    for ext in ext_to_remove:
        del dict[ext]
        
    with open(config_path,'w') as config_file:
        json.dump(dict,config_file)
        
    load_extentions()
    

def update_ext_tree(tree):
    dict = {}
    with open(config_path,'r') as config_file:
        dict = json.load(config_file)
    for ext,active in dict.items():
        is_active_by_default = ""
        if active:
            is_active_by_default = "Oui"
        else:
            is_active_by_default = "Non"
        tree.insert('', 'end', values=(ext, is_active_by_default))
    if len(dict.keys()) > 0:
        row_id = tree.get_children()[0]
        tree.focus(row_id)
        tree.selection_set(row_id)


def switch_default_state(tree, mode = -1):
    dict = {}
    with open(config_path,'r') as config_file:
        dict = json.load(config_file)
    selected_items = tree.selection()
    for item in selected_items:
        item_details = tree.item(item)
        ext = item_details.get("values")[0]
        default_state = item_details.get("values")[1]
        active = False
        if default_state == "Oui":
            active = True
            
        if mode == -1:
            if active:
                tree.set(item, "active", "Non")
            else:
                tree.set(item, "active", "Oui")
            dict[ext] = not active
        elif mode == 0:
            tree.set(item, "active", "Non")
            dict[ext] = False
        elif mode == 1:
            tree.set(item, "active", "Oui")
            dict[ext] = True
        
    with open(config_path,'w') as config_file:
        json.dump(dict,config_file)
    
def edit_config():
    display_config = Toplevel(takefocus = True)
    display_config.iconbitmap(icon_path)
    display_config.title("Gérer les extensions")
    display_config.bind("<Escape>", lambda args : quit_window(args,window = display_config))
    tree_frame = ttk.Frame(display_config)
    tree_frame.pack( side = TOP, expand=True, fill = BOTH)
    
    tree = ttk.Treeview(tree_frame, column=("ext", "active"), show='headings')
    tree.pack(fill=BOTH, side = LEFT, expand=True, padx=10, pady=10)
    tree.column("# 1", anchor=CENTER)
    tree.heading("# 1", text="Extension")
    tree.column("# 2", anchor=CENTER)
    tree.heading("# 2", text="Actif par défaut")
    scrollbar = Scrollbar(tree_frame)
    scrollbar.pack(side = RIGHT, fill = BOTH)
    tree.config(yscrollcommand = scrollbar.set)
    scrollbar.config(command = tree.yview)
    tree.bind("<Delete>", lambda event, tree = tree: rmext(tree))
    tree.bind("<Double-Button-1>", lambda event, tree = tree: switch_default_state(tree))
    tree.bind("<O>", lambda event, tree = tree: switch_default_state(tree,1))
    tree.bind("<o>", lambda event, tree = tree: switch_default_state(tree,1))
    tree.bind("<N>", lambda event, tree = tree: switch_default_state(tree,0))
    tree.bind("<n>", lambda event, tree = tree: switch_default_state(tree,0))
    update_ext_tree(tree)
    tree.focus_set()
    add_ext_frame = ttk.Frame(display_config)
    add_ext_frame.pack( side = BOTTOM, expand=True, fill = BOTH)
    
    ext_variable = StringVar()
    ext_variable.set(".")
    ext_entry = ttk.Entry(add_ext_frame, textvariable = ext_variable)
    ext_entry.bind("<Return>", lambda *args,ext_var = ext_variable, ext_entry=ext_entry, tree=tree : addext(ext_var,ext_entry,tree))
    ext_entry.pack()

    add_ext_button = ttk.Button(add_ext_frame, text="Ajouter l'extension", command= lambda ext_var = ext_variable, ext_entry=ext_entry, tree=tree : addext(ext_var,ext_entry,tree))
    add_ext_button.pack()
    

default_config = '{".php": true, ".txt": true, ".json": false, ".html": false, ".py": false}'

if not os.path.exists(os.environ['LOCALAPPDATA'] + "\outil_de_recherche"):
    os.mkdir(os.environ['LOCALAPPDATA'] + "\outil_de_recherche")

if not os.path.exists(config_path):
    with open(config_path,'w') as config_file:
        config_file.write(default_config)

root = Tk()
root.title("Recherche PHP")
root.iconbitmap(icon_path)

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

current_dir = StringVar()
current_dir.set("Aucun dossier sélectionné")
current_dir_text = ttk.Label(mainframe, textvariable = current_dir).grid(column=1, row=2, sticky=W)

word = StringVar()
word_entry = ttk.Entry(mainframe, width=20, textvariable=word)
word_entry.grid(column=1, row=3, sticky=(W, E))


ttk.Button(mainframe, text="Rechercher dans le dossier <Entrée>", command=search).grid(column=1, row=6, sticky=W)
ttk.Button(mainframe, text="Rechercher dans le dossier + sous-dossiers <Ctrl+Entrée>", command=search_rec).grid(column=1, row=5, sticky=W)
but_select = ttk.Button(mainframe, text="Sélectionner un dossier <Ctrl+E>", command=ask_for_directory).grid(column=1, row=1, sticky=W)


subframe = ttk.Frame(mainframe, padding="3 3 12 12")
subframe.grid(column=1, row=4, sticky=(N, W, E, S))

load_default_state_extentions()

for child in mainframe.winfo_children(): 
    child.grid_configure(padx=5, pady=5)

word_entry.bind("<Return>", search)
word_entry.bind("<Control-Return>", search_rec)
root.bind("<Escape>", lambda args : quit_window(args,window = root))
root.bind("<Control-E>", ask_for_directory)
root.bind("<Control-e>", ask_for_directory)
root.mainloop()