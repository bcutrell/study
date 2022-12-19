#include <iostream>
#include <fstream>

int main() {
    // Read txt file
    std::ifstream file("data/day_3.txt");
    std::string str;

    // initialize a sum
    int sum = 0;

    while (std::getline(file, str)) {
        // Skip newline
        if (str == "") {
            break;
            // continue;
        }

        // Count the number of characters
        int count = 0;
        for (int i = 0; i < str.length(); i++) {
            count++;
        }

        // initialize a hash table
        char hash_table[count];

        // initialize an array with zeros
        char array[count];
        for (int i = 0; i < count; i++) {
            array[i] = 0;
        }

        // Iterate through the first half of the string
        for (int i = 0; i < str.length() / 2; i++) {
            char temp = str[i];

            // store temp in a hash table
            hash_table[i] = temp;
        }

        // Iterate over the second half of the string
        for (int i = str.length() / 2; i < str.length(); i++) {
            char temp = str[i];

            // check if temp is in hash table
            for (int j = 0; j < count; j++) {
                if (temp == hash_table[j]) {
                    array[j] = 1;
                }
            }
        }

        // Find similar characters between the two halves
        for (int i = 0; i < count; i++) {
            if (array[i] == 1) {
                int temp = hash_table[i];

                // convert the character to an integer where
                // a = 1, b = 2, c = 3, etc.
                // A = 27, B = 28, C = 29, etc.
                //
                // check if capital letter
                bool capital = false;
                if (temp >= 65 && temp <= 90) {
                    capital = true;
                }

                if (temp >= 97 && temp <= 122) {
                    temp -= 96;
                } else if (temp >= 65 && temp <= 90) {
                    temp -= 64;
                }

                // if capital letter, add 26
                if (capital) {
                    temp += 26;
                }

                // Print the integer
                std::cout << "Integer: " << temp << std::endl;

                // Add the integer to the sum
                sum += temp;
                break;
            }
        }
    }

    // print the sum
    std::cout << "Sum: " << sum << std::endl;

    return 0;
}