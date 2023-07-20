import tkinter as tk
from pynput import mouse, keyboard
from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Key, Controller as KeyboardController
import configparser
import webbrowser
import sys
import os

# Création des contrôleurs pour la souris et le clavier
souris = MouseController()
clavier = KeyboardController()

# Initialisation d'un compteur à 0
compteur = 0

# Mode d'écoute pour définir la nouvelle touche de capture
mode_ecoute = False

# Configuration
config = configparser.ConfigParser()
config.read('config.ini')

# Load window size from config file
try:
    fenetre_size = config['DEFAULT']['fenetre_size']
except KeyError:
    fenetre_size = '280x50'

try:
    # Chargement de la touche de capture depuis le fichier de configuration
    touche_capture = getattr(Key, config['DEFAULT']['touche_capture'])
except (KeyError, AttributeError):
    # Si la touche de capture n'est pas trouvée dans le fichier de configuration ou est invalide, on utilise F1 par défaut
    touche_capture = Key.f1

def lors_appui(touche):
    global compteur
    global mode_ecoute
    global touche_capture

    if mode_ecoute:
        touche_capture = touche
        config['DEFAULT']['touche_capture'] = str(touche).split('.')[1]  # Sauvegarde de la touche de capture dans la configuration
        with open('config.ini', 'w') as configfile:  # Écriture de la configuration sur le disque
            config.write(configfile)
        label_touche['text'] = f"La touche sélectionnée est : {str(touche)}"
        mode_ecoute = False
        return False
    elif touche == touche_capture:  # Si la touche pressée est la touche de capture
        compteur += 1
        # Ouverture du fichier 'positions_souris.txt' en mode 'append' (ajout à la fin)
        with open('coordonner/positions_souris.txt', 'a') as f:
            # Écriture de la position actuelle de la souris dans le fichier
            f.write(f"{compteur} coordoner : \"{str(souris.position)}\"\n")

def lors_relache(touche):
    return not mode_ecoute  # Stopper l'écoute si le mode "d'écoute" est actif

def lancer_ecoute():
    global mode_ecoute
    global touche_capture
    mode_ecoute = True

    fenetre_touche = tk.Toplevel(fenetre)
    global label_touche
    label_touche = tk.Label(fenetre_touche, text=f"Appuyez sur la touche que vous voulez utiliser pour la capture...")
    label_touche.pack()

    bouton_valider = tk.Button(fenetre_touche, text="Valider", command=fenetre_touche.destroy)
    bouton_valider.pack()

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Création de l'interface utilisateur
fenetre = tk.Tk()
fenetre.geometry(fenetre_size)
fenetre.title("Capture Coordonnée")  # Ajoutez cette ligne pour changer le titre
fenetre.iconbitmap(resource_path('icone/icone.ico')) # Remplacez par le chemin vers votre fichier .ico

# Création du label de coordonnées
label = tk.Label(fenetre, text='', font=('Arial', 14))
label.pack()

# Création du menu
menubar = tk.Menu(fenetre)
menu1 = tk.Menu(menubar, tearoff=0)
menu1.add_command(label=f"Touche de capture : {str(touche_capture)}", command=lancer_ecoute)
menubar.add_cascade(label="Options", menu=menu1)
fenetre.config(menu=menubar)


def open_github():
    webbrowser.open('https://github.com/your-repo')  # Remplacez par votre lien GitHub réel

def about():
    fenetre_about = tk.Toplevel(fenetre)
    fenetre_about.title("À propos")

    frame = tk.Frame(fenetre_about, width=300)
    frame.pack()

    info_label = tk.Label(frame, text="Info :", font=("Arial", 10, "bold italic"))
    info_label.pack()

    info_text = "Ce programme a été créé par Squall98 à l'aide de ChatGPT. Ce programme sert à connaître la position du curseur et à enregistrer les positions dans un fichier texte. Ce programme est disponible gratuitement sur mon GitHub."

    # Diviser le texte en phrases et afficher chacune sur une nouvelle ligne via le "."
    for sentence in info_text.split('. '):
        tk.Label(frame, text=sentence).pack()

    creator_label = tk.Label(frame, text="Créateur :", font=("Arial", 10, "bold italic"))
    creator_label.pack()

    creator_name = tk.Label(frame, text="Squall98", fg="red")
    creator_name.pack()

    github_link = tk.Label(frame, text="Lien GitHub : https://github.com/Squall98/Capture-Coordonnee", fg="blue", cursor="hand2")
    github_link.pack()
    github_link.bind("<Button-1>", lambda e: open_github())

menu_help = tk.Menu(menubar, tearoff=0)
menu_help.add_command(label="À propos", command=about)
menubar.add_cascade(label="Help", menu=menu_help)

fenetre.config(menu=menubar)

# Mise à jour des coordonnées du label
def update_coords():
    label['text'] = f"Coordonnées actuelles de la souris : {str(souris.position)}"
    label.after(100, update_coords)  # Mise à jour tous les 100 ms

label.after(100, update_coords)

def on_exit():
    # Update window size in config file on exit
    config['DEFAULT']['fenetre_size'] = fenetre.geometry()
    with open('config.ini', 'w') as configfile:  # Écriture de la configuration sur le disque
        config.write(configfile)
    fenetre.destroy()

fenetre.protocol("WM_DELETE_WINDOW", on_exit)

# Écoute du clavier
with keyboard.Listener(on_press=lors_appui, on_release=lors_relache) as listener:
    fenetre.mainloop()
    listener.join()
