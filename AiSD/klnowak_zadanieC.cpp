#include <stdio.h>
#include <math.h>
#include <iostream>
using namespace std;

long long int powerofseven(char s)
{
return (long long int)s - 48;
}

void go_up(char **input, long long int **matrix, int columns, int row)
{

    for (int i = 0; i < columns; i++)
    {
        long long int amount = pow(7, powerofseven(input[row-1][i]));
        //printf("P: %lld\n",amount);
        if (i < 2 && i > columns-3) 
        // nie może wykonać ruchu
        return;

        else if (i < 2 && i < columns - 2)
        //moze wykonowac ruch w prawo
        {
            matrix[(row - 1) % 3][i] = max(matrix[(row - 1) % 3][i], matrix[row % 3][i + 2] + amount);
        }
        else if ( i > columns - 3)
        // moze wykonac ruch w lewo
        {
            matrix[(row - 1) % 3][i] = max(matrix[(row - 1) % 3][i], matrix[row % 3][i - 2] + amount);
        }
        else 
        //if (i >= 2 && i <= columns - 3)
        // moze wykonac ruch w obie strony
        {
            matrix[(row - 1) % 3][i] = max(matrix[(row - 1) % 3][i], max(matrix[row % 3][i - 2], matrix[row % 3][i + 2]) + amount);
        }
    }
}

void go_down(char **input, long long int **matrix, int columns, int row)
{

    for (int i = 0; i < columns; i++)
    {
        long long int amount = pow(7, powerofseven(input[row][i]));
        if (i < 1)
        {
            // moze wykonac ruch w prawo
            matrix[row % 3][i] = matrix[(row - 2) % 3][i + 1] + amount;
        }
        else if (i > columns - 2)
        {
            // moze wykonac ruch w lewo
            matrix[row % 3][i] = matrix[(row - 2) % 3][i - 1] + amount;
        }
        else
        {
            // moze wykonac oba ruchy
            matrix[row % 3][i] = max(matrix[(row - 2) % 3][i - 1], matrix[(row - 2) % 3][i + 1]) + amount;
        }
    }
}
int main()
{

    int columns;
    int rows;

    if ((scanf("%d %d", &rows, &columns) != 2) || rows < 3 || columns > 10000)
    {
        return -1;
    }
    long long int **matrix = new long long int *[3];
    char **row = new char *[rows];

    for (int i = 0; i < rows; i++)
    {
        row[i] = new char[columns];
        getchar();
        fgets(row[i], columns + 1, stdin);
            }
    for (int i = 0; i < 3; i++)
    {
        matrix[i] = new long long int[columns];
    }
    for (int j = 0; j < columns; j++)
    {
        matrix[0][j] = pow(7, powerofseven(row[0][j]));
        matrix[1][j] = 0;
        matrix[2][j] = 0;
    }

    for (int i = 2; i < rows; i++)
    {
        go_down(row, matrix, columns, i);
        if (i < rows - 1)
        {
            go_up(row, matrix, columns, i);

        }
    }
    long long int maximum = matrix[(rows-1)%3][0];
    for (int i = 1; i < columns; i++)
    {
        if(maximum < matrix[(rows-1)%3][i])
        maximum = matrix[(rows-1)%3][i];
    }
    printf("%lld\n",maximum);
}