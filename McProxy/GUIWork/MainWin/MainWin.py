import gi
import time

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import GLib

class AddNewPageAssistant():
    def __init__(self, parent):
        pass

class MainWin():

    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("TheGUIMainWin.glade")

        self.window = self.builder.get_object("MainWindow")
        self.notebook = self.builder.get_object("content_notebook")
        self.nb_default = self.builder.get_object("nb_default_page")
        self.builder.connect_signals(self)

        self.window.show_all()

    def on_add_page_clicked(self, *args):
        if self.notebook.page_num(self.nb_default) != -1:
            self.notebook.remove_page(self.notebook.page_num(self.nb_default))
        window = AddNewPageAssistant(parent = self.notebook)
        #then it will do all things autolly

    def on_hb_setting_clicked(self, *args):
        pass

    def on_hn_question_clicked(self, *args):
        pass

    def on_hb_info_clicked(self, *args):
        pass

win = MainWin()
Gtk.main()
