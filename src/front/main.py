from typing import Optional
from screeninfo import get_monitors
import sys
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GdkPixbuf, Gdk
from telephone import PhoneWindow
from shopping_list import ShoppingMenu
from to_do import AccessibleTodoListWindow
from recipe import RecipeWindow
import requests
import os.path
import api

token = None


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

        # Register Button
        self.register_button = Gtk.Button(label="Register")
        self.register_button.connect("clicked", self.on_register_clicked)
        layout.pack_start(self.register_button, False, False, 0)

        # Feedback label
        self.feedback_label = Gtk.Label()
        layout.pack_start(self.feedback_label, False, False, 0)

        layout.show_all()

    def on_login_clicked(self, button):
        global token
        email = self.email_entry.get_text()
        password = self.password_entry.get_text()

        # Replace with your authentication logic
        response = api.login(email, password)
        if response is not None:
            token = response
            self.feedback_label.set_text("Login successful!")
            self.hide()  # Hide the login window
            app = MyApp()
            app.run()
        else:
            self.feedback_label.set_text("Invalid credentials. Try again.")

    def on_register_clicked(self, button):
        register_window = RegisterWindow(self)
        register_window.show_all()


class RegisterWindow(Gtk.Window):
    def __init__(self, login_window):
        super().__init__(title="Register")
        self.login_window = login_window
        self.set_border_width(10)
        self.set_default_size(300, 300)

        # Layout
        layout = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        layout.set_margin_top(20)
        layout.set_margin_bottom(20)
        layout.set_margin_start(20)
        layout.set_margin_end(20)
        self.add(layout)

        # Name Entry
        self.name_entry = Gtk.Entry()
        self.name_entry.set_placeholder_text("Name")
        layout.pack_start(self.name_entry, False, False, 0)

        # Email Entry
        self.email_entry = Gtk.Entry()
        self.email_entry.set_placeholder_text("Email")
        layout.pack_start(self.email_entry, False, False, 0)

        # Password Entry
        self.password_entry = Gtk.Entry()
        self.password_entry.set_placeholder_text("Password")
        self.password_entry.set_visibility(False)
        layout.pack_start(self.password_entry, False, False, 0)

        # Register Button
        self.register_button = Gtk.Button(label="Create Account")
        self.register_button.connect("clicked", self.on_register_clicked)
        layout.pack_start(self.register_button, False, False, 0)

        # Feedback Label
        self.feedback_label = Gtk.Label()
        layout.pack_start(self.feedback_label, False, False, 0)

    def on_register_clicked(self, button):
        name = self.name_entry.get_text()
        email = self.email_entry.get_text()
        password = self.password_entry.get_text()

        # Basic validation
        if not name or not email or not password:
            self.feedback_label.set_text("All fields are required.")
        else:
            # Save account in the simulated database
            api.register(name, email, password)
            self.feedback_label.set_text("Account created successfully!")
            self.close()  # Close the register window
            self.login_window.feedback_label.set_text(
                "Account created. You can now log in."
            )


class MyApp(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="com.example.autonomix")
        self.pixbuf1 = GdkPixbuf.Pixbuf.new_from_file("img/main_menu/food.png")
        self.pixbuf2 = GdkPixbuf.Pixbuf.new_from_file("img/main_menu/todo.png")
        self.pixbuf3 = GdkPixbuf.Pixbuf.new_from_file("img/main_menu/courses.png")
        self.pixbuf4 = GdkPixbuf.Pixbuf.new_from_file("img/main_menu/phone.png")
        self.previous_window_size = None  # Track the previous window size
        self.token = token
        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(b"""
            .return-button {\
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
        if len(sys.argv) < 2:
            input = 0
        else:
            input = int(sys.argv[1])
        monitor = get_monitors()[input]
        window.fullscreen()
        window.set_default_size(monitor.width, monitor.height)

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

        wscale = monitor.width / 2 - 300
        hscale = monitor.height / 2 - 150
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
        screen_recipe = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        recipe = RecipeWindow(token)
        return_button = Gtk.Button(label="←")
        return_button.get_style_context().add_class("return-button")
        return_button.set_halign(Gtk.Align.START)
        return_button.connect("clicked", self.show_screen, stack, "main_menu")
        screen_recipe.pack_start(return_button, False, False, 0)
        screen_recipe.pack_start(recipe, True, True, 0)
        stack.add_named(screen_recipe, "screen1")

        screen_phone = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        phone = PhoneWindow(token)
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

        screen_todo = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        todo = AccessibleTodoListWindow()
        return_button = Gtk.Button(label="←")
        return_button.get_style_context().add_class("return-button")
        return_button.set_halign(Gtk.Align.START)
        return_button.connect("clicked", self.show_screen, stack, "main_menu")
        screen_todo.pack_start(return_button, False, False, 0)
        screen_todo.pack_start(todo, True, True, 0)
        stack.add_named(screen_todo, "screen2")

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
            hscale*1.18, hscale, GdkPixbuf.InterpType.BILINEAR
        )
        self.pixbuf2 = self.pixbuf2.scale_simple(
            hscale, hscale, GdkPixbuf.InterpType.BILINEAR
        )
        self.pixbuf3 = self.pixbuf3.scale_simple(
            hscale * 1.13, hscale, GdkPixbuf.InterpType.BILINEAR
        )
        self.pixbuf4 = self.pixbuf4.scale_simple(
            hscale*1.23, hscale, GdkPixbuf.InterpType.BILINEAR
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
    global token
    if os.path.exists(api.token_file):
        with open(api.token_file, "r") as f:
            token = f.read()
            if token is not None:
                app = MyApp()
                app.run()
                return
    win = LoginWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()


main()
