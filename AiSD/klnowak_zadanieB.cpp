#include <cstdio>
#include <utility>
using namespace std;

void przywroc_porzadek(pair<int, int> M_M[], int n)
{
    int i = 0;
    int index = -1;
    long long int e, left, right;
    while (index != i)
    {
        index = i;
        if (2 * index + 2 < n)
        {
            e = (long long)M_M[index].first * M_M[index].second;
            left = (long long)M_M[2 * index + 1].first * M_M[2 * index + 1].second;
            right = (long long)M_M[2 * index + 2].first * M_M[2 * index + 2].second;
            if (e < right && right > left)
            {
                i = 2 * index + 2;
            }
            else if (e < left)
            {
                i = 2 * index + 1;
            }
        }
        else if (2 * index + 1 < n)
        {
            e = (long long)M_M[index].first * M_M[index].second;
            left = (long long)M_M[2 * index + 1].first * M_M[2 * index + 1].second;
            if (e < left)
            {
                i = 2 * index + 1;
            }
        }
        swap(M_M[index], M_M[i]);
    }
}

int main()
{
    int M;
    long long int k;

    if ((scanf("%d %lld", &M, &k) != 2) || M < 1 || M > 1000000 || k < 1 || k > 2000000)
    {
        return -1;
    }
    pair<int, int> M_M[M];

    int i = 0;
    while (i < M)
    {
        M_M[i].first = M - i;
        M_M[i].second = M - i;
        i++;
    }
    int j = 0;
    long long int max = 0;

    while (j < k && M_M[0].second >= 0)
    {

        przywroc_porzadek(M_M, M);
        long long int wynik = (long long)M_M[0].first * M_M[0].second;
        if (max != wynik && M_M[0].second != 0)
        {
            max = wynik;
            printf("%lld\n", max);
            j++;
        }
        M_M[0].second -= 1;
    }
}
