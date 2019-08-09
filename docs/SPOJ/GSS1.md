# GSS1 - Can you answer these queries I

> time limit: 1s | memory limit: 1536mb

You are given a sequence $A[1], A[2], ..., A[N]$ . ( $|A[i]| \leq 15007$ , $1 \leq N \leq 50000$ ).

A query is defined as follows: 

$$Query(x,y) = max \{ a[i]+a[i+1]+...+a[j] ; x \leq i \leq j \leq y \}$$

Given $M$ queries, your program must output the results of these queries.

##### Input

The first line of the input file contains the integer $N$.

In the second line, $N$ numbers follow.

The third line contains the integer $M$.

$M$ lines follow, where line $i$ contains $2$ numbers $x_i$ and $y_i$.

##### Output

Your program should output the results of the $M$ queries, one query per line.

##### Example

Input
```text
3 
-1 2 3
1
1 2
```
Output
```text
2
```

#### 题意

输入一个长度为 `N` 的序列，然后进行 `M` 次查询。每次询问一个区间 `[l, r]` ，求这个区间内**子区间内元素和的最大值**。

举个例子可能更好理解一些，对于序列 `-1, 3, 2, -4, 3, -5, 1` ，它取到最大和的子区间为 `3, 2, -4, 3` ，最大和就为 `4` 。

#### 解法

通过题目条件，我们很容易想到需要使用线段树。

因为子区间的位置十分不确定，所以在建树时，我们很难对两个区间的信息进行合并。为了能够解决这个问题，我们需要在一个区间中保存四个信息：

-   `sum` - 区间和
-   `maxl` - 包含左边界的区间和的最大值
-   `maxr` - 包含右边界的区间和的最大值
-   `maxm` - 不限制边界的区间和的最大值

合并区间时，我们需要这样更新区间的四个参数：

-   `sum = l->sum + r->sum`
-   `maxl = max(l->sum + r->maxl, l->maxl)`
-   `maxr = max(l->maxr + r->sum, r->maxr)`
-   `maxm = max3(l->maxm, r->maxm, l->maxr + r->maxl)`

其中， `max3` 代表三个元素的最大值。

而在查询时，我们只需要用同样的方法搜索，合并区间，最终的 `maxm` 就是整个区间内子区间元素和的最大值。

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

node *build(int li, int ri)
{
    if (li == ri)
        return new node(li, num[li]);

    node *nd = new node;
    nd->li = li;
    nd->ri = ri;

    nd->l = build(li, (li + ri) / 2);
    nd->r = build((li + ri) / 2 + 1, ri);

    nd->sum = nd->l->sum + nd->r->sum;
    nd->maxl = getmaxl(nd->l, nd->r);
    nd->maxr = getmaxr(nd->l, nd->r);
    nd->maxm = getmaxm(nd->l, nd->r);

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
        int li, ri;
        cin >> li >> ri;
        cout << ask(li, ri, tree) << endl;
    }

    return 0;
}
```