#include <termios.h> 
#include <unistd.h> 
#include <dirent.h>
#include <sys/types.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <sys/stat.h>
#include <time.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <ctype.h>
#include <errno.h>
#include <fcntl.h>

#define BUFFER 4096
#define MAXELEMS 32
/*definition des fonctions*/
void cexit(void);
void init();
void grandiossa();
void malentoff();
void alton();
void mode_raw(int activer);
void decoupe(char *input);
void attent(pid_t pid);
void execute(char **argument);
/*variable géneral indispensable a la gestion de l'input*/
char *argument[MAXELEMS];
char c;
char history[BUFFER];
char tmp[BUFFER];
	
int main()
{
	init();
	while(c != EOF) {
		mode_raw(1);
c = getchar();
switch(c) {
	case '\r': putc('\r',stdout);
	putc('\n',stdout);
	if(tmp[0] == '\0') 
	{
		printf("ikigezu>");
	} 
	   else
		   {
			   if(!strcmp(tmp,"exit")||!strcmp(tmp,"quit"))
			   {
				   cexit();
			   }
				memset(history,'\0', BUFFER);
				strncpy(history,tmp,BUFFER);
				decoupe(tmp);
				if(strcmp(argument[0],"alton"))
				{
				execute(argument);
				}
				else
				{
					alton();
				}
				printf("ikigezu>");
			}
				   
				   memset(tmp,'\0', BUFFER);
		break;
	case EOF:cexit();
		break;
	case 3:memset(tmp,'\0', BUFFER);
		printf("\r\ndefqon1#");
		break; 
	case 4:cexit();
		break;
	case 8:
		tmp[strlen(tmp)-1]='\0';
		printf("\033[1D");
		putc(' ',stdout);
		printf("\033[1D");
		break;
	case 127:
		tmp[strlen(tmp)-1]='\0';
		printf("\033[1D");
		putc(' ',stdout);
		printf("\033[1D");
		break;
	case 27:c=getchar();
		if (c=='[')
		{
			c=getchar();
			switch(c){
				case 'A': strncpy(tmp,history,BUFFER);
				printf("\x0d");
				printf("\033[K");
				printf("ikigezu>%s",tmp);
				break;
				}
		}
		break;
	default:
		strncat(tmp, &c, 1);
		putc(c,stdout);
		break;
	}
	}
	return 0;
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

void cexit(void)
{
	
	mode_raw(0);
	putc('\n',stdout);
	exit(0);
}

void execute(char **argument)
{
  pid_t pid;

  pid = fork();
  if (pid < 0) {
    printf("fork a échoué (%s)\r\n",strerror(errno));
    return;
  }
mode_raw(0);
  if (pid==0) {
    /* fils */
	execvp(argument[0],argument);
    /* on n'arrive ici que si le exec a échoué */
    printf("impossible d'éxecuter \"%s\" (%s)\r\n",argument[0],strerror(errno));
    exit(1);
  }
  else {
    /* père */
    attent(pid);
  }
  mode_raw(1);
}

void decoupe(char *input)
{
char* carac=input;
int i;
for (i=0; i<MAXELEMS-1; i++) {
	    if (!*carac) break;
argument[i]=carac;
while(*carac && *carac!=' ') carac++;
if (*carac){
	*carac='\0';
	carac++;

}
}
argument[i]=NULL;
}
/* attent la fin du processus pid */
void attent(pid_t pid)
{
  /* il faut boucler car waitpid peut retourner avec une erreur non fatale */
  while (1) {
    int status;
    int r = waitpid(pid,&status,0); /* attente bloquante */
    if (r<0) { 
      if (errno==EINTR) continue; /* interrompu => on recommence à attendre */
      printf("erreur de waitpid (%s)\r\n",strerror(errno));
      break;
    }
    if (WIFSIGNALED(status))
      printf("terminaison par signal %i \r\n",WTERMSIG(status));
    break;
  }
}
void init()
{
	mode_raw(1);
	memset(tmp,'\0', BUFFER);
	memset(history,'\0', BUFFER);
	printf("ikigezu>");
}
void alton()
{
	char *cmd=argument[1];
	if(!strcmp(cmd,"malentoff"))
	{
		malentoff();
	}
	if(!strcmp(cmd,"grandiossa"))
	{
		grandiossa();
	}
		
}

void malentoff()
{
	printf("mallentoff \r\n");
}

void grandiossa()
{
	printf("grandiossa \r\n");	
}
