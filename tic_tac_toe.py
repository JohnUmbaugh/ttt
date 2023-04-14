import os
import openai
import numpy as np
import json

openai.api_key = os.getenv("OPENAI_API_KEY")

def print_board(board):
    print("")
    print("-------------")
    for i in range(3):
        print("|", end=" ")
        for j in range(3):
            print(board[i][j], "|", end=" ")
        print()
        print("-------------")

def check_win(board, player):
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] == player:
            return True
        if board[0][i] == board[1][i] == board[2][i] == player:
            return True
    if board[0][0] == board[1][1] == board[2][2] == player:
        return True
    if board[0][2] == board[1][1] == board[2][0] == player:
        return True
    return False

commandDict = None
with open('ttt_embeddings.json', 'r') as f:
    commandDict = json.load(f)

def cosineSimilarity( a, b ):
    return np.dot(a, b)/(np.linalg.norm(a)*np.linalg.norm(b))

def obtain_command_from_freetext( freeText ):
    freeText = freeText.lower()
    embedding_data = openai.Embedding.create( input = freeText, model="text-embedding-ada-002" )
    npInputEmbeddingVector = np.array( embedding_data[ "data" ][ 0 ][ "embedding" ] )

    # find the command that is closest to the freeText input, according to cosine similarity
    best = None
    for command in commandDict:
        for precomputedEmbedding in commandDict[ command ]:
            npPrecomputedEmbeddingVector = np.array( precomputedEmbedding[ "vector" ] )
            if best is None:
                best = ( command, precomputedEmbedding[ "phrase" ], npPrecomputedEmbeddingVector )
            else:
                if cosineSimilarity( npInputEmbeddingVector, npPrecomputedEmbeddingVector ) > cosineSimilarity( npInputEmbeddingVector, best[ 2 ] ):
                    best = ( command, precomputedEmbedding[ "phrase" ], npPrecomputedEmbeddingVector )
                    # print( "Newest best: " + best + ": " + str( cosineSimilarity( testVector, tokenToVector[ bestToken ] ) ) )

    print( "Best matching command = " + best[ 0 ] + ", matching phrase = '" + best[ 1 ] + "'")

    return( best[ 0 ] )

def tic_tac_toe():
    board = [[" ", " ", " "] for i in range(3)]
    players = ["X", "O"]
    current_player = players[0]

    while True:
        print_board(board)

        freetext = input( "Player {}, please describe your move: ".format(current_player) )
        command = obtain_command_from_freetext( freetext )

        row = None
        col = None
        unrolledCommand = json.loads( command )

        if unrolledCommand[ "type" ] == "placement":
            row = unrolledCommand[ "position" ][ 0 ]
            col = unrolledCommand[ "position" ][ 1 ]

            if board[row][col] != " ":
                print("This position is already occupied. Please try again!")
                continue

            board[row][col] = current_player

            if check_win(board, current_player):
                print_board(board)
                print("Player {} wins!".format(current_player))
                break

            if all([board[i][j] != " " for i in range(3) for j in range(3)]):
                print_board(board)
                print("The game is a tie!")
                break

            current_player = players[(players.index(current_player) + 1) % 2]
        elif unrolledCommand[ "type" ] == "resignation":
            print("Player {} loses by resigning -- but at least you maintain your dignity!".format(current_player))
            break

if __name__ == "__main__":
    tic_tac_toe()
