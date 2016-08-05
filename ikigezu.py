import subprocess
import os
import exceptions
init_ascii_art="""
,_,_,_,_,_,_,_,_,_,_,_|______________________________________________________
| | |I|K|I|G|E|Z|U| | |_____________________________________________________/
'-'-'-'-'-'-'-'-'-'-'-|----------------------------------------------------'
to use python inside os cmd use #(your python expression)#
"""

def main():
    print init_ascii_art
    while True:
        cmd=raw_input("DG>")
        try:
            os_pythonize_args = cmd.split('#(')
            cmd = str(os_pythonize_args[0])
            if len(os_pythonize_args) >= 2:
                for i in range(1, len(os_pythonize_args)):
                    tmp_args = os_pythonize_args[i].split(")#")
                    if not "import" in tmp_args[0]:
                        exec ('tmp=' + tmp_args[0])
                        cmd += str(tmp)
                        cmd += str(tmp_args[1])
                    else:
                        exec (tmp_args[0])
                print "Executing:", cmd
            exec(cmd)
        except Exception,python_e:
            #print python_e.__class__
            #if not isinstance(python_e, exceptions.SyntaxError) and not isinstance(python_e,exceptions.NameError):
                print "python err: [{}]".format(python_e)
            #else:
                try:
                    args=cmd.split(" ")
                    #print args
                    p_cmd=subprocess.call(args,shell=True)

                except Exception,os_e:
                    print("Sorry error both on python :{}\n and in OS: {}\n".format(python_e,os_e))

main()
