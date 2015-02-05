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
void unix_clear_screen(void);
void attent(pid_t pid);
void execute(char *nom,char *argument);

int main()
{
	mode_raw(1);
	char c;
	char history[BUFFER];
	char tmp[BUFFER];
	memset(tmp,'\0', 100);
	printf("ikigezu>");
	while(c != EOF) {
		mode_raw(1);
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
					   /*printf("\r\nbuffer='%s'\r\n",tmp);*/
					   verifPath(tmp);
					   
					    printf("ikigezu>");
				   }
				   memset(history,'\0', 100);
				   strncpy(history,tmp,100);
				   memset(tmp,'\0', 100);
	break;
	case EOF:cexit();
	break;
	case 3:memset(tmp,'\0', 100);
	printf("\r\ndefqon1#");
	break; 
	case 4:cexit();
	break;
	case 8:
	tmp[strlen(tmp)-1]='\0';
	printf("\033[1D");
	putc(' ',stdout);
	printf("\033[1D");
	case 127:
	tmp[strlen(tmp)-1]='\0';
	printf("\033[1D");
	putc(' ',stdout);
	printf("\033[1D");
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
	default:strncat(tmp, &c, 1);
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

int verifPath(char input[])
{

char *fichier;
char *argument;
char commande[BUFFER];
strcpy(commande,input);
fichier=strtok(commande," ");
argument=strtok(NULL,"\0");
execute(fichier,argument);
return 0;
}


void cexit(void)
{
	
	mode_raw(0);
	putc('\n',stdout);
	exit(0);
}

void execute(char *nom,char *argument)
{
  pid_t pid;
  char *arguments[] = { nom,argument, NULL };

  pid = fork();
  if (pid < 0) {
    printf("fork a échoué (%s)\r\n",strerror(errno));
    return;
  }
mode_raw(0);
  if (pid==0) {
    /* fils */
	printf("valeur de nom :'%s',\r\nvaleur de argument:'%s'\r\n",nom,argument);
   
	execvp(nom,arguments);

    /* on n'arrive ici que si le exec a échoué */
    printf("impossible d'éxecuter \"%s\" (%s)\r\n",nom,strerror(errno));
    exit(1);
  }
  else {
    /* père */
    attent(pid);
  }
  mode_raw(1);
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
