import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk


class MyApp(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="com.example.MyApp")

    def do_activate(self):
        # Main window
        window = Gtk.ApplicationWindow(application=self)
        window.set_title("My App")
        window.set_default_size(400, 300)

        # Stack for multiple screens
        stack = Gtk.Stack()
        stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)

        # Main menu
        main_menu = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        for i in range(5):
            button = Gtk.Button(label=f"Screen {i+1}")
            button.connect("clicked", self.show_screen, stack, f"screen{i+1}")
            main_menu.append(button)
        stack.add_named(main_menu, "main_menu")

        # Sub-screens
        for i in range(5):
            screen = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
            label = Gtk.Label(label=f"This is screen {i+1}")
            return_button = Gtk.Button(label="Return")
            return_button.connect("clicked", self.show_screen, stack, "main_menu")
            screen.append(label)
            screen.append(return_button)
            stack.add_named(screen, f"screen{i+1}")

        # Add stack to the window
        window.set_child(stack)
        window.present()

    def show_screen(self, button, stack, screen_name):
        stack.set_visible_child_name(screen_name)


app = MyApp()
app.run()
