#encoding:utf-8
import socket,time,threading

#这里填写本地监听的ip和端口
ip='127.0.0.1'
port=9050

#这列填写公网ip和端口
send_ip='zqat.top'
send_port=25565

#以下部分无需修改
#这是用来存放转发到公网数据的队列
outList=[]
#这是用来存放转发到内网数据的队列
inList=[]
#这是用来标记是否发送的断开连接信息
runStation=True

def  in_get(sock):
    '''
    该函数负责监听本地的端口，传入的sock，收到数据后，将其增加到转发到公网的队列中
    '''
    global outList,inList,runStation
    while runStation:
        try:
            try:
                data=sock.recv(8192)
                #time.sleep(0.1)
            except Exception as ie:
                print(+str(ie))
                #time.sleep(0.1)

            #如果内网发送的空数据，即代表需要断开连接（管家婆特性）
            if data==b'':
                runStation=False
            outList.append(data)
        except Exception as err:
            print('inget'+str(err))
            print(type(sock))

def in_out(sock):
    '''
    该函数负责循环检查对内发送的队列是是否有数据
    发现存在数据后，将数据转发到内部，并且清空对内转发的队列
    '''
    global outList,inList
    while runStation:
        try:
            if len(inList)!=0:
                for i in inList:
                    sock.send(i)
                inList.clear()
            else:
                time.sleep(0.001)
        except Exception as err:
            print(err)

def  out_get(sock):
    '''
    该函数负责监听外网数据，收到数据后，将其增加到对内转发队列
    '''
    global outList,inList
    while runStation:
        try:
            data=sock.recv(8192)
            #time.sleep(0.1)
            inList.append(data)
        except Exception as err:
            print('outget'+str(err))

def out_out(sock):
    '''
    该函数负责对外转发，发现对外转发队列有数据后，判断锁状态，发送数据后清空队列，关闭锁。
    '''
    global outList,inList
    while runStation:
        try:
            if len(outList)!=0:
                for i in outList:
                    if i!=b'':
                        sock.send(i)
                outList.clear()
            else:
                time.sleep(0.001)
        except Exception as err:
            print(err)


def tcplink(sock, addr,ip,port):
    '''
    内部建立起连接后，该函数负责统一处理，其中传入的ip和port指的是外网的。
    '''
    global runStation
    print('Accept new connection from %s:%s...' % addr)
    #与外网建立连接
    s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 建立连接:
    s1.connect((ip, port))
    #启动线程，开始监听内网
    inGet = threading.Thread(target=in_get, args=(sock,))
    inGet.start()
    #启动多个内网发送线程，提高速度
    inOut = threading.Thread(target=in_out, args=(sock,))
    inOut.start()
    #启动一个外网监听进程，开始监听
    outGet = threading.Thread(target=out_get, args=(s1,))
    outGet.start()
    #启动多个外网发送线程，提高速度
    outOut = threading.Thread(target=out_out, args=(s1,))
    outOut.start()
    #在发现连接断开后，即断开内网和外网的套接字
    while runStation:
        time.sleep(0.5)
    else:
        try:
            sock.close()
            s1.close()
        except Exception:
            pass
    print('Connection from %s:%s closed.' % addr)
    runStation = True

#新建套接字
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#绑定本地端口
s.bind((ip, port))
#设置最大连接数
s.listen(5)

while True:
    # 接受一个新连接:
    sock1, addr = s.accept()
    #初始化数据
    runStation=True
    outList=[]
    inList=[]
    runStation=True
    # 创建新线程来处理TCP连接:
    t = threading.Thread(target=tcplink, args=(sock1, addr,send_ip,send_port))
    t.start()
