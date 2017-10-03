#include <iostream>
#include <queue>
#include <stack>
#include <algorithm>
#include <cstring>
#include <bitset>

using namespace std;

#define x first
#define y second
#define SZN 111
#define MXN 1111111
// #define debug

typedef pair<int,int> PII;

const int dx[] = {-1, 1, 0, 0};
const int dy[] = {0, 0, -1, 1};
const int BITS = 12;

struct state {
    int idx, b;
    state() {}
    state(int idx, int b) : idx(idx), b(b) {}

    bool operator<(const state& other) const {
        return idx < other.idx;
    }
};

short n, m, stx, sty, num;
priority_queue<pair<int, state>, vector<pair<int, state> >, greater<pair<int, state> > > pq;
char board[SZN][SZN], sol[SZN][SZN];
pair<short, int> par[25][MXN];
// bfs for all pairs shortest path
short dist[SZN][SZN], idx[SZN][SZN], dis[25][25], d[25][MXN];
bool visited[SZN][SZN];
vector<PII> v, shortest[25];


void print(char b[SZN][SZN]) {
    for (int i = 1; i < n; ++i) {
        for (int j = 1; j <= m; ++j)
            cout << b[i][j];
        cout << "\n";
    }
}


void a_star() {
    memset(d, 0x3f, sizeof(d));
    d[num][0] = 0;
    pq.push(make_pair(0, state(num, 0)));
    int idx, bitmask, nb, expand = 0;
    while (pq.size()) {
        idx = pq.top().y.idx;
        bitmask = pq.top().y.b;
        if (bitmask == (1<<num)-1) break;
        if (pq.top().x > d[idx][bitmask]) {
            pq.pop();
            continue;
        } 
        ++expand;
        pq.pop();
#ifdef debug
        cout << d[idx][bitmask] << " " << idx << " " << bitset<BITS>(bitmask) << "\n";
#endif
        for (int i = 0; i < num; ++i) {
            if (!(bitmask & (1<<i))) {
                nb = bitmask | (1<<i);
                if (d[i][nb] > dis[idx][i] + d[idx][bitmask]) {
                    d[i][nb] = dis[idx][i] + d[idx][bitmask];
                    par[i][nb] = make_pair(idx, bitmask);
                    /*
                    for (int j = 0; j < shortest[i].size(); ++j) {
                        if (shortest[i][j].y == num || (nb & (1<<shortest[i][j].y))) continue;
#ifdef debug
                        cout << "push " << d[i][nb] + shortest[i][j].x << " " << i << " " 
                            << bitset<BITS>(nb) << "\n";
#endif
                        pq.push(make_pair(d[i][nb] + shortest[i][j].x, state(i, nb)));
                        break;
                    }
                    */
                    pq.push(make_pair(d[i][nb], state(i, nb)));
#ifdef debug
                    cout << "push " << d[i][nb] << " " << i << " " << bitset<BITS>(nb) << "\n";
#endif
                }
                /*
                for (int j = 0; j < shortest[i].size(); ++j) {
                    if (shortest[i][j].y == num || (nb & (1<<shortest[i][j].y))) continue;
#ifdef debug
                    cout << "push " << d[idx][bitmask] + dis[idx][i] + shortest[i][j].x << " " << i << " " << bitset<BITS>(nb) << "\n";
#endif
                    pq.push(make_pair(d[idx][bitmask] + dis[idx][i] + shortest[i][j].x, 
                                state(i, nb)));
                    break;
                }
                */
            }
        }
    }
    memcpy(sol, board, sizeof(sol));
    int tmp;
    char cur = 'a' + num;
    cout << "distance: " << d[idx][bitmask] << "\n";
    cout << "expanded: " << expand << "\n";
    while (bitmask) {
        sol[v[idx].x][v[idx].y] = cur;
        tmp = par[idx][bitmask].x;
        bitmask = par[idx][bitmask].y;
        idx = tmp;
        --cur;
    }
    sol[v[idx].x][v[idx].y] = cur;
    print(sol);
}

void find_dist() {
    int x, y, nx, ny;
    queue<PII> q;
    for (int i = 0; i < v.size(); ++i) {
        memset(visited, 0, sizeof(visited));
        memset(dist, 0, sizeof(dist));
        q.push(make_pair(v[i].x, v[i].y));
        visited[v[i].x][v[i].y] = 1;
        while (q.size()) {
            x = q.front().x;
            y = q.front().y;
            q.pop();
            for (int j = 0; j < 4; ++j) {
                nx = x+dx[j], ny = y+dy[j];
                if (board[nx][ny] != '%' && !visited[nx][ny]) {
                    visited[nx][ny] = 1;
                    dist[nx][ny] = 1+dist[x][y];
                    q.push(make_pair(nx, ny));
                }
            }
        }
        for (int j = 0; j < v.size(); ++j) {
            dis[i][j] = dist[v[j].x][v[j].y];
            shortest[i].push_back(make_pair(dis[i][j], j));
        }
        sort(shortest[i].begin(), shortest[i].end());
    }
#ifdef debug
    cout << v.size() << "\n";
    for (int i = 0; i < v.size(); ++i) {
        for (int j = 0; j < v.size(); ++j) 
            cout << dis[i][j] << " ";
        cout << "\n";
    }
#endif
}


int main() {
    string str;
    n = 1;
    while (getline(cin, str)) {
        m = str.length();
        for (int i = 1; i <= m; ++i)
            board[n][i] = str[i-1];
        ++n;
    }
#ifdef debug
    print(board);
#endif

    for (int i = 1; i <= n; ++i) {
        for (int j = 1; j <= m; ++j) {
            if (board[i][j] == 'P') {
                stx = i, sty = j;
            } else if (board[i][j] == '.') {
                v.push_back(make_pair(i, j));
                idx[i][j] = num++;
            }
        }
    }
    v.push_back(make_pair(stx, sty));
    find_dist();
    a_star();

    return 0;
}
