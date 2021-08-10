#都放在一起是懒得搞隔离，所以先整一堆 begin end 之类的垃圾方法，等到时候会拆开来的
import gi
import time

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib, Gdk
from string import Template

#fakes
#constants begin::
SLEEP_TIME = 0.02 # second
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
        if self.time > 3:
            return "success"
        else:
            return "connecting"

class FakeLib():
    def __init__(self):
        pass

    def summon_local_info(self):
        return "LALALALALALLSAJFOIUAWJFLIKAHSOIDafs"

class FakePage():
    def __init__(self, parent, title="testing"):
        self.parent = parent
        self.header = Gtk.HBox()
        self.title = Gtk.Label(label=title)
        close_button = Gtk.Button.new_from_icon_name("gtk-close", Gtk.IconSize.MENU)
        close_button.set_relief(Gtk.ReliefStyle.NONE)
        close_button.connect("clicked", self.on_tab_close)

        self.header.pack_start(self.title, expand=True, fill=True, padding=0)
        self.header.pack_end(close_button, expand=False, fill=False, padding=0)
        self.header.show_all()

        self.page = Gtk.ScrolledWindow()
        self.page.add(Gtk.Label(label=title))
        self.page.show_all()

    def on_tab_close(self, button):
        self.parent.remove_page(self.parent.page_num(self.page))

class FakeLink():
    '''
    Fakelink's anctions:
        get_infos
        get_ip
        remove
        reflash
        stop
        alive
    '''
    def __init__(self):
        pass

    def get_infos(self):
        return {
            "linkname" : "LINKNAME_FAKE",
            "nickname" : "NICKNAME_FAKE",
            "mode" : "FAKETESTING",
            "ping" : 999,
            "num" : 99,
            "maxnum" : 999,
            "state" : "TESING",
            "upspeed" : 555,
            "downspeed" : 444
        }

    def get_ip(self):
        return "999.999.999.999:55555"

    def remove(self):
        pass

    def reflash(self):
        pass

    def stop(self):
        pass

    def alive(self):
        return True

class FakeServerLink():
    def __init__(self):
        pass

    def get_infos(self):
        return {
            "name" : "TEST_NAME",
            "uid"  : "ad8a762a0f97a09s9821047",
            "state": "TEST",
            "mode" : "TESTING",
            "upspeed"  : 999,
            "downspeed": 999,
            "ping" : 999
        }

    def running(self):
        return True
#test class end::
#constants end::

####################
##ServerPage begin::
##很多pass是因为自己还没有想好细节处理逻辑
##毕竟核心部分完全没有开写，搞不好还要推倒重来
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
    def __init__(self, parent, infos, title="TESTNG"):
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
        self.builder.add_from_file("server_view_box.glade")
        self.page = self.builder.get_object("server_view_box")

        self.links = {}
        # links: "uid" : link;
        self.liststore = Gtk.ListStore(str, str, str, str, float, float, int)



        # user code state mode upspeed downspeed ping
        # SEE:server_view_arg_list list.
        self.tree_sw = self.builder.get_object("server_view_sw")
        self.tree = Gtk.TreeView()
        self.tree.set_model(self.liststore)

        for i, column_title in enumerate(server_view_arg_list):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            self.tree.append_column(column)

        self.tree_sw.add(self.tree)
        self.page = self.builder.get_object("server_view_box")

        ###############################################################
        #######FORTESTING
        fakelink = FakeServerLink()
        infos = fakelink.get_infos()
        self.links = { infos["uid"] : fakelink }
        roww = self.link_to_row(fakelink)
        print(roww)
        self.liststore.append(roww)
        #######
        ###############################################################

        self.timeout_id = GLib.timeout_add(1000, self.on_timeout, None)

        self.page.show_all()

        #page end::

    #page actions begin::
    def link_to_row(self, link):
        row = [0] * 7
        info = link.get_infos()
        row[0] = info["name"]
        row[1] = info["uid"]
        row[2] = info["state"]
        row[3] = info["mode"]
        row[4] = info["upspeed"]
        row[5] = info["downspeed"]
        row[6] = info["ping"]
        return row

    def on_tab_close(self, button):
        if self.timeout_id:
            GLib.source_remove(self.timeout_id)
            self.timeout_id = None
        self.parent.remove_page(self.parent.page_num(self.page))
        #then remove each link

    def on_timeout(self, *args):
        for row in self.liststore:
            row_link = self.links[row[1]]
            info = row_link.get_infos()
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

##ServerPage end::
####################

####################
##ClientPage begin::
class ClientPage():
    def __init__(self, parent, link, title = "Client"):
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
        self.info_templete = Template("连接名: $linkname ;    用户名: $nickname ; 模式: $mode ; \nPing: $ping ;    已连接: $num /$maxnum ;    状态: $state ;\n 上传速度: $upspeed kbps;    下载速度: $downspeed kbps;")

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

        self.clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        #page end::

    def on_tab_close(self, button):
        if self.timeout_id:
            GLib.source_remove(self.timeout_id)
            self.timeout_id = None
        self.parent.remove_page(self.parent.page_num(self.page))
        self.link.remove()

    #page action begin::
    def on_timeout(self, *args):
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

    def on_cilent_link_ip_copy_clicked(self, *args):
        self.clipboard.set_text(self.link.get_ip(), -1)

    def on_cilent_link_reflash_clicked(self, *ars):
        self.on_timeout() # Just reflash infos

    def on_cilent_link_reconnect_clicked(self, *args):
        self.link.reconnect()

    def on_cilent_link_stop_clicked(self, *args):
        self.link.stop()
    #page action end::
##ClientPage end::
####################

####################
##Assistant begin::
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

    def __init__ (self, notebook):

        Gtk.Assistant.__init__(self, title="Assistant Example", )
        self.set_size_request(-1, 300)
        self.set_border_width(10)

        self.notebook = notebook
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
                #showed a dialog to make user check
                pass

        #server
        elif page_num == 2:
            if self.server_page_info():
                self.success = True
                self.set_current_page(3)
            else:
                #showed a dialog to make user check
                pass

        elif page_num == 3:
            if self.mode == "client":
                tab = ClientPage(parent=self.notebook, link = FakeLink())
            else:
                tab = ServerPage(parent=self.notebook, infos="AAAA")
            self.notebook.append_page(tab.page, tab.header)
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
                self.textbuffer.get_enFakePaged_iter(),
                "[状态]发生错误。\n" + self.link.get_err_text()
            )
            return False

        else:
            return True
##Assistant end::
####################

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
        window = AddNewPageAssistant(notebook = self.notebook)
        #then it will do all things autolly

    def on_hb_setting_clicked(self, *args):
        pass

    def on_hn_question_clicked(self, *args):
        pass

    def on_hb_info_clicked(self, *args):
        pass

win = MainWin()
Gtk.main()
