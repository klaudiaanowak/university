// Klaudia Nowak
//297936
//SDU

#include <cstdio>

void swap(int *a, int *b)
{
    if (*a > *b)
    {
        int temp = *a;
        *a = *b;
        *b = temp;
    }
}

int main()
{
    int a, b;
    if (scanf("%d  %d", &a, &b) != 2)
    {
        return -1;
    }
    swap(&a, &b);

    if (a < 0 || b > 1000000000 || b - a >= 100000)
    {
        return -1;
    }
    if (a % 2018 == 0)
    {
        a = a - (a % 2018);
    }
    else
    {
        a = a + 2018 - (a % 2018);
    }

    while (a <= b)
    {
        printf("%d ", a);
        a = a + 2018;
    }

    return 0;
}