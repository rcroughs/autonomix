import gi
import api
import subprocess

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GdkPixbuf

tokeng = None


class RecipeWindow(Gtk.Box):
    def __init__(self, token: str):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.get_style_context().add_class("window-grocery")
        self.token = token
        global tokeng
        tokeng = self.token

        # CSS pour le style
        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(b"""
            .window-grocery {
                background-color: #FFC0CB;  
            }
            .button-contact {
                background-color: #FF9999; 
                border-radius: 10px;
            }
            """)
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        )

        # Créer le Stack pour les écrans
        self.stack = Gtk.Stack()
        self.stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        self.stack.set_transition_duration(500)
        self.pack_start(self.stack, True, True, 0)

        # Écran principal avec les boutons
        main_screen = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)

        # Ajouter les boutons
        for i in range(3):  # 3 rangées
            row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
            main_screen.pack_start(row, True, True, 0)

            for j in range(1, 6):  # 5 boutons par rangée
                button_index = i * 5 + j
                button = self.create_image_button(f"animations/button_{button_index}.png")
                button.set_hexpand(True)
                button.set_vexpand(True)
                row.pack_start(button, True, True, 0)

                # Associer les boutons 1, 2, 3 aux écrans
                if button_index in [1, 2, 3]:
                    button.connect("clicked", self.on_button_clicked, f"screen_{button_index}")

        self.stack.add_named(main_screen, "main_screen")

        # Ajouter des écrans spécifiques avec le bouton retour
        self.add_screen_with_back_button("screen_1", "")
        self.add_screen_with_back_button("screen_2", "")
        self.add_screen_with_back_button("screen_3", "")

        # Afficher l'écran principal par défaut
        self.stack.set_visible_child_name("main_screen")

    def add_screen_with_back_button(self, screen_name, label_text):
        """
        Crée un écran avec un bouton retour vers l'écran principal.
        """
        screen = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)

        # Bouton retour
        back_button = Gtk.Button(label="←")
        back_button.connect("clicked", self.on_button_clicked, "main_screen")
        back_button.set_halign(Gtk.Align.START)
        screen.pack_start(back_button, False, False, 0)

        # Contenu de l'écran
        label = Gtk.Label(label=label_text)
        screen.pack_start(label, True, True, 0)

        # Ajouter l'écran au Stack
        self.stack.add_named(screen, screen_name)

    def update_screen(self, screen_name, new_content=None):
        """
        Met à jour le contenu d'un écran.
        """
        # Récupérer l'écran depuis le Gtk.Stack
        screen = self.stack.get_child_by_name(screen_name)


    def add_image_to_top_box(self, button, top_box):
        """
        Ajoute une image dans la zone supérieure (top_box), jusqu'à un maximum de 5.
        """
        if self.image_count < 5:
            try:
                pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale("animations/person.png", 100, 100, True)
                person_image = Gtk.Image.new_from_pixbuf(pixbuf)
                top_box.pack_start(person_image, False, False, 20)
                self.image_count += 1
                top_box.show_all()
            except Exception as e:
                print(f"Erreur lors du chargement de l'image : {e}")

    def remove_image_from_top_box(self, button, top_box):
        """
        Supprime une image de la zone supérieure (top_box) si au moins une image est présente.
        """
        if self.image_count > 0:
            children = top_box.get_children()
            for child in reversed(children):  # Supprimer la dernière image ajoutée
                if isinstance(child, Gtk.Image):
                    top_box.remove(child)
                    self.image_count -= 1
                    top_box.show_all()
                    break

    def on_button_clicked(self, button, screen_name):
        """
        Gère le clic sur les boutons pour afficher l'écran correspondant.
        """
        # Mettre à jour le contenu dynamiquement avant d'afficher
        if screen_name == "screen_1":
            self.update_screen("screen_1", [Gtk.Label(label="Contenu dynamique pour Screen 1")])
        elif screen_name == "screen_2":
            self.update_screen("screen_2", [Gtk.Label(label="Contenu dynamique pour Screen 2")])
        elif screen_name == "screen_3":
            self.update_screen("screen_3", [Gtk.Label(label="Contenu dynamique pour Screen 3")])

        self.stack.set_visible_child_name(screen_name)

    def create_image_button(self, image_path):
        """
        Crée un bouton avec une image comme arrière-plan.
        """
        try:
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(image_path, 300, 300, True)
            image = Gtk.Image.new_from_pixbuf(pixbuf)
        except Exception as e:
            print(f"Erreur lors du chargement de l'image {image_path}: {e}")
            image = Gtk.Image.new_from_icon_name("image-missing", Gtk.IconSize.BUTTON)

        button = Gtk.Button()
        button.set_image(image)
        return button


