import gi
import api
import subprocess

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GdkPixbuf

tokeng = None


class PhoneWindow(Gtk.Box):
    def __init__(self, token: str):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.get_style_context().add_class("window-phone")
        self.token = token
        global tokeng
        tokeng = self.token

        # LISTE DE CONTACTS

        self.contacts = api.get_contacts(token)

        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(b"""
            .window-phone {
                background-color: #58855C;
            }
            .button-contact {
                background-color: #2BF52E;
                border-radius: 10px;
            }
        """)

        # Appliquer la feuille de style
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        )

        self.grid = Gtk.Grid()
        self.grid.set_halign(Gtk.Align.CENTER)
        self.grid.set_valign(Gtk.Align.CENTER)
        self.grid.set_row_spacing(10)
        self.grid.set_column_spacing(10)
        self.grid.set_row_homogeneous(False)
        self.grid.set_column_homogeneous(False)
        self.add(self.grid)

        # plus
        self.plus = Gtk.Button()
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
            "img/contacts/plus.png",
            width=150,  # Set appropriate width
            height=150,  # Set appropriate height
            preserve_aspect_ratio=True,
        )
        image5 = Gtk.Image.new_from_pixbuf(pixbuf)
        self.plus.set_image(image5)
        self.plus.connect("clicked", self.on_plus_clicked)

        self.update_contacts()

    def update_contacts(self):
        for wid in self.grid.get_children():
            self.grid.remove(wid)

        self.contacts = api.get_contacts(tokeng)

        if self.contacts is None:
            return
        for index, contact in enumerate(self.contacts):
            button = Gtk.Button()
            button.get_style_context().add_class("button-contact")

            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
                contact["image_url"], width=300, height=300, preserve_aspect_ratio=True
            )
            button.set_image(Gtk.Image.new_from_pixbuf(pixbuf))
            button.connect("clicked", self.on_contact_clicked, contact["phone_number"])
            self.grid.attach(button, index // 2, index % 2, 1, 1)

        self.grid.attach(self.plus, 0, (len(self.contacts) + 1) // 2, 2, 1)
        self.grid.show_all()

    def on_contact_clicked(self, widget, phone_number):
        subprocess.run(["skype", f"tel:{phone_number}"], check=True)

    def on_plus_clicked(self, widget):
        top_window = self.get_toplevel()
        dialog = Gtk.Dialog(title="Add Contact", transient_for=top_window, flags=0)
        dialog.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK
        )

        dialog.set_default_size(400, 400)

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
                api.add_contact(tokeng, name, phone, image)
                self.update_contacts()

        dialog.destroy()
