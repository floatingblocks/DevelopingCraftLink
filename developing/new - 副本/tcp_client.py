import socket
import stun
import threading

import setting

def recv_func(sock_recv):
    times=0
    while True :
        conn,addr=sock_recv.accept()
        times+=1
        msg=conn.recv(1024).decode()
        print(msg+" recv,"+str(times)+" time")
        msg=conn.recv(1024).decode()
        print(msg+" recv,"+str(times)+" time")
        conn.send(str(times).encode())
        conn.close()

def connect() :
    if stun.info['nat_type']==None :
        stun.get_nat_type()
    
    pub_port=stun.info["external_port"]
    pub_host=stun.info["external_ip"]

    sock_recv=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock_recv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        sock_recv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    except:
        pass
    sock_recv.bind(("0.0.0.0",20000))
    sock_recv.listen(5)
    recv_th = threading.Thread(target=recv_func,args=(sock_recv,))
    recv_th.start()
    
    #sock_send=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    #sock_send.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #sock_send.settimeout(0.1)
    #try:
        #sock_send.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    #except:
        #pass
    
    sock_server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        sock_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    except:
        pass


    for i in range(100) :
        try:
            sock_send=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            sock_send.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock_send.settimeout(0.5)
            try:
                sock_send.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
            except:
                pass
            sock_send.connect((pub_host,pub_port-10+i))
        except socket.timeout:
            print("ex")
            #sock_send.close()
        else :
            sock_send.send(str(pub_port-50+i).encode())
            sock_send.send("again".encode())
            msg = sock_send.recv(1024)
            print("client received "+msg.decode())
            sock_send.close()

if __name__ == "__main__" :
    connect()