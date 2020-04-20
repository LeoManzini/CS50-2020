#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    //if we receive args != 2
    if (argc != 2)
    {
        fprintf(stderr, "Usage: ./recover image\n");
        return 1;
    }

    //Open sdcard files
    char *file = argv[1];
    FILE *sdcard = fopen(file, "r");

    //Each block has 512 bytes, so create an char * whith that size
    unsigned char *buffer = malloc(512);
    int much_jpg = 0; //how much jpg files we found
    FILE *img;

    //While the 512 bytes dont end read
    while (fread(buffer, 512, 1, sdcard))
    {
        //if the current image is a jpeg file
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            //if alredy have found a jpg file
            if (much_jpg > 0)
            {
                fclose(img);
            }

            //give a name to the file
            char filename[7];
            sprintf(filename, "%03i.jpg", much_jpg);

            //writing
            img = fopen(filename, "w");
            much_jpg++;
        }
        //if we dont found jpg yet
        if (!much_jpg)
        {
            continue;
        }

        fwrite(buffer, 512, 1, img);
    }
    //close all and free alocated memory
    fclose(sdcard);
    fclose(img);
    free(buffer);
}

