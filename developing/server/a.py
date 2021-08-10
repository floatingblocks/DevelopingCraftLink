
import socket

if __name__ == '__main__' :
    sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.bind(('0.0.0.0',5005))
    sock.listen(5)
    while True :
        conn,addr=sock.accept()
        conn.close()

