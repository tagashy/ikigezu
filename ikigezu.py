import os
import socket
import subprocess
import sys
import thread

global tmp
init_ascii_art="""
,_,_,_,_,_,_,_,_,_,_,_|______________________________________________________
| | |I|K|I|G|E|Z|U| | |_____________________________________________________/
'-'-'-'-'-'-'-'-'-'-'-|----------------------------------------------------'
"""


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
    try:
        if cmd == "exit" or cmd == "quit":
            exit(1)
        elif cmd == "tcp_connect":
            tcp_connector()
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
