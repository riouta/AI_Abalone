import socket
import sys
from jsonNetwork import sendJSON

def subs(port_ia, port_destinataire=3000) :
    msg={
        "request": "subscribe",
        "port": port_ia, #port de mon ia
        "name": "bokchita",
        "matricules": ["18383"]
    }
    s= socket.socket()
    s.connect((socket.gethostname(), port_destinataire))
    sendJSON(s, msg)
if __name__ == '__main__':
    args = sys.argv[1:] 
    port = 3000 #ne change pas tjs mm
    print(args) #pr changer le port (pas vrmt;))
    port_ia= args[0]
    if len(args)==2:
        port= args[1]
    subs(int(port_ia),port_destinataire=port) #je subscribe mon ia ds serveur tournoi
#résumé= importer module+ piger sys et jouer avec les ports 

