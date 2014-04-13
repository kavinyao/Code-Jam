#include <iostream>

using namespace std;

int main() {
    int T;
    cout.precision(7);
    cin >> T;

    for (int i = 0;i < T;++i) {
        cout << "Case #" << (i+1) << ": ";
        cout << fixed << 0.0;
        cout << endl;
    }
}
