import sys
import logging
import socket
import threading
import util
import time
import stun

logger = logging.getLogger('client')
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
success=threading.Event()

pub_addr=priv_addr=client_pub_addr=client_priv_addr=None
connect_addr=None
sock_send = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock_recv = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

TYPE_TCP=1

def recv_func():
    while True :
        conn,addr=sock_recv.accept()
        msg=util.recv_msg(sock_recv)
        if msg == "lan" :
            

def lan_connect():
    

def get_sock(host='0.0.0.0', port=5005,socks=(),sock_type=(),success_var=threading.Event()) :
    global pub_addr, priv_addr, client_pub_addr, client_priv_addr
    global connect_addr
    global sock_send,sock_recv
    
    sock_send.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    try :
        sock_send.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    except :
        pass
    sock_send.connect((host,port))
    priv_addr = sock_send.getsockname()

    sock_recv.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    try :
        sock_recv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    except :
        pass
    
    sock_recv .bind(("",priv_addr[1]))
    sock_recv.listen(5)

    util.send_msg(sock_send,util.addr_to_msg(priv_addr)+'|'+stun.info["nat_type"])
    data=util.recv_msg(sock_send)
    pub_addr = util.msg_to_addr(data)
    
    util.send_msg(sock_send, util.addr_to_msg(pub_addr))
    data = util.recv_msg(sock_send)
    pubdata, privdata,peer_nat_type = data.split('|')
    client_pub_addr = util.msg_to_addr(pubdata)
    client_priv_addr = util.msg_to_addr(privdata)
    logger.info(
        "client public is %s and private is %s, peer public is %s private is %s",
        pub_addr, priv_addr, client_pub_addr, client_priv_addr,
    )

    seperate_priv_addr=priv_addr[0].split('.')
    seperate_client_priv_addr = client_priv_addr[0].split('.')
    same_lan=True
    if seperate_priv_addr[0] != seperate_client_priv_addr[0] :
        same_lan = False
    if stun.info['nat_type']==stun.OpenInternet or peer_nat_type==stun.OpenInternet:
        same_lan = False
    recv_thread=threading.Thread(target=recv_func)
    recv_thread.start()
    if same_lan :
        lan_connect()