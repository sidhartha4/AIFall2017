#include <iostream>
#include <vector>

using namespace std;

#define SZN 15
#define CZN 10
#define debug

int n, c;
vector<int> edges[SZN][SZN][CZN][2];
bool assign[SZN][SZN][CZN][2]; 
string board[SZN];
int bij[300];

int main() {
    // reduce to SAT
    n = c = 0;
    while (cin >> board[n]) ++n;
#ifdef debug
    for (int i = 0; i < n; ++i) cout << board[i] << "\n";
#endif
    for (int i = 0; i < n; ++i) 
        for (int j = 0; j < n; ++j)
            if (board[i][j] != '_') 
                bij[board[i][j]] = c++;

    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            if (board[i][j] != '_') {
                // assign false to the other colors and true to current color
                for (int k = 0; k < c; ++k)
                    assign[i][j][k][1] = 1;
                assign[i][j][bij[board[i][j]]][0] = 1;
                assign[i][j][bij[board[i][j]]][1] = 0;
            }
        }
    }

    return 0;
}
