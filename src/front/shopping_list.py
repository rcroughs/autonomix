import gi
import subprocess

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GdkPixbuf


class ShoppingMenu(Gtk.Box):
    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.get_style_context().add_class("window-shop")


        self.white_circle_path = "img/shopping_icons/cropped_image(1).png"
        self.green_circle_path = "img/shopping_icons/cropped_image.png"

        # LISTE DE COURSES
        self.items = [
            "img/shopping_icons/6aaaa4aa91a44d6ea88d1c9cb2626827.png",
            "img/shopping_icons/png-clipart-unopened-milk-carton-illustration-milk-paper-tetra-pak-carton-milk-milk-box-model-blue-white-thumbnail-removebg-preview.png",
            "img/shopping_icons/435979677b2eae91687cc7685bcabcbe.png",
            "img/shopping_icons/ai-generated-breakfast-cereal-isolated-on-transparent-background-free-png.png",
            "img/shopping_icons/lemon-png-image-0.png",
            "img/shopping_icons/png-clipart-red-bell-pepper-bell-pepper-chili-pepper-red-pepper-natural-foods-food-thumbnail-removebg-preview.png",
            "img/shopping_icons/png-clipart-sack-of-wheat-flour-atta-flour-dal-wheat-flour-roti-flour-and-wheat-food-whole-grain-removebg-preview.png",
            "img/shopping_icons/pngimg.com - banana_PNG842.png",
            "img/shopping_icons/pngimg.com - butter_PNG17.png",
            "img/shopping_icons/pngimg.com - coffee_beans_PNG9284.png",
            "img/shopping_icons/34-egg-png-image-thumb.png",
            "img/shopping_icons/pngimg.com - tomato_PNG12528.png",
            "img/shopping_icons/pngtree-a-piece-of-meat-that-is-cut-in-half-png-image_11955762.png",
            "img/shopping_icons/pngtree-bakery-bread-milky-plain-white-bread-png-image_11503244.png",
            "img/shopping_icons/pngtree-fresh-apple-fruit-red-png-image_10203073.png",
            "img/shopping_icons/pngtree-fresh-orange-png-png-image_10159570.png",
            "img/shopping_icons/pngtree-salami-dry-bonded-isolated-picture-image_13042049.png",
            "img/shopping_icons/pngtree-strawberry-ice-cream-cone-png-image_11925089.png",
            "img/shopping_icons/pngtree-sugar-white-sugar-picture-image_13276467.png",
            "img/shopping_icons/pngtree-the-peach-fruit-png-png-image_11500775.png",
            "img/shopping_icons/purepng.com-cheesefood-organic-cheese-piece-block-dairy-9415246353872kvm0.png",
            "img/shopping_icons/rice-removebg-preview.png",
            "img/shopping_icons/whole-grains-beans-isolated-healthy-diet-raw-ingredients-free-png.png"
        ]

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
        erase_button.set_valign(Gtk.Align.END)
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
            "img/shopping_icons/trash.png",
            width=50,
            height=50,
            preserve_aspect_ratio=True,
        )
        erase_image = Gtk.Image.new_from_pixbuf(pixbuf)
        erase_button.set_image(erase_image)
        erase_button.connect("clicked", self.erase_everything)

        # Add erase button at the bottom
        list_and_button_box.pack_start(erase_button, False, False, 0)

        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(b"""
            .window-shop {
                background-color: #716D54;
            }
            .button-shop {
                background-color: transparent;
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
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
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

            item_container1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
            item_container1.set_margin_top(10)  # Add top margin
            item_container1.set_margin_start(30)  # Add left margin
            

            # Load the image
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
                image_path, width=100, height=100, preserve_aspect_ratio=False
            )
            image = Gtk.Image.new_from_pixbuf(pixbuf)

            image.set_halign(Gtk.Align.CENTER)  # Horizontal alignment: Center
            image.set_valign(Gtk.Align.CENTER)

            plus_button = Gtk.Button(label="+")
            minus_button = Gtk.Button(label="-")
            plus_button.get_style_context().add_class("quantity-buttons")
            minus_button.get_style_context().add_class("quantity-buttons")
            
            
            # Connect signals
            plus_button.connect("clicked", self.add_to_shopping_list, image_path)
            minus_button.connect("clicked", self.remove_from_shopping_list, image_path)

            # Add the image and buttons to the vertical box
            item_container1.pack_start(image, False, False, 0)
            item_container1.pack_start(plus_button, False, False, 0)
            item_container1.pack_start(minus_button, False, False, 0)

            # Add the item container to the grid
            self.grid.attach(item_container1, col, row, 1, 1)

    def add_to_shopping_list(self, button, path):
        if path not in self.shopping_list:
            self.shopping_list[path] = 0
        self.shopping_list[path] += 1
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
            item_box.set_margin_top(30)

            # Load the image
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
                image_path, width=100, height=100, preserve_aspect_ratio=True
            )
            image = Gtk.Image.new_from_pixbuf(pixbuf)

            # Create a label to show the quantity
            quantity_label = Gtk.Label(label=f"{quantity}")
            quantity_label.get_style_context().add_class("quantity-label")

            toggle = Gtk.Button()
            toggle.set_relief(Gtk.ReliefStyle.NONE)
            toggle.set_image(Gtk.Image.new_from_pixbuf(
                GdkPixbuf.Pixbuf.new_from_file_at_scale(self.white_circle_path, width=30, height=30, preserve_aspect_ratio=True)
            ))
            toggle.get_style_context().add_class("button-shop")


            # Connect the toggle functionality
            self.toggle_state = False
            toggle.connect("clicked", self.toggle_circle, toggle)

            # Add the image and label to the horizontal box
            item_box.pack_start(quantity_label, False, False, 0)
            item_box.pack_start(image, False, False, 0)
            item_box.pack_start(toggle, False, False, 0)

            # Add the item box to the shopping list box
            self.shopping_list_box.add(item_box)
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
        self.toggle_state = False