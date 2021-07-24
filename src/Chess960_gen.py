# -*- coding: utf-8 -*-
"""
This program generate a text file Commands.txt
setoption name UCI_Chess960 value true
d
eval
go depth 20
d 
eval ...

using the command Commands.txt|stockfish_13_win_x64_bmi2>output.txt
parsing is Trivial
"""
if __name__== "__main__":
    with open("Chess960.txt", "r", encoding="utf-8") as chess:
        with open("Commands.txt", "w", encoding="utf-8") as cmds:
            cmds.write("setoption name UCI_Chess960 value true\n")
            line_count=0
            for row in chess:
                if line_count==0:
                    line_count+=1
                    continue
                start_index=row.find("[")+4
                end_index=row.find("]")
                s=row[start_index:end_index]
                cmds.write("position fen "+s+"\nd\neval\ngo depth 20\n")
