import os
import socket
import string
import subprocess
import sys
import thread

global tmp
global cmd_history
init_ascii_art="""
,_,_,_,_,_,_,_,_,_,_,_|______________________________________________________
| | |I|K|I|G|E|Z|U| | |_____________________________________________________/
'-'-'-'-'-'-'-'-'-'-'-|----------------------------------------------------'
"""


def save_as(name, data):
    try:
        f = open(name, mode="w")
        f.write(data)
        f.close()
    except:
        print_error("Can't save data")


def store_data(cmd):
    global cmd_history
    if cmd is not None:
        cmd_history += cmd
        cmd_history += "\n"


def print_history():
    global cmd_history
    i = 0
    for line in cmd_history.split("\n"):
        if line != "":
            print "#{} - {}".format(i, line)
            i += 1


def flush_history():
    global cmd_history
    cmd_history = ""


def pattern_create(size, pattern_charset=(string.ascii_letters + string.octdigits)):
    ret = ""
    pattern_charsets = []
    patterns_size = len(pattern_charset)
    # print patterns_size,pattern_charset
    for i in range(4):
        pattern_charsets.append(pattern_charset)
    cpt = 0
    x = y = z = i = 0
    while cpt < size:

        patern_index = cpt % 4
        if patern_index == 0:
            ret += (pattern_charsets[patern_index])[i]
            if i >= patterns_size:
                if z >= patterns_size:
                    if y >= patterns_size:
                        if x >= patterns_size:
                            print_error("Pattern error", 2)
                        else:
                            x += 1
                            y = 0
                            z = 0
                            i = 0
                    else:
                        y += 1
                        z = 0
                        i = 0
                else:
                    z += 1
                    i = 0
            else:
                i += 1
        elif patern_index == 1:
            ret += (pattern_charsets[patern_index])[z]
        elif patern_index == 2:
            ret += (pattern_charsets[patern_index])[y]
        elif patern_index == 3:
            ret += (pattern_charsets[patern_index])[x]

        cpt += 1
    print ret
    return ret



def print_error(msg, niv=0):
    niveau = ["INFO", 'WARNING', "ERROR", "CRITICAL"]
    if verbose:
        print "[{}] {}".format(niveau[niv], msg)
    elif niv > 1:
        print "[{}] {}".format(niveau[niv], msg)
        if niv == 3:
            exit(-1)

def exec_partial(cmd):
    try:
        os_pythonize_args = cmd.split('#(')
        cmd = str(os_pythonize_args[0])
        if len(os_pythonize_args) >= 2:
            for i in range(1, len(os_pythonize_args)):
                # print os_pythonize_args[i]
                tmp_args = os_pythonize_args[i].split(")#")
                # print tmp_args
                if not "import" in tmp_args[0]:
                    exec ('tmp=' + tmp_args[0])
                    cmd += str(tmp)
                    cmd += str(tmp_args[1])
                else:
                    # print "exec ", tmp_args[0]
                    exec (tmp_args[0])
        #
        # set locals imported global
        #
        vals = []
        for val in locals():
            if (val is not "os_pythonize_args") and (val is not "cmd") and (val is not "tmp_args"):
                vals.append(val)
        for val in vals:
            globals()[val] = locals()[val]
        return cmd
    except Exception, python_e:
        print_error("error in #()# syntax " + str(python_e), 2)


def tcp_read(sock):
    try:
        while True:
            chunk = sock.recv(9999)
            if chunk == '':
                print_error("socket closed", 3)
                raise RuntimeError("socket connection broken")
            else:
                print "\nTCP<", chunk
    except:
        return


def tcp_connector():
    global tmp
    addr = "127.0.0.1"
    port = 80
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print "welcome to ikigezu tcp connector address must be a ip or fqdn followed by port ex: www.google.com:80"
    addr_field = ["none"]
    send_CRLF = raw_input("Would you like to send CRLF after input? [y]/n")
    if send_CRLF.lower() == "n" or send_CRLF.lower() == "no":
        send_CRLF = False
    else:
        send_CRLF = True
    while len(addr_field) < 2:
        addr = raw_input("please enter adress:")
        addr_field = addr.split(":")
        if len(addr_field) < 2:
            print "error no port selected"
        else:
            addr = addr_field[0]
            port = int(addr_field[1])
    sock.connect((addr, port))
    print "connection succesfull"
    thread.start_new_thread(tcp_read, (sock,))
    while True:
        send = raw_input("TCP>")
        if send == "exit":
            return
        else:
            send = exec_partial(send)
            if send_CRLF:
                send += "\n"
            sock.sendall(send)


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
            exec_cmd(cmd)
    else:
        print_error("script path is invalid", 2)
        return


def exec_cmd(cmd):
    cmd = exec_partial(cmd)
    if cmd != "history":
        store_data(cmd)
    try:
        if cmd == "exit" or cmd == "quit":
            exit(1)
        elif cmd == "tcp_connect":
            tcp_connector()
        elif cmd == "history":
            print_history()
        elif cmd == "flush_history":
            flush_history()
        elif "store" in cmd:
            if len(cmd.split(" ")) > 1:
                save_as(cmd.split(" ")[1], cmd_history)
        elif "pattern_create" in cmd:
            arg = cmd.split(" ")
            if len(arg) == 2:
                print (pattern_create(arg[1]))
            elif len(arg) == 3:
                print (pattern_create(arg[1], arg[2]))
            else:
                print_error("no size specified", 2)
        else:
            exec (cmd)
            # LEGB rule bypass
            vals = []
            for val in locals():
                vals.append(val)
            for val in vals:
                globals()[val] = locals()[val]

    except Exception, python_e:
        # print python_e.__class__
        # if not isinstance(python_e, exceptions.SyntaxError) and not isinstance(python_e,exceptions.NameError):

        print_error("python err: [{}]".format(python_e))
        if isinstance(python_e, socket.error):
            print_error("socket_closed", 2)

        else:
            try:
                args = cmd.split(" ")
                p_cmd = subprocess.call(args, shell=True)

            except Exception, os_e:
                print_error("Sorry error both on python :{}\n and in OS: {}\n".format(python_e, os_e), 1)


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
        exec_cmd(cmd)


if __name__ == '__main__':
    cmd_history = ""
    global verbose
    verbose = False
    argv = []
    script_path = "none"
    if len(sys.argv) > 1:

        for i in range(1, len(sys.argv)):
            if (sys.argv[i] == "-s" or sys.argv[i] == "-si") and i + 1 <= len(sys.argv):
                script_path = sys.argv[i + 1]
            if sys.argv[i] == "-v":
                verbose = True

            argv.append(sys.argv[i])
    if script_path != "none":
        script_main(script_path)
        for val in argv:
            if "-i" == val or "-si" == val:
                ikigezu_main()
    else:
        ikigezu_main()
