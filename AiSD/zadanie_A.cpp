#include <cstdio>

int min(int a, int b)
{
    if (a < b)
    {
        return a;
    }
    else
    {
        return b;
    }
}

int max(int a, int b)
{
    if (a > b)
    {
        return a;
    }
    else
    {
        return b;
    }
}
int main()
{
    int n;
    if ((scanf("%d", &n) != 1) || n < 2 || n > 1000000)
    {
        return -1;
    }
    int K[n];
    int i = 0;
    int sum = 0;

    while (i < n)
    {
        if ((scanf("%d", &K[i]) != 1) || K[i] < 0 || K[i] > 1000000000)
        {
            return -1;
        }
        sum += K[i];
        i++;
    }
    
    bool flag_f = true;
    bool flag_s = true;
    int begin_f = 0;
    int begin_s = 1;
    int sum_f = K[begin_f];
    int sum_s = sum - sum_f;
    int max_dist = min(sum_f, sum_s);
    int index_f = begin_f;
    int index_s = begin_s;

    while ((index_f != begin_f || flag_f) && (index_s != begin_s || flag_s))
    {
        if (sum_f < sum_s)
        {
            flag_s = false;
            sum_s -= K[index_s];
            sum_f += K[index_s];
            index_s = (index_s + 1) % n;
        }
        else
        {
            flag_f = false;
            sum_f -= K[index_f];
            sum_s += K[index_f];
            index_f = (index_f + 1) % n;
        }

        max_dist = max(max_dist, min(sum_f, sum_s));
    }
    printf("%d", max_dist);
}