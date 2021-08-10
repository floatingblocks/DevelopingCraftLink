from gi.repository import Gtk as gtk

class Tab():
    def __init__(self, title, parent):
        self.title = title
        self.parent = parent
        self.header = gtk.HBox()
        self.title = gtk.Label(label=title)
        image = gtk.Image()
        image.set_from_stock(gtk.STOCK_CLOSE, gtk.IconSize.MENU)
        close_button = gtk.Button()
        close_button.set_image(image)
        close_button.set_relief(gtk.ReliefStyle.NONE)
        close_button.connect("clicked", self.on_tab_close)

        self.header.pack_start(self.title,
                          expand=True, fill=True, padding=0)
        self.header.pack_end(close_button,
                        expand=False, fill=False, padding=0)
        self.header.show_all()

    def on_tab_close(self, button):
        self.parent.remove_page(self.parent.get_current_page())

class Dash(gtk.Notebook):

    def new_tab(self, title):
        tab = Tab(title, self)
        self.sw = gtk.ScrolledWindow()
        self.page = self.sw
        self.page.add(gtk.Label(label=title))
        self.append_page(self.page, tab.header)


d = Dash()
d.new_tab("first")
d.new_tab("second")
d.new_tab("third")
window = gtk.Window(gtk.WindowType.TOPLEVEL)
window.set_default_size(400, 400);
window.connect("destroy", gtk.main_quit)
window.add(d)
window.show_all()

gtk.main()