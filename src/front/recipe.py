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
            .etapes{
                font-size: 70px;
                color: #000000;
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

        ingredients_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        screen.add(ingredients_box)
        ingredients_box.set_halign(Gtk.Align.CENTER)  # Center-align the box
        ingredients_box.set_margin_top(20)  # Add some top margin
        

        if screen_name == "screen_3":
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale("img/shopping_icons/ai-generated-potato-food-free-png.png", width=100, height=100, preserve_aspect_ratio=True)
            image = Gtk.Image.new_from_pixbuf(pixbuf)
            ingredients_box.pack_start(image, False, False, 0)
            pixbuf2 = GdkPixbuf.Pixbuf.new_from_file_at_scale("img/shopping_icons/ai-generated-potato-food-free-png.png", width=100, height=100, preserve_aspect_ratio=True)
            image2 = Gtk.Image.new_from_pixbuf(pixbuf2)
            ingredients_box.pack_start(image2, False, False, 0)
            pixbuf3 = GdkPixbuf.Pixbuf.new_from_file_at_scale("img/shopping_icons/28021-1024x1024-removebg-preview.png", width=150, height=150, preserve_aspect_ratio=True)
            image3 = Gtk.Image.new_from_pixbuf(pixbuf3)
            ingredients_box.pack_start(image3, False, False, 0)
            pixbuf4 = GdkPixbuf.Pixbuf.new_from_file_at_scale("img/shopping_icons/pngimg.com - salt_PNG22363.png", width=150, height=150, preserve_aspect_ratio=True)
            image4 = Gtk.Image.new_from_pixbuf(pixbuf4)
            ingredients_box.pack_start(image4, False, False, 0)

        etapes_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        screen.add(etapes_box)
        etapes_box.set_halign(Gtk.Align.CENTER)  # Center-align the box
        etapes_box.set_margin_top(20)  # Add some top margin

        if screen_name == "screen_3":
            lab1 = Gtk.Label(label="1")
            lab1.get_style_context().add_class("etapes")
            pixbuf5 = GdkPixbuf.Pixbuf.new_from_file_at_scale("img/recipes_icons/550px-nowatermark-Clean-Potatoes-Step-2-Version-5.jpg", width=200, height=200, preserve_aspect_ratio=True)
            image5 = Gtk.Image.new_from_pixbuf(pixbuf5)
            image5.set_margin_end(50)
            image5.set_margin_top(50)
            etapes_box.pack_start(lab1, False, False, 0)
            etapes_box.pack_start(image5, False, False, 0)
            lab2 = Gtk.Label(label="2")
            lab2.get_style_context().add_class("etapes")
            pixbuf6 = GdkPixbuf.Pixbuf.new_from_file_at_scale("img/recipes_icons/doit-eplucher-les-pommes-terre-avant-les-faire-cuire-une-dieteticienne-tranche.jpeg", width=200, height=200, preserve_aspect_ratio=True)
            image6 = Gtk.Image.new_from_pixbuf(pixbuf6)
            image6.set_margin_end(50)
            image6.set_margin_top(50)
            etapes_box.pack_start(lab2, False, False, 0)
            etapes_box.pack_start(image6, False, False, 0)
            lab3 = Gtk.Label(label="3")
            lab3.get_style_context().add_class("etapes")
            pixbuf7 = GdkPixbuf.Pixbuf.new_from_file_at_scale("img/recipes_icons/medium_Capture_decran_2020_03_17_a_16_23_26_o_G_Pk_Nr1_3fcf265d07.jpeg", width=200, height=200, preserve_aspect_ratio=True)
            image7 = Gtk.Image.new_from_pixbuf(pixbuf7)
            image7.set_margin_end(50)
            image7.set_margin_top(50)
            etapes_box.pack_start(lab3, False, False, 0)
            etapes_box.pack_start(image7, False, False, 0)
        
        etapes_box2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        screen.add(etapes_box2)
        etapes_box2.set_halign(Gtk.Align.CENTER)  # Center-align the box
        etapes_box2.set_margin_top(20)  # Add some top margin

        if screen_name == "screen_3":
            lab4 = Gtk.Label(label="4")
            lab4.get_style_context().add_class("etapes")
            pixbuf8 = GdkPixbuf.Pixbuf.new_from_file_at_scale("img/recipes_icons/image.png", width=200, height=200, preserve_aspect_ratio=True)
            image8 = Gtk.Image.new_from_pixbuf(pixbuf8)
            image8.set_margin_end(50)
            image8.set_margin_top(50)
            etapes_box2.pack_start(lab4, False, False, 0)
            etapes_box2.pack_start(image8, False, False, 0)
            lab5 = Gtk.Label(label="5")
            lab5.get_style_context().add_class("etapes")
            pixbuf9 = GdkPixbuf.Pixbuf.new_from_file_at_scale("img/recipes_icons/image(2).png", width=200, height=200, preserve_aspect_ratio=True)
            image9 = Gtk.Image.new_from_pixbuf(pixbuf9)
            image9.set_margin_end(50)
            image9.set_margin_top(50)
            etapes_box2.pack_start(lab5, False, False, 0)
            etapes_box2.pack_start(image9, False, False, 0)
            lab6 = Gtk.Label(label="6")
            lab6.get_style_context().add_class("etapes")
            pixbuf10 = GdkPixbuf.Pixbuf.new_from_file_at_scale("img/recipes_icons/image(5).png", width=200, height=200, preserve_aspect_ratio=True)
            image10 = Gtk.Image.new_from_pixbuf(pixbuf10)
            image10.set_margin_end(50)
            image10.set_margin_top(50)
            etapes_box2.pack_start(lab6, False, False, 0)
            etapes_box2.pack_start(image10, False, False, 0)
        

        screen.pack_start(ingredients_box, False, False, 0)
        screen.pack_start(etapes_box, False, False, 0)
        screen.pack_start(etapes_box2, False, False, 0)


            


        screen.show_all()
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


