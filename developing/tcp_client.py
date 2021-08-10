#!/usr/bin/env python
import sys
import logging
import socket
import struct
from threading import Event, Thread
from util import *
import time


logger = logging.getLogger('client')
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
STOP1 = Event()
STOP2 = Event()
pub_addr=priv_addr=client_pub_addr=client_priv_addr=None
connect_addr=None

TYPE_TCP=1

def accept(port):
    logger.info("accept %s", port)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    listen_success=True
    try:
        #s.bind(('', port))
        #s.listen(1)
        s.settimeout(5)
    except OSError:
        logger.info('failed to listen port {}'.format(port))
        listen_success=False
    
    while (not STOP1.is_set()) and listen_success:
        try:
            conn, addr = s.accept()
        except socket.timeout:
            continue
        else:
            logger.info("Accept %s connected!", port)
            STOP1.set()


def connect(local_addr, addr):
    global connect_addr
    logger.info("connect from %s to %s", local_addr, addr)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    s.bind(local_addr)
    while not STOP2.is_set():
        try:
            s.connect(addr)
        except socket.error:
            continue
        # except Exception as exc:
        #     logger.exception("unexpected exception encountered")
        #     break
        else:
            logger.info("connected from %s to %s success!", local_addr, addr)
            connect_addr=addr
            STOP2.set()
            STOP1.set()


def main(host='0.0.0.0', port=5005,socks=(),sock_type=(),success_var=Event()):
    global pub_addr, priv_addr, client_pub_addr, client_priv_addr
    global connect_addr
    sa = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sa.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sa.connect((host, port))
    priv_addr = sa.getsockname()

    sock_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #so.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    sock_server.bind(("",priv_addr[1]))
    sock_server.listen(200)

    send_msg(sa, addr_to_msg(priv_addr))
    data = recv_msg(sa)
    logger.info("client %s %s - received data: %s", priv_addr[0], priv_addr[1], data)
    pub_addr = msg_to_addr(data)
    send_msg(sa, addr_to_msg(pub_addr))

    data = recv_msg(sa)
    pubdata, privdata = data.split(b'|')
    client_pub_addr = msg_to_addr(pubdata)
    client_priv_addr = msg_to_addr(privdata)
    logger.info(
        "client public is %s and private is %s, peer public is %s private is %s",
        pub_addr, priv_addr, client_pub_addr, client_priv_addr,
    )

    threads = {
        #'0_accept': Thread(target=accept, args=(priv_addr[1],)),
        '1_accept': Thread(target=accept, args=(pub_addr[1],)),
        '2_connect': Thread(target=connect, args=(priv_addr, client_pub_addr,)),
        #'3_connect': Thread(target=connect, args=(priv_addr, client_priv_addr,)),
    }
    for name in sorted(threads.keys()):
        logger.info('start thread %s', name)
        threads[name].start()

    while threads:
        keys = list(threads.keys())
        for name in keys:
            try:
                threads[name].join(1)
            except TimeoutError:
                continue
            if not threads[name].is_alive():
                threads.pop(name)
    
    server_th=Thread(target=server_func,args=(sock_server,))
    server_th.start()

    #time.sleep(0.4)
    for i in range(5) :
        sock_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock_client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #print(client_pub_addr)
        host=connect_addr[0];port = connect_addr[1]
        try:
            sock_client.connect((host, port))
            print(recv_msg(sock_client).decode())
        except:
            time.sleep(0.4)
        finally:
            sock_client.close()
    
    socks=(sock_server,sock_client)
    sock_type=(TYPE_TCP,0)
    success_var.set()


def server_func(sock):
    while True :
        peer,addr=sock.accept()
        print('connection from ',addr)
        send_msg(peer,b"WHO cares you")
        peer.close()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, message='%(asctime)s %(message)s')
    main(host='192.168.1.24',port=5005)
    #main(*addr_from_args(sys.argv))
