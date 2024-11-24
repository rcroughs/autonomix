import gi
import datetime
import threading
import time
import speech

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GdkPixbuf, Gdk, GLib


class AccessibleTodoListWindow(Gtk.Box):
    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.clicked = []
        self.get_style_context().add_class("window-todo")

        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(b"""
                .window-todo {
                    background-color: #90caf9; 
                }
                .blue-box {
                    background-color: #90caf9;  
                    margin:0;
                    padding:0; 
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
                .button-micro{
                    font-size: 40px;
                }
                """)
        screen = Gdk.Screen.get_default()
        style_context = Gtk.StyleContext()
        style_context.add_provider_for_screen(
            screen, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER
        )

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(vbox)

        self.button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.button_box.get_style_context().add_class("blue-box")
        self.button_box.set_margin_start(0)
        self.button_box.set_margin_end(0)
        self.button_box.set_margin_top(0)
        self.button_box.set_margin_bottom(0)
        vbox.pack_start(self.button_box, False, False, 0)

        clear_button = Gtk.Button()
        clear_button.set_valign(Gtk.Align.END)
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
            "img/shopping_icons/trash.png",
            width=50,
            height=50,
            preserve_aspect_ratio=True,
        )
        clear_image = Gtk.Image.new_from_pixbuf(pixbuf)
        clear_button.set_image(clear_image)
        clear_button.set_margin_start(0)
        clear_button.set_margin_end(0)
        clear_button.set_margin_top(0)
        clear_button.set_margin_bottom(0)
        clear_button.connect("clicked", self.clear_tasks)
        vbox.pack_start(clear_button, False, False, 0)

        self.listbox = Gtk.FlowBox()
        self.listbox.get_style_context().add_class("blue-box")
        self.listbox.set_margin_start(0)
        self.listbox.set_margin_end(0)
        self.listbox.set_margin_top(0)
        self.listbox.set_margin_bottom(0)
        self.listbox.set_max_children_per_line(1)
        self.listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        list_and_button_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        vbox.pack_start(list_and_button_box, False, False, 0)

        # Add shopping list above the button
        list_and_button_box.pack_start(self.listbox, True, True, 0)

        self.image_paths = [
            ("img/to_do/chien.png", "Image 1"),
            ("img/to_do/clean.png", "Image 2"),
            ("img/to_do/groceries.jpg", "Image 4"),
            ("img/to_do/doctor.jpeg", "Image 5"),
            ("img/to_do/pills.jpg", "Image 6"),
        ]

        for idx, (img_path, desc) in enumerate(self.image_paths):
            self.add_image_to_buttons(img_path, desc, idx)

    def clear_tasks(self, widget):
        for row in self.listbox.get_children():
            self.listbox.remove(row)
        self.clicked.clear()

    def add_image_to_buttons(self, img_path, description, index):
        button = Gtk.Button()
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(img_path, 200, 200, True)
        image = Gtk.Image.new_from_pixbuf(pixbuf)
        button.set_image(image)
        button.set_tooltip_text(description)
        button.set_margin_start(133)
        button.set_margin_top(10)
        button.connect("clicked", self.on_image_clicked, img_path)
        self.button_box.pack_start(button, False, False, 0)

    def on_image_clicked(self, widget, img_path):
        dialog = DateTimePickerDialog(self)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            date, time_str = dialog.get_datetime()
            task_datetime = datetime.datetime.strptime(
                f"{date} {time_str}", "%Y-%m-%d %H:%M"
            )
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

        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(img_path, 150, 150, True)
        image = Gtk.Image.new_from_pixbuf(pixbuf)

        countdown_label = Gtk.Label(label="")
        countdown_label.get_style_context().add_class("countdown-label")

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

                days, seconds = divmod(int(remaining.total_seconds()), 86400)
                hours, seconds = divmod(seconds, 3600)
                minutes, _ = divmod(seconds, 60)
                countdown_str = (
                    f"       <span size='x-large'>{days}☀️ {hours}🕐 {minutes}⏱️ </span>"
                )
                GLib.idle_add(label.set_markup, countdown_str)

                # Appliquer la classe CSS au label
                GLib.idle_add(
                    lambda: label.get_style_context().add_class("countdown-label")
                )

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

        circle_button.remove(
            circle_button.get_child()
        )  # Enlever l'image actuelle du cercle
        circle_button.add(new_circle_image)  # Ajouter la nouvelle image du cercle

        circle_button.show_all()


class DateTimePickerDialog(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title="Sélectionner date et heure", flags=0)
        self.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK
        )
        self.calendar = Gtk.Calendar()
        self.time_entry = Gtk.Entry()
        self.time_entry.set_text("12:00")
        self.micro_button = Gtk.Button(label="🎤")
        self.micro_button.get_style_context().add_class("button-micro")
        self.micro_button.set_tooltip_text("Utiliser la date et l'heure actuelles")
        self.micro_button.connect("clicked", self.on_micro_clicked)
        box = self.get_content_area()
        box.add(self.micro_button)
        box.add(Gtk.Label(label="Sélectionnez une date:"))
        box.add(self.calendar)
        box.add(Gtk.Label(label="Entrez l'heure (HH:MM):"))
        box.add(self.time_entry)
        box.show_all()

    def on_micro_clicked(self, widget):
        self.spinner = Gtk.Spinner()
        self.get_content_area().add(self.spinner)
        self.get_content_area().show_all()
        self.spinner.start()
        self.micro_button.set_sensitive(False)
        threading.Thread(target=self.run_speech_recording, daemon=True).start()

    def run_speech_recording(self):
        try:
            res = speech.record()
            if res is not None:
                parsed_datetime = datetime.datetime.fromisoformat(res)
                GLib.idle_add(self.update_ui_with_result, res)
            else:
                GLib.idle_add(self.on_recording_error)
        except Exception as e:
            GLib.idle_add(self.on_recording_error, str(e))

    def update_ui_with_result(self, res):
        self.spinner.stop()
        self.get_content_area().remove(self.spinner)
        self.micro_button.set_sensitive(True)

        # Update the calendar and time entry
        self.calendar.select_month(int(res[5:7]) - 1, int(res[:4]))
        self.calendar.select_day(int(res[8:10]))
        self.time_entry.set_text(res[11:16])

    def on_recording_error(self, error_message="Erreur lors de l'enregistrement"):
        self.spinner.stop()
        self.get_content_area().remove(self.spinner)
        self.micro_button.set_sensitive(True)
        error_dialog = Gtk.MessageDialog(
            transient_for=self,
            flags=0,
            message_type=Gtk.MessageType.ERROR,
            buttons=Gtk.ButtonsType.OK,
            text="Erreur de reconnaissance vocale",
        )
        error_dialog.format_secondary_text(error_message)
        error_dialog.run()
        error_dialog.destroy()

    def get_datetime(self):
        year, month, day = self.calendar.get_date()
        month += 1
        date = f"{year}-{month:02d}-{day:02d}"
        time_str = self.time_entry.get_text()
        return date, time_str
