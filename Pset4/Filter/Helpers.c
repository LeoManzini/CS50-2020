#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int gray = round((image[i][j].rgbtBlue + image[i][j].rgbtGreen + image[i][j].rgbtRed) / 3.0);
            image[i][j].rgbtBlue = gray;
            image[i][j].rgbtGreen = gray;
            image[i][j].rgbtRed = gray;
        }
    }
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int sred = round((0.393 * (image[i][j].rgbtRed)) + (0.769 * (image[i][j].rgbtGreen)) + (0.189 * (image[i][j].rgbtBlue)));
            int sgreen = round((0.349 * (image[i][j].rgbtRed)) + (0.686 * (image[i][j].rgbtGreen)) + (0.168 * (image[i][j].rgbtBlue)));
            int sblue = round((0.272 * (image[i][j].rgbtRed)) + (0.534 * (image[i][j].rgbtGreen)) + (0.131 * (image[i][j].rgbtBlue)));

            image[i][j].rgbtRed = sred;
            image[i][j].rgbtGreen = sgreen;
            image[i][j].rgbtBlue = sblue;

            if (sred > 255)
            {
                sred = 255;
                image[i][j].rgbtRed = sred;
            }
            if (sgreen > 255)
            {
                sgreen = 255;
                image[i][j].rgbtGreen = sgreen;
            }
            if (sblue > 255)
            {
                sblue = 255;
                image[i][j].rgbtBlue = sblue;
            }
        }
    }
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        int final = width - 1;

        for (int j = 0; j < width; j++)
        {
            if (j < final)
            {
                RGBTRIPLE aux = image[i][j];
                image[i][j] = image[i][final];
                image[i][final] = aux;
                final--;
            }
        }
    }
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    int sblue;
    int sgreen;
    int sred;
    float counter;

    RGBTRIPLE temp[height][width];

    for (int i = 0; i < width; i++)
    {
        for (int j = 0; j < height; j++)
        {
            sblue = 0;
            sgreen = 0;
            sred = 0;
            counter = 0.00;

            for (int k = -1; k < 2; k++)
            {
                if (j + k < 0 || j + k > height - 1)
                {
                    continue;
                }

                for (int h = -1; h < 2; h++)
                {
                    if (i + h < 0 || i + h > width - 1)
                    {
                        continue;
                    }

                    sblue += image[j + k][i + h].rgbtBlue;
                    sgreen += image[j + k][i + h].rgbtGreen;
                    sred += image[j + k][i + h].rgbtRed;
                    counter++;
                }
            }

            // averages the sum to make picture look blurrier
            temp[j][i].rgbtBlue = round(sblue / counter);
            temp[j][i].rgbtGreen = round(sgreen / counter);
            temp[j][i].rgbtRed = round(sred / counter);
        }
    }

    for (int i = 0; i < width; i++)
    {
        for (int j = 0; j < height; j++)
        {
            image[j][i].rgbtBlue = temp[j][i].rgbtBlue;
            image[j][i].rgbtGreen = temp[j][i].rgbtGreen;
            image[j][i].rgbtRed = temp[j][i].rgbtRed;
        }
    }
}
