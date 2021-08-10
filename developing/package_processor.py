import threading
import time
import util
import socket
import logging

import tcp_client

class pack_processor :

    to_local_list=[]
    to_peer_list=[]
    socks=()
    #socks[0] is the listen sock && socks[1] is the sending sock
    sock_type=()
    send_timeout=0
    
    def keep_receive (self) :
        if self.socks == False :
            return
        while True :
            try :
                msg=util.recv_msg(self.socks[0])
            except socket.error as e:
                self.logger.info(e)
                raise e
            self.lock.acquire()
            self.to_local_list.append(msg.decode())
            self.lock.release()
    
    def keep_send (self) :
        while True :
            time.sleep(0.01)
            send_success = True
            if self.to_peer_list :
                self.lock.acquire()
                msg=self.to_peer_list.pop(index=0)
                self.lock.release()
                try :
                    util.send_msg(self.socks[1],'003'+msg)
                except socket.timeout :
                    self.send_timeout+=1
                    send_success = False
                if send_success :
                    self.send_timeout = 0

    def heart_beat (self) :
        msg="001"
        util.send_msg(self.socks[1],msg)
        time.sleep(15)   

    
    def __init__ (self):
        self.logger = logging.getLogger('client')
        logging.basicConfig(level=logging.INFO, message='%(asctime)s %(message)s')
        self.lock = threading.Lock()

        hole_punching_success=threading.Event()

        hole_punching=threading.Thread(target=tcp_client.main,args=('127.0.0.1', 5005, self.socks, self.sock_type, hole_punching_success, ))
        hole_punching.start()

        while hole_punching_success.is_set ==0 :
            time.sleep(0.01)
        


        receiver=threading.Thread(target=self.keep_receive)


    def recv_remote (self):
        while self.to_local_list==0 :
            time.sleep(0.01)
        ret=None
        while True :
            time.sleep(0.01)
            if self.to_local_list :
                self.lock.acquire()
                ret = self.to_local_list.pop(index=0)
                self.lock.release()
                if ret.decode()[:2]=="003":
                    break
        return ret

    def send_remote (self,msg) :
        self.lock.acquire()
        self.to_peer_list.append(msg)
        self.lock.release()