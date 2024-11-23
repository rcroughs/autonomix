import gi 
import subprocess
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GdkPixbuf

class PhoneWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Phone Directory")

        # LISTE DE CONTACTS

        self.contacts = [
            {"name": "Boy", "phone": "+32111111111", "image": "front/img/shopping_icons/boy1.jpg"},
            {"name": "Mom", "phone": "+32222222222", "image": "front/img/shopping_icons/mom.jpg"},
            {"name": "Man", "phone": "+32333333333", "image": "front/img/shopping_icons/man.jpg"},
            {"name": "Doctor", "phone": "+32444444444", "image": "front/img/shopping_icons/doctor.jpeg"}
        ]

        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(b"""
            window {
                background-color: #58855c;
            }
            button {
                background-color: #2BF52E;
                border-radius: 10px;
            }
        """)
        
        # Appliquer la feuille de style
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )


        self.grid = Gtk.Grid()
        self.grid.set_halign(Gtk.Align.CENTER)
        self.grid.set_valign(Gtk.Align.CENTER)
        self.grid.set_row_spacing(10)
        self.grid.set_column_spacing(10)
        self.grid.set_row_homogeneous(False)
        self.grid.set_column_homogeneous(False)
        self.add(self.grid)

        self.maximize()

        #plus
        self.plus = Gtk.Button()
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
            "front/img/shopping_icons/plus.png", 
            width=150,  # Set appropriate width
            height=150,  # Set appropriate height
            preserve_aspect_ratio=True
        )
        image5 = Gtk.Image.new_from_pixbuf(pixbuf)
        self.plus.set_image(image5)
        self.plus.connect("clicked", self.on_plus_clicked)
        
        self.update_contacts()

    def update_contacts(self):
        for wid in self.grid.get_children():
            self.grid.remove(wid)

        for index, contact in enumerate(self.contacts):
            button = Gtk.Button()
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
                contact["image"],
                width = 400,
                height = 400,
                preserve_aspect_ratio = True
            )
            button.set_image(Gtk.Image.new_from_pixbuf(pixbuf))
            button.connect("clicked", self.on_contact_clicked, contact["phone"])
            self.grid.attach(button, index//2, index%2, 1, 1)
        
        self.grid.attach(self.plus, 0, (len(self.contacts)+1)//2, 2, 1)
        self.show_all()

    def  on_contact_clicked(self, widget, phone_number):
        subprocess.run(["skype", f"tel:{phone_number}"], check=True)

    def on_plus_clicked(self, widget):
        dialog = Gtk.Dialog(title="Add Contact", transient_for=self, flags=0)
        dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK)
        dialog.set_default_size(400,400)

        box = dialog.get_content_area()

        name_entry = Gtk.Entry()
        name_entry.set_placeholder_text("Name")
        box.add(name_entry)

        phone_entry = Gtk.Entry()
        phone_entry.set_placeholder_text("Phone Number")
        box.add(phone_entry)

        image_entry = Gtk.Entry()
        image_entry.set_placeholder_text("Image Path")
        box.add(image_entry)

        box.show_all()
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            name = name_entry.get_text()
            phone = phone_entry.get_text()
            image = image_entry.get_text()

            if name and phone and image:
                # Ajouter le nouveau contact
                self.contacts.append({"name": name, "phone": phone, "image": image})
                self.update_contacts()

        dialog.destroy()

phoneWindow = PhoneWindow()
phoneWindow.connect("destroy", Gtk.main_quit)
phoneWindow.show_all()
Gtk.main()