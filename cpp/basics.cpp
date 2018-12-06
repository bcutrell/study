#include <iostream>

using namespace std;

int main() {
    // variables
    int A = 4;
    cout << A << endl;
    cout << &A << endl;

    A = 10;
    cout << A << endl;
    cout << &A << endl;

    // -32768 to 32767
    short int t1 = 5; // or short t1=5;

    float t2 = 5.12; // 4 bytes nr up to 38 zeros

    double t3 = 5.12; // 8 bytes nr up to 308 zeros

    char t4 = 'a'; // character

    string t5 = "hello there";
    string x = "hello";
    string y = "there";
    string xplusy = x + y;

    bool t6 = true; // FALSE is always 0

    // for unsigned short int 65535
    unsigned short int t7 = 65535;

    const string NAME = "can not change";
    
    // console input
    // int a;
    // cin >> a; 
    // cout << a;

    // operators
    int m = 10;
    int n = 5;

    cout << m + n << endl;
    cout << m - n << endl;
    cout << m * n << endl;
    cout << m / n << endl;
    cout << m % n << endl;

    // incrementation - increase by 1
    // decrementation - decrease by 1
    int z = 1;
    z = z + 1;
    z += 1;
    cout << z << endl;

    int d = 1;
    cout << d++ << endl; // 1
    cout << d << endl; // 2
    cout << ++d << endl; // 3

    cout << (d == z) << endl;

    return 0;
}

