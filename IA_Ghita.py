import socket
import sys
from jsonNetwork import receiveJSON, sendJSON
import random



def get_key(val,my_dict):
    for key, value in my_dict.items():
         if val == value:
             return key

def get_allies_pos(posofpions,board,color):
      marbleslist=[]
      directions = [(-1,-1),(-1,0),(0,1),(1,1),(1,0),(0,-1)]
      for pos in posofpions:
            for direction in directions:
                  marbles=[pos]
                  if marbles not in marbleslist:
                        marbleslist.append(marbles)
                  i=1
                  run = True
                  while i <3 and run:
                        if (pos[0]+i*direction[0],pos[1]+i*direction[1]) in posofpions:
                              marbles+=[(pos[0]+i*direction[0],pos[1]+i*direction[1])]
                              marbleslist.append(marbles[:])
                              i+=1
                        else:
                              run = False
      new_marbleslist=[]
      for marbles in marbleslist:
            for direction in directions:
                  pos = marbles[0]
                  if 0<=pos[0]+direction[0]<9 and 0<pos[1]+direction[1]<9:
                        if (pos[0]+direction[0],pos[1]+direction[1]) not in posofpions and board[pos[0]+direction[0]][pos[1]+direction[1]] == "E":
                              if marbles not in new_marbleslist:
                                    new_marbleslist.append(marbles)
      new2marbleslist=[]
      for marbles in new_marbleslist:
            if len(marbles )!=1:
                  pos=marbles[0]
                  direction = (marbles[0][0]-marbles[1][0],marbles[0][1]-marbles[1][1])
                  to = (pos[0]+direction[0],pos[1]+direction[1])
                  if 0<=to[0]<9and 0<=to[1]<9:
                      
                      if board[to[0]][to[1]] not in  'X'+color:
                            new2marbleslist.append(marbles)
            else:
                  new2marbleslist.append(marbles)
      return new2marbleslist

def possible_moves(allies,board,colorenemy):
      directions = {
	'NE': (-1,  0),
	'SW': ( 1,  0),
	'NW': (-1, -1),
	'SE': ( 1,  1),
	 'E': ( 0,  1),
	 'W': ( 0, -1)
      }
      moves = []
      moves2 = []
      moves3 = []
      for marble in allies:
            if len(marble)==1:
                  for direction,value in directions.items():
                        if 0<=marble[0][0]+value[0]<9 and 0<=marble[0][1]+value[1]<9:
                              if board[marble[0][0]+value[0]][marble[0][1]+value[1]] == "E":
                                    moves.append({'marbles':marble,'direction':direction})
            else:
                direction=(marble[0][0]-marble[1][0],marble[0][1]-marble[1][1])
                if 0<=marble[0][0]+direction[0]<9 and 0<=marble[0][1]+direction[1]<9:
                    if board[marble[0][0]+direction[0]][marble[0][1]+direction[1]] == "E":
                        direction =get_key(direction,directions)
                        moves.append({'marbles':marble,'direction':direction})
                    elif board[marble[0][0]+direction[0]][marble[0][1]+direction[1]] == colorenemy:
                        lengthmine = len(marble)
                        if 0<=marble[0][0]+2*direction[0]<9  and 0<=marble[0][1]+2*direction[1]<9 :
                            if board[marble[0][0]+2*direction[0]][marble[0][1]+2*direction[1]] == "E":
                                direction =get_key(direction,directions)
                                moves2.append({'marbles':marble,'direction':direction})
                            elif board[marble[0][0]+2*direction[0]][marble[0][1]+2*direction[1]] == "X":
                                direction =get_key(direction,directions)
                                moves3.append({'marbles':marble,'direction':direction})
                            elif 0<=marble[0][0]+3*direction[0]<9 and 0<=marble[0][1]+3*direction[1]<9:
                                if board[marble[0][0]+2*direction[0]][marble[0][1]+2*direction[1]] == colorenemy and board[marble[0][0]+3*direction[0]][marble[0][1]+3*direction[1]] =="E" and lengthmine ==3:
                                    direction =get_key(direction,directions)
                                    moves2.append({'marbles':marble,'direction':direction})
                                elif board[marble[0][0]+2*direction[0]][marble[0][1]+2*direction[1]] == colorenemy and board[marble[0][0]+3*direction[0]][marble[0][1]+3*direction[1]] =="X" and lengthmine ==3:
                                    direction =get_key(direction,directions)
                                    moves3.append({'marbles':marble,'direction':direction})
                        elif marble[0][0]+2*direction[0]==-1 or marble[0][0]+2*direction[0]==9 or marble[0][1]+2*direction[1]==-1 or marble[0][1]+2*direction[1]==9 :
                            direction =get_key(direction,directions)
                            moves3.append({'marbles':marble,'direction':direction})
                        elif  board[marble[0][0]+2*direction[0]][marble[0][1]+2*direction[1]] == colorenemy or marble[0][0]+3*direction[0]==-1 or marble[0][0]+3*direction[0]==9 or marble[0][1]+3*direction[1]==-1 or marble[0][1]+3*direction[1]==9 and lengthmine ==3:
                            direction =get_key(direction,directions)
                            moves3.append({'marbles':marble,'direction':direction})

                        
      if len(moves)==0:
            moves.append({'marbles':[],'direction':[]})
      return moves,moves2,moves3


def IA(board, num_joueur):
    #put all your if else statement here at the end you should send a move which shd be good
    color = "B"
    colorenemy="W"
    if num_joueur==1:
        color="W"
        colorenemy="B"

    posofpions = []
    for line in range(len(board)):
        for column in range(len(board[line])):
            if board[line][column] == color:
                posofpions.append((line,column))
    allies = get_allies_pos(posofpions,board,color
                            )
    moves,moves2,moves3 = possible_moves(allies,board,colorenemy)
    if len(moves3)!=0:
        move = random.choice(moves3)
    elif len(moves2)!=0:
        move = random.choice(moves2)
    else:
        move = random.choice(moves)
    random.choice(moves)
    move = {
        'response':'move',
        'move': move,
        'message': 'ok'

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
            board = msg["state"]["board"]
            current = msg["state"]["current"]

            obj = IA(board,current)
            sendJSON(conn, obj) # Envoie un move au serveur