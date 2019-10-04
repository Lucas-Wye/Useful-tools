/*
 * @Author: Lucas Wye
 * @Date: 2019-05-21 14:05:35
 * @Description: encrytion and decryption with rc4
 */

#include <stdio.h>
#include <string.h>

#define MAX 256
#define swap(a, b) \
  {                \
    short t;       \
    t = a;         \
    a = b;         \
    b = a;         \
  }

void rc4_init(unsigned char *S, unsigned char *key, unsigned long key_len)
{
  short i;
  short j = 0;
  unsigned char T[MAX] = {0};

  //(1)Initialization
  for (i = 0; i < MAX; i++)
  {
    S[i] = i;
    T[i] = key[i % key_len];
  }

  //(2)Permutation of S
  for (i = 0; i < MAX; i++)
  {
    j = (j + S[i] + T[i]) % MAX;
    swap(S[i], S[j]);
  }
}

// use for both encryption and decryption
void rc4_crypto(unsigned char *S, unsigned char *data, unsigned long data_len)
{
  short i = 0;
  short j = 0;
  unsigned long k = 0;
  for (k = 0; k < data_len; k++)
  {
    i = (i + 1) % MAX;
    j = (j + S[i]) % MAX;
    swap(S[i], S[j]);
    data[k] ^= S[(S[i] + S[j]) % MAX];
  }
}

int main(void)
{
  unsigned char s1[MAX] = {0};
  unsigned char s2[MAX] = {0};
  char key[MAX] = {0};
  char data[2 * MAX] = {0};

  printf("Please input the key:\n");
  scanf("%s", key);

  printf("Please input the data:\n");
  scanf("%s", data);
  unsigned long len = strlen(data);

  rc4_init(s1, (unsigned char *)key, strlen(key));

  // backup for S box
  for (short i = 0; i < MAX; i++)
  {
    s2[i] = s1[i];
  }

  // encryption
  rc4_crypto(s1, (unsigned char *)data, len);
  printf("Encryption result: %s\n", data);
  // for(short i = 0;i<len;i++){
  // 	printf("%d\n",data[i] );
  // }

  // decryption
  rc4_crypto(s2, (unsigned char *)data, len);
  printf("Decryption result: %s\n", data);

  return 0;
}
