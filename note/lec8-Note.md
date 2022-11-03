### Lecture 8 Exceptions
1. **Exception**: 对于一个面向用户的接口，应当明确定义当其输入不满足**预条件**(Precondition)时的行为
2. 异常处理
```Python
raise <Exception>       # raise 语句执行后当前函数立即终止

try:
    <statement>
except [exception]:
    <statement>
```
3. 装饰器
```Python
@Decorator          # 用于函数递归时性质的改变
def function(*args):
    <statement>
```
装饰器等价于 $x = \textrm{Decorator}(function)$