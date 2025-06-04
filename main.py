from saving import save, load
from Node import Node
from constructor import constructTree


tree = constructTree("models/50")
# save(tree, "models/50PlayerTree.pkl")
# tree = load("models/50PlayerTree.pkl")


# Game
# user play the whites
gamelog = ""
current = tree
running = True

while running:
    # TODO Check winning conditions

    # User play
    print("\n\n###########################")
    print(f"Available move for player: {current.getChilds().keys()}")
    # move = input("user: >>> ")
    move = list(current.getChilds().keys())[0]
    print(f"user play: {move}")
    gamelog += f"{move} "
    current = current.getChilds()[move]

    # Computer play
    print(f"Available move for computer: {current.getChilds().keys()}")
    play = current.getNextMove()
    if(play == None):
        print("Computer resign.")
        running = False
    else:
        gamelog += f"{play} "
        current = current.getChilds()[play]
        print("\n\n###########################")
        print(f"played: {play}")
        print(f"Current log: [[[ {gamelog} ]]]")


    


