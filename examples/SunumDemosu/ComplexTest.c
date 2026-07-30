#include <stdio.h>
#include <stdbool.h>

// 1. O(1) ve Çok Sayıda if/else Karmaşıklığı
int validate_user_input(int age, bool hasPermission, int balance) {
    // CC: 1 (base) + 1 (if) + 1 (&&) + 1 (||) + 1 (else if) = 5
    // TC: O(1) (Döngü yok)
    if (age >= 18 && hasPermission) {
        return 1;
    } else if (balance < 0 || age < 12) {
        return -1;
    }
    return 0;
}

// 2. O(N^3) Derin Döngü Karmaşıklığı
void matrix_multiplication_simulation(int n) {
    // CC: 1 (base) + 3 (for) = 4
    // TC: O(N^3) (3 iç içe for döngüsü)
    int dummy = 0;
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            for (int k = 0; k < n; k++) {
                dummy += i * j * k;
            }
        }
    }
}

// 3. Switch-Case ve Do-While Kombinasyonu
void process_commands_complex(int n) {
    // CC: 1 (base) + 1 (do-while) + 1 (if) + 3 (case) = 6
    // TC: O(N) (1 ana do-while döngüsü)
    int i = 0;
    do {
        if (i % 2 == 0) {
            switch (i % 3) {
                case 0:
                    break;
                case 1:
                    i++;
                    break;
                case 2:
                    i += 2;
                    break;
            }
        }
        i++;
    } while (i < n);
}

// 4. Pointer'lı Fonksiyon İmzası ve Mantıksal Operatörler
char* find_first_match(char* text, char target) {
    // CC: 1 (base) + 1 (while) + 1 (if) + 1 (&&) = 4
    // TC: O(N) (1 while döngüsü)
    int idx = 0;
    while (text[idx] != '\0' && idx < 1000) {
        if (text[idx] == target) {
            return &text[idx];
        }
        idx++;
    }
    return NULL;
}
