### Lecture 3 Control
1. 条件控制语句
$$
TruePart \quad \text{if} \quad Cond \quad \text{else} \quad FalsePart
$$
等价于
```python
if expr:    
    statement   
elif expr:  
    statement   
.....   
else:      
    statement
```
2. 逻辑运算符
不同于 C 和 Java ，Python 中的逻辑运算符是 `and`, `or`, `not`，其中`and`和`or`都是短路的，并且参数不一定是bool值，返回值也不一定是bool值，其返回值为两参数之一
对于非bool值，`0`，`None`，`[]`，`{}`，`()`等在bool运算中都默认为`false`
```python
>>> not 0
True
>>> not []
True
>>> 1 and 2
2
>>> 0 and 1
0
>>> 1 or 2
1
>>> [] or 2
2
```
3. 循环
Python中的循环语句有 `while`和`for`。一般来说`while`用于不定数迭代。