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
STOP = Event()
pub_addr=priv_addr=client_pub_addr=client_priv_addr=None
connect_success=False

def accept(port):
    logger.info("accept %s", port)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    s.bind(('', port))
    s.listen(1)
    s.settimeout(5)
    while not STOP.is_set():
        try:
            conn, addr = s.accept()
        except socket.timeout:
            continue
        else:
            logger.info("Accept %s connected!", port)
            STOP.set()


def connect(local_addr, addr):
    global connect_success
    logger.info("connect from %s to %s", local_addr, addr)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    s.bind(local_addr)
    while not STOP.is_set():
        try:
            s.connect(addr)
        except socket.error:
            continue
        # except Exception as exc:
        #     logger.exception("unexpected exception encountered")
        #     break
        else:
            logger.info("connected from %s to %s success!", local_addr, addr)
            connect_success=True
            STOP.set()


def main(host='10.145.85.166', port=5005):
    global pub_addr, priv_addr, client_pub_addr, client_priv_addr,connect_success
    sa = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sa.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sa.connect((host, port))
    priv_addr = sa.getsockname()

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
        '0_accept': Thread(target=accept, args=(priv_addr[1],)),
        '1_accept': Thread(target=accept, args=(client_pub_addr[1],)),
        '2_connect': Thread(target=connect, args=(priv_addr, client_pub_addr,)),
        '3_connect': Thread(target=connect, args=(priv_addr, client_priv_addr,)),
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
    
    so = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    so.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #so.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    #so.bind(("",priv_addr[1]))
    #so.listen(1)
    print(client_pub_addr)
    host=client_pub_addr[0];port = client_pub_addr[1]
    so.connect((host, port))
    #send_th=Thread(target=service_send,args=(so,))
    #recv_th=Thread(target=service_recv,args=(so,))
    #send_th.start()
    #recv_th.start()
    print(recv_msg(so))
    


#def service_send(sock) :
#    msg='It works!'
#    send_msg(sock,msg.encode())
#    print(recv_msg(sock))

def service_recv(sock):
    while True :
        data=recv_msg(sock)
        print(data.decode())

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, message='%(asctime)s %(message)s')
    #main()
    main(*addr_from_args(sys.argv))
