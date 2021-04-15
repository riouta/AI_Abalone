import socket
import sys
from jsonNetwork import receiveJSON, sendJSON

def IA(board, num_joueur):
    #put all your if else statement here at the end you should send a move which shd be good
    print(board)
    print(num_joueur)
    move = {
    "marbles": [[1, 1], [2, 2]],
    "direction": "SE"
    }
    return move

if __name__ == '__main__':
    s= socket.socket()
    args = sys.argv[1:]
    port = int(args[0])
    s.bind(("",port)) # bind prend l'adresse ip et le port en parametre as a tuple
    s.listen()   ##€coute(voir la source de la requete) une infinté de pers a la fois 
    print("I am listening hihi")
    while True:
        conn,detail= s.accept()# accepte la connextion du serveur externe
        msg = receiveJSON(conn)
        print(msg)
        if msg["request"] == "ping":
            resp = {"response" : "pong"}
            sendJSON(conn, resp) #online= connexion etablie sinon affixhe lost
        elif msg["request"] == "play":
            board = msg["board"]
            current = msg["current"]
            obj = IA(board,current)
            sendJSON(conn, obj) # Envoie un move au serveur