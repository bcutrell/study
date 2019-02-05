#include <iostream>

using namespace std;

int main(int argc, char *argv[]) {
  // arguments counter
  cout << argc << endl;

  // argument values
  for (int i = 0; i < argc; i++) 
  {
    if (strcmp(argv[i], "-h") == 0) 
    {
      cout << argv[i] << endl;
    }
  }

  char x[] = "a";
  char y[] = "a";
  // (x == y) -> false because x and y are pointers
  // we can use 
  // strcmp(x,y) -> -1,0,1 less than, equal, greater than

  return 0;
}
