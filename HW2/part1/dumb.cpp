#include <iostream>
#include <vector>
#include <cassert>

using namespace std;

#define SZN 15
#define CZN 10
// #define debug

const int dx[] = {-1, 0, 1, 0};
const int dy[] = {0, -1, 0, 1};


int n, c, m;
int bij[300], stx[CZN], sty[CZN], enx[CZN], eny[CZN];
char b[SZN][SZN]; // use char because easier to code
char rev[CZN];
bool done;

void print() {
    for (int i = 0; i <= n+1; ++i) {
        for (int j = 0; j <= m+1; ++j) {
            cout << (b[i][j] ? b[i][j] : ' ');
        }
        cout << "\n";
    }
    cout << "\n";
    cout.flush();
}

bool check(int x, int y) {
    assert(b[x][y] && b[x][y] != '#');
    int cx, cy, nx, ny, cnt;
    for (int i = -1; i <= 1; ++i) {
        for (int j = -1; j <= 1; ++j) {
            cx = i+x, cy = j+y;
            cnt = 0;
            if (b[cx][cy] == b[x][y] && b[cx][cy] != '#') {
                for (int k = 0; k < 4; ++k) {
                    nx = cx+dx[k], ny = cy+dy[k];
                    if (b[nx][ny] == b[x][y]) ++cnt;
                }
            }
            if (cnt > 2) return 0;
        }
    }
    return 1;
}

void dfs(int x, int y, int col, int lft) {
#ifdef debug
    cout << x << " " << y << " " << col << " " << lft << "\n";
    print();
#endif
    if (done) return;
    if (!lft) {
        assert(col == c);
        for (int i = 1; i <= n; ++i) {
            for (int j = 1; j <= m; ++j) {
                assert(b[i][j]);
                cout << b[i][j];
            }
            cout << "\n";
        }
        done = 1;
        return;
    }
    if (col == c+1) return;

    int nx, ny;
    for (int k = 0; k < 4 && !done; ++k) {
        nx = x+dx[k], ny = y+dy[k];
        if (!b[nx][ny]) {
            // empty spot, place same color
            b[nx][ny] = rev[col];
            if (check(nx, ny)) 
                dfs(nx, ny, col, lft-1);
            b[nx][ny] = 0;
        } else if (nx == enx[col] && ny == eny[col]) {
            // at end
            if (check(nx, ny)) 
                dfs(stx[col+1], sty[col+1], col+1, lft);
        }
    }
}

int main() {
    n = c = 0;
    memset(b, '#', sizeof(b));

    string s;
    while (cin >> s) {
        m = s.length();
        ++n;
        for (int i = 0; i < m; ++i) {
            if (s[i] != '_') {
                if (!bij[s[i]]) {
                    bij[s[i]] = ++c;
                    rev[c] = s[i];
                    stx[c] = n, sty[c] = i+1;
                } else {
                    enx[bij[s[i]]] = n, eny[bij[s[i]]] = i+1;
                }
                b[n][i+1] = s[i];
            } else b[n][i+1] = '\0';
        }
    }

#ifdef debug
    for (int i = 1; i <= c; ++i) {
        cout << rev[i] << ": (" << stx[i] << "," << sty[i] << ") -> (" << enx[i] << "," << eny[i] << ")\n";
    }
#endif
    dfs(stx[1], sty[1], 1, n*m-2*c);
    assert(done);

    return 0;
}
