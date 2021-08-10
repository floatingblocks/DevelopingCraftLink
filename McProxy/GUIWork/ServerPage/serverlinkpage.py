import gi
import time

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import GLib

from string import Template

server_view_arg_list = [
	"用户",
	"Code",
	"状态",
	"模式",
	"上传速度",
	"下载速度",
	"Ping"
]

class ServerPage():
	def __init__(self, title, parent, infos):
		self.parent = parent
        self.header = Gtk.HBox()
        self.title = Gtk.Label(label=title)
        self.infos = infos

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
		self.builder.add_from_file("server_ciew_box.glade")
		self.page = self.builder.get_object("server_view_box")

		self.links = {}
		# links: "uid" : link;

		self.liststore = Gtk.ListStore(str, str, str, str, float, float, int)
		# user code state mode upspeed downspeed ping
		# SEE:server_view_arg_list list.
		self.tree = self.builder.get_object("server_all_link_view")
		self.tree.set_model(self.liststore)

		for i, column_title in enumerate(server_view_arg_list):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            self.tree.append_column(column)



		self.builder = Gtk.Builder()
        self.builder.add_from_file("server_view_box.glade")
		self.page = self.builder.get_object("server_view_box")

		#page end::

	#page actions begin::
	def on_tab_close(self, button):
		if self.timeout_id:
            GLib.source_remove(self.timeout_id)
            self.timeout_id = None
		self.parent.remove_page(self.parent.get_current_page())
		#remove each link

	def on_timeout(self, *args):
		for row in self.liststore:
			row_link = self.links[row[1]]
			info = row_link.get_info()
			#name state mode upspeed downspeed ping
			row[0] = info["name"]
			row[2] = info["state"]
			row[3] = info["mode"]
			row[4] = info["upspeed"]
			row[5] = info["downspeed"]
			row[6] = info["ping"]

			if not row_link.running():
				row_link.remove()
				del self.links[row[1]]
				treeiter = self.liststore.get_iter(row)
				self.liststore.remove(treeiter)

		return True

	#server self actions begin::
	def on_server_self_reflash_clicked(self, *args):
		pass

	def on_server_self_addlink_clicked(self, *args):
		pass

	def on_server_self_setting_clicked(self, *args):
		pass

	def on_server_link_code_copy_clicked(self, *args):
		pass
	#server self action end::

	#server link action begin::
	def on_server_link_select_all_clicked(self, *args):
		pass

	def on_server_link_pause_clicked(self, *args):
		pass

	def on_server_link_reconnect_clicked(self, *args):
		pass

	def on_server_link_delete_clicked(self, *args):
		pass

	def on_server_link_ping_clicked(self, *args):
		pass
	#server link action end::
