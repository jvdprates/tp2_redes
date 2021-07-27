import socket as skt
import argparse as ap
import networkx as nx
import sys
import json

# Constantes do programa
PORT = 55151

# Argumentos de chamada do programa
parser = ap.ArgumentParser(
    description='Trabalho pratico 2 - Bruno Oliveira, João Prates')
parser.add_argument('addr', help='Endereço de ip do roteador')
parser.add_argument('period', help='Período entre envio de mensagens de update (π)')
parser.add_argument("-s", "--startup_commands",
                    help='O nome de um arquivo .txt contendo comandos de teclado para adicionar links')
args = parser.parse_args()
# ./router.py <ADDR> <PERIOD> [STARTUP]

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
    
# Espera o comando do usuario
print("Para fechar, digite 'q', 'quit' ou ctrl+c")
command, args = get_input()
# printSuccess("Input recebido", "{} - {}".format(command, args), "Inputs:")
while command not in ["q", "quit"]:
    if command == 'add':
        printSuccess("Adicionar!")
    elif command == 'del':
        printSuccess("Deletar!")
    elif command == 'trace':
        printSuccess("Trace!")
    else:
        printError("Comando desconhecido - {}".format(command), "Tente 'add', 'del', 'trace' ou 'quit'")
    command, args = get_input()
printSuccess("Finalizando programa...")