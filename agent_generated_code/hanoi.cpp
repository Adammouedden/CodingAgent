#include <iostream>

void towersOfHanoi(int n, char source, char auxiliary, char destination) {
    if (n == 1) {
        std::cout << "Move disk 1 from peg " << source << " to peg " << destination << std::endl;
        return;
    }
    towersOfHanoi(n - 1, source, destination, auxiliary);
    std::cout << "Move disk " << n << " from peg " << source << " to peg " << destination << std::endl;
    towersOfHanoi(n - 1, auxiliary, source, destination);
}

int main() {
    int n = 7;
    char source = 'A';
    char auxiliary = 'B';
    char destination = 'C';
    std::cout << "Towers of Hanoi for " << n << " disks:" << std::endl;
    towersOfHanoi(n, source, auxiliary, destination);
    return 0;
}