#include <iostream>

using namespace std;

int main() {
    int n;
    cout.precision(7);
    cin >> n;

    for (int i = 0;i < n;++i) {
        cout << "Case #" << (i+1) << ": ";
        cout << fixed << 0.0;
        cout << endl;
    }
}
