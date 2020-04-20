#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int height;
    do
    {
        height = get_int("Type the height of the pyramid: ");
    }
    while (height <= 0 || height > 8);

    int counter = height - 1;

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < height; j++)
        {
            if (j >= counter)
            {
                printf("#");
            }
            else
            {
                printf(" ");
            }
        }
        counter--;
        printf("\n");
    }
}
