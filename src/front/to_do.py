import gi
import datetime
import threading
import time

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GdkPixbuf, Gdk, GLib


class AccessibleTodoListWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="To-Do List")
        self.clicked = []
        self.set_border_width(20)
        self.maximize()


        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(b"""
                window {
                    background-color: #003366; 
                }
                .blue-box {
                    background-color: #003366;  
                    padding: 10px;
                }
                .countdown-label {
                    font-size: 35px;  
                    color: #FFFFFF; 
                }
                .countdown-label-grand {
                    font-size: 45px;  
                    color: #FFFFFF; 
                }
                .large-button {
                    min-width: 1000px;
                    min-height: 1000px;
                }
                """)
        screen = Gdk.Screen.get_default()
        style_context = Gtk.StyleContext()
        style_context.add_provider_for_screen(screen, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)


        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(vbox)


        self.button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.button_box.get_style_context().add_class("blue-box")
        vbox.pack_start(self.button_box, False, False, 0)


        clear_button = Gtk.Button()
        image_trash = Gtk.Image.new_from_file("img/to_do/trash.png")
        clear_button.set_image(image_trash)
        clear_button.connect("clicked", self.clear_tasks)
        vbox.pack_start(clear_button, False, False, 0)


        scrolled_window_tasks = Gtk.ScrolledWindow()
        scrolled_window_tasks.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scrolled_window_tasks.set_size_request(-1, 300)
        self.listbox = Gtk.ListBox()
        self.listbox.get_style_context().add_class("blue-box")
        scrolled_window_tasks.add(self.listbox)
        vbox.pack_start(scrolled_window_tasks, True, True, 0)


        self.image_paths = [
            ("img/to_do/chien.png", "Image 1"),
            ("img/to_do/clean.png", "Image 2"),
            ("img/to_do/groceries.png", "Image 4"),
            ("img/to_do/doctor.png", "Image 5"),
            ("img/to_do/pills.png", "Image 6")
        ]


        for idx, (img_path, desc) in enumerate(self.image_paths):
            self.add_image_to_buttons(img_path, desc, idx)

    def clear_tasks(self, widget):
        for row in self.listbox.get_children():
            self.listbox.remove(row)
        self.clicked.clear()

    def add_image_to_buttons(self, img_path, description, index):
        button = Gtk.Button()
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(img_path, 300, 300, True)
        image = Gtk.Image.new_from_pixbuf(pixbuf)
        button.set_image(image)
        button.set_tooltip_text(description)
        button.connect("clicked", self.on_image_clicked, img_path)
        self.button_box.pack_start(button, False, False, 0)

    def on_image_clicked(self, widget, img_path):
        dialog = DateTimePickerDialog(self)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            date, time_str = dialog.get_datetime()
            task_datetime = datetime.datetime.strptime(f"{date} {time_str}", "%Y-%m-%d %H:%M")
            self.add_task(img_path, task_datetime)
        dialog.destroy()

    def add_task(self, img_path, task_datetime):
        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)


        circle_button = Gtk.Button()
        circle_button.set_size_request(50, 50)
        circle_button.set_relief(Gtk.ReliefStyle.NONE)
        circle_image = Gtk.Image.new_from_file("img/to_do/CIRCLEwhite.png")
        circle_white = True
        circle_button.add(circle_image)
        circle_button.connect("clicked", self.on_circle_clicked, circle_button)
        self.clicked.append((circle_button, False))


        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(img_path, 100, 100, True)
        image = Gtk.Image.new_from_pixbuf(pixbuf)


        countdown_label = Gtk.Label(label="")
        self.update_countdown(countdown_label, task_datetime)


        hbox.pack_start(circle_button, False, False, 0)
        hbox.pack_start(image, False, False, 0)
        hbox.pack_start(countdown_label, False, False, 0)

        row.add(hbox)
        self.listbox.add(row)
        self.listbox.show_all()

    def update_countdown(self, label, task_datetime):
        def countdown():
            while True:
                now = datetime.datetime.now()
                remaining = task_datetime - now
                if remaining.total_seconds() <= 0:
                    today_str = "  ⏳"
                    GLib.idle_add(label.set_markup, today_str)

                    # Appliquer la classe CSS au label
                    GLib.idle_add(lambda: label.get_style_context().add_class("countdown-label-grand"))

                    break
                days, seconds = divmod(int(remaining.total_seconds()), 86400)
                hours, seconds = divmod(seconds, 3600)
                minutes, _ = divmod(seconds, 60)
                countdown_str = f"       <span size='x-large'>{days}☀️ {hours}🕐 {minutes}⏱️ restants</span>"
                GLib.idle_add(label.set_markup, countdown_str)

                # Appliquer la classe CSS au label
                GLib.idle_add(lambda: label.get_style_context().add_class("countdown-label"))

                time.sleep(60)
        threading.Thread(target=countdown, daemon=True).start()

    def on_circle_clicked(self, widget, circle_button):
        # Remplacer l'image du cercle par une nouvelle image (par exemple CIRCLEblue.png)
        new_circle_image = None  # Nouvelle image du cercle
        if (circle_button, False) in self.clicked:
            new_circle_image = Gtk.Image.new_from_file("img/to_do/cerclevert.png")
            self.clicked.remove((circle_button, False))
            self.clicked.append((circle_button, True))
        else:
            new_circle_image = Gtk.Image.new_from_file("img/to_do/CIRCLEwhite.png")
            self.clicked.remove((circle_button, True))
            self.clicked.append((circle_button, False))

        circle_button.remove(circle_button.get_child())  # Enlever l'image actuelle du cercle
        circle_button.add(new_circle_image)  # Ajouter la nouvelle image du cercle

        circle_button.show_all()

class DateTimePickerDialog(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title="Sélectionner date et heure", transient_for=parent, flags=0)
        self.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK)
        self.calendar = Gtk.Calendar()
        self.time_entry = Gtk.Entry()
        self.time_entry.set_text("12:00")
        box = self.get_content_area()
        box.add(Gtk.Label(label="Sélectionnez une date:"))
        box.add(self.calendar)
        box.add(Gtk.Label(label="Entrez l'heure (HH:MM):"))
        box.add(self.time_entry)
        self.show_all()

    def get_datetime(self):
        year, month, day = self.calendar.get_date()
        month += 1
        date = f"{year}-{month:02d}-{day:02d}"
        time_str = self.time_entry.get_text()
        return date, time_str


# Lancement de l'application
win = AccessibleTodoListWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()

