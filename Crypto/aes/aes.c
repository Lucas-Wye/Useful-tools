/*
 * @Author: Lucas Wye
 * @Date: 2019-05-16 14:05:35
 * @Description: aes
 */
/*
   ./aes 00112233445566778899aabbccddeeff 000102030405060708090a0b0c0d0e0f
*/

#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define LENGTH 16
#define CHAR_ERR 1

// 加密解密
#define ENC 0
#define DEC 1

// 打印or不打印
#define PRINT 1
#define NOPRINT 0

// S box
unsigned char S_box[16][16] = {
    // 0     1     2     3     4     5     6     7     8     9     a     b     c     d     e     f
    0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76, // 0
    0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0, // 1
    0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15, // 2
    0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75, // 3
    0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84, // 4
    0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf, // 5
    0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8, // 6
    0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2, // 7
    0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73, // 8
    0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb, // 9
    0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79, // a
    0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08, // b
    0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a, // c
    0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e, // d
    0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf, // e
    0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16  // f
};

// S inv_box
unsigned char S_inv_box[16][16] = {
    // 0     1     2     3     4     5     6     7     8     9     a     b     c     d     e     f
    0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38, 0xbf, 0x40, 0xa3, 0x9e, 0x81, 0xf3, 0xd7, 0xfb, // 0
    0x7c, 0xe3, 0x39, 0x82, 0x9b, 0x2f, 0xff, 0x87, 0x34, 0x8e, 0x43, 0x44, 0xc4, 0xde, 0xe9, 0xcb, // 1
    0x54, 0x7b, 0x94, 0x32, 0xa6, 0xc2, 0x23, 0x3d, 0xee, 0x4c, 0x95, 0x0b, 0x42, 0xfa, 0xc3, 0x4e, // 2
    0x08, 0x2e, 0xa1, 0x66, 0x28, 0xd9, 0x24, 0xb2, 0x76, 0x5b, 0xa2, 0x49, 0x6d, 0x8b, 0xd1, 0x25, // 3
    0x72, 0xf8, 0xf6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xd4, 0xa4, 0x5c, 0xcc, 0x5d, 0x65, 0xb6, 0x92, // 4
    0x6c, 0x70, 0x48, 0x50, 0xfd, 0xed, 0xb9, 0xda, 0x5e, 0x15, 0x46, 0x57, 0xa7, 0x8d, 0x9d, 0x84, // 5
    0x90, 0xd8, 0xab, 0x00, 0x8c, 0xbc, 0xd3, 0x0a, 0xf7, 0xe4, 0x58, 0x05, 0xb8, 0xb3, 0x45, 0x06, // 6
    0xd0, 0x2c, 0x1e, 0x8f, 0xca, 0x3f, 0x0f, 0x02, 0xc1, 0xaf, 0xbd, 0x03, 0x01, 0x13, 0x8a, 0x6b, // 7
    0x3a, 0x91, 0x11, 0x41, 0x4f, 0x67, 0xdc, 0xea, 0x97, 0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6, 0x73, // 8
    0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0x85, 0xe2, 0xf9, 0x37, 0xe8, 0x1c, 0x75, 0xdf, 0x6e, // 9
    0x47, 0xf1, 0x1a, 0x71, 0x1d, 0x29, 0xc5, 0x89, 0x6f, 0xb7, 0x62, 0x0e, 0xaa, 0x18, 0xbe, 0x1b, // a
    0xfc, 0x56, 0x3e, 0x4b, 0xc6, 0xd2, 0x79, 0x20, 0x9a, 0xdb, 0xc0, 0xfe, 0x78, 0xcd, 0x5a, 0xf4, // b
    0x1f, 0xdd, 0xa8, 0x33, 0x88, 0x07, 0xc7, 0x31, 0xb1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xec, 0x5f, // c
    0x60, 0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d, 0x2d, 0xe5, 0x7a, 0x9f, 0x93, 0xc9, 0x9c, 0xef, // d
    0xa0, 0xe0, 0x3b, 0x4d, 0xae, 0x2a, 0xf5, 0xb0, 0xc8, 0xeb, 0xbb, 0x3c, 0x83, 0x53, 0x99, 0x61, // e
    0x17, 0x2b, 0x04, 0x7e, 0xba, 0x77, 0xd6, 0x26, 0xe1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0c, 0x7d  // f
};

// Mix_columns
unsigned char Mix_Mul[4][4] = {
    0x02, 0x03, 0x01, 0x01,
    0x01, 0x02, 0x03, 0x01,
    0x01, 0x01, 0x02, 0x03,
    0x03, 0x01, 0x01, 0x02};

// Mix_inv_columns
unsigned char Mix_inv_Mul[4][4] = {
    0x0e, 0x0b, 0x0d, 0x09,
    0x09, 0x0e, 0x0b, 0x0d,
    0x0d, 0x09, 0x0e, 0x0b,
    0x0b, 0x0d, 0x09, 0x0e};

// RC
unsigned char RC[10] = {
    0x01, 0x02, 0x04, 0x08, 0x10,
    0x20, 0x40, 0x80, 0x1b, 0x36};

// 将字符转换为16进制数字
int Characters_Process(char *string);

// 轮密相加
void Add_Round_Key(unsigned char *state, unsigned char *round_key);

// 字节代替变换
void Substitute_Bytes(unsigned char *state, int type);

// 行移位
void Shift_Rows(unsigned char *state, int type);

// 乘法实现
unsigned char Mul(unsigned char cons, unsigned char num);

// 列混淆
void Mix_Columns(unsigned char *state, int type);

// 用于输出中间结果
void Print(unsigned char *input);

// 轮密产生
void Key_Expansion(unsigned char *Key, int Round_Num);

// 加密函数
void AES_Encryption(unsigned char *Plaintxt, unsigned char *Key, unsigned char all_key[11][LENGTH], int type);

// 解密
void AES_Decryption(unsigned char *Plaintxt, unsigned char *Key, unsigned char all_key[11][LENGTH]);

int main(int argc, char *argv[])
{
  // 对输入做检验
  if (argc < 3)
  {
    fprintf(stderr, "Usage:   %s  Plaintxt  Key\n", argv[0]);
    fprintf(stderr, "Example: %s  00112233445566778899aabbccddeeff 000102030405060708090a0b0c0d0e0f\n", argv[0]);
    return 1;
  }
  if (strlen(argv[1]) != 2 * LENGTH)
  {
    fprintf(stderr, "No enough length of Plaintxt!\n");
    return 1;
  }
  if (strlen(argv[2]) != 2 * LENGTH)
  {
    fprintf(stderr, "No enough length of Key!\n");
    return 1;
  }
  if (Characters_Process(argv[1]) != 0)
  {
    fprintf(stderr, "Invalid characters found in Plaintxt!\n");
    return 1;
  }
  if (Characters_Process(argv[2]) != 0)
  {
    fprintf(stderr, "Invalid characters found in Key!\n");
    return 1;
  }

  // 128bits明文，采用8bits的unsigned char类型
  unsigned char Plaintxt[LENGTH];
  // 128bits密钥
  unsigned char Key[LENGTH];
  int i, j;

  printf("\n------------------------------------------------\n");
  // 赋值给明文
  for (i = 0; i < LENGTH; i++)
  {
    Plaintxt[i] = argv[1][2 * i] * 16 + argv[1][2 * i + 1];
  }
  printf("The input Plaintxt is:\n");
  Print(Plaintxt);

  // 赋值给密钥
  for (i = 0; i < LENGTH; i++)
  {
    Key[i] = argv[2][2 * i] * 16 + argv[2][2 * i + 1];
  }
  printf("The input Key is:\n");
  Print(Key);

  // 所有密钥集合
  unsigned char all_key[11][LENGTH];
  for (i = 0; i < LENGTH; i++)
  {
    all_key[0][i] = Key[i];
  }

  // 加密
  AES_Encryption(Plaintxt, Key, all_key, PRINT);

  // 解密
  AES_Decryption(Plaintxt, Key, all_key);

  // OFB
  // 时变值
  unsigned char IV[LENGTH] = {
      0x08, 0x07, 0x06, 0x05,
      0x04, 0x03, 0x02, 0x01,
      0x00, 0x99, 0xaa, 0xbb,
      0xcc, 0xdd, 0xee, 0xff};
  // 密钥
  Key[0] = 0x00;
  Key[1] = 0x01;
  Key[2] = 0x02;
  Key[3] = 0x03;
  Key[4] = 0x04;
  Key[5] = 0x05;
  Key[6] = 0x06;
  Key[7] = 0x07;
  Key[8] = 0x08;
  Key[9] = 0x09;
  Key[10] = 0x0a;
  Key[11] = 0x0b;
  Key[12] = 0x0c;
  Key[13] = 0x0d;
  Key[14] = 0x0e;
  Key[15] = 0x0f;

  // 保存Key的值
  for (i = 0; i < LENGTH; i++)
  {
    all_key[0][i] = Key[i];
  }

  // 需要加密的消息
  unsigned char message[] = "AES became effective as a federal government standard after approval by the Secretary of Commerce. It is the first publicly accessible cipher approved by the National Security Agency for top secret information.";
  int len = sizeof(message) / sizeof(unsigned char);
  // 加密次数
  int enc_time = len / 16 + 1;
  // 加密结果
  unsigned char *cipher = (unsigned char *)malloc(sizeof(unsigned char) * len);
  // 加密过程
  for (j = 0; j < enc_time; j++)
  {
    // 此处生成的all_key直接丢弃即可
    AES_Encryption(IV, Key, all_key, NOPRINT);

    if (j != (enc_time - 1))
    {
      for (i = 0; i < LENGTH; i++)
      {
        // 恢复Key的值
        Key[i] = all_key[0][i];
        // 做一次异或
        cipher[j * LENGTH + i] = message[j * LENGTH + i] ^ IV[i];
      }
    }
    // 最后一次加密时，取有效位做异或
    else
    {
      for (i = 0; i < (len - j * LENGTH); i++)
      {
        // 做一次异或
        cipher[j * LENGTH + i] = message[j * LENGTH + i] ^ IV[i];
      }
    }
  }
  // 输出结果
  printf("\n\n\n------------------------------------------------\n");
  printf("OFB\n");
  printf("The input message is:\n%s\n\n", message);
  printf("The length of input message is %d\n\n", len);
  printf("The output cipher is:\n");
  for (i = 0; i < len; i++)
  {
    printf("%3.2x", cipher[i]);
  }
  printf("\n");

  return 0;
}

// 将字符转换为16进制数字
int Characters_Process(char *string)
{
  int i;
  for (i = 0; i < 2 * LENGTH; i++)
  {
    if (string[i] >= '0' && string[i] <= '9')
    {
      string[i] = string[i] - '0';
    }
    else if (string[i] >= 'a' && string[i] <= 'f')
    {
      string[i] = string[i] - 'a' + 10;
    }
    else if (string[i] >= 'A' && string[i] <= 'F')
    {
      string[i] = string[i] - 'A' + 10;
    }
    else
    {
      return CHAR_ERR;
    }
  }
  return 0;
}

// 轮密相加
void Add_Round_Key(unsigned char *state, unsigned char *round_key)
{
  int i;
  for (i = 0; i < LENGTH; i++)
  {
    // GP(2^8)加法为异或
    state[i] = state[i] ^ round_key[i];
  }
}

// 字节代替变换
void Substitute_Bytes(unsigned char *state, int type)
{
  int i;
  // 加密
  if (type == ENC)
  {
    for (i = 0; i < LENGTH; i++)
    {
      // 高位选择行，低位选择列
      state[i] = S_box[state[i] / 16][state[i] % 16];
    }
  }
  // 解密
  else
  {
    for (i = 0; i < LENGTH; i++)
    {
      state[i] = S_inv_box[state[i] / 16][state[i] % 16];
    }
  }
}

// 行移位
void Shift_Rows(unsigned char *state, int type)
{
  int i, j;
  int shift = 1;
  unsigned char temp[4];

  if (type == ENC)
  {
    for (i = 1; i < 4; i++)
    {
      for (j = 0; j < 4; j++)
      {
        temp[j] = state[i + j * 4];
      }

      for (j = 0; j < 4; j++)
      {
        // 左移shift位
        state[i + j * 4] = temp[(j + shift) % 4];
      }
      shift++;
    }
  }
  else
  {
    for (i = 1; i < 4; i++)
    {
      for (j = 0; j < 4; j++)
      {
        temp[j] = state[i + j * 4];
      }

      for (j = 0; j < 4; j++)
      {
        //右移shift位
        state[i + j * 4] = temp[(j - shift + 4) % 4];
      }
      shift++;
    }
  }
}

// 乘法实现
unsigned char Mul(unsigned char cons, unsigned char num)
{
  // for encryption
  if (cons == 0x01)
  {
    return num;
  }
  else if (cons == 0x02)
  {
    if (num < 128)
      return num << 1;
    else
      return (num << 1) ^ 0b00011011;
  }
  else if (cons == 0x03)
  {
    return Mul(2, num) ^ num;
  }

  // for decryption
  else if (cons == 0x0e)
  {                                 //0b1110
    unsigned char t1 = Mul(2, num); // *2
    unsigned char t2 = Mul(2, t1);  // *4
    unsigned char t3 = Mul(2, t2);  // *8
    return t1 ^ t2 ^ t3;            // 2+4+8
  }
  else if (cons == 0x0b)
  {                                 //0b1011
    unsigned char t1 = Mul(2, num); // *2
    unsigned char t2 = Mul(2, t1);  // *4
    unsigned char t3 = Mul(2, t2);  // *8
    return num ^ t1 ^ t3;           // 1+2+8
  }
  else if (cons == 0x0d)
  {                                 //0b1101
    unsigned char t1 = Mul(2, num); // *2
    unsigned char t2 = Mul(2, t1);  // *4
    unsigned char t3 = Mul(2, t2);  // *8
    return num ^ t2 ^ t3;           // 1+4+8
  }
  else if (cons == 0x09)
  {                                 //0b1001
    unsigned char t1 = Mul(2, num); // *2
    unsigned char t2 = Mul(2, t1);  // *4
    unsigned char t3 = Mul(2, t2);  // *8
    return num ^ t3;                // 1+8
  }
  return 0;
}

// 列混淆
void Mix_Columns(unsigned char *state, int type)
{
  int i, j;
  unsigned char temp[4][4] = {0};
  // 加密
  if (type == ENC)
  {
    for (i = 0; i < 4; i++)
    {
      for (j = 0; j < 4; j++)
      {
        temp[i][j] =
            Mul(Mix_Mul[i][0], state[0 + j * 4]) ^ Mul(Mix_Mul[i][1], state[1 + j * 4]) ^ Mul(Mix_Mul[i][2], state[2 + j * 4]) ^ Mul(Mix_Mul[i][3], state[3 + j * 4]);
      }
    }

    for (i = 0; i < 4; i++)
    {
      for (j = 0; j < 4; j++)
      {
        state[i + j * 4] = temp[i][j];
      }
    }
  }
  // 解密
  else
  {
    for (i = 0; i < 4; i++)
    {
      for (j = 0; j < 4; j++)
      {
        temp[i][j] =
            Mul(Mix_inv_Mul[i][0], state[0 + j * 4]) ^ Mul(Mix_inv_Mul[i][1], state[1 + j * 4]) ^ Mul(Mix_inv_Mul[i][2], state[2 + j * 4]) ^ Mul(Mix_inv_Mul[i][3], state[3 + j * 4]);
      }
    }

    for (i = 0; i < 4; i++)
    {
      for (j = 0; j < 4; j++)
      {
        state[i + j * 4] = temp[i][j];
      }
    }
  }
}

// 用于输出中间结果
void Print(unsigned char *input)
{
  int i;
  for (i = 0; i < LENGTH; i++)
  {
    printf("%3.2x", input[i]);
  }
  printf("\n");
}

// 轮密产生
void Key_Expansion(unsigned char *Key, int Round_Num)
{
  unsigned char temp[4];
  int i, j;

  //字循环
  for (i = LENGTH - 3; i < LENGTH; i++)
  {
    temp[i - LENGTH + 3] = Key[i];
  }
  temp[3] = Key[LENGTH - 4];

  // 字代替
  for (i = 0; i < 4; i++)
  {
    temp[i] = S_box[temp[i] / 16][temp[i] % 16];
  }

  // 字异或
  temp[0] = temp[0] ^ RC[Round_Num];

  // 轮密钥求解
  for (i = 0; i < 4; i++)
  {
    Key[i] = Key[i] ^ temp[i];
  }
  for (i = 4; i < LENGTH; i++)
  {
    Key[i] = Key[i] ^ Key[i - 4];
  }
}

// 加密函数
void AES_Encryption(unsigned char *Plaintxt, unsigned char *Key, unsigned char all_key[11][LENGTH], int type)
{
  int i, j;
  if (type == PRINT)
  {
    printf("\n\n\n------------------------------------------------\n");
    printf("Encryption\n");
  }
  // 1. 初始变换: 轮密相加，直接将Key与Plaintxt相加
  Add_Round_Key(Plaintxt, Key);
  // printf("The add round key result is:\n");
  // Print(Plaintxt);

  // 2. 10轮加密
  for (i = 0; i < 9; i++)
  {

    // 字节代替
    Substitute_Bytes(Plaintxt, ENC);
    // printf("The substitute bytes result is:\n");
    // Print(Plaintxt);

    // 行移位
    Shift_Rows(Plaintxt, ENC);
    // printf("The shift rows result is:\n");
    // Print(Plaintxt);

    // 列混淆
    Mix_Columns(Plaintxt, ENC);
    // printf("The mix columns result is:\n");
    // Print(Plaintxt);

    // 轮密产生
    Key_Expansion(Key, i);
    // printf("The round key is:\n");
    // Print(Key);

    // 轮密相加
    Add_Round_Key(Plaintxt, Key);
    // printf("The round result is:\n");
    // Print(Plaintxt);

    if (type == PRINT)
    {
      printf("Round[%d]\n", i + 1);
      printf("The round result is:\n");
      Print(Plaintxt);
      printf("\n");
    }

    // 保存密钥
    for (j = 0; j < LENGTH; j++)
    {
      all_key[i + 1][j] = Key[j];
    }
  }

  // 字节代替
  Substitute_Bytes(Plaintxt, ENC);
  // printf("The substitute bytes result is:\n");
  // Print(Plaintxt);

  // 行移位
  Shift_Rows(Plaintxt, ENC);
  // printf("The shift rows result is:\n");
  // Print(Plaintxt);

  // 轮密产生
  Key_Expansion(Key, 9);
  // printf("The round key is:\n");
  // Print(Key);

  // 轮密相加
  Add_Round_Key(Plaintxt, Key);
  // printf("The round result is:\n");
  // Print(Plaintxt);

  if (type == PRINT)
  {
    printf("Round[10]\n");
    printf("The round result is:\n");
    Print(Plaintxt);
  }

  // 保存密钥
  for (j = 0; j < LENGTH; j++)
  {
    all_key[10][j] = Key[j];
  }

  if (type == PRINT)
  {
    // 输出加密结果
    printf("\n------------------------------------------------\n");
    printf("The Final Encryption Result Is:\n");
    Print(Plaintxt);
    printf("\n");
  }
}

// 解密
void AES_Decryption(unsigned char *Plaintxt, unsigned char *Key, unsigned char all_key[11][LENGTH])
{
  printf("\n\n\n------------------------------------------------\n");
  printf("Decryption\n");
  int i, j;
  // 1. 初始变换: 轮密相加，直接将Key与Plaintxt相加
  // 轮密相加
  Add_Round_Key(Plaintxt, all_key[10]);
  // printf("The round result is:\n");
  // Print(Plaintxt);

  // 2. 10轮解密
  for (i = 9; i > 0; i--)
  {

    printf("Round[%d]\n", 10 - i);

    // 逆向行移位
    Shift_Rows(Plaintxt, DEC);
    // printf("The inv-shift rows result is:\n");
    // Print(Plaintxt);

    // 逆向字节代替
    Substitute_Bytes(Plaintxt, DEC);
    // printf("The inv-substitute bytes result is:\n");
    // Print(Plaintxt);

    // 轮密相加
    Add_Round_Key(Plaintxt, all_key[i]);
    // printf("The round result is:\n");
    // Print(Plaintxt);

    // 列混淆
    Mix_Columns(Plaintxt, DEC);
    // printf("The inv-mix columns result is:\n");
    // Print(Plaintxt);

    printf("The round result is:\n");
    Print(Plaintxt);

    printf("\n");
  }

  printf("Round[%d]\n", 10 - i);
  // 逆向行移位
  Shift_Rows(Plaintxt, DEC);
  // printf("The inv-shift rows result is:\n");
  // Print(Plaintxt);

  // 逆向字节代替
  Substitute_Bytes(Plaintxt, DEC);
  // printf("The inv-substitute bytes result is:\n");
  // Print(Plaintxt);

  // 轮密相加
  Add_Round_Key(Plaintxt, all_key[i]);
  // printf("The round result is:\n");
  // Print(Plaintxt);

  printf("The round result is:\n");
  Print(Plaintxt);

  // 输出解密结果
  printf("\n------------------------------------------------\n");
  printf("The Final Decryption Result Is:\n");
  Print(Plaintxt);
  printf("\n");
}
