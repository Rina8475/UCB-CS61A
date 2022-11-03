### Lecture 6 Recursion
1. 递归的分类
    ```mermaid 
    graph TD
    start("Recursion") --- linear("Linear Recursion")
    start --- tree("Tree Recursion")
    linear --- tail("Tail Recursion")
    ```  
    线性递归：在计算问题规模为 $n$ 的问题时，所需的函数调用次数为 $\Theta(n)$ 
    尾递归：是线性递归，且原函数所做的最后一件事即为调用自己
    树递归的时间复杂度一般为指数级别
2. 递归函数的书写：
     依赖注释来抽象封装函数，而不是每次都深入函数内部
     注意递归的终止条件，要保证在每次递归之后原问题的规模都在严格缩小
3. **整数拆分问题**