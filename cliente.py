import socket
import os
import threading
from time import sleep

Conectado = False
mensagem = ''
port = 7000 
addr = (('localhost',port)) 

def Conectar():
    global Conectado
    global port
    global addr
    RetonoPorta = os.popen('netstat -o -n -a | findstr 127.0.0.1:' + str(port)).read()
    if (RetonoPorta.find('ESTABLISHED') == -1) and ( not Conectado):
       client_socket.connect(addr) 
       Conectado = True 
    else:
        port = port + 1
        addr = (('localhost',port))  

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_EXCLUSIVEADDRUSE, 1)

login = input('Login: ')
senha = input('Senha: ')
while (login != 'admin') or (senha != 'admin'):
    print('login/senha incorreto, favor digitar novamente')
    login = input('Login: ')
    senha = input('Senha: ')

for loop in range(10):
    threading.Thread(target=Conectar).start()
    if Conectado:
        break
    sleep(1)

print('Conectado com sucesso em porta : ' + str(port)) 

ContinuarAcao = True
while ContinuarAcao:
    mensagem = input("Escolha uma ação: 1 - Adicionar, 2 - Mover, 3 - Deletar : ")
    client_socket.send(mensagem.encode('utf-8'))

    if int(mensagem) == 1:
        listaCard = input("Card será adicionado a Lista ? 1 - A fazer, 2 - Em Andamento, 3 - Concluído : ") 
        client_socket.send(listaCard.encode('utf-8'))
        card = input('Descrição do cartão :')
        client_socket.send(card.encode('utf-8')) 

    elif int(mensagem) == 2:
        listaCard = input('Descrição do cartão a ser movido:')
        client_socket.send(listaCard.encode('utf-8'))
        listaOrigem = input("Lista Origem ? 1 - A fazer, 2 - Em Andamento, 3 - Concluído : ")
        client_socket.send(listaOrigem.encode('utf-8'))
        listaDestino = input("Lista Destino ? 1 - A fazer, 2 - Em Andamento, 3 - Concluído : ")
        client_socket.send(listaDestino.encode('utf-8'))
    else:
        listaCard = input('Descrição do cartão a ser deletado:')
        client_socket.send(listaCard.encode('utf-8'))
        listaOrigem = input("Lista Origem do cartão ? 1 - A fazer, 2 - Em Andamento, 3 - Concluído : ")
        client_socket.send(listaOrigem.encode('utf-8'))

    
    client_socket.send(mensagem.encode('utf-8')) 
    Mensagem = client_socket.recv(1024)
    print(str(Mensagem.decode('utf-8')))

    OpcaoContAcao = input('Fazer outra ação ? 1 - Sim, 2 - Não : ')
    client_socket.send(OpcaoContAcao.encode('utf-8'))
    if OpcaoContAcao == '1':
        ContinuarAcao = True
    else:
        ContinuarAcao = False  

client_socket.close()