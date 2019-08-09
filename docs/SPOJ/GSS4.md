# GSS4 - Can you answer these queries IV

> time limit: 0.5s | memory limit: 1536mb

You are given a sequence $A$ of $N$ ($N \leq 100,000$) positive integers. There sum will be less than $10^{18}$. On this sequence you have to apply $M$ ($M \leq 100,000$) operations:

(A) For given $x,y$, for each elements between the $x$-th and the $y$-th ones (inclusively, counting from $1$), modify it to its positive square root (rounded down to the nearest integer).

(B) For given $x,y$, query the sum of all the elements between the $x$-th and the $y$-th ones (inclusively, counting from $1$) in the sequence.

##### Input

Multiple test cases, please proceed them one by one. Input terminates by $EOF$.

For each test case:

The first line contains an integer $N$. The following line contains $N$ integers, representing the sequence $A1..AN$.

The third line contains an integer $M$. The next $M$ lines contain the operations in the form "i x y".$i=0$ denotes the modify operation, $i=1$ denotes the query operation.

##### Output

For each test case:

Output the case number (counting from $1$) in the first line of output. Then for each query, print an integer as the problem required.

Print an blank line after each test case.

See the sample output for more details.

##### Example

Input
```text
5
1 2 3 4 5
5
1 2 4
0 2 4
1 2 4
0 4 5
1 1 5
4
10 10 10 10
3
1 1 4
0 2 3
1 1 4
```
Output
```text
Case #1:
9
4
6

Case #2:
40
26

```

#### 题意

给定一个序列，要求支持两种操作：一种是将一段区间内的数开根号，另一种操作是询问区间的元素和。

#### 解法

首先我们研究一下**对区间中的数开根号**这个操作的性质，不难发现对于 $10^{18}$ 范围内的数，我们最多只需要进行 $6$ 次操作，这个区间中的所有数就会变为 $1$ ，而 $1$ 无论怎么进行开根，也还是保持为 $1$ 。

考虑到这个性质之后，我们就可以用线段树维护两个值：区间和以及区间的最大元素。如果一个区间内的最大元素为 $1$ 的话，那么我们就可以跳过开根这个操作，从而减少操作次数。

#### 代码

```cpp
#include <iostream>  // C++ I/O
#include <string>    // C++ string
#include <fstream>   // File I/O
#include <sstream>   // String stream I/O
#include <iomanip>   // C++ I/O manipulator

#include <cstdlib>   // C library
#include <cstdio>    // C I/O
#include <ctime>     // C time
#include <cmath>     // Math library
#include <cstring>   // C strings

#include <vector>    // Vector
#include <queue>     // Queue
#include <stack>     // Stack
#include <map>       // Map
#include <set>       // Set
#include <bitset>    // Bitset
#include <algorithm> // Algorithms

using namespace std;

#define INF 0x3f3f3f3f
#define EPS 1e-8

typedef long long ll;
typedef unsigned long long ull;

#define memclr(_var) memset(_var, 0, sizeof(_var))
#define maximize(_var, _cur) _var = max(_var, _cur)
#define minimize(_var, _cur) _var = min(_var, _cur)
#define reps(_var, _begin, _end, _step) for (int _var = (_begin); _var <= (_end); _var += (_step))
#define reps_(_var, _end, _begin, _step) for (int _var = (_end); _var >= (_begin); _var -= (_step))
#define rep(_var, _begin, _end) reps(_var, _begin, _end, 1)
#define rep_(_var, _end, _begin) reps_(_var, _end, _begin, 1)

inline ll read()
{
    char ch = getchar();
    ll x = 0, f = 1;
    while (ch < '0' || ch > '9')
    {
        if (ch == '-')
            f = -1;
        ch = getchar();
    }
    while (ch >= '0' && ch <= '9')
        x = x * 10 + ch - '0', ch = getchar();
    return x * f;
}

const int MAXN = 100010;

ll a[MAXN], t[MAXN << 2], maxnum[MAXN << 2];

void pushup(int x)
{
    t[x] = t[x << 1] + t[x << 1 | 1];
    maxnum[x] = max(maxnum[x << 1], maxnum[x << 1 | 1]);
}
void build(int root, int l, int r)
{
    if (l == r)
    {
        t[root] = maxnum[root] = a[l];
        return;
    }
    int mid = (l + r) >> 1;
    build(root << 1, l, mid);
    build(root << 1 | 1, mid + 1, r);
    pushup(root);
}
void getsqrt(int root, int l, int r, int tl, int tr)
{
    if (maxnum[root] <= 1)
        return;

    if (l == r)
    {
        t[root] = sqrt(t[root]);
        maxnum[root] = t[root];
        return;
    }
    int mid = (l + r) >> 1;
    if (tl <= mid && maxnum[root << 1] > 1)
        getsqrt(root << 1, l, mid, tl, tr);
    if (tr > mid && maxnum[root << 1 | 1] > 1)
        getsqrt(root << 1 | 1, mid + 1, r, tl, tr);
    pushup(root);
}
ll query(int root, int l, int r, int tl, int tr)
{
    if (tl <= l && r <= tr)
        return t[root];
    int mid = (l + r) >> 1;
    ll res = 0;
    if (tl <= mid)
        res += query(root << 1, l, mid, tl, tr);
    if (tr > mid)
        res += query(root << 1 | 1, mid + 1, r, tl, tr);
    return res;
}

int main(int argc, char *argv[])
{
    ios::sync_with_stdio(false);
    cin.tie(0);

    int n, m, k = 0;
    
    while (~scanf("%d", &n))
    {
        printf("Case #%d:\n", ++k);

        rep(i, 1, n)
            a[i] = read();

        build(1, 1, n);

        m = read();

        rep(_, 1, m)
        {
            int opt = read(), l = read(), r = read();

            if (l > r)
                swap(l, r);
            
            if (opt == 1)
                printf("%lld\n", query(1, 1, n, l, r));
            else
                getsqrt(1, 1, n, l, r);
        }

        putchar('\n');
    }

    return 0;
}
```