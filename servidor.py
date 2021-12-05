import socket 
import threading
import time
from trello import TrelloClient

client = TrelloClient(
    api_key='cd17fd0b09001a5e435cd85369581f76',
    api_secret='cd17fd0b09001a5e435cd85369581f76',
    token='92c666944449616ff7a1ae49dc701768a36112316127499ffedac34749829575',
    token_secret='92c666944449616ff7a1ae49dc701768a36112316127499ffedac34749829575'
)

quadro = client.get_board('61773b5adb289b79297b3a4b')
listaAFazer = quadro.get_list('61773b5adb289b79297b3a4c') # A Fazer
listaEmAndamento = quadro.get_list('61773b5adb289b79297b3a4d') # Em Andamento
listaConcluido = quadro.get_list('61773b5adb289b79297b3a4e') # Concluido  
host = '' 
port = 7000

def ExecutaTrello():
    try:
        global port
        portaAtual = port 
        addr = (host, port) 
        serv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
        serv_socket.bind(addr) 
        serv_socket.listen(10)
        print('aguardando conexao') 
        con, cliente = serv_socket.accept() 
        con.setblocking(True)
        print('Conectado com sucesso em porta : ' + str(addr[1])) 
        print('aguardando')

        def Adiciona(Lista, CardDesc):
            cardDuplicado = False
            for cardLista in Lista.list_cards():
                if cardLista.name == str(CardDesc.decode('utf-8')):
                    cardDuplicado = True
                    break
            if cardDuplicado == False:
                Lista.add_card(str(CardDesc.decode('utf-8')))
                CardDesc = 'Card "' + str(CardDesc.decode('utf-8')) + '" Adicionado com sucesso !'
                con.send(CardDesc.encode('utf-8'))
            else:
                CardDesc = 'Card "' + str(CardDesc.decode('utf-8')) + '" Já existente !'
                con.send(CardDesc.encode('utf-8'))

        def RetornaLista(Lista):
            if int(Lista) == 1:
                return listaAFazer
            elif int(Lista) == 2: 
                return listaEmAndamento
            else: 
                return listaConcluido
            
        ContinuarAcao = True
        while ContinuarAcao:
            Acao = con.recv(1024) 
            if int(Acao.decode('utf-8')) == 1: #Adicionar
                Lista = con.recv(1024)
                Card = con.recv(1024)
                if int(Lista) == 1:
                    Adiciona(listaAFazer, Card)      
                elif int(Lista) == 2:
                    Adiciona(listaEmAndamento, Card)
                elif int(Lista) == 3:
                    Adiciona(listaConcluido, Card)
            elif int(Acao) == 2: #Mover
                Card = con.recv(1024)
                CardMensagem = Card
                ListaOrigem = con.recv(1024)
                ListaDestino = con.recv(1024)
                ListaOrigem = RetornaLista(ListaOrigem)
                ListaDestino = RetornaLista(ListaDestino)
                TemCard = False

                for cardLista in ListaOrigem.list_cards():
                    if cardLista.name == str(Card.decode('utf-8')):
                        Card = cardLista
                        TemCard = True
                        break
                
                if TemCard:
                    ListaOrigem.move_card(ListaDestino, Card)
                    CardDesc = 'Card "' + str(CardMensagem.decode('utf-8')) + '" Movido com Sucesso !'
                    con.send(CardDesc.encode('utf-8'))
                else:
                    CardDesc = 'Card "' + str(CardMensagem.decode('utf-8')) + '" Não Encontrado !'
                    con.send(CardDesc.encode('utf-8'))

            elif int(Acao) == 3: #Deletar
                Card = con.recv(1024)
                CardMensagem = Card
                ListaOrigem = con.recv(1024)
                ListaOrigem = RetornaLista(ListaOrigem)
                TemCard = False

                for cardLista in ListaOrigem.list_cards():
                    if cardLista.name == str(Card.decode('utf-8')):
                        Card = cardLista
                        TemCard = True
                        break

                if TemCard:
                    ListaOrigem.delete_card(Card)
                    CardDesc = 'Card "' + str(CardMensagem.decode('utf-8')) + '" Deletado com Sucesso !'
                    con.send(CardDesc.encode('utf-8'))
                else:
                    CardDesc = 'Card "' + str(CardMensagem.decode('utf-8')) + '" Não Encontrado !'
                    con.send(CardDesc.encode('utf-8'))

            Acao = con.recv(1024)
            OpcaoContAcao = con.recv(1024)
            if str(OpcaoContAcao.decode('utf-8')) == '1':
                ContinuarAcao = True
            else:
                ContinuarAcao = False  

        serv_socket.close()
        port = portaAtual
        print('Conexao Porta : ' + str(port))
        threading.Thread(target=ExecutaTrello).start()

    except:
        serv_socket.close()
        port = portaAtual
        print('Conexao Porta : ' + str(port))
        threading.Thread(target=ExecutaTrello).start()

for loop in range(10):
    print('Conexao Porta : ' + str(port))
    threading.Thread(target=ExecutaTrello).start()
    host = '' 
    port = port + 1
    time.sleep(1)