#include <stdio.h>
#include <fstream>
#include <string.h>
#include <math.h>


int main() {
    auto f = std::ifstream("day4/input.txt", std::ios::in);

    char * dumpster = new char[256];
    int copies[11] = { 0 };

    int winning_numbers[10] = { 0 },
        my_numbers[25] = { 0 };

    int total_copies = 0,
        total_winnings = 0;

    while (f >> dumpster >> dumpster) { // remove "Card" and "No."
        for (int & winning_number : winning_numbers) {
            f >> winning_number;
        }
        f >> dumpster; // remove "|"
        for (int & my_number : my_numbers) {
            f >> my_number;
        }

        // calculate matches
        int matches = 0;
        for (int winning_number : winning_numbers) {
            for (int my_number : my_numbers) {
                if (winning_number == my_number) {
                    matches++;
                    break;
                }
            }
        }

        // calculate winnings; part 1
        if (matches > 0) {
            total_winnings += (int)pow(2, matches - 1);
        }

        copies[0] += 1; // add 1 copy for this card
        for (size_t i = 0; i < matches; i++) {
            copies[i + 1] += copies[0];
        }

        // calculate total amount of copies; part 2
        total_copies += copies[0];
        // shift copies
        for (size_t i = 0; i < 10; i++) {
            copies[i] = copies[i + 1];
        }
        copies[10] = 0;
    }

    printf("%d\n%d\n", total_winnings, total_copies);

    delete[] dumpster;
    return 0;
}