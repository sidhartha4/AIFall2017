#include <iostream>
#include <queue>
#include <stack>
#include <algorithm>
#include <cstring>

using namespace std;

#define x first
#define y second
#define SZN 205
// #define debug

typedef pair<int,int> PII;

const int dx[] = {-1, 1, 0, 0};
const int dy[] = {0, 0, -1, 1};

int n, m, stx, sty, enx, eny;
char board[SZN][SZN];
char sol[SZN][SZN];
int dist[SZN][SZN];
bool visited[SZN][SZN];
PII par[SZN][SZN];
queue<PII> q;
stack<PII> s;
priority_queue<pair<int, PII>, vector<pair<int, PII> >, greater<pair<int, PII> > > pq;


void print(char b[SZN][SZN]) {
    for (int i = 1; i < n; ++i) {
        for (int j = 1; j <= m; ++j)
            cout << b[i][j];
        cout << "\n";
    }
}

void bfs() {
    memset(visited, 0, sizeof(visited));
    memset(dist, 0, sizeof(dist));
    q.push(make_pair(stx, sty));
    visited[stx][sty] = 1;
    int pushed = 1, popped = 0, x, y, nx, ny;
    while (q.size()) {
        x = q.front().x;
        y = q.front().y;
        if (board[x][y] == '.') break;
        ++popped;
        q.pop();
        for (int i = 0; i < 4; ++i) {
            nx = x+dx[i], ny = y+dy[i];
            if (board[nx][ny] != '%' && !visited[nx][ny]) {
                visited[nx][ny] = 1;
                q.push(make_pair(nx, ny));
                ++pushed;
                dist[nx][ny] = 1+dist[x][y];
                par[nx][ny] = make_pair(x, y);
            }
        }
    }
    cout << "BFS cost: " << dist[x][y] << "\n";
    cout << "pushed: " << pushed << " " << " popped: " << popped << "\n";
    memcpy(sol, board, sizeof(sol));
    int tmp;
    while (board[x][y] != 'P') {
        tmp = par[x][y].x;
        y = par[x][y].y;
        x = tmp;
        sol[x][y] = '.';
    }
    print(sol);
    while (q.size()) q.pop();
    cout << "\n";
}

void dfs() {
    memset(visited, 0, sizeof(visited));
    memset(dist, 0, sizeof(dist));
    s.push(make_pair(stx, sty));
    visited[stx][sty] = 1;
    int pushed = 1, popped = 0, x, y, nx, ny;
    while (s.size()) {
        x = s.top().x;
        y = s.top().y;
        if (board[x][y] == '.') break;
        ++popped;
        s.pop();
        for (int i = 0; i < 4; ++i) {
            nx = x+dx[i], ny = y+dy[i];
            if (board[nx][ny] != '%' && !visited[nx][ny]) {
                visited[nx][ny] = 1;
                s.push(make_pair(nx, ny));
                ++pushed;
                dist[nx][ny] = 1+dist[x][y];
                par[nx][ny] = make_pair(x, y);
            }
        }
    }
    cout << "DFS cost: " << dist[x][y] << "\n";
    cout << "pushed: " << pushed << " " << " popped: " << popped << "\n";
    memcpy(sol, board, sizeof(sol));
    int tmp;
    while (board[x][y] != 'P') {
        tmp = par[x][y].x;
        y = par[x][y].y;
        x = tmp;
        sol[x][y] = '.';
    }
    print(sol);
    while (s.size()) s.pop();
    cout << "\n";
}

void greedy() {
    memset(visited, 0, sizeof(visited));
    memset(dist, 0, sizeof(dist));
    pq.push(make_pair(0, make_pair(stx, sty)));
    visited[stx][sty] = 1;
    int pushed = 1, popped = 0, x, y, nx, ny;
    while (pq.size()) {
        x = pq.top().y.x;
        y = pq.top().y.y;
        if (board[x][y] == '.') break;
        ++popped;
        pq.pop();
        for (int i = 0; i < 4; ++i) {
            nx = x+dx[i], ny = y+dy[i];
            if (board[nx][ny] != '%' && !visited[nx][ny]) {
                visited[nx][ny] = 1;
                pq.push(make_pair(abs(enx - nx) + abs(eny - ny), make_pair(nx, ny)));
                ++pushed;
                dist[nx][ny] = 1+dist[x][y];
                par[nx][ny] = make_pair(x, y);
            }
        }
    }
    cout << "Greedy best first cost: " << dist[x][y] << "\n";
    cout << "pushed: " << pushed << " " << " popped: " << popped << "\n";
    memcpy(sol, board, sizeof(sol));
    int tmp;
    while (board[x][y] != 'P') {
        tmp = par[x][y].x;
        y = par[x][y].y;
        x = tmp;
        sol[x][y] = '.';
    }
    print(sol);
    while (pq.size()) pq.pop();
    cout << "\n";
}

void a_star() {
    memset(dist, 0, sizeof(dist));
    pq.push(make_pair(0, make_pair(stx, sty)));
    int pushed = 1, popped = 0, x, y, nx, ny;
    while (pq.size()) {
        x = pq.top().y.x;
        y = pq.top().y.y;
        if (board[x][y] == '.') break;
        ++popped;
        pq.pop();
        for (int i = 0; i < 4; ++i) {
            nx = x+dx[i], ny = y+dy[i];
            if (board[nx][ny] != '%') {
                dist[nx][ny] = 1+dist[x][y];
                ++pushed;
                pq.push(make_pair(dist[nx][ny] + abs(enx - nx) + abs(eny - ny), make_pair(nx, ny)));
                par[nx][ny] = make_pair(x, y);
            }
        }
    }
    cout << "A* cost: " << dist[x][y] << "\n";
    cout << "pushed: " << pushed << " " << " popped: " << popped << "\n";
    memcpy(sol, board, sizeof(sol));
    int tmp;
    while (board[x][y] != 'P') {
        tmp = par[x][y].x;
        y = par[x][y].y;
        x = tmp;
        sol[x][y] = '.';
    }
    print(sol);
    while (pq.size()) pq.pop();
    cout << "\n";
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
                enx = i, eny = j;
            }
        }
    }
    bfs();
    dfs();
    greedy();
    a_star();

    return 0;
}
