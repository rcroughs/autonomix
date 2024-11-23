from typing import Optional
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GdkPixbuf, Gdk
from telephone import PhoneWindow
from shopping_list import ShoppingMenu
import requests

url = "http://127.0.0.1:5000"
token = None


def register(name, mail, password):
    data = {"name": name, "mail": mail, "password": password}
    try:
        # Envoi de la requête POST
        response = requests.post(url + "/auth/register", json=data)

        # Affichage de la réponse
        if response.status_code == 200:
            print("Enregistrement réussi :", response.json())
        else:
            print(f"Erreur {response.status_code} :", response.text)

    except requests.exceptions.RequestException as e:
        print("Erreur lors de la connexion :", e)


def login(mail, password) -> Optional[str]:
    global token
    data = {"mail": mail, "password": password}
    try:
        # Envoi de la requête POST
        response = requests.post(url + "/auth/login", json=data)
        # Affichage de la réponse
        if response.status_code == 200:
            print("Connexion réussie :", response.json())
            token = response.json()["token"]
            return token
        else:
            print(f"Erreur {response.status_code} :", response.text)
            return None
    except requests.exceptions.RequestException as e:
        print("Erreur lors de la connexion :", e)
        return None


class LoginWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Login")
        self.set_border_width(10)
        self.set_default_size(300, 200)

        # Main layout
        layout = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(layout)

        # Username
        self.email_entry = Gtk.Entry()
        self.email_entry.set_placeholder_text("Email")
        layout.pack_start(self.email_entry, False, False, 0)

        # Password
        self.password_entry = Gtk.Entry()
        self.password_entry.set_placeholder_text("Password")
        self.password_entry.set_visibility(False)  # Hide password input
        layout.pack_start(self.password_entry, False, False, 0)

        # Login button
        self.login_button = Gtk.Button(label="Login")
        self.login_button.connect("clicked", self.on_login_clicked)
        layout.pack_start(self.login_button, False, False, 0)

        # Feedback label
        self.feedback_label = Gtk.Label()
        layout.pack_start(self.feedback_label, False, False, 0)

        layout.show_all()

    def on_login_clicked(self, button):
        email = self.email_entry.get_text()
        password = self.password_entry.get_text()

        # Replace with your authentication logic
        response = login(email, password)
        if response is not None:
            self.feedback_label.set_text("Login successful!")
            self.hide()  # Hide the login window
            app = MyApp()
            app.run()
        else:
            self.feedback_label.set_text("Invalid credentials. Try again.")


class MyApp(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="com.example.autonomix")
        self.pixbuf1 = GdkPixbuf.Pixbuf.new_from_file("img/main_menu/food.png")
        self.pixbuf2 = GdkPixbuf.Pixbuf.new_from_file("img/main_menu/todo.png")
        self.pixbuf3 = GdkPixbuf.Pixbuf.new_from_file("img/main_menu/courses.png")
        self.pixbuf4 = GdkPixbuf.Pixbuf.new_from_file("img/main_menu/tel.png")
        self.previous_window_size = None  # Track the previous window size
        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(b"""
            .return-button {
            color: #FFFFFF;
            border-radius: 5px;
            padding: 5px;
            padding-left: 10px;
            padding-left: 10px;
            font-size: 60px;
            }
        """)

        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        )

    def do_activate(self):
        window = Gtk.ApplicationWindow(application=self)
        window.set_title("Autonomix")
        window.set_default_size(800, 600)
        window.maximize()

        stack = Gtk.Stack()
        stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)

        grid = Gtk.Grid()
        grid.set_row_spacing(10)
        grid.set_column_spacing(10)
        grid.halign = Gtk.Align.CENTER
        grid.valign = Gtk.Align.CENTER

        # Create buttons
        self.button1 = Gtk.Button()
        self.button2 = Gtk.Button()
        self.button3 = Gtk.Button()
        self.button4 = Gtk.Button()

        wscale = window.get_size()[0] / 2
        hscale = window.get_size()[1] / 2
        self.update_images(wscale, hscale)

        image1 = Gtk.Image.new_from_pixbuf(self.pixbuf1)
        image2 = Gtk.Image.new_from_pixbuf(self.pixbuf2)
        image3 = Gtk.Image.new_from_pixbuf(self.pixbuf3)
        image4 = Gtk.Image.new_from_pixbuf(self.pixbuf4)

        # Assign images to buttons
        self.button1.set_image(image1)
        self.button2.set_image(image2)
        self.button3.set_image(image3)
        self.button4.set_image(image4)

        for button in (self.button1, self.button2, self.button3, self.button4):
            button.set_hexpand(True)
            button.set_vexpand(True)

        grid.attach(self.button1, 0, 0, 1, 1)
        grid.attach(self.button2, 1, 0, 1, 1)
        grid.attach(self.button3, 0, 1, 1, 1)
        grid.attach(self.button4, 1, 1, 1, 1)

        self.button1.connect("clicked", self.show_screen, stack, "screen1")
        self.button2.connect("clicked", self.show_screen, stack, "screen2")
        self.button3.connect("clicked", self.show_screen, stack, "screen3")
        self.button4.connect("clicked", self.show_screen, stack, "screen4")

        # Main Menu screen
        stack.add_named(grid, "main_menu")

        return_button = Gtk.Button(label="←")
        return_button.get_style_context().add_class("return-button")
        return_button.set_halign(Gtk.Align.START)
        return_button.connect("clicked", self.show_screen, stack, "main_menu")

        # Sub-screens
        screen_phone = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        phone = PhoneWindow()
        return_button = Gtk.Button(label="←")
        return_button.get_style_context().add_class("return-button")
        return_button.set_halign(Gtk.Align.START)
        return_button.connect("clicked", self.show_screen, stack, "main_menu")
        screen_phone.pack_start(return_button, False, False, 0)
        screen_phone.pack_start(phone, True, True, 0)
        # # label = Gtk.Label(label=f"This is screen")
        # return_button = Gtk.Button(label="Return")
        # return_button.connect("clicked", self.show_screen, stack, "main_menu")
        # screen.pack_start(label, False, False, 0)
        # screen.pack_start(return_button, False, False, 0)
        stack.add_named(screen_phone, "screen4")  # Ensure screen name is consistent

        shopping_screen = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        shopping = ShoppingMenu()
        return_button = Gtk.Button(label="←")
        return_button.get_style_context().add_class("return-button")
        return_button.set_halign(Gtk.Align.START)
        return_button.connect("clicked", self.show_screen, stack, "main_menu")
        shopping.set_hexpand(True)
        shopping.set_vexpand(True)
        shopping.set_halign(Gtk.Align.FILL)
        shopping.set_valign(Gtk.Align.FILL)
        shopping_screen.pack_start(return_button, False, False, 0)
        shopping_screen.pack_start(shopping, True, True, 0)
        stack.add_named(shopping_screen, "screen3")

        window.add(stack)

        # Set the default visible child of the stack to be 'main_menu'
        stack.set_visible_child_name("main_menu")

        window.show_all()

    def update_images(self, wscale, hscale):
        self.pixbuf1 = self.pixbuf1.scale_simple(
            wscale, hscale, GdkPixbuf.InterpType.BILINEAR
        )
        self.pixbuf2 = self.pixbuf2.scale_simple(
            wscale, hscale, GdkPixbuf.InterpType.BILINEAR
        )
        self.pixbuf3 = self.pixbuf3.scale_simple(
            wscale, hscale, GdkPixbuf.InterpType.BILINEAR
        )
        self.pixbuf4 = self.pixbuf4.scale_simple(
            wscale, hscale, GdkPixbuf.InterpType.BILINEAR
        )

    def do_resize(self, window):
        width, height = window.get_size()
        wscale = width / 2
        hscale = height / 2
        self.update_images(wscale, hscale)

        self.button1.set_image(Gtk.Image.new_from_pixbuf(self.pixbuf1))
        self.button2.set_image(Gtk.Image.new_from_pixbuf(self.pixbuf2))
        self.button3.set_image(Gtk.Image.new_from_pixbuf(self.pixbuf3))
        self.button4.set_image(Gtk.Image.new_from_pixbuf(self.pixbuf4))

    def show_screen(self, button, stack, screen_name):
        stack.set_visible_child_name(screen_name)


def main():
    win = LoginWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()

register("sasha", "sasha", "sasha")

main()
