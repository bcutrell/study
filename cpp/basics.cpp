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

    int a;
    cin >> a; // console input

    cout << a;

    return 0;
}

