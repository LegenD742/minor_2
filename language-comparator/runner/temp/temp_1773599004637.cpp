#include <stdio.h>

int main() {
    int n = 10000;
    long long sum = 0;

    for(int i = 0; i < n; i++){
for(int j =0;j<40000;j++){
        sum += i;
}
    }

    printf("Done: %lld\n", sum);
}