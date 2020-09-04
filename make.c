#include <stdio.h>
#include <stdlib.h>
int main()
{
	printf("\n Mode : "); int mode; scanf("%d",&mode);

	if(mode==1){
		system("cc -Wall -o3 file1.c file2.c -o bin_file_name");
	}
	else if(mode==2){
		system("cc -Wall -Wextra -pedantic file1.c file2.c -o bin_file_name");
	}
	else if(mode==3){
		system("cc -Wall -Wextra -pedantic -Wconversion -o0 file1.c file2.c -o bin_file_name");
	}
	return 0;
}