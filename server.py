from http import client
import socket
from threading import Thread

host="127.0.0.1"
port= 8080
clients={}
adresses={}
sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.bind((host,port))
def handle_clients(conn,adress):
    name=conn.recv(1024).decode()
    welcome="Welcome "+name+" you can type #quit if you want to leave the chat"
    conn.send(bytes(welcome,"utf8"))
    msg= name+ " Has recently joined the chat room"
    broadcast(bytes(msg,"utf8"))
    clients[conn]=name

    while True:
        msg=conn.recv(1024)
        if msg!=bytes("#quit","utf8"):
            broadcast(msg, name+":")
        else:
            conn.send(bytes("#quit","utf8"))
            conn.close()
            del clients[conn]
            broadcast(bytes(name+ " Has left the chat","utf8"))



def accept_client_connetions():
    while True:
        client_connec, client_adress=sock.accept()
        print(client_adress, "has connected")
        client_connec.send("welcome to the chat room, please type your name".encode('utf8'))
        adresses[client_connec]=client_adress

        Thread(target=handle_clients,args=(client_connec,client_adress)).start()
        
def broadcast(msg, prefix=""):
    for x in clients:
        x.send(bytes(prefix,"utf8")+msg)

if __name__ == "__main__":
    sock.listen(5)
    print("the server is on and listening")
    t1= Thread(target=accept_client_connetions)
    t1.start()
    t1.join()
conn,adress=sock.accept()

message ="hello message"
conn.send(message.encode())
conn.close()




