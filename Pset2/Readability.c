#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

int main(void)
{
    //Data input
    string text = get_string("Text: ");
    int n = strlen(text); //n é o tamanho da string, pois assim não precisa ficar perguntando o tamanho toda vez que correr o for
    int i, j; //declarados aqui porque dentro do laço dá erro
    float letters = 0; //letters word and sentences are float cause if they are int de operations give another numbers
    float words = 0;
    float sentences = 0;
    float index = 0;
    float l;
    float s;

    //Data process
    for (i = 0; i < n; i++)
    {
        if (isalpha(text[i])) //se a posição atual da string for uma letra, is alpha vem da lib ctype
        {
            letters++;
            if (text[i + 1] == ' ' || text[i + 1] == ',' || text[i + 1] == '\0' || text[i + 1] == ';' || text[i + 1] == '?'
                || text[i + 1] == '!' || text[i + 1] == '.') //se o caracter depois de uma letra for algum desses, incrementa um em palavra
            {
                words++;
            }
        }
        else if (text[i] == '.' || text[i] == '!' || text[i] == '?') //se na posição atual do vetor, tiver algum desses caracteres, sentença é incrementado
        {
            sentences++;
        }
    }

    l = (letters / words) * 100; //l é a media de letras por palavras vezes 100
    s = (sentences / words) * 100; //s é a media de sentenças por palavras vezes 100
    index = 0.0588 * l - 0.296 * s - 15.8;
    index = round(index);

    //Data output
    if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (index >= 1 && index < 16)
    {
        printf("Grade %.0f\n", index);
    }
    else
    {
        printf("Grade 16+\n");
    }
}
