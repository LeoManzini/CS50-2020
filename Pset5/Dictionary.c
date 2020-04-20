// Implements a dictionary's functionality

#include <stdbool.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include <stdlib.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
const unsigned int N = 1;

// Hash table
node *table[N];
unsigned int totalWords = 0;

// Returns true if word is in dictionary else false
bool check(const char *word)
{
   // creates an aux string to receive the lower word
    char aux[LENGTH + 1];
    int len = strlen(word);
    for(int i = 0; i < len; i++)
    {
        aux[i] = tolower(word[i]);
    }

    aux[len] = '\0'; //define his end

    // find what position of the array the word should be in
    int position = hash(aux);

    // if hashtable is empty at index, return false
    if (table[position] == NULL)
    {
        return false;
    }

    //create head off the table
    node *head = table[position];

    //while table is not empty at position
    while (head != NULL)
    {
        if (strcmp(aux, head->word) == 0) //compair the strings
        {
            return true;
        }
        head = head->next;
    }
    //word isnt there...
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    //function hash, give me the hash position
    int sum = 0;

    for(int i = 0; word[i] != '\0'; i++)
    {
        sum += tolower(word[i]);
    }
    return sum % N;
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    //open a new file
    FILE *text = fopen(dictionary, "r");
    if (text == NULL)
    {
        fprintf(stderr, "Could not open %s.\n",dictionary);
        return false;
    }

    //create a char to receive the word
    char word[LENGTH+1];

    //read the word
    while (fscanf(text, "%s\n", word)!= EOF)
    {
        totalWords++; //increments the number of words
        node *n = malloc(sizeof(node)); //alocate memo to an aux node
        if (n == NULL)
        {
            printf("Can't alocate memo\n");
            return false;
        }
        strcpy(n->word, word); //copy word at the array and atribuite it to the new node
        int location = hash(word); //generate a hash position

        //if this node is the first!!
        if (table[location] == NULL)
        {
            table[location] = n;
            n->next = NULL;
        }
        //else we already have a node
        else
        {
            n->next = table[location];
            table[location] = n;
        }
    }
    //free all messy in our memo
    fclose(text);

    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    return totalWords;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    //run all our hash table and free the memory
    for (int i = 0; i < N; i++)
    {
        if (table[i] != NULL)
        {
            node *head = table[i];
            table[i] = head->next;
            free(head);
        }
    }
    return true;
}
