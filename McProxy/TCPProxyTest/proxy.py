import sys
import socket
import threading

def request_handler(buffer):
    return buffer

def response_handler(buffer):
    return buffer

def receive_from(connection):
    buffer = ""
    connection.settimeout(5)
    try:
        while True:
            data = connection.recv(4096).decode("utf8")
            if not data:
                break
            buffer += data

    except:
        pass
    return buffer

def server_loop(local_host,local_port,remote_host,remote_port,receive_first):
#作为服务器监听并接受remote_client连接,这里一般是监听本地客户端
    #监听本地端口，接受远程客户端的连接
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind((local_host,local_port))
    server.listen(5)

    while True:
        client_socket,addr = server.accept()
        print("client {}:{} connect proxy.".format(addr[0],addr[1]))
        #分配一个线程处理与remote_client客户端的连接，相当于取代了remote_server
        client_thread = threading.Thread( target=proxy_handler,args=(client_socket,remote_host,remote_port,receive_first,) )
        client_thread.start()

def proxy_handler(client_socket,remote_host,remote_port,receive_first):
#作为客户端连接remote_server
#转发remote_clien            data=sock.recv(8192)
t和client_server之间的发送的数据
    #与远程服务器建立连接
    print("proxy make remote_socket.")
    remote_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    remote_socket.connect((remote_host,remote_port))

    #判断是否先接受remote_server的信息
    #if receive_first:
    remote_buffer = receive_from(remote_socket)
    print("[proxy<==server] from remote_server:\n",remote_buffer)
    if len(remote_buffer):
        print("[client<==proxy] sending to client")
        client_socket.send(remote_buffer)

    print("after first")
    #这个循环为代理真正工作的内容，转发两方的信息
    while True:
        print("proxy working!")
        #接收来自remote_client的信息并存储在local_buffer
        #将local_buffer的信息再发送到remote_server
        local_buffer = receive_from(client_socket)
        if len(local_buffer):
            print("[client==>proxy] from cient:\n",local_buffer)
            local_buffer = request_handler(local_buffer)
            print("[proxy==>server] sending to server")
            remote_socket.send(local_buffer.encode('utf-8'))

        #接收来自remote_server的信息并存储在remote_buffer
        #将remote_buffer的信息再发送到remote_client
        remote_buffer = receive_from(remote_socket)
        if len(remote_buffer):
            print("[proxy<==server] from server:\n",remote_buffer)
            remote_buffer = response_handler(remote_buffer)
            print("[client<==proxy] sending to client")
            client_socket.send(remote_buffer.encode('utf-8'))

         #没有数据就关闭连接
        if not len(local_buffer) or not len(remote_buffer):
            client_socket.close()
            remote_socket.close()
            print("[*] No more data. Closing connetctions.")

            break
def main():
    if len(sys.argv[1:]) != 5:
        print("failed to input.")
        sys.exit(0)

    #绑定的监听地址端口，用于本程序作为服务器连接远端客户端
    #当本程序运行时开始监听，需要客户端主动连接，这里的客户端一般是本地客户端
    local_host = sys.argv[1]
    local_port = int(sys.argv[2])

    #远端服务器的地址，用于本程序作为客户端时连接远端服务器
    remote_host = sys.argv[3]
    remote_port = int(sys.argv[4])

    receive_first = sys.argv[5]

    if "true" in receive_first:
        receive_first = True
    else:
        receive_first = False

    server_loop(local_host,local_port,remote_host,remote_port,receive_first)

if __name__ == '__main__':
    main()
