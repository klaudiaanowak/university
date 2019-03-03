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
    if (a < 0 || b > 1000)
    {
        return -1;
    }
    while (a <= b)
    {
        printf("%d\n", a);
        a++;
    }
    return 0;
}