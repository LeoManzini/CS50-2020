#include <stdio.h>
#include <math.h>
#include <cs50.h>

int main(void) 
{
    float money;
    int roundMoney;
    int counter = 0;

    do
    {
        money = get_float("Enter with the money value: ");
    }
    while (money <= 0);

    money = money * 100;    
    roundMoney = round(money);
    
    while (roundMoney - 25 >= 0)
    {
        roundMoney = roundMoney - 25;
        counter++;
    }
    while (roundMoney - 10 >= 0)
    {
        roundMoney = roundMoney - 10;
        counter++;
    }    
    while (roundMoney - 5 >= 0)
    {
        roundMoney = roundMoney - 5;
        counter++;
    }
    while (roundMoney - 1 >= 0)
    {
        roundMoney = roundMoney - 1;
        counter++;
    }
   
    printf("%i\n", counter);
}
