# Doubao-1-5-thinking-pro-250415

## 题目
计算积分$\oint_{|z| = 3} \frac{e^z}{z(z^2 - 1)}dz$ 计算积分$\oint_{|z| = 3} \frac{e^z}{z(z^2 - 1)}dz$

## 回答

要计算积分$\oint_{|z| = 3} \frac{e^z}{z(z^2 - 1)}dz$，我们可以使用留数定理或柯西积分公式。以下是详细步骤：

### 步骤1：确定奇点
被积函数$\frac{e^z}{z(z^2 - 1)}$的分母为$z(z-1)(z+1)$，因此奇点为$z=0$，$z=1$和$z=-1$。这些奇点均在积分路径$|z|=3$内部（因为它们的模分别为0, 1, 1，均小于3）。

### 步骤2：分解被积函数为部分分式
将被积函数分解为部分分式：
$$
\frac{1}{z(z^2 - 1)} = \frac{A}{z} + \frac{B}{z-1} + \frac{C}{z+1}
$$
解得$A=-1$，$B=\frac{1}{2}$，$C=\frac{1}{2}$，因此：
$$
\frac{e^z}{z(z^2 - 1)} = -\frac{e^z}{z} + \frac{e^z}{2(z-1)} + \frac{e^z}{2(z+1)}
$$

### 步骤3：应用柯西积分公式
对于解析函数$f(z)$，柯西积分公式为$\oint_{|z|=3} \frac{f(z)}{z-a}dz = 2\pi i f(a)$（当$a$在积分路径内时）。这里$f(z)=e^z$，因此：
- $\oint_{|z|=3} \frac{e^z}{z}dz = 2\pi i e^0 = 2\pi i$
- $\oint_{|z|=3} \frac{e^z}{z-1}dz = 2\pi i e^1 = 2\pi i e$
- $\oint_{|z|=3} \frac{e^z}{z+1}dz = 2\pi i e^{-1} = 2\pi i \cdot \frac{1}{e}$

### 步骤4：计算积分
将各部分积分结果代入分解后的表达式：
$$
\oint_{|z|=3} \frac{e^z}{z(z^2 - 1)}dz = -\oint \frac{e^z}{z}dz + \frac{1}{2}\oint \frac{e^z}{z-1}dz + \frac{1}{2}\oint \frac{e^z}{z+1}dz
$$
代入柯西积分公式的结果：
$$
= -2\pi i + \frac{1}{2} \cdot 2\pi i e + \frac{1}{2} \cdot 2\pi i \cdot \frac{1}{e} = \pi i \left(e + \frac{1}{e} - 2\right)
$$

### 最终结果
$$
\boxed{\pi i \left(e + \frac{1}{e} - 2\right)}
$$

## 处理时间
65.84秒
