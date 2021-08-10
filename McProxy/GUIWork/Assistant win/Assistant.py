import gi
from time import sleep

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import GLib

#fakes
#constants begin::

SLEEP_TIME = 0.2 # second
TIMEOUT = 5000 # 5000*0.2 second

class CraftConLang():
    def __init__(self):
        self.NPCD_connecting_statu_text = "[状态]正在建立连接……\n"
        self.NP_newlink = "新建连接"
        self.NP_newclient = "建立链接"

CClang = CraftConLang()

#test class begin::

class FakeClientConn():
    def __init__(self):
        self.time = 0

    def set(self, mode, arg, port=0):
        pass

    def connect(self):
        pass

    def check(self):
        self.time += 1
        if self.time > 15:
            return "success"
        else:
            return "connecting"

class FakeLib():
    def __init__(self):
        pass

    def summon_local_info(self):
        return "LALALALALALLSAJFOIUAWJFLIKAHSOIDafs"



#test class end::

#constants end::


class FakeMainWin(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Example")

        self.set_border_width(6)

        button = Gtk.Button(label="Open")
        button.connect("clicked", self.on_button_clicked)

        self.add(button)

    def on_button_clicked(self, widget):
        dialog = AddNewPageAssistant()

class AddNewPageAssistant(Gtk.Assistant):
    """
    Use Gbuilder with file "AddNewPageAssistant.glade"

    This class's function is as same as its name
    It has those variable:resource
        self.mode "client" ot "server"
        for client:
            self.nickname
            self.link #the link class
            self.manual

        for server:
            self.info


    """

    def __init__ (self, parent=""):

        Gtk.Assistant.__init__(self, title="Assistant Example", )
        self.set_size_request(-1, 300)
        self.set_border_width(10)

        self.mode = ""
        self.manual = False
        self.success = False
        self.finished = False

        self.builder = Gtk.Builder()
        #print("Start builing")
        self.builder.add_from_file("AddNewPageAssistant.glade")
        #print("added form file")
        self.creat_pages()
        #print("created pages")
        self.connect_my_signals()
        #print("sinalsss")
        self.builder.connect_signals(self)
        #print("sinals")
        self.show_all()
        #print("showed")

    def creat_pages(self):
        #print("getting ob0")
        page0 = self.builder.get_object("new_page_choose_cs_box")
        page0.show_all()
        #print("appending0")
        self.append_page(page0)
        #print("setting title")
        self.set_page_title(page0, CClang.NP_newlink)
        #print("setting type")
        self.set_page_type(page0, Gtk.AssistantPageType.CUSTOM)

        page1 = self.builder.get_object("new_page_client_config_box")
        page1.show_all()
        self.append_page(page1)
        self.set_page_title(page1, CClang.NP_newclient)
        self.set_page_type(page1, Gtk.AssistantPageType.CUSTOM)

        page2 = self.builder.get_object("new_page_server_config_box")
        page2.show_all()
        self.append_page(page2)
        self.set_page_title(page2, "配置服务端")
        self.set_page_type(page2, Gtk.AssistantPageType.CUSTOM)

        page3 = self.builder.get_object("new_page_success_label")
        self.append_page(page3)
        self.set_page_title(page3, "配置服务端")
        page3.show_all()
        self.set_page_type(page3, Gtk.AssistantPageType.CUSTOM)



    def connect_my_signals(self):
        self.back_button  = Gtk.Button.new_with_label("后退")
        self.apply_button = Gtk.Button.new_with_label("前进")
        self.close_button = Gtk.Button.new_with_label("关闭")

        self.back_button.connect("clicked", self.on_AddNewPageWindow_back)
        self.apply_button.connect("clicked", self.on_AddNewPageWindow_apply)
        self.close_button.connect("clicked", self.on_AddNewPageWindow_close)
        self.add_action_widget(self.apply_button)
        self.add_action_widget(self.back_button)
        self.add_action_widget(self.close_button)

    def running(self):

        while True:
            sleep(SLEEP_TIME)
            if self.finished:
                return self.success

    # Asisstant signal begin::
    def on_AddNewPageWindow_back(self, *args):
        page_num = self.get_current_page()
        if page_num != 0 and page_num != 3:
            self.previous_page()

    def on_AddNewPageWindow_apply(self, *args):

        page_num = self.get_current_page()
        if page_num == 0:
             server_button = self.builder.get_object("new_page_choose_server_button")
             if server_button.get_active():

                 self.mode = "server"
                 self.set_current_page(2)

             else:
                 #to client
                 self.mode = "client"
                 self.set_current_page(1)

        #client
        elif page_num == 1:
            #check and connect
            if self.check_client_page() and self.connect_client_page():
                    self.success = True
                    self.set_current_page(3)
            else:
                #show a dialog to make user check
                pass

        #server
        elif page_num == 2:
            if self.server_page_info():
                self.success = True
                self.set_current_page(3)
            else:
                #show a dialog to make user check
                pass

        elif page_num == 3:
            self.on_AddNewPageWindow_close()


    def on_AddNewPageWindow_cancel(self, *args):
        self.finished = True
        self.destroy()


    def on_AddNewPageWindow_close(self, *args):
        self.finished = True
        self.destroy()

    #Asisstant signal end::

    #Client actions begin::
    def on_npcl_conf_extern_manual_enable_toggled(self, button):
        if button.get_active():
            self.manual = True
            #do sth
            text = FakeCraftConLib.summon_local_info()
            info_label = self.builder.get_object("npcl_conf_extern_manual_clinfo")
            info_label.set_text(text)

        else:
            self.manual = False

    def check_client_page(self):
        if self.manual:
            manual_entry = self.builder.get_object("npcl_conf_extern_manual_serverinfo")
            manual_text = manual_entry.get_text()
            if manual_text:
                return True
            else:
                dialog = Gtk.MessageDialog(
                    transient_for=self,
                    flags=0,
                    message_type=Gtk.MessageType.ERROR,
                    buttons=Gtk.ButtonsType.CANCEL,
                    text="未填写对方信息。",
                )
                dialog.run()
                dialog.destroy()
                return False
        else:
            autocon_entry = self.builder.get_object("npcl_conf_autocon_entry")
            autocon_text = autocon_entry.get_text()
            if autocon_text:
                return True
            else:
                dialog = Gtk.MessageDialog(
                    transient_for=self,
                    flags=0,
                    message_type=Gtk.MessageType.ERROR,
                    buttons=Gtk.ButtonsType.CANCEL,
                    text="未填写连接码。",
                )
                dialog.run()
                dialog.destroy()
                return False

    def connect_client_page(self):

        if self.manual:
            manual_entry = self.builder.get_object("npcl_conf_extern_manual_serverinfo")
            text = manual_entry.get_text()
        else:
            autocon_entry = self.builder.get_object("npcl_conf_autocon_entry")
            text = autocon_entry.get_text()

        if text:
            port_entry = self.builder.get_object("npcl_conf_extern_port_entry")
            port = port_entry.get_text()
            self.link = FakeClientConn()
            if port:
                self.link.set(mode="manual", arg=text, port=port)
            else:
                self.link.set(mode="manual", arg=text)
            dialog = ConnectDialog(parent = self, link = self.link)
            res = dialog.run()
            dialog.destroy()
            if res == Gtk.ResponseType.OK:
                return True
            else:
                return False
        else:
            return False

    #client actions end::

    #server actions begin::

    def server_page_info(self):
        ip_entry = self.builder.get_object("nps_conf_ip_entry")
        port_entry = self.builder.get_object("nps_conf_port_entry")
        maxnum_entry = self.builder.get_object("nps_conf_maxnum_entry")
        linkname_entry = self.builder.get_object("nps_conf_linkname_entry")

        ip = ip_entry.get_text()
        port = port_entry.get_text()
        maxnum = maxnum_entry.get_text()
        linkname = linkname_entry.get_text()

        if ip and maxnum and linkname:
            server_entry = self.builder.get_object("nps_conf_extern_server_entry")
            server_text = server_entry.get_text()
            self.server_info = {
                "ip" : ip,
                "port" : port,
                "maxnum" : maxnum,
                "linkname" : linkname,
                "server" : server_text
            }
            return True
        else:
            dialog = Gtk.MessageDialog(
                transient_for=self,
                flags=0,
                message_type=Gtk.MessageType.ERROR,
                buttons=Gtk.ButtonsType.CANCEL,
                text="未填写全部必填项。",
            )
            dialog.run()
            dialog.destroy()
            return False
    #server actions end::

    #for parent action begin::

    #for parent action end::

class ConnectDialog(Gtk.Dialog):
    def __init__(self, parent, link):
        super().__init__(title="My Dialog", transient_for=parent, flags=0)
        self.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL
        )
        #Gtk.ResponseType.OK means it has successed
        self.set_default_size(150, 100)

        self.times = 0
        self.link = link

        self.spinner = Gtk.Spinner()
        self.spinner.start()
        self.label = Gtk.Label(label=CClang.NPCD_connecting_statu_text)

        self.sw = Gtk.ScrolledWindow()
        self.sw.set_size_request(300, 100)
        self.sw.new()
        self.textview = Gtk.TextView()
        self.textview.set_editable(False)
        self.textbuffer = self.textview.get_buffer()
        self.textbuffer.set_text(CClang.NPCD_connecting_statu_text)
        self.sw.add(self.textview)

        self.box = self.get_content_area()
        self.box.pack_start(self.spinner, True, True, 0)
        self.box.pack_start(self.label, True, True, 0)
        self.box.pack_start(self.sw, True, True, 0)

        self.timeout_id = GLib.timeout_add(200, self.on_timeout, None)

        self.show_all()

    def on_timeout(self, *args):
        if self.times > TIMEOUT:
            self.spinner.stop()
            self.label.set_text("[状态]超时。\n")
            self.textbuffer.insert(self.textbuffer.get_end_iter(), "[状态]超时。\n")
            return False

        elif self.link.check() == "success":
            self.spinner.stop()
            self.label.set_text("[状态]已完成。\n")
            self.textbuffer.insert(self.textbuffer.get_end_iter(), "[状态]已完成。\n")
            self.response(Gtk.ResponseType.OK)
            return False

        elif self.link.check() == "err":
            self.spinner.stop()
            self.label.set_text("[状态]发生错误。\n" + self.link.get_err_text())
            self.textbuffer.insert(
                self.textbuffer.get_end_iter(),
                "[状态]发生错误。\n" + self.link.get_err_text()
            )
            return False

        else:
            return True

win = FakeMainWin()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
