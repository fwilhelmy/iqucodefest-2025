# the_game/main.py
from board  import Board
from space  import Space

def build_demo():
    return Board([
        Space(0,"Start", None,[1],      (0,0)),
        Space(1,"Blue",  None,[2],      (1,0)),
        Space(2,"Fork",  None,[3,4],    (2,0)),
        Space(3,"Red",   None,[4],      (2,1)),
        Space(4,"Blue",  None,[5],      (3,0)),
        Space(5,"Goal", "END",[],       (4,0)),
    ])

def play_demo():
    

if __name__ == "__main__":
    board = build_demo()
    print(board.draw_ascii())
