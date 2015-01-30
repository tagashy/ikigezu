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
#define BUFFER 256
#ifdef WIN32
#define SPATH ";"
#define ARBORESCENCE "\\"
#elif defined (linux)
#define SPATH ":"
#define ARBORESCENCE "/"
#endif
void cexit(void);
void mode_raw(int activer);
int verifPath();
int isFile(char* path);
void unix_clear_screen(void);
int main()
{
	mode_raw(1);
	char c;
	char history[BUFFER];
	char tmp[BUFFER];
	printf("ikigezu>");
	while(c != EOF) {
c = getchar();
switch(c) {
	case '\r': putc('\r',stdout);
	putc('\n',stdout);
	if(tmp[0] == '\0') {
					   printf("ikigezu>");
				   } else {if(!strcmp(tmp,"exit")||!strcmp(tmp,"quit"))
					   {
						   cexit();
					   }
					   verifPath(tmp);
					   
					    printf("ikigezu>");
				   }
				   memset(history,'\0', 100);
				   strncpy(history,tmp,100);
				   memset(tmp,'\0', 100);
	break;
	case EOF:cexit();
	break;
	case 3:printf("\r\ndefqon1#");
	break; 
	case 4:cexit();
	break;
	case 27:c=getchar();
		if (c=='[')
		{
			switch(c){
				case 'A':putc('A',stdout);
				break;
				}
		}
	break;
	default: strncat(tmp, &c, 1);
	putc(c,stdout);
	break;
	}
	}
}
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

int verifPath(char input[])
{

char *fichier;
char *argument;
char *path;
char cppath[BUFFER];
char *token;
char cptoken[BUFFER];
char commande[BUFFER];
int exist;
char *chemin;

strcpy(commande,input);
path = getenv("PATH");
fichier=strtok(commande," ");
argument=strtok(NULL,"\0");
strcpy(cppath,path);
token=strtok(cppath,SPATH);
 
while ( token != NULL )
{
	exist=0;
	strcpy(cptoken,token);
	strcat(cptoken,ARBORESCENCE);
	chemin=strcat(cptoken,fichier);
	exist=isFile(chemin);
	if (exist)
	{
		printf("FOUND : '%s'\r\n",chemin);
		printf("argument : '%s'\r\n",argument);
	}
	
	token=strtok(NULL,SPATH);
}
return 0;
}


int isFile(char* dir)
{
	DIR* directory = opendir(dir);
	FILE * file = NULL;
 
	if(directory == NULL)
	{
		file = fopen(dir, "r");
		if (file == NULL)
		{
			return 0;
		}
		else
		{
			fclose(file);
			return 1;
		}
	}
	else
	{
		closedir(directory);
		return 1;
	}
}

void cexit(void)
{
	
	mode_raw(0);
	putc('\n',stdout);
	exit(0);
}
