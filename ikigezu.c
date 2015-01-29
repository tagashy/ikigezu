#include <dirent.h>
#include <sys/types.h>
#include <time.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>
#include <sys/types.h>
#include <ctype.h>
#include <errno.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <ncurses.h> 

#ifdef WIN32
#define SPATH ";"
#define ARBORESCENCE "\\"
#elif defined (linux)
#define SPATH ":"
#define ARBORESCENCE "/"
#endif


void handle_signal(int signo);
int verifPath();
void shell();
int isFile(char* path);

int main()
{

	signal(SIGINT, SIG_IGN);
	signal(SIGINT, handle_signal);
		shell();
	
return 0;
}

void shell()
{
	char history[100];
	char c;
	char tmp[100];/* = (char *)malloc(sizeof(char) * 100);*/

	printf("ikigezu>");
	while(c != EOF) {
		c = getchar();
		switch(c) {
	case '\n': if(tmp[0] == '\0') {
					   printf("ikigezu>");
				   } else {
					   if(!strcmp(tmp,"exit")||!strcmp(tmp,"quit"))
					   {
						   exit(0);
					   }
					   verifPath(tmp);
					   printf("ikigezu>");
				   }
				   memset(history,'\0', 100);
				   strncpy(history,tmp,100);
				   memset(tmp,'\0', 100);
				   break;
	case 27:printf("first Lock: open\n");
				c = getchar();
				if (c=='[')
				{
					printf("second Lock: open\n");
					c = getchar();
					switch(c) {
					case 'A':printf("third Lock: open\n");
					memset(tmp,'\0', 100);
					strncpy(tmp,history,100);
					printf("ikigezu>%s",tmp);
					break;
					}
				}
				fflush(stdout);
				break;
	default: strncat(tmp, &c, 1);
				 break;
		}
	}

}


int verifPath(char input[])
{

char *fichier;
char *argument;
char *path;
char cppath[100];
char *token;
char cptoken[100];
char commande[200];
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
		printf("FOUND : '%s'\n",chemin);
		printf("argument : '%s'\n",argument);
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


void handle_signal(int signo)
{
	printf("\ndefqon1#");
	fflush(stdout);
}

void unix_clear_screen(void) 
{ 
    clear(); 
    move(0, 0); 
}
