import gi
import api
import subprocess

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GdkPixbuf

tokeng = None


class RecipeWindow(Gtk.Box):
    def __init__(self, token: str):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.get_style_context().add_class("Courses")
        self.token = token
        self.person_count = 1  # Initialiser à 1 personne par défaut
        global tokeng
        tokeng = self.token

        # Initialiser la liste des ingrédients
        self.ingredients = [
            {'name': 'Œuf', 'image': 'animations/egg.png', 'per_person_quantity': 1, 'unit': ''},
            {'name': 'Beurre', 'image': 'animations/butter1.png', 'per_person_quantity': 8, 'unit': 'g'},
        ]

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
            .little-button {  
                -GtkWidget-min-height: 50px;
                -GtkWidget-min-width: 50px;
                -GtkWidget-max-height: 20px;
                -GtkWidget-max-width: 20px;
                padding: 0;
                margin: 0;
            }
            .zone-persons {
                background-color: #FFB6C1; 
            }
            .zone-ingredients {
                background-color: #FF69B4;  
            }
            .zone-bottom {
                background-color: #E6E6FA;  
            }
            .large-button {
                min-width: 1000px;
                min-height: 1000px;
                }
            """)
        screen = Gdk.Screen.get_default()
        Gtk.StyleContext.add_provider_for_screen(
            screen, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER
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

        if screen_name == "screen_1":
            # Initialiser le compteur de personnes
            self.person_count = 1  # Commencer avec une personne par défaut
            max_persons = 5  # Nombre maximum de personnes

            # Création des zones pour screen_1

            # Top box : zone haut gauche et zone haut droite
            top_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
            left_top = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
            right_top = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)

            # Fixer la hauteur maximale du top_box
            top_box.set_size_request(-1, 200)  # Hauteur maximale de 200 pixels

            # Appliquer les classes CSS aux zones
            left_top.get_style_context().add_class("zone-persons")
            right_top.get_style_context().add_class("zone-ingredients")

            # Conteneur pour les images des personnes
            image_container = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
            left_top.pack_start(image_container, True, True, 0)

            # Conteneur pour les ingrédients (défini AVANT d'appeler add_image)
            self.ingredients_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
            right_top.pack_start(self.ingredients_container, True, True, 0)

            # Bouton "+" pour ajouter des personnes (avec image personnalisée)
            add_button = Gtk.Button()
            # Redimensionner l'image du bouton "+"
            pixbuf_plus = GdkPixbuf.Pixbuf.new_from_file_at_scale("animations/button_plus1.png", 40, 40, True)
            add_image = Gtk.Image.new_from_pixbuf(pixbuf_plus)
            add_button.set_image(add_image)
            add_button.set_size_request(40, 40)  # Fixer la taille du bouton à 40x40
            add_button.connect("clicked", self.add_image, image_container)
            image_container.pack_start(add_button, False, False, 0)

            # Ajouter une première personne par défaut
            self.add_image(None, image_container)

            top_box.pack_start(left_top, True, True, 0)
            top_box.pack_start(right_top, True, True, 0)

            # Mettre à jour les ingrédients pour la première fois
            self.update_ingredients()

            # Bottom box : grande zone inférieure
            bottom_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
            bottom_box.get_style_context().add_class("zone-bottom")

            # Étapes de la recette avec images
            steps = [
                {'step': '--1--', 'images': ['animations/poele.png'], 'description': ''},
                {'step': '--2--', 'images': ['animations/poele.png', 'animations/chauffer.png'], 'description': '' },
                {'step': '--3--', 'images': ['animations/butter_in_pan.png'], 'description': ''},
                {'step': '--3--', 'images': ['animations/oeuf_dans_poele.png', 'animations/fleche.png'] + ['animations/egg.png'], 'description': ''},
                {'step': '--4--', 'images': ['animations/chrono.png'], 'description': ''},]


            for step in steps:
                # Créer un cadre pour chaque étape sans label
                step_frame = Gtk.Frame()
                step_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)

                # Créer un label pour le titre de l'étape
                step_label = Gtk.Label()
                step_label.set_markup(f"<span size='xx-large'><b>{step['step']}</b></span>")
                step_label.set_justify(Gtk.Justification.CENTER)
                step_label.set_alignment(0.5, 0.5)  # Centrer le texte
                step_box.pack_start(step_label, False, False, 5)

                # Si des images sont disponibles, les ajouter
                images = step.get('images', [])
                if images:
                    images_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
                    for img_path in images:
                        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(img_path, 300, 300, True)
                        image = Gtk.Image.new_from_pixbuf(pixbuf)
                        images_box.pack_start(image, False, False, 0)
                    step_box.pack_start(images_box, False, False, 0)

                # Si une description est disponible, l'ajouter
                if step['description']:
                    label = Gtk.Label()
                    label.set_markup(f"<span size='large'>{step['description']}</span>")
                    label.set_justify(Gtk.Justification.CENTER)
                    label.set_alignment(0.5, 0.5)  # Centrer le texte
                    step_box.pack_start(label, False, False, 0)

                # Ajouter le step_box au cadre
                step_frame.add(step_box)

                # Ajouter le cadre au bottom_box
                bottom_box.pack_start(step_frame, False, False, 5)

            # Créer une fenêtre défilante pour le bottom_box
            scrolled_window = Gtk.ScrolledWindow()
            scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
            scrolled_window.add(bottom_box)

            # Ajouter les boîtes au screen
            screen.pack_start(top_box, False, False, 0)  # Ne pas étendre verticalement le top_box
            screen.pack_start(scrolled_window, True, True, 0)  # Zone inférieure avec défilement

        else:
            # Écran générique avec un bouton retour
            back_button = Gtk.Button(label="←")
            back_button.connect("clicked", self.on_button_clicked, "main_screen")
            back_button.set_halign(Gtk.Align.START)
            screen.pack_start(back_button, False, False, 0)

            label = Gtk.Label(label=label_text)
            screen.pack_start(label, True, True, 0)

        # Ajouter l'écran au Stack
        self.stack.add_named(screen, screen_name)

    def add_image(self, button, container):
        if self.person_count < 5:
            # Créer une box pour la personne
            person_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)

            # Image de la personne
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale("animations/person.png", 100, 100, True)
            person_image = Gtk.Image.new_from_pixbuf(pixbuf)
            person_box.pack_start(person_image, False, False, 0)

            # Bouton "-" pour supprimer cette personne (avec image personnalisée)
            remove_button = Gtk.Button()
            # Redimensionner l'image du bouton "-"
            pixbuf_moins = GdkPixbuf.Pixbuf.new_from_file_at_scale("animations/button_moins1.png", 50, 50, True)
            remove_image = Gtk.Image.new_from_pixbuf(pixbuf_moins)
            remove_button.set_image(remove_image)
            remove_button.set_size_request(40, 40)  # Fixer la taille du bouton à 40x40
            remove_button.connect("clicked", self.remove_person_image, person_box)
            person_box.pack_start(remove_button, False, False, 0)

            # Insérer la person_box avant le bouton "+"
            children = container.get_children()
            add_button = children[-1]  # Le bouton "+" est le dernier enfant
            container.pack_start(person_box, False, False, 0)
            container.reorder_child(person_box, len(children) - 1)  # Place avant "+"

            container.show_all()
            self.person_count += 1

            # Mettre à jour les ingrédients
            self.update_ingredients()

            # Désactiver le bouton "+" si le max est atteint
            if self.person_count >= 5:
                add_button.set_sensitive(False)

    def remove_person_image(self, button, person_box):
        container = person_box.get_parent()
        container.remove(person_box)
        container.show_all()
        self.person_count -= 1

        # Mettre à jour les ingrédients
        self.update_ingredients()

        # Réactiver le bouton "+" si le nombre de personnes est inférieur à 5
        add_button = container.get_children()[-1]  # Le bouton "+" est toujours le dernier
        if not add_button.get_sensitive():
            add_button.set_sensitive(True)

    def update_ingredients(self):
        # Vider le conteneur des ingrédients
        for child in self.ingredients_container.get_children():
            self.ingredients_container.remove(child)

        # Pour chaque ingrédient, afficher l'image et la quantité
        for ingredient in self.ingredients:
            # Créer une box pour cet ingrédient
            ingredient_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)

            # Charger l'image de l'ingrédient avec une taille plus grande
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(ingredient['image'], 200, 200, True)
            ingredient_image = Gtk.Image.new_from_pixbuf(pixbuf)

            # Calculer la quantité totale en fonction du nombre de personnes
            total_quantity = ingredient['per_person_quantity'] * self.person_count - 1

            # Créer un label pour la quantité avec une taille de police plus grande
            quantity_label = Gtk.Label()
            markup = f"<span size='xx-large'>{total_quantity} {ingredient['unit']}</span>"
            quantity_label.set_markup(markup)

            # Ajouter l'image et le label à la box de l'ingrédient
            ingredient_box.pack_start(ingredient_image, False, False, 0)
            ingredient_box.pack_start(quantity_label, False, False, 0)

            # Ajouter la box de l'ingrédient au conteneur des ingrédients
            self.ingredients_container.pack_start(ingredient_box, False, False, 0)

        # Afficher tous les widgets
        self.ingredients_container.show_all()

    def update_screen(self, screen_name, new_content=None):
        """
        Met à jour le contenu d'un écran.
        """
        # Récupérer l'écran depuis le Gtk.Stack
        screen = self.stack.get_child_by_name(screen_name)

    def on_button_clicked(self, button, screen_name):
        """
        Gère le clic sur les boutons pour afficher l'écran correspondant.
        """
        # Mettre à jour le contenu dynamiquement avant d'afficher
        if screen_name == "screen_1":
            self.update_screen("screen_1")
        elif screen_name == "screen_2":
            self.update_screen("screen_2")
        elif screen_name == "screen_3":
            self.update_screen("screen_3")

        self.stack.set_visible_child_name(screen_name)

    def create_image_button(self, image_path):
        """
        Crée un bouton avec une image comme arrière-plan.
        """
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(image_path, 300, 300, True)
        image = Gtk.Image.new_from_pixbuf(pixbuf)

        button = Gtk.Button()
        button.set_image(image)
        return button
