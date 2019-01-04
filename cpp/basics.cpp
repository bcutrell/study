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

    if (m > n) // anything that != 0
      cout << "something less" << endl;

    if (m > n)
    {
      cout << "something" << endl;
      cout << "something more" << endl;
    }

    if (n > m)
      cout << "wrong" << endl;
    else if (m > n)
      cout << "yep" << endl;
    else
      cout << "still wrong yep" << endl;

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

    int xx = 50;
    // only int and char values
    // remember all chars are ints e.g. 100 == 'd'
    switch (xx)
    {
      case 0:
        cout << "when switched value = 0";
        break;
      case 25:
        cout << "when switched value = 25";
        break;
      case 50:
        cout << "when switched value = 50";
        break;
      default:
        cout << "when switched != any case";
    }
    
    // coditional operator
    // CONDITION ? (exec if true) : (exec if false)

    // system("cls") -> clear console output
    // goto beginning -> rerun main function

    // Arrays
    int array[3]; // TYPE NAME[SIZE_OF_ELEMENTS]
    array[0] = 10;
    array[1] = 50;
    array[2] = 256;

    // multi dimensional
    int biArray[3][4] = {0};
    // &biArray[0][0] see addr

    // Loops
    // for (initilization; condition; inc/dec)
    //  instruction-to-repeat

    for ( int i=0; i < 5; i++ )
      cout << "tasdasd";
    
    int array[4];
    for (int i=0; i < 4; i++)
      array[i] = i;

    i = 0;
    // ++i < 10 increment and then check
    // i++ < 10 check and then increment
    while(++i < 10)
    {
      cout << "lalal";
    }

    const int SIZEOFARRAY = 10;
    int i = 0;
    int array[SIZEOFARRAY];
    while ( i < SIZEOFARRAY )
    {
      array[i] = 10 * i;
      cout << array[i++] << endl;
    }

    do 
    {
      // runs before while
    } while (i);

    // find number of digits
    int nr = 1234;
    int nrOfDigits = 1;
    int tmp = nr;
    while (tmp /= 10)
      nrOfDigits++;

    cout << "the number " << nr << " has  " << nrOfDigits << " digits" << endl;

    // multiplication table
    for (int i=1; i < 10; i++)
    {
      for (int j=1; i < 10; j++)
      {
        cout.width(4);
        cout << i * j << " ";
      }
      cout << endl;
    }

    // break 
    // continue
}

// FUNCTIONS
// string tmp; string.length();
void welcome(); // declaration
void welcome() 
{
  cout << "Welcome"
}

bool isNumber(string tmp)
{
  // not actually working
  if (tmp[0] == '0')
    return false;
  return true
}

