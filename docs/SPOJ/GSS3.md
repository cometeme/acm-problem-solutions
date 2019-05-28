# GSS3 - Can you answer these queries III

> time limit: 0.330s | memory limit: 1536mb

You are given a sequence $A$ of $N$ ($N <= 50000$) integers between $-10000$ and $10000$. On this sequence you have to apply $M$ ($M <= 50000$) operations: 

modify the $i-th$ element in the sequence or for given $x$ $y$ print $max\{Ai + Ai+1 + .. + Aj | x<=i<=j<=y \}$.

##### Input

The first line of input contains an integer $N$. The following line contains $N$ integers, representing the sequence $A_1..A_N$. 

The third line contains an integer M. The next M lines contain the operations in following form:

0 x y: modify $A_x$ into $y$ ($|y|<=10000$).

1 x y: print $max\{Ai + Ai+1 + .. + Aj | x<=i<=j<=y \}$.

##### Output

For each query, print an integer as the problem required.

##### Example

Input:
```text
4
1 2 3 4
4
1 1 3
0 3 -3
1 2 4
1 3 3
```
Output:
```text
6
4
-3
```

#### 题意

类似于 [GSS1](/SPOJ/GSS1.md) ，只不过多了一个单点修改的操作。

#### 解法

前面的解法略，可以详见 [GSS1](/SPOJ/GSS1.md) 的题解。下面主要简述一下单点更新的过程。

首先，先遍历到这个节点的所在位置，将其的 `sum` `maxl` `maxr` `maxm` 都赋值为为修改后的值。

修改后向上回溯，重新更新这条路径上的每个节点，就可以实现单点修改的操作了。

#### 代码

```cpp
#include <iostream> // C++ I/O
#include <string>   // C++ string
#include <fstream>  // File I/O
#include <sstream>  // String stream I/O
#include <iomanip>  // C++ I/O manipulator

#include <cstdlib> // C library
#include <cstdio>  // C I/O
#include <ctime>   // C time
#include <cmath>   // Math library
#include <cstring> // C strings

#include <vector>    // Vector
#include <queue>     // Queue
#include <stack>     // Stack
#include <map>       // Map
#include <set>       // Set
#include <algorithm> // Algorithms

using namespace std;

#define INF 0x3f3f3f3f
#define EXP 1e-8

#define ll long long

#define memclr(_var) memset(_var, 0, sizeof(_var))
#define maximize(_var, _cur) _var = max(_var, _cur)
#define minimize(_var, _cur) _var = min(_var, _cur)
#define reps(_var, _begin, _end, _step) for (int _var = (_begin); _var <= (_end); _var += (_step))
#define reps_(_var, _end, _begin, _step) for (int _var = (_end); _var >= (_begin); _var -= (_step))
#define rep(_var, _begin, _end) reps(_var, _begin, _end, 1)
#define rep_(_var, _end, _begin) reps_(_var, _end, _begin, 1)

const int MAXN = 50010;

int N, M;
int num[MAXN];

#define max3(a, b, c) max(a, max(b, c))

struct node
{
    node *l, *r;
    int li, ri, sum, maxl, maxr, maxm;
    node()
    {
        l = r = NULL;
        sum = maxl = maxr = maxm = 0;
    }
    node(int index, int value)
    {
        l = r = NULL;
        li = ri = index;
        sum = maxl = maxr = maxm = value;
    }
};

int getmaxl(node *l, node *r)
{
    return max(l->sum + r->maxl, l->maxl);
}

int getmaxr(node *l, node *r)
{
    return max(l->maxr + r->sum, r->maxr);
}

int getmaxm(node *l, node *r)
{
    return max3(l->maxm, r->maxm, l->maxr + r->maxl);
}

void update_node(node *nd)
{
    nd->sum = nd->l->sum + nd->r->sum;
    nd->maxl = getmaxl(nd->l, nd->r);
    nd->maxr = getmaxr(nd->l, nd->r);
    nd->maxm = getmaxm(nd->l, nd->r);
}

node *build(int li, int ri)
{
    if (li == ri)
        return new node(li, num[li]);

    node *nd = new node;
    nd->li = li;
    nd->ri = ri;

    nd->l = build(li, (li + ri) / 2);
    nd->r = build((li + ri) / 2 + 1, ri);

    update_node(nd);

    // cout << li << " " << ri << " @ " << nd->sum << " " << nd->maxl << " " << nd->maxr << " " << nd->maxm << endl;

    return nd;
}

void get(int li, int ri, node *nd, node *res, bool &find)
{
    // cout << nd->li << " " << nd->ri << endl;
    if (nd->li >= li && nd->ri <= ri)
    {
        if (!find)
        {
            res->sum = nd->sum;
            res->maxl = nd->maxl;
            res->maxr = nd->maxr;
            res->maxm = nd->maxm;

            find = true;
            return;
        }

        int maxl = getmaxl(res, nd);
        int maxr = getmaxr(res, nd);
        int maxm = getmaxm(res, nd);

        res->maxl = maxl;
        res->maxr = maxr;
        res->maxm = maxm;

        // cout << "res=" << res->maxm << endl;
        return;
    }

    int mid = (nd->li + nd->ri) / 2;
    if (mid >= li)
        get(li, ri, nd->l, res, find);

    if (mid + 1 <= ri)
        get(li, ri, nd->r, res, find);
}

int ask(int li, int ri, node *tree)
{
    node res;
    bool find = false;
    get(li, ri, tree, &res, find);

    return res.maxm;
}

void change(int pos, int value, node *nd)
{
    // cout << nd->li << " " << nd->ri << endl;
    if (nd->li == pos && nd->ri == pos)
    {
        num[pos] = value;
        nd->sum = nd->maxl = nd->maxr = nd->maxm = value;
        return;
    }

    int mid = (nd->li + nd->ri) / 2;
    if (mid < pos)
        change(pos, value, nd->r);
    if (mid >= pos)
        change(pos, value, nd->l);
    
    update_node(nd);
}

int main(int argc, char *argv[])
{
    ios::sync_with_stdio(false);

    cin >> N;

    rep (i, 1, N)
        cin >> num[i];

    node *tree = build(1, N);

    cin >> M;

    rep(i, 1, M)
    {
        int op, a, b;
        cin >> op >> a >> b;
        if (op == 1)
            cout << ask(a, b, tree) << endl;
        else
            change(a, b, tree);
    }

    return 0;
}
```