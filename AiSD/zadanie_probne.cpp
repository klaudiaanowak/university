#include <cstdio>

void swap(int *a, int *b){
    if (*a > *b){
        int temp = *a;
        *a = *b;
        *b = temp;
    }
}

int main(){
    int a,b;
    scanf("%d %d",&a,&b);
    printf("%d %d\n",a,b);
    swap(&a, &b);
    printf("%d %d\n",a,b);
    while (a<=b){
        printf("%d\n",a);
        a++;
    }
    return 0;
}