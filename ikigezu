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

#ifdef WIN32
#define SPATH ";"
#define ARBORESCENCE "\\"
#elif defined (linux)
#define SPATH ":"
#define ARBORESCENCE "/"
#endif


void handle_signal(int signo);
int verifPath();
static void purger();
static void search(char *chaine);
void shell();
int isFile(char* path);

int main()
{

		shell();
	
return 0;
}

void shell()
{
	char history[100];
	char c;
	char tmp[100];/* = (char *)malloc(sizeof(char) * 100);*/

	signal(SIGINT, SIG_IGN);
	signal(SIGINT, handle_signal);
	printf("ikigezu>");
	while(c != EOF) {
		c = getchar();
		switch(c) {
			case '\n': if(tmp[0] == '\0') {
					   printf("ikigezu>");
				   } else {
					   verifPath(tmp);
					   printf("ikigezu>");
				   }
				   memset(history,'\0', 100);
				   strncpy(history,tmp,100);
				   memset(tmp,'\0', 100);
				   break;
				case 27:printf("first Lock: open\n");
				strncat(tmp, &c, 1);
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
					fflush(stdout);
					}
				}
				break;
	default: strncat(tmp, &c, 1);
				 break;
		}
	}
	/*
char input[100];
printf("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n");
	while(1==1)
	{	
	printf("ikigezu>");
	fgets(input, sizeof input, stdin);
	search(input);
	verifPath(input);
	}
	*/
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
printf("commande : '%s'\n",fichier);
printf("argument : '%s'\n",argument);
printf("PATH : '%s'\n",path);
strcpy(cppath,path);
printf("CPPATH : '%s'\n",cppath);
token=strtok(cppath,SPATH);



 
while ( token != NULL )
{
	exist=0;
	strcpy(cptoken,token);
	printf("chemin actuel: '%s'\n",cptoken);
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

static void purger()
{

    int c;

    while ((c = getchar()) != '\n' && c != EOF)

    {}

}

static void search(char chaine[])
{

    char *p = strchr(chaine, '\n');
    if (p)

    {
        *p = '\0';
    }
	else
	{
	purger();
	}

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
