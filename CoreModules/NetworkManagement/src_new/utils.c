#include <stdio.h>
#include <stdlib.h>

void stop(char *message)
{
    char buffer[500];
    sprintf(buffer, "\033[1;31m%s\033[1;0m", message);
    perror(buffer);
    exit(EXIT_FAILURE);
}

void printNHex(int n, void *content)
{
    unsigned char *p = (unsigned char *)content;
    for (size_t i = 0; i < n; i++)
    {
        printf("\\x%02x", *(p + i));
        if ((i + 1) % 4 == 0)
        {
            printf("\n");
        }
    }
    printf("\n");
}

void formatIPAddress(char address[15], unsigned int intAddress)
{
    sprintf(address, "%d.%d.%d.%d", intAddress >> 0 & 0xFF, intAddress >> 8 & 0xFF, intAddress >> 16 & 0xFF, intAddress >> 24 & 0xFF);
}