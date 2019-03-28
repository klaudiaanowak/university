#include <cstdio>
#include <iostream>

void zamien(long long int *a, long long int *b)
{
    long long int temp = *a;
    *a = *b;
    *b = temp;
}

void przywroc_porzadek(long long int M[][2], int n)
{
    bool flag = true;
    int i = 0;
    while (flag && 2*i + 2< n)
    {
        long long int e = M[2 * i][1] * M[2 * i][0];
        long long int l = M[2 * i + 1][0] * M[2 * i + 1][1];
        long long int r = M[2 * i + 2][0] * M[2 * i + 2][1];
        if ( e < l || e < r )
        {

            if (l > r)
            {
                zamien(&M[2 * i][1], &M[2 * i + 1][1]);
                zamien(&M[2 * i][0], &M[2 * i + 1][0]);

                i += 1;
            }
            else
            {
                zamien(&M[2 * i][1], &M[2 * i + 2][1]);
                zamien(&M[2 * i][0], &M[2 * i + 2][0]);

                i += 1;
            }
        }

        else
        {
            flag = false;
        }
    }
if ( 2*i + 1 < n && (M[2 * i][1] * M[2 * i][0] < M[2 * i + 1][0] * M[2 * i + 1][1]) ){
                zamien(&M[2 * i][1], &M[2 * i + 1][1]);
                zamien(&M[2 * i][0], &M[2 * i + 1][0]);
}
}

int main()
{
    int n;
    long long int k;

    if ((scanf("%d %lld", &n, &k) != 2) || n < 1 || n > 1000000 || k < 1 || k > 2000000)
    {
        return -1;
    }
    long long int M[n][2];

    int i = 0;
    while (i < n)
    {
        M[i][0] = n - i;
        M[i][1] = n - i;
        i++;
    }
    int j = 0;
    long long int max = 0;

    while (j < k && M[0][1] >= 0)
    {

        przywroc_porzadek(M, n);

        if (max != (M[0][0] * M[0][1]) && M[0][1] != 0)
        {
            max = (M[0][0] * M[0][1]);
            printf("%lld\n", max);
            j++;
        }
        M[0][1] -= 1;
    }
}
