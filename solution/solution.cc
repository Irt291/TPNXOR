#include <string>
#include <iostream>

using std::string;
using std::ios_base;


int main(int argc, char *argv[]) {
    std::cin.tie(nullptr); ios_base::sync_with_stdio(false);
    string data, output, query; std::cin >> data >> output;
    int q; std::cin >> q;

    char xorKey = (data[0] ^ output[0]);
    // std::cout << xorKey;

    for (int i=0; i<q; i++) {
        std::cin >> query;
        for (char &chr : query) std::cout << (char)(chr ^ xorKey);
        std::cout << "\n";
    }

    return 0;
}