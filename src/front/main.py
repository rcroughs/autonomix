import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GdkPixbuf
from telephone import PhoneWindow


class MyApp(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="com.example.autonomix")
        self.pixbuf1 = GdkPixbuf.Pixbuf.new_from_file("img/main_menu/food.png")
        self.pixbuf2 = GdkPixbuf.Pixbuf.new_from_file("img/main_menu/todo.png")
        self.pixbuf3 = GdkPixbuf.Pixbuf.new_from_file("img/main_menu/courses.png")
        self.pixbuf4 = GdkPixbuf.Pixbuf.new_from_file("img/main_menu/tel.png")
        self.previous_window_size = None  # Track the previous window size

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

        # Sub-screens
        screen = PhoneWindow()
        # # label = Gtk.Label(label=f"This is screen")
        # return_button = Gtk.Button(label="Return")
        # return_button.connect("clicked", self.show_screen, stack, "main_menu")
        # screen.pack_start(label, False, False, 0)
        # screen.pack_start(return_button, False, False, 0)
        stack.add_named(screen, "screen4")  # Ensure screen name is consistent

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


app = MyApp()
app.run()
