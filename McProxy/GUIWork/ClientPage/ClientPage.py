import gi
import time
import pyperclip


gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import GLib

from string import Template

#fake testing begin::

#fake testing end::


'''
Fakelink's anctions:
    get_infos
    get_ip
    remove
    reflash
    stop
    alive
'''
class ClientPage():
    def __init__(self, title, parent, link):
        self.parent = parent
        self.header = Gtk.HBox()
        self.title = Gtk.Label(label=title)
        self.link = link

        # header begin::
        close_button = Gtk.Button.new_from_icon_name("gtk-close", Gtk.IconSize.MENU)
        close_button.set_relief(Gtk.ReliefStyle.NONE)
        close_button.connect("clicked", self.on_tab_close)

        self.header.pack_start(self.title, expand=True, fill=True, padding=0)
        self.header.pack_end(close_button, expand=False, fill=False, padding=0)
        self.header.show_all()
        #haeder end::

        #page begin::
        self.builder = Gtk.Builder()
        self.builder.add_from_file("client_view_box.glade")
        self.builder.connect_signals(self)
        self.page = self.builder.get_object("cilent_link_view")
        self.info_label = self.builder.get_object("cilent_link_info")
        self.info_templete = Template("连接名: $linkname ;	用户名: $nickname ; 模式: $mode ; \nPing: $ping ;	已连接: $num /$maxnum ;	状态: $state ;\n 上传速度: $upspeed kbps;	下载速度: $downspeed kbps;")

        infos = self.link.get_infos()
        self.info_label.set_text(
            self.info_templete.substitute(
                linkname = infos["linkname"],
                nickname = infos["nickname"],
                mode = infos["mode"],
                ping = infos["ping"],
                num = infos["num"],
                maxnum = infos["maxnum"],
                state = infos["state"],
                upspeed = infos["upspeed"],
                downspeed = infos["downspeed"]
            )
        )

        self.ip_label = self.builder.get_object("cilent_link_ip")
        self.ip_label.set_text(self.link.get_ip())

        self.times = 0
        self.timeout_id = GLib.timeout_add(1000, self.on_timeout, None)

        self.page.show_all()
        #page end::

    def on_tab_close(self, button):
        if self.timeout_id:
            GLib.source_remove(self.timeout_id)
            self.timeout_id = None
        self.parent.remove_page(self.parent.page_num(self.page))
        self.link.remove()

    #page action begin::
    def on_timeout(self, *args):
        if self.link.alive():
            infos = self.link.get_infos()
            self.info_label.set_text(
                self.info_templete.substitute(
                    linkname = infos["linkname"],
                    nickname = infos["nickname"],
                    mode = infos["mode"],
                    ping = infos["ping"],
                    num = infos["num"],
                    maxnum = infos["maxnum"],
                    state = infos["state"],
                    upspeed = infos["upspeed"],
                    downspeed = infos["downspeed"]
                )
            )
            return True
        else:
            return False

    def on_cilent_link_ip_copy_clicked(self, *args):
        pyperclip.copy(self.link.get_ip())

    def on_cilent_link_reflash_clicked(self, *ars):
        self.on_timeout() # Just reflash infos

    def on_cilent_link_reconnect_clicked(self, *args):
        self.link.reconnect()

    def on_cilent_link_stop_clicked(self, *args):
        self.link.stop()
    #page action end::


class Dash(Gtk.Notebook):

    def new_page(self, title):
        tab = ClientPage(
            title=title,
            parent=self,
        )
        self.append_page(tab.page, tab.header)


d = Dash()
d.new_tab("first")
d.new_tab("second")
d.new_tab("third")
window = Gtk.Window(Gtk.WindowType.TOPLEVEL)
window.set_default_size(400, 400);
window.connect("destroy", Gtk.main_quit)
window.add(d)
window.show_all()

Gtk.main()
