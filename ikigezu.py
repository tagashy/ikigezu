import os
import sys

import function

global tmp
init_ascii_art="""
,_,_,_,_,_,_,_,_,_,_,_|______________________________________________________
| | |I|K|I|G|E|Z|U| | |_____________________________________________________/
'-'-'-'-'-'-'-'-'-'-'-|----------------------------------------------------'
"""

def script_main(script_path):
    if os.path.isfile(script_path):
        script_file = file(script_path)
        script = script_file.read()
        script = script.split("\n")
        i = 0
        while i < len(script):
            cmd = script[i]
            if "class" in cmd or "def" in cmd or "if" in cmd or "elif" in cmd or "else" in cmd:
                next_instruct = "\t"
                while next_instruct.startswith("\t") or next_instruct.startswith(" "):
                    i += 1
                    if i < len(script):
                        next_instruct = script[i]
                        cmd += "\n" + next_instruct
            i += 1
            function.exec_cmd(cmd)
    else:
        function.print_error("script path is invalid", 2)
        return

def ikigezu_main():
    print init_ascii_art
    print "to use python inside os cmd use #(your python expression)#"
    while True:
        cmd=raw_input("DG>")
        if "class" in cmd or "def" in cmd or "if" in cmd or "elif" in cmd or "else" in cmd:
            next_instruct = "\t"
            while next_instruct.startswith("\t") or next_instruct.startswith(" "):
                next_instruct = raw_input()
                cmd += "\n" + next_instruct
        function.exec_cmd(cmd)


if __name__ == '__main__':

    function.verbose = False
    argv = []
    script_path = "none"
    if len(sys.argv) > 1:
        for i in range(1, len(sys.argv)):
            if (sys.argv[i] == "-s" or sys.argv[i] == "-si") and i + 1 <= len(sys.argv):
                script_path = sys.argv[i + 1]
            if sys.argv[i] == "-v":
                function.verbose = True

            argv.append(sys.argv[i])
    if script_path != "none":
        script_main(script_path)
        for val in argv:
            if "-i" == val or "-si" == val:
                ikigezu_main()
    else:
        ikigezu_main()
