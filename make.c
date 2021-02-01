#include <stdio.h>
#include <stdlib.h>

int main(int frequency, char * arguments[])
{
	if(frequency >= 2)
	{
		int mode = strtol(arguments[1],NULL,10);
		
		if(mode==1)
		{
			system("cc -Wall -o3 file1.c file2.c -o binary_filename");
		}
		
		else if(mode==2)
		{
			system("cc -Wall -Wextra -pedantic file1.c file2.c -o binary_filename");
		}
		
		else if(mode==3)
		{
			system("cc -Wall -Wextra -pedantic -Wconversion -o0 file1.c file2.c -o binary_filename");
		}
	}
	else
	{
		printf("Not enough arguments.\n");
	}
	
	return 0;
}
