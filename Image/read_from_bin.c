/*
 * @Author: Lucas Wye
 * @Date: 2019-03-24 14:05:35
 * @Description: this code is used to read the RGBA data from a binary file  
 */

#include<stdio.h>
#include <stdlib.h>
#define ROW 1028// h + 4
#define COL 2052// w + 4

int main(int argc,char * argv[]){
  
  if(argc != 2)
  {
    fprintf(stderr, "Usage: ./read_from_bin infile\n");
    return 1;
  }

  // input                                  
  double ***input;
  int i,j;
  input = (double***)malloc(4 * sizeof(double**));
  input[0] = (double**)malloc(ROW * sizeof(double*));
  input[1] = (double**)malloc(ROW * sizeof(double*));
  input[2] = (double**)malloc(ROW * sizeof(double*));
  input[3] = (double**)malloc(ROW * sizeof(double*));
  for(i=0;i<ROW;i++){
  	input[0][i] = (double*)calloc(COL,sizeof(double));
  	input[1][i] = (double*)calloc(COL,sizeof(double));
  	input[2][i] = (double*)calloc(COL,sizeof(double));
    input[3][i] = (double*)calloc(COL,sizeof(double));
  }

  FILE *infile;
  infile = fopen(argv[1],"rb");

  int w,h;
  int temp;
  fread(&w,sizeof(int),1,infile);
  fread(&h,sizeof(int),1,infile);
  
  printf("%d %d\n", w,h);



  for(i=2;i<(ROW-2);i++){
  	for(j=2;j<(COL-2);j++){
  		fread(&temp,sizeof(int),1,infile); 
  		input[0][i][j] = temp;
  		fread(&temp,sizeof(int),1,infile); 
  		input[1][i][j] = temp;
  		fread(&temp,sizeof(int),1,infile); 
  		input[2][i][j] = temp;
  		fread(&temp,sizeof(int),1,infile); 
        input[3][i][j] = temp;
        printf("%lf,%lf,%lf,%lf\n",input[0][i][j],input[1][i][j],input[2][i][j],input[3][i][j] );
  	}
  }
}
