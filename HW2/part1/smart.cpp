/* Compile with g++ -Wall -O2 smart.cpp */
#include <iostream>
#include <vector>
#include <cassert>
#include <queue>
#include <ctime>

using namespace std;

#define SZN 15
#define CZN 15
// #define debug
#define x first
#define y second

typedef pair<int,int> PII;

// up, left, down, right
const int dx[] = {-1, 0, 1, 0};
const int dy[] = {0, -1, 0, 1};


int n, c, m;
int bij[300], stx[CZN], sty[CZN], enx[CZN], eny[CZN];
int cstx[CZN], csty[CZN], cenx[CZN], ceny[CZN];
char b[SZN][SZN]; // use char because easier to code
char rev[CZN], crev[SZN];
bool done;
int visited[SZN][SZN];
queue<PII> q;
vector<PII> ord;

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

bool forward_check(int cx, int cy, int col) {
    memset(visited, 0, sizeof(visited));
    while (q.size()) q.pop();
    int x, y, nx, ny, cnt;
    bool good;
    // check if there exists path for remaining colors
    for (int i = col; i <= c; ++i) {
        if (i == col) {
            q.push(make_pair(cx, cy));
            visited[cx][cy] = i;
        } else {
            q.push(make_pair(stx[i], sty[i]));
            visited[stx[i]][sty[i]] = i;
        }
        good = 0;
        while (!good && q.size()) {
            x = q.front().x;
            y = q.front().y;
            if (x == enx[i] && y == eny[i]) good = 1;
            q.pop();
            for (int k = 0; k < 4 && !good; ++k) {
                nx = x+dx[k], ny = y+dy[k];
                if (!b[nx][ny] && visited[nx][ny] != i) {
                    visited[nx][ny] = i;
                    q.push(make_pair(nx, ny));
                } else if (nx == enx[i] && ny == eny[i]) {
                    good = 1;
                }
            }
        }
        if (!good) return 0;
        while (q.size()) q.pop();
    }

    // check if there are loops
    memset(visited, 0, sizeof(visited));
    while (q.size()) q.pop();
    for (int i = 1; i <= n; ++i) {
        for (int j = 1; j <= m; ++j) {
            if (!b[i][j] && !visited[i][j]) {
                q.push(make_pair(i, j));
                visited[i][j] = 1;
                visited[cx][cy] = visited[enx[col]][eny[col]] = 0;
                cnt = good = 0;
                while (q.size()) {
                    x = q.front().x;
                    y = q.front().y;
                    q.pop();
                    for (int k = 0; k < 4; ++k) {
                        nx = x+dx[k], ny = y+dy[k];
                        if (!b[nx][ny] && !visited[nx][ny]) {
                            visited[nx][ny] = 1;
                            q.push(make_pair(nx, ny));
                        } else if (bij[b[nx][ny]] > col) {
                            good = 1;
                        } else if (((nx == cx && ny == cy) || (nx == enx[col] && ny == eny[col])) && !visited[nx][ny]) {
                            ++cnt;
                            visited[nx][ny] = 1;
                        }
                    }
                }
                if (!good && cnt != 2) return 0;
            }
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
            if (check(nx, ny) && forward_check(nx, ny, col))
                dfs(nx, ny, col, lft-1);
            b[nx][ny] = 0;
        } else if (nx == enx[col] && ny == eny[col]) {
            // at end
            if (check(nx, ny) && forward_check(nx, ny, col))
                dfs(stx[col+1], sty[col+1], col+1, lft);
        }
    }
}

int main() {
    clock_t begin = clock();
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
                    crev[c] = s[i];
                    cstx[c] = n, csty[c] = i+1;
                } else {
                    cenx[bij[s[i]]] = n, ceny[bij[s[i]]] = i+1;
                }
                b[n][i+1] = s[i];
            } else b[n][i+1] = '\0';
        }
    }

    // Most Constraining Variable (MCV)
    for (int i = 1; i <= c; ++i) 
        ord.push_back(make_pair(abs(cenx[i]-cstx[i]) + abs(ceny[i]-csty[i]), i));
    sort(ord.rbegin(), ord.rend());
    for (int i = 0; i < ord.size(); ++i) {
        rev[i+1] = crev[ord[i].y];
        stx[i+1] = cstx[ord[i].y];
        sty[i+1] = csty[ord[i].y];
        enx[i+1] = cenx[ord[i].y];
        eny[i+1] = ceny[ord[i].y];
    }
    for (int i = 1; i <= c; ++i) bij[rev[i]] = i;
#ifdef debug
    for (int i = 1; i <= c; ++i) {
        cout << bij[rev[i]] << " " << rev[i] << ": (" << stx[i] << "," << sty[i] << ") -> (" << enx[i] << "," << eny[i] << ")\n";
    }
#endif

    dfs(stx[1], sty[1], 1, n*m-2*c);
    assert(done);

    clock_t end = clock();
    double duration = (double) (end - begin) / CLOCKS_PER_SEC;
    cout << "\nelasped time: " << duration << "\n";

    return 0;
}
