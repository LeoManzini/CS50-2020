#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>

int main(int argc, string argv[])
{
    //input treatment
    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
    else if (isalpha(*argv[1]))
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
    else
    {
        int x = strlen(argv[1]);
        for (int i = 0; i < x; i++)
        {
            if (isalpha(argv[1][i]))
            {
                printf("Usage: ./caesar key\n");
                return 1;
            }
        }
    }

    //data input
    int n = atoi(argv[1]);
    string plaintext = get_string("Plaintext: ");
    int counter = strlen(plaintext);

    //data processing
    for (int i = 0; i < counter; i++)
    {
        if (isalpha(plaintext[i]) && isupper(plaintext[i]))
        {
            int ciperChar = plaintext[i] + n;

            if (ciperChar > 90)
            {
                int rest = ciperChar - 90;
                char letter = rest + 64;
                plaintext[i] = letter;
            }
            else
            {
                plaintext[i] = ciperChar;
            }
        }
        else if (isalpha(plaintext[i]) && islower(plaintext[i]))
        {
            int ciperChar = plaintext[i] + n;

            if (ciperChar > 122)
            {
                int rest = ciperChar - 122;
                char letter = rest + 96;
                plaintext[i] = letter;
            }
            else
            {
                plaintext[i] = ciperChar;
            }
        }
    }

    //data output
    printf("ciphertext: %s\n", plaintext);
}
