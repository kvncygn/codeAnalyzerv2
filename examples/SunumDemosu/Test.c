#include <stdio.h>

void calculate_linear(int n) {
    // Time Complexity should be O(N)
    int sum = 0;
    for (int i = 0; i < n; i++) {
        sum += i;
    }
}

void calculate_quadratic(int n) {
    // Time Complexity should be O(N^2)
    // Cyclomatic complexity should be 4 (1 base + 2 for loops + 1 if)
    int count = 0;
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            if (i == j) {
                count++;
            }
        }
    }
}

int complex_function(int a, int b) {
    // CC: 1 + 1 (while) + 1 (if) + 1 (else if) = 4
    // TC: O(N) because of one while loop
    int res = 0;
    while (a > 0) {
        if (a % 2 == 0) {
            res += a;
        } else if (b > 0) {
            res += b;
        }
        a--;
    }
    return res;
}
