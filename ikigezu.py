import os
import subprocess
import sys

global tmp
init_ascii_art="""
,_,_,_,_,_,_,_,_,_,_,_|______________________________________________________
| | |I|K|I|G|E|Z|U| | |_____________________________________________________/
'-'-'-'-'-'-'-'-'-'-'-|----------------------------------------------------'
"""


def print_error(msg, niv=0):
    niveau = ["INFO", 'WARNING', "ERROR", "CRITICAL"]
    print "[{}]{}".format(niveau[niv], msg)

def exec_partial(cmd):
    try:
        # print len(cmd.split('#('))
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
        # set locals imported global
        vals = []
        for val in locals():
            if (val is not "os_pythonize_args") and (val is not "cmd") and (val is not "tmp_args") and (
                val is not "tmp"):
                vals.append(val)
        for val in vals:
            globals()[val] = locals()[val]
        return cmd
    except Exception, python_e:
        print_error("error in #()# syntax " + str(python_e), 3)


def tcp_read(sock):
    try:
        while True:
            chunk = sock.recv(9999)
            if chunk == '':
                raise RuntimeError("socket connection broken")
            else:
                print "\nTCP<", chunk
    except:
        return


def tcp_connector():
    global tmp
    addr = "127.0.0.1"
    port = 80
    import thread
    import socket
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
        script = script.split("def")
        if len(script) > 1:
            exec_cmd(script[0])
            for i in range(1, len(script)):
                exec_cmd("def" + script[i])

        else:
            exec_cmd(script[0])
    else:
        print_error("script path is invalid", 3)
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
        # else:
        try:
            args = cmd.split(" ")
            p_cmd = subprocess.call(args, shell=True)

        except Exception, os_e:
            print_error("Sorry error both on python :{}\n and in OS: {}\n".format(python_e, os_e), 1)


def ikigezu_main():
    cmd = ""
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
    argv = []
    script_path = "none"
    if len(sys.argv) > 1:

        for i in range(1, len(sys.argv)):
            if sys.argv[i] == "-s" and i + 1 <= len(sys.argv):
                script_path = sys.argv[i + 1]
            argv.append(sys.argv[i])
    if script_path != "none":
        script_main(script_path)
        for val in argv:
            print val
            if "-i" == val or "-si" == val:
                ikigezu_main()
    else:
        ikigezu_main()
