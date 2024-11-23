import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk


class MyWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Autonomix")
        self.set_border_width(10)

        self.maximize()

 
        # Créer une grille pour organiser les boutons
        grid = Gtk.Grid()
        grid.set_row_spacing(10)
        grid.set_column_spacing(10)
        grid.set_halign(Gtk.Align.CENTER)
        grid.set_valign(Gtk.Align.CENTER)
        self.add(grid)

        # Créer les boutons
        button1 = Gtk.Button()
        button2 = Gtk.Button()
        button3 = Gtk.Button()
        button4 = Gtk.Button()


        # Charger les images pour chaque bouton
        image1 = Gtk.Image.new_from_file("food.png")
        image2 = Gtk.Image.new_from_file("todo.png")
        image3 = Gtk.Image.new_from_file("courses.png")
        image4 = Gtk.Image.new_from_file("tel.png")

        # Assigner les images aux boutons
        button1.set_image(image1)
        button2.set_image(image2)
        button3.set_image(image3)
        button4.set_image(image4)

        # Définir des tailles minimales pour les boutons
        button1.set_size_request(700, 500)
        button2.set_size_request(700, 500)
        button3.set_size_request(700, 500)
        button4.set_size_request(700, 500)

        # Positionner les boutons dans la grille
        grid.attach(button1, 0, 0, 1, 1)
        grid.attach(button2, 1, 0, 1, 1)
        grid.attach(button3, 0, 1, 1, 1)
        grid.attach(button4, 1, 1, 1, 1)

        # Connecter les signaux des boutons
        button1.connect("clicked", self.on_button_clicked, "Bouton 1")
        button2.connect("clicked", self.on_button_clicked, "Bouton 2")
        button3.connect("clicked", self.on_button_clicked, "Bouton 3")
        button4.connect("clicked", self.on_button_clicked, "Bouton 4")

        # Connecter l'événement pour quitter le plein écran avec Échap (facultatif)
        self.connect("key-press-event", self.on_key_press_event)

	def on_button_clicked(self, widget, button_name):
		print(f"{button_name} cliqué")

    def on_key_press_event(self, widget, event):
        if event.keyval == Gdk.KEY_Escape:
            self.unmaximize()  # Quitte le mode maximisé

# Initialiser l'application
win = MyWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
