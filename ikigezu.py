import subprocess

global tmp
init_ascii_art="""
,_,_,_,_,_,_,_,_,_,_,_|______________________________________________________
| | |I|K|I|G|E|Z|U| | |_____________________________________________________/
'-'-'-'-'-'-'-'-'-'-'-|----------------------------------------------------'
to use python inside os cmd use #(your python expression)#
"""


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
                    print "exec ", tmp_args[0]
                    exec (tmp_args[0])
        # LEGB rule bypass
        vals = []
        for val in locals():
            vals.append(val)
        for val in vals:
            globals()[val] = locals()[val]
        return cmd
    except Exception, python_e:
        print "error in #()# syntax", python_e


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




def main():
    global tmp
    tmp = ""
    print init_ascii_art
    while True:
        cmd=raw_input("DG>")
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
        except Exception,python_e:
            #print python_e.__class__
            #if not isinstance(python_e, exceptions.SyntaxError) and not isinstance(python_e,exceptions.NameError):
                print "python err: [{}]".format(python_e)
            #else:
                try:
                    args=cmd.split(" ")
                    p_cmd=subprocess.call(args,shell=True)

                except Exception,os_e:
                    print("Sorry error both on python :{}\n and in OS: {}\n".format(python_e,os_e))

main()
