#include <iostream>
#include <queue>
#include <stack>
#include <algorithm>
#include <cstring>
#include <bitset>

using namespace std;

#define x first
#define y second
#define SZN 105
#define MXN 1111111
#define debug

typedef pair<int,int> PII;

const int dx[] = {-1, 1, 0, 0};
const int dy[] = {0, 0, -1, 1};

struct state {
    int idx, b;
    state() {}
    state(int idx, int b) : idx(idx), b(b) {}

    bool operator<(const state& other) const {
        return idx < other.idx;
    }
};

short n, m, stx, sty, num;
char board[SZN][SZN];
char sol[SZN][SZN];
pair<short, int> par[25][MXN];
short d[25][MXN];
priority_queue<pair<int, state>, vector<pair<int, state> >, greater<pair<int, state> > > pq;
// bfs for all pairs shortest path
bool visited[SZN][SZN];
short dist[SZN][SZN];
short idx[SZN][SZN];
short dis[25][25];
vector<PII> v;
vector<PII> shortest[25];


void print(char b[SZN][SZN]) {
    for (int i = 1; i < n; ++i) {
        for (int j = 1; j <= m; ++j)
            cout << b[i][j];
        cout << "\n";
    }
}


void a_star() {
    memset(dist, 0, sizeof(dist));
    pq.push(make_pair(0, state(num, 0)));
    int idx, bitmask, nb;
    while (pq.size()) {
        idx = pq.top().y.idx;
        bitmask = pq.top().y.b;
        cout << idx << " " << bitset<20>(bitmask) << "\n";
        if (bitmask == (1<<num)-1) break;
        pq.pop();
        for (int i = 0; i < num; ++i) {
            if (!(bitmask & i)) {
                nb = bitmask | i;
                d[i][nb] = dis[idx][i] + d[idx][bitmask];
                par[i][nb] = make_pair(idx, bitmask);
                for (int j = 0; j < shortest[i].size(); ++j) {
                    if (shortest[i][j].x == num || (nb & shortest[i][j].x)) continue;
                    pq.push(make_pair(d[idx][bitmask] + d[i][nb] + shortest[i][j].x, state(i, nb)));
                    break;
                }
            }
        }
    }
    memcpy(sol, board, sizeof(sol));
    char cur = 'a' + num;
    while (bitmask) {
        sol[v[idx].x][v[idx].y] = cur;
        tmp = par[idx][bitmask].x;
        bitmask = par[idx][bitmask].y;
        idx = tmp;
        --cur;
    }
    print(sol);
    cout << d[idx][bitmask] << "\n";
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
