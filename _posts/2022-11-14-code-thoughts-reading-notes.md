---
layout: post
title: "无标题"
date: 2022-11-14 12:00:00 +0800
categories: [编程, 学习]
tags: []
---

https://www.programmercarl.com/

选用语言c++

编程素养

代码规范

参考google c++编程规范

变量命名使用小驼峰

库函数使用

如果题目关键的部分直接用库函数就可以解决，建议不要使用库函数。

如果库函数仅仅是 解题过程中的一小部分，并且你已经很清楚这个库函数的内部实现原理的话，那么直接用库函数。

本地编译

参考如下示例 采用添加日志输出的方式

#include &lt;iostream&gt;
#include &lt;vector&gt;
using namespace std;

class Solution {
public:
    int minCostClimbingStairs(vector&lt;int&gt;&amp; cost) {
        vector&lt;int&gt; dp(cost.size());
        dp[0] = cost[0];
        dp[1] = cost[1];
        for (int i = 2; i &lt; cost.size(); i++) {
            dp[i] = min(dp[i - 1], dp[i - 2]) + cost[i];
        }
        return min(dp[cost.size() - 1], dp[cost.size() - 2]);
    }
};

int main() {
    int a[] = {1, 100, 1, 1, 1, 100, 1, 1, 100, 1};
    vector&lt;int&gt; cost(a, a + sizeof(a) / sizeof(int));
    Solution solution;
    cout &lt;&lt; solution.minCostClimbingStairs(cost) &lt;&lt; endl;
}
`

核心代码模式&ACM模式

由于自己刷题多是牛客  所以目前选择ACM

核心代码模式

如下示例只需要填入相关算法即可

class Solution {
public:
   int getDays(vector&lt;int&gt;&amp; work, vector&lt;int&gt;&amp; gym) {
       // 处理逻辑
   }
};
`

ACM模式

ACM模式下除了要写核心算法 还要处理输入输出逻辑

#include&lt;iostream&gt;
#include&lt;vector&gt;
using namespace std;

int getDays(vector&lt;int&gt;&amp; work, vector&lt;int&gt;&amp; gym);

int main() {
   int n;
   while (cin &gt;&gt; n) {
       vector&lt;int&gt; gym(n);
       vector&lt;int&gt; work(n);
       for (int i = 0; i &lt; n; i++) cin &gt;&gt; work[i];
       for (int i = 0; i &lt; n; i++) cin &gt;&gt; gym[i];
       int result = 0;

       // 处理逻辑
       result = getDays(work,gym);
       cout &lt;&lt; result &lt;&lt; endl;
   }
   return 0;
}

int getDays(vector&lt;int&gt;&amp; work, vector&lt;int&gt;&amp; gym) {
       // 处理逻辑
   }
`

ACM模式下如何自己构造二叉树输入用例

二叉树可以有两种存储方式，

    一种是 链式存储

    就是大家熟悉的二叉树，用指针指向左右孩子。

    一种是顺序存储。

    就是用一个数组来存二叉树

    数组如何转化成二叉树:如果父节点的数组下标是i，那么它的左孩子下标就是i * 2 + 1，右孩子下标就是 i * 2 + 2

测试模式如下

#include &lt;iostream&gt;
#include &lt;vector&gt;
#include &lt;queue&gt;
using namespace std;

struct TreeNode {
    int val;
    TreeNode *left;
    TreeNode *right;
    TreeNode(int x) : val(x), left(NULL), right(NULL) {}
};

// 根据数组构造二叉树
TreeNode* construct_binary_tree(const vector&lt;int&gt;&amp; vec) {
    vector&lt;TreeNode*&gt; vecTree (vec.size(), NULL);
    TreeNode* root = NULL;
     // 把输入数值数组，先转化为二叉树节点数组
    for (int i = 0; i &lt; vec.size(); i++) {
        TreeNode* node = NULL;
        if (vec[i] != -1) node = new TreeNode(vec[i]);
        vecTree[i] = node;
        if (i == 0) root = node;
    }
    // 遍历一遍，根据规则左右孩子赋值就可以了
    // 注意这里 结束规则是 i * 2 + 1 &lt; vec.size()，避免空指针
    // 为什么结束规则不能是i * 2 + 2 &lt; arr.length呢?
    // 如果i * 2 + 2 &lt; arr.length 是结束条件
    // 那么i * 2 + 1这个符合条件的节点就被忽略掉了
    // 例如[2,7,9,-1,1,9,6,-1,-1,10] 这样的一个二叉树,最后的10就会被忽略掉
    // 遍历一遍，根据规则左右孩子赋值就可以了
    for (int i = 0; i * 2 + 1 &lt; vec.size(); i++) {
        if (vecTree[i] != NULL) {
            vecTree[i]-&gt;left = vecTree[i * 2 + 1];
            if(i * 2 + 2 &lt; vec.size())
            vecTree[i]-&gt;right = vecTree[i * 2 + 2];
        }
    }
    return root;
}

// 层序打印打印二叉树
void print_binary_tree(TreeNode* root) {
    queue&lt;TreeNode*&gt; que;
    if (root != NULL) que.push(root);
    vector&lt;vector&lt;int&gt;&gt; result;
    while (!que.empty()) {
        int size = que.size();
        vector&lt;int&gt; vec;
        for (int i = 0; i &lt; size; i++) {
            TreeNode* node = que.front();
            que.pop();
            if (node != NULL) {
                vec.push_back(node-&gt;val);
                que.push(node-&gt;left);
                que.push(node-&gt;right);
            }
            // 这里的处理逻辑是为了把null节点打印出来，用-1 表示null
            else vec.push_back(-1);
        }
        result.push_back(vec);
    }
    for (int i = 0; i &lt; result.size(); i++) {
        for (int j = 0; j &lt; result[i].size(); j++) {
            cout &lt;&lt; result[i][j] &lt;&lt; " ";
        }
        cout &lt;&lt; endl;
    }
}

int main() {
    // 注意本代码没有考虑输入异常数据的情况
    // 用 -1 来表示null
    vector&lt;int&gt; vec = {4,1,6,0,2,5,7,-1,-1,-1,3,-1,-1,-1,8};
    TreeNode* root = construct_binary_tree(vec);
    print_binary_tree(root);
}
`