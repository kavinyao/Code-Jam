#include <iostream>
#include <vector>

using namespace std;

/*
 * layout: the mine sweeper layout
 * CC: number of columns
 * mines: number of mines left
 * row: current row
 * width: number of mines in previous row
 * seq: number of bars with width == `width`
 */
bool recurse(vector<string> &layout, const int CC, int mines, int row, int width, int seq) {
    if (mines > 0 && row == -1)
        return false;

    if (mines == 0) {
        // no more strategy
        return row >= 1 || (row == -1 && seq >= 2);
    }

    // previous width must be valid, make sure
    int new_width = mines >= width ? width : (CC-mines >= 2 ? mines : mines-1);
    // new_width <= width, CC-new_width >= 2
    mines -= new_width;
    fill(layout[row].end()-new_width, layout[row].end(), '*');
    if (recurse(layout, CC, mines, row-1, new_width, new_width==width?seq+1:1))
        return true;

    // retry
    while (new_width > 1) {
        layout[row][CC-new_width] = '.';
        ++mines;
        --new_width;
        if (CC-new_width >= 2 && recurse(layout, CC, mines, row-1, new_width, new_width==width?seq+1:1))
            return true;
    }

    // new_width == 1
    layout[row][CC-1] = '.';
    return false;
}

void solve_small(int R, int C, int M) {
    // special case
    if (R == 1 && C == 1 && M == 0) {
        cout << 'c' << endl;
        return;
    }

    // special case 2
    if (M == (R*C-1)) {
        vector<string> layout(R, string(C, '*'));
        layout[0][0] = 'c';
        for (string &s : layout)
            cout << s << endl;
        return;
    }

    // special case 3:
    if ((M/R == C) || (M/C) == R) {
        cout << "Impossible" << endl;
        return;
    }

    int RR = max(R, C);
    int CC = min(R, C);
    vector<string> layout(RR, string(CC, '.'));
    bool got_solution = recurse(layout, CC, M, RR-1, CC, 0);
    if (got_solution) {
        layout[0][0] = 'c';
        if (R >= C) {
            for (string &s : layout)
                cout << s << endl;
        } else {
            for (int j = 0;j < R;++j) {
                for (int i = 0;i < C;++i) cout << layout[i][j];
                cout << endl;
            }
        }
    } else {
        cout << "Impossible" << endl;
    }
}

int main() {
    int n;
    cout.precision(7);
    cin >> n;

    int R, C, M;
    for (int i = 0;i < n;++i) {
        cout << "Case #" << (i+1) << ":" << endl;
        cin >> R >> C >> M;
        /* cout << "R=" << R << ", C=" << C << ", M=" << M << endl; */
        solve_small(R, C, M);
        /* cout << endl; */
    }
}
