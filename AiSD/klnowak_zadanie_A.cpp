#include <cstdio>

long long int min(long long int a, long long int b)
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

long long int max(long long int a, long long int b)
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
    long long int K[n];
    int i = 0;
    long long int sum = 0;

    while (i < n)
    {
        if ((scanf("%lld", &K[i]) != 1) || K[i] < 0 || K[i] > 1000000000)
        {
            return -1;
        }
        sum += K[i];
        i++;
    }

    bool flag_f = false;
    bool flag_s = false;
    bool move_f = false;
    bool move_s = false;
    int begin_f = 0;
    int begin_s = 1;
    long long int sum_f = K[begin_f];
    long long int sum_s = sum - sum_f;
    long long int max_dist = min(sum_f, sum_s);
    int index_f = begin_f;
    int index_s = begin_s;

    while (!(flag_f && flag_s))
    {
        if (sum_f < sum_s)
        {
            move_s = true;
            sum_s -= K[index_s];
            sum_f += K[index_s];
            index_s = (index_s + 1) % n;
        }
        else
        {
            move_f = true;
            sum_f -= K[index_f];
            sum_s += K[index_f];
            index_f = (index_f + 1) % n;
        }

        max_dist = max(max_dist, min(sum_f, sum_s));
        if (max_dist == sum / 2)
        {
            break;
        }
        if (index_f == begin_f && move_f)
        {
            flag_f = true;
        }
        if (index_s == begin_s && move_s)
        {
            flag_s = true;
        }
    }
    printf("%lld\n", max_dist);
}