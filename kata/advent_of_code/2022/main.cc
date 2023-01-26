#include <iostream>
#include <fstream>
#include <vector>

// Declare global DEBUG boolean
bool DEBUG = true;

// read file to a vector
std::vector<std::string> read_file(std::string file_name) {
    // Read txt file
    std::ifstream file(file_name);
    std::string str;

    // initialize a vector
    std::vector<std::string> vec;

    // Read line by line
    while (std::getline(file, str)) {
        vec.push_back(str);
    }

    return vec;
}

void day_3() {
    // Read txt file
    std::ifstream file("data/day_3.txt");
    std::string str;

    // initialize a sum
    int sum = 0;

    while (std::getline(file, str)) {
        // Skip newline
        if (str == "") {
            continue;
        }

        // print string
        if (DEBUG) {
            std::cout << str << std::endl;
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

                // Add the integer to the sum
                sum += temp;
                break;
            }
        }
    }
    std::cout << "Part 1: " << sum << std::endl;

    // Part 2
    // Read txt file
    std::ifstream file2("data/day_3.txt");

    // read 3 lines at a time
    std::string str1;
    std::string str2;
    std::string str3;

    // initialize a sum
    int sum2 = 0;

    while (std::getline(file2, str1)) {
        // Skip newline
        if (str1 == "") {
            continue;
        }

        std::getline(file2, str2);
        std::getline(file2, str3);

        // Find characters that are in str1, str2, and str3
        for (int i = 0; i < str1.length(); i++) {
            char temp = str1[i];

            // check if temp is in str2
            bool in_str2 = false;
            for (int j = 0; j < str2.length(); j++) {
                if (temp == str2[j]) {
                    in_str2 = true;
                    break;
                }
            }

            // check if temp is in str3
            bool in_str3 = false;
            for (int j = 0; j < str3.length(); j++) {
                if (temp == str3[j]) {
                    in_str3 = true;
                    break;
                }
            }

            // if temp is in str2 and str3, add to sum
            if (in_str2 && in_str3) {
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

                // Add the integer to the sum
                sum2 += temp;
                break;
            }
        }
    }
    std::cout << "Part 2: " << sum2 << std::endl;
}

void day_4() {
    // Read txt file
    std::ifstream file("data/day_4.txt");
    std::string str;

    // initialize a count
    int count = 0;

    // initialize a count
    int part_two_count = 0;

    // Read line by line
    while (std::getline(file, str)) {
        std::string left1;
        std::string left2;

        std::string right1;
        std::string right2;

        int i = 0;
        while (str[i] != '-') {
            left1 += str[i];
            i++;
        }

        i += 1;
        while (str[i] != ',') {
            left2 += str[i];
            i++;
        }

        i += 1;
        while (str[i] != '-') {
            right1 += str[i];
            i++;
        }

        i += 1;
        while (str[i] != '-') {
            right2 += str[i];
            i++;
        }

        // create ramge of left1 and left2
        int min1 = std::stoi(left1);
        int max1 = std::stoi(left2);

        // create ramge of right1 and right2
        int min2 = std::stoi(right1);
        int max2 = std::stoi(right2);

        if (DEBUG) {
                // Print min and max
                std::cout << "min1: " << min1 << std::endl;
                std::cout << "max1: " << max1 << std::endl;
                std::cout << "min2: " << min2 << std::endl;
                std::cout << "max2: " << max2 << std::endl;
            }

        // check if one range is contained in the other
        if ((min1 >= min2 && max1 <= max2) || (min2 >= min1 && max2 <= max1)) {
            // add to count
            count++;
        }

        // check if there is any overlap between the two ranges
        if (min1 <= max2 && max1 >= min2) {
            part_two_count++;
        }

    }
    // print counts
    std::cout << "Part 1: " << count << std::endl;
    std::cout << "Part 2: " << part_two_count << std::endl;
}

int main() {
    std::cout << "Day 3" << std::endl;
    day_3();

    std::cout << "Day 4" << std::endl;
    day_4();

    return 0;
}