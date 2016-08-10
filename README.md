# ikigezu
Python shell that allow you to execute python command and system command whithin the same line.
A simple tcp client is available with tcp_connect
It is possible to execute python everywhere you can type it with #(expression)#

It is possible to execute a script with -s argument and to continue to the interactive shell after with -i or -si



Order of processing inside the shell:
1. Executing #()# in order and store the result inside command line
2. Try to execute command line in python
3. If fail try to execute it inside OS shell (with subprocess)
4. Print Error message


Ex: downloading google.com page and store it in google.html 
echo #(import requests)# #(requests.get("http://google.com").text)# >> google.html

