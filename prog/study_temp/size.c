#include <stdio.h>

int main() {
    char c = '1';    // символ
    printf("%-18s %-4s %d\n", "char", "c:", sizeof(c));    // символ

    int i = 42;      // целое число (занимает, как правило, 4 байта)
    printf("%-18s %-4s %d\n", "int", "i:", sizeof(i));    // символ

    short int si = 17;           // короткое целое (занимает 2 байта)
    printf("%-18s %-4s %d\n", "short int", "si:", sizeof(si));    // символ

    unsigned short int usi = 25;           // короткое целое (занимает 2 байта)
    printf("%-18s %-4s %d\n", "unsigned short int", "usi:", sizeof(si));    // символ

    long li = 12321321312;       // длинное целое (как правило, 8 байт)
    printf("%-18s %-4s %d\n", "long", "li:", sizeof(li));    // символ

    long long lli = 12321321312; // длинное целое (как правило, 8 байт)
    printf("%-18s %-4s %d\n", "long long", "lli:", sizeof(lli));    // символ

    float f = 2.71828;           // дробное число с плавающей запятой (4 байта)
    printf("%-18s %-4s %d\n", "float", "f:", sizeof(f));    // символ

    double d = 3.141592;         // дробное число двойной точности (8 байт)
    printf("%-18s %-4s %d\n", "double", "d: ", sizeof(d));    // символ

    long double ld = 1e15;       // длинное дробное (как правило, 16 байт)
    printf("%-18s %-4s %d\n", "long double", "ld:", sizeof(ld));    // символ
}
