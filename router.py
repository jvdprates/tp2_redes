import socket as skt
import argparse as ap
import networkx as nx
import threading
import time
import json

# Constantes do programa
PORT = 55151

# Argumentos de chamada do programa
parser = ap.ArgumentParser(
    description='Trabalho pratico 2 - Bruno Oliveira, João Prates')
parser.add_argument('addr', help='Endereço de ip do roteador')
parser.add_argument(
    'period', help='Período entre envio de mensagens de update (π)')
parser.add_argument("-s", "--startup_commands",
                    help='O nome de um arquivo .txt contendo comandos de teclado para adicionar links')
args = parser.parse_args()
# ./router.py <ADDR> <PERIOD> [STARTUP]
# python router.py 127.0.1.0 10

# Argumentos
ADDR = args.addr
PI = args.period
STARTUP = args.startup_commands

# Busca um input do usuário
def get_input():
    user_input = input("> ")
    command = user_input.split(" ")[0]
    args = user_input.split(" ")[1:]
    return command, args

# Printa um erro
def printError(title, message="", note="Erro"):
    print("❗", title)
    if not message == "":
        print("[", note, "]:", message)

# Printa um sucesso
def printSuccess(title, message="", note="Sucesso"):
    print("✅", title)
    if not message == "":
        print("[", note, "]:", message)

# Inicializa o programa e faz o bind ao endereço
printError("Programa iniciado!")
socket = skt.socket(skt.AF_INET, skt.SOCK_DGRAM)
socket.bind((ADDR, PORT))
printSuccess("Roteador vinculado ao endereço {}/{}".format(ADDR, PORT))

# Verifica se há comandos de startup
if STARTUP:
    printSuccess("Arquivos recebido", "{}".format(STARTUP), "Nome do arquivo")

# Variavel local que guarda endereços, tabela de roteamento
routes = []

# Variavel local que guarda uma tabela de endereços recebidos
routeTable = {}

# Imprime uma lista de endereços
def printAddressList(list):
    print("Lista: \n[")
    for i in list:
        print(i)
    print("]")

# Função que retorna vetor de rota-distancia
def getRouteDistances():
    obj = {}
    for i in routes:
        obj[i["addr"]] = i["weight"]
    return obj

# Função que cria um JSON data
def createJSON(obj, type):
    if type == "update":
        return json.dumps({
            "type": "update",
            "source": ADDR,
            "destination": obj["destination"],
            "distances": getRouteDistances()
        })
    elif type == "trace":
        return json.dumps({
            "type": "trace",
            "source": ADDR,
            "destination": obj["destination"],
            "hops": obj["hops"],
        })
    elif type == "data":
        return json.dumps({
            "type": "data",
            "source": ADDR,
            "destination": obj["destination"],
            "payload": obj["payload"],
        })

# Função que periodicamente manda update para todos as rotas
def updateTh():
    while True:
        for i in routes:
            data = createJSON({"destination": i["addr"]},"update")
            socket.sendto(bytes(data, "UTF-8"), (i["addr"], PORT))
        time.sleep(int(PI))
threading.Thread(target = updateTh).start()

# Função que recebe as mensagens de outros roteadores
def receiveTh():
    while True:
        data = socket.recv(1024)
        message = data.decode("UTF-8")
        printSuccess("Recebi uma mensagem!", message)
        if message['type'] == "update":
            print("Update!")
            routeTable[message["source"]] = message["distances"]
        elif message['type'] == "trace":
            print("Trace!")
        elif message['type'] == "data":
            print("Data!")     
threading.Thread(target = receiveTh).start()

# Espera o comando do usuario 
print("Para fechar, digite 'q', 'quit' ou ctrl+c")
command, args = get_input()
# printSuccess("Input recebido", "{} - {}".format(command, args), "Inputs:")
while command not in ["q", "quit"]:
    address = args[0]
    if len(args) > 1:
        weight = args[1]
    if command == 'add':
        if not any(x for x in routes if x["addr"] == address):
            routes.append({"addr": address, "weight": weight})
            printSuccess("Endereço adicionado!")
            printAddressList(routes)
        else:
            printError("Endereço já existe na lista!")
    elif command == 'del':
        index = next((x for x, item in enumerate(routes)
                     if item["addr"] == address), None)
        if index != None:
            routes.pop(index)
            printSuccess("Endereço removido!")
            printAddressList(routes)
        else:
            printError("Endereço não existe na lista!")
    elif command == 'trace':
        printSuccess("Trace!")
    else:
        printError("Comando desconhecido - {}".format(command),
                   "Tente 'add', 'del', 'trace' ou 'quit'")
    command, args = get_input()
printSuccess("Finalizando programa...")
