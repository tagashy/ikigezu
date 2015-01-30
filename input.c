#include <termios.h> 
#include <unistd.h> 
  #include <dirent.h>
#include <sys/types.h>
#include <time.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <sys/types.h>
#include <ctype.h>
#include <errno.h>
#include <sys/stat.h>
#include <fcntl.h>

void mode_raw(int activer) 
{ 
    static struct termios cooked; 
    static int raw_actif = 0; 
  
    if (raw_actif == activer) 
        return; 
  
    if (activer) 
    { 
        struct termios raw; 
  
        tcgetattr(STDIN_FILENO, &cooked); 
  
        raw = cooked; 
        cfmakeraw(&raw); 
        tcsetattr(STDIN_FILENO, TCSANOW, &raw); 
    } 
    else 
        tcsetattr(STDIN_FILENO, TCSANOW, &cooked); 
  
    raw_actif = activer; 
}
int main()
{
	mode_raw(1);
	char c;
	while(c != EOF) {
c = getchar();
switch(c) {
	case '\r': putc('\r',stdout);
	putc('\n',stdout);
	break;
	case EOF:mode_raw(0);
	exit(0);
	break;
	default: putc(c,stdout);
	break;
	}
	}
}
