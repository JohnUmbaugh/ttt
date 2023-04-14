import os
import openai
import json

openai.api_key = os.getenv("OPENAI_API_KEY")

def createPlacementCommandKey( positions ):
	command = {
		"type": "placement",
		"positions": positions,
	}
	return json.dumps(command)

def createResignationCommandKey():
	command = {
		"type": "resignation"
	}
	return json.dumps(command)

def addToCommandDict( localCommandDict, command, freeText ):
	if command not in localCommandDict:
		localCommandDict[ command ] = []

	embedding_data = openai.Embedding.create( input = freeText, model="text-embedding-ada-002" )
	localCommandDict[ command ].append( {
		"phrase": freeText,
		"vector": embedding_data[ "data" ][ 0 ][ "embedding" ]
	} )

commandDict = {}

# placement

addToCommandDict( commandDict, createPlacementCommandKey( [ ( 0, 0 ) ] ), "upper left" )
addToCommandDict( commandDict, createPlacementCommandKey( [ ( 0, 2 ) ] ), "upper right" )
addToCommandDict( commandDict, createPlacementCommandKey( [ ( 2, 0 ) ] ), "lower left" )
addToCommandDict( commandDict, createPlacementCommandKey( [ ( 2, 2 ) ] ), "lower right" )
addToCommandDict( commandDict, createPlacementCommandKey( [ ( 0, 1 ) ] ), "upper center" )
addToCommandDict( commandDict, createPlacementCommandKey( [ ( 2, 1 ) ] ), "lower center" )
addToCommandDict( commandDict, createPlacementCommandKey( [ ( 1, 0 ) ] ), "left center" )
addToCommandDict( commandDict, createPlacementCommandKey( [ ( 1, 2 ) ] ), "right center" )
addToCommandDict( commandDict, createPlacementCommandKey( [ ( 1, 1 ) ] ), "center" )
addToCommandDict( commandDict, createPlacementCommandKey( [ ( 0, 0 ) ] ), "top left" )
addToCommandDict( commandDict, createPlacementCommandKey( [ ( 0, 2 ) ] ), "top right" )
addToCommandDict( commandDict, createPlacementCommandKey( [ ( 2, 0 ) ] ), "bottom left" )
addToCommandDict( commandDict, createPlacementCommandKey( [ ( 2, 2 ) ] ), "bottom right" )
addToCommandDict( commandDict, createPlacementCommandKey( [ ( 0, 0 ), ( 0, 1 ), ( 0, 2 ) ] ), "top" )
addToCommandDict( commandDict, createPlacementCommandKey( [ ( 2, 0 ), ( 2, 1 ), ( 2, 2 ) ] ), "bottom" )
addToCommandDict( commandDict, createPlacementCommandKey( [ ( 0, 0 ), ( 1, 0 ), ( 2, 0 ) ] ), "left" )
addToCommandDict( commandDict, createPlacementCommandKey( [ ( 0, 2 ), ( 1, 2 ), ( 2, 2 ) ] ), "right" )
addToCommandDict( commandDict, createPlacementCommandKey( [ ( 1, 1 ) ] ), "middle" )

# non-specific placement

addToCommandDict( commandDict, createPlacementCommandKey( [ ( 0, 0 ), ( 0, 1 ), ( 0, 2 ), ( 1, 0 ), ( 1, 1 ), ( 1, 2 ), ( 2, 0 ), ( 2, 1 ), ( 2, 2 ) ] ), "anywhere" )
addToCommandDict( commandDict, createPlacementCommandKey( [ ( 0, 0 ), ( 2, 0 ), ( 0, 2 ), ( 2, 2 ) ] ), "any corner" )
addToCommandDict( commandDict, createPlacementCommandKey( [ ( 0, 1 ), ( 1, 0 ), ( 1, 1 ), ( 1, 2 ), ( 2, 1 ) ] ), "any non-corner" )
addToCommandDict( commandDict, createPlacementCommandKey( [ ( 0, 1 ), ( 1, 0 ), ( 1, 1 ), ( 1, 2 ), ( 2, 1 ) ] ), "anywhere except a corner" )
addToCommandDict( commandDict, createPlacementCommandKey( [ ( 0, 0 ), ( 0, 1 ), ( 0, 2 ), ( 1, 0 ), ( 1, 2 ), ( 2, 0 ), ( 2, 1 ), ( 2, 2 ) ] ), "anywhere except the middle" )

# resignation

addToCommandDict( commandDict, createResignationCommandKey(), "quit" )
addToCommandDict( commandDict, createResignationCommandKey(), "i don't want to play anymore" )
addToCommandDict( commandDict, createResignationCommandKey(), "i give up" )

with open('ttt_embeddings.json', 'w') as f:
    json.dump(commandDict, f)