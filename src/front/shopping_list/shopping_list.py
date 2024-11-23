import gi 
import subprocess
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GdkPixbuf

class ShoppingMenu(Gtk.Window):
    def __init__(self):
        super().__init__(title="Shopping List")
        self.maximize()

        self.white_circle_path = "front/img/shopping_icons/cropped_image(1).png"
        self.green_circle_path = "front/img/shopping_icons/cropped_image.png"
        self.toggle_data = False


        # LISTE DE COURSES
        self.items = ["front/img/shopping_icons/184532.png",
            "front/img/shopping_icons/395211.png",
            "front/img/shopping_icons/766020.png",
            "front/img/shopping_icons/837560.png",
            "front/img/shopping_icons/883514.png",
            "front/img/shopping_icons/1206237.png",
            "front/img/shopping_icons/2079330.png",
            "front/img/shopping_icons/2909779.png",
            "front/img/shopping_icons/2909894.png",
            "front/img/shopping_icons/3093581.png",
            "front/img/shopping_icons/4853298.png",
            "front/img/shopping_icons/7401602.png",
            "front/img/shopping_icons/banane.png",
            "front/img/shopping_icons/bouteille-de-lait.png",
            "front/img/shopping_icons/cafe.png",
            "front/img/shopping_icons/farine.png",
            "front/img/shopping_icons/leau.png",
            "front/img/shopping_icons/lemon_6866595.png",
            "front/img/shopping_icons/orange.png",
            "front/img/shopping_icons/pain.png",
            "front/img/shopping_icons/peach_680930.png",
            "front/img/shopping_icons/pomme.png",
            "front/img/shopping_icons/potato_1652127.png",
            "front/img/shopping_icons/sucre.png"]
        
        self.shopping_list = {}

        self.grid = Gtk.Grid()
        self.grid.set_row_spacing(20)
        self.grid.set_column_spacing(30)


        # Vertical layout
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(vbox)
        vbox.pack_start(self.grid, True, True, 0)

        self.shopping_list_box = Gtk.FlowBox()
        self.shopping_list_box.set_max_children_per_line(8)
        self.shopping_list_box.set_selection_mode(Gtk.SelectionMode.NONE)

        list_and_button_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        vbox.pack_start(list_and_button_box, False, False, 0)

        # Add shopping list above the button
        list_and_button_box.pack_start(self.shopping_list_box, True, True, 0)

        # Erase Everything button
        erase_button = Gtk.Button()
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
            "front/img/shopping_icons/trash.png", 
            width=50, height=50, preserve_aspect_ratio=True
        )
        erase_image = Gtk.Image.new_from_pixbuf(pixbuf)
        erase_button.set_image(erase_image)
        erase_button.connect("clicked", self.erase_everything)

        # Add erase button at the bottom
        list_and_button_box.pack_start(erase_button, False, False, 0)

        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(b"""
            window {
                background-color: #B36BF9;
            }
            button {
                border-radius: 10px;
            }
            .quantity-label {
                font-size: 70px;
                color: #000000;
            }
            .quantity-buttons {
                font-size: 35px;
                color: #FFFFFF;
                font-weight: bold;
            }
        """)

        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )


        # Populate initial grid
        self.update_grid()

    def update_grid(self):
        rows = 2
        columns = 12
        total_items = rows * columns

        for index, image_path in enumerate(self.items[:total_items]):
            # Calculate row and column
            row = index // columns
            col = index % columns

            item_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
            item_container.set_margin_top(10)  # Add top margin
            item_container.set_margin_start(30)  # Add left margin

            # Load the image
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(image_path, width=100, height=100, preserve_aspect_ratio=True)
            image = Gtk.Image.new_from_pixbuf(pixbuf)

            plus_button = Gtk.Button(label="+")
            minus_button = Gtk.Button(label="-")
            plus_button.get_style_context().add_class("quantity-buttons")
            minus_button.get_style_context().add_class("quantity-buttons")

            # Connect signals
            plus_button.connect("clicked", self.add_to_shopping_list, image_path)
            minus_button.connect("clicked", self.remove_from_shopping_list, image_path)

            # Add the image and buttons to the vertical box
            item_container.pack_start(image, False, False, 0)
            item_container.pack_start(plus_button, False, False, 0)
            item_container.pack_start(minus_button, False, False, 0)

            # Add the item container to the grid
            self.grid.attach(item_container, col, row, 1, 1)

    def add_to_shopping_list(self, button, path):
        if path not in self.shopping_list:
            self.shopping_list[path] = 0
        self.shopping_list[path] +=1
        self.update_shopping_list()

    def remove_from_shopping_list(self, button, path):
        if path in self.shopping_list and self.shopping_list[path] > 0:
            self.shopping_list[path] -= 1
            if self.shopping_list[path] == 0:
                del self.shopping_list[path]
        self.update_shopping_list()

    def update_shopping_list(self):
        for child in self.shopping_list_box.get_children():
            self.shopping_list_box.remove(child)

        for image_path, quantity in self.shopping_list.items():
            # Horizontal box for the item and quantity
            item_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)

            # Load the image
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(image_path, width=100, height=100, preserve_aspect_ratio=True)
            image = Gtk.Image.new_from_pixbuf(pixbuf)

            # Create a label to show the quantity
            quantity_label = Gtk.Label(label=f"{quantity}")
            quantity_label.get_style_context().add_class("quantity-label")
            toggle = Gtk.Button()
            toggle.set_relief(Gtk.ReliefStyle.NONE)
            toggle.set_image(Gtk.Image.new_from_pixbuf(
                GdkPixbuf.Pixbuf.new_from_file_at_scale(self.white_circle_path, width=30, height=30, preserve_aspect_ratio=True)
            ))

            # Connect the toggle functionality
            self.toggle_state = False
            toggle.connect("clicked", self.toggle_circle, toggle)

            # Add the image and label to the horizontal box
            item_box.pack_start(quantity_label, False, False, 0)
            item_box.pack_start(image, False, False, 0)
            item_box.pack_start(toggle, False, False, 0)


            # Add the item box to the shopping list box
            self.shopping_list_box.add(item_box)

        # Show all updates
        self.shopping_list_box.show_all()
    
    def erase_everything(self, button):
        self.shopping_list.clear()
        self.update_shopping_list()


    def toggle_circle(self, button, toggle_button):
        # Toggle the state
        new_state = not self.toggle_state
        self.toggle_state = new_state
        # Update the image based on the new state
        if new_state:
            # Set to green circle
            toggle_button.set_image(Gtk.Image.new_from_pixbuf(
                GdkPixbuf.Pixbuf.new_from_file_at_scale(self.green_circle_path, width=30, height=30, preserve_aspect_ratio=True)
            ))
        else:
            # Set to white circle
            toggle_button.set_image(Gtk.Image.new_from_pixbuf(
                GdkPixbuf.Pixbuf.new_from_file_at_scale(self.white_circle_path, width=30, height=30, preserve_aspect_ratio=True)
            ))


    


shoppingWindow = ShoppingMenu()
shoppingWindow.connect("destroy", Gtk.main_quit)
shoppingWindow.show_all()
Gtk.main()