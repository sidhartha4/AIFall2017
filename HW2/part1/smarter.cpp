/* Compile with g++ -Wall -O2 smart.cpp */
#include <iostream>
#include <vector>
#include <cassert>
#include <queue>
#include <ctime>
#include <cstring>
#include <cmath>
#include <algorithm>

using namespace std;

#define SZN 20
#define CZN 15
// #define debug
#define x first
#define y second

typedef pair<int,int> PII;

// up, left, down, right
const int dx[] = {-1, 0, 1, 0};
const int dy[] = {0, -1, 0, 1};
const int ddx[] = {-2, -2, -1, 0, 1, 1, 0, -1};
const int ddy[] = {-1, 0, 1, 1, 0, -1, -2, -2};


bool done;
int n, c, m, steps;
char b[SZN][SZN]; // use char because easier to code

int bij[300], stx[CZN], sty[CZN], enx[CZN], eny[CZN]; // used for ordering
int cstx[CZN], csty[CZN], cenx[CZN], ceny[CZN]; // used for ordering
char rev[CZN], crev[SZN]; // used for ordering
vector<PII> ord; // ordering

int visited[SZN][SZN], cnt[CZN]; // bfs
queue<PII> q; // bfs

clock_t begt, endt; // time



// debug print output
void print() {
    for (int i = 0; i <= n+1; ++i) {
        for (int j = 0; j <= m+1; ++j) {
            cout << (b[i][j] ? b[i][j] : ' ');
        }
        cout << "\n";
    }
    cout << "\n";
}

// check for no zigzags
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

bool square_helper(int i, int j, int col) {
    if (i && i < n && j && j < m) {
        if (!b[i][j] && !b[i][j+1] && !b[i+1][j] && !b[i+1][j+1]) {
            int num = 0;
            if (b[i-1][j] && bij[b[i-1][j]] <= col && b[i-1][j+1] && bij[b[i-1][j+1]] <= col) 
                ++num;
            if (b[i+2][j] && bij[b[i+2][j]] <= col && b[i+2][j+1] && bij[b[i+2][j+1]] <= col) 
                ++num;
            if (b[i][j-1] && bij[b[i][j-1]] <= col && b[i+1][j-1] && bij[b[i+1][j-1]] <= col) 
                ++num;
            if (b[i][j+2] && bij[b[i][j+2]] <= col && b[i+1][j+2] && bij[b[i+1][j+2]] <= col) 
                ++num;
            if (num >= 3) return 0;
        }
    }
    return 1;
}

// forward checking
bool forward_check(int cx, int cy, int col) {
    int x, y, nx, ny, tmp, tmp2, tmp3;
    bool good;

    // check C shapes (empty space surrounded by >= 3 of same type)
    for (int i = 0; i < 4; ++i) {
        x = cx+dx[i], y = cy+dy[i];
        if (!b[x][y]) {
            tmp = tmp2 = tmp3 = 0;
            for (int k = 0; k < 4; ++k) {
                nx = x+dx[k], ny = y+dy[k];
                if (b[nx][ny] == b[cx][cy]) {
                    if (nx != enx[col] || ny != eny[col]) ++tmp2;
                    ++tmp;
                } else if (b[nx][ny] && bij[b[nx][ny]] < col) 
                    ++tmp3;
            }
            if (tmp >= 3 || (tmp2 >= 2 && tmp3))
                return 0;
        }
    }

    // check square spots
    for (int k = 0; k < 8; ++k) {
        nx = cx+ddx[k], ny = cy+ddy[k];
        if (!square_helper(nx, ny, col)) return 0;
    }

    memset(visited, 0, sizeof(visited));
    while (q.size()) q.pop();
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
                good = 0;
                memset(cnt, 0, sizeof(cnt));
                q.push(make_pair(i, j));
                visited[i][j] = 1;
                visited[cx][cy] = visited[enx[col]][eny[col]] = 0;
                for (int k = col+1; k <= c; ++k) 
                    visited[stx[k]][sty[k]] = visited[enx[k]][eny[k]] = 0;
                while (q.size()) {
                    x = q.front().x;
                    y = q.front().y;
                    q.pop();
                    for (int k = 0; k < 4; ++k) {
                        nx = x+dx[k], ny = y+dy[k];
                        if (!b[nx][ny] && !visited[nx][ny]) {
                            visited[nx][ny] = 1;
                            q.push(make_pair(nx, ny));
                        } else if (bij[b[nx][ny]] >= col && !visited[nx][ny]) {
                            tmp = bij[b[nx][ny]];
                            if ((tmp != col && nx == stx[tmp] && ny == sty[tmp]) ||
                                    (nx == enx[tmp] && ny == eny[tmp]) ||
                                    (tmp == col && nx == cx && ny == cy)) {
                                cnt[tmp]++;
                                visited[nx][ny] = 1;
                            }
                        }
                    }
                }

                for (int k = 0; k < 4; ++k) {
                    nx = cx+dx[k], ny = cy+dy[k];
                    if (nx == enx[col] && ny == eny[col]) 
                        cnt[col] = 0;
                }
                for (int k = col; k <= c; ++k) 
                    if (cnt[k] == 2) good = 1;
                for (int k = col; k <= c; ++k) 
                    if (cnt[k] && cnt[k] != 2 && !good) 
                        return 0;

                good = 0;
                for (int k = col; k <= c; ++k) 
                    if (cnt[k]) good = 1;
                if (!good) return 0;
            }
        }
    }

    return 1;
}

// check for "deadends"
bool check_bound(int cx, int cy, int col) {
    int tmp, x, y, nx, ny;
    for (int i = 0; i < 4; ++i) {
        x = cx+dx[i], y = cy+dy[i];
        if (!b[x][y]) {
            tmp = 0;
            for (int k = 0; k < 4; ++k) {
                nx = x+dx[k], ny = y+dy[k];
                if (b[nx][ny] && bij[b[nx][ny]] <= col)
                    ++tmp;
            }
            if (tmp >= 3) return 0;
        }
    }

    return 1;
}

// check for force moves
bool force(int x, int y, int col) {
    int nx, ny, num = 0;
    for (int i = 0; i < 4; ++i) {
        nx = x+dx[i], ny = y+dy[i];
        if (b[nx][ny] && bij[b[nx][ny]] <= col)
            ++num;
    }
    return num >= 3;
}

// dfs with backtracking and forward checking
void dfs(int x, int y, int col, int lft) {
#ifdef debug
    cout << x << " " << y << " " << col << " " << lft << "\n";
    print();
#endif
    ++steps;
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
        endt = clock();
        double duration = (double) (endt - begt) / CLOCKS_PER_SEC;
        cout << "\nelapsed time: " << duration << " seconds\n";
        cout << "assignments: " << steps << "\n";

        exit(0);
    }
    if (col == c+1) return;

    int nx, ny, num = 0;
    for (int k = 0; k < 4 && !done; ++k) {
        nx = x+dx[k], ny = y+dy[k];
        if (!b[nx][ny] && force(nx, ny, col)) ++num;
    } 

    if (num < 2) {
        for (int k = 0; k < 4 && !done; ++k) {
            nx = x+dx[k], ny = y+dy[k];
            if (!num || (num == 1 && force(nx, ny, col))) {
                if (!b[nx][ny]) {
                    // empty spot, place same color
                    b[nx][ny] = rev[col];
                    if (check(nx, ny) && forward_check(nx, ny, col))
                        dfs(nx, ny, col, lft-1);
                    b[nx][ny] = 0;
                } else if (nx == enx[col] && ny == eny[col]) {
                    // at end
                    if (check(nx, ny) && check_bound(nx, ny, col) && 
                            forward_check(stx[col+1], sty[col+1], col+1))
                        dfs(stx[col+1], sty[col+1], col+1, lft);
                }
            }
        }
    }
}

int main() {
    begt = clock();
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
        cout << bij[rev[i]] << " " << rev[i] << ": (" << 
            stx[i] << "," << sty[i] << ") -> (" << enx[i] << "," << eny[i] << ")\n";
    }
#endif

    dfs(stx[1], sty[1], 1, n*m-2*c);
    assert(done);

    return 0;
}