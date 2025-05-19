#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
简化版的Markdown和LaTeX渲染器使用示例
"""

from md_latex_renderer import MdLatexRenderer
import os

def main():
    # 创建输出目录
    output_dir = "rendered_output"
    os.makedirs(output_dir, exist_ok=True)
    
    # 创建渲染器实例
    renderer = MdLatexRenderer(output_dir=output_dir)
    
    # 示例1: 渲染包含数学公式的Markdown
    math_content = """# 数学公式示例

## 二次方程
二次方程 $ax^2 + bx + c = 0$ 的解为:

$$x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}$$

## 微积分
导数的定义:

$$f'(x) = \\lim_{h \\to 0} \\frac{f(x+h) - f(x)}{h}$$

## 线性代数
矩阵乘法:

$$
\\begin{bmatrix} a & b \\\\ c & d \\end{bmatrix}
\\begin{bmatrix} e & f \\\\ g & h \\end{bmatrix} =
\\begin{bmatrix} ae+bg & af+bh \\\\ ce+dg & cf+dh \\end{bmatrix}
$$

## 统计学
正态分布的概率密度函数:

$$f(x) = \\frac{1}{\\sigma\\sqrt{2\\pi}}e^{-\\frac{1}{2}(\\frac{x-\\mu}{\\sigma})^2}$$

其中 $\\mu$ 是均值，$\\sigma$ 是标准差。
"""
    
    renderer.render_to_image(
        math_content, 
        output_filename="math_example", 
        width=800,
        llm_name="LaTeX渲染示例"
    )
    
    # 示例2: 模拟LLM回答
    llm_response = """首先，我们需要计算给定函数的积分。

原始函数：
$$f(x) = \\int_0^x \\sin(t^2) dt$$

这个积分没有初等函数表示，是一个Fresnel积分。我们可以使用数值方法计算，但在这里我们会推导一些性质。

$f'(x) = \\sin(x^2)$，这意味着：

$$f''(x) = \\frac{d}{dx}\\sin(x^2) = \\cos(x^2) \\cdot 2x = 2x\\cos(x^2)$$

所以，$f''(x) = 2x\\cos(x^2)$

当 $x = 0$ 时，$f(0) = \\int_0^0 \\sin(t^2) dt = 0$ 且 $f'(0) = \\sin(0) = 0$

所以这个函数在原点处的行为是 $f(x) \\approx 0$ 当 $x$ 接近 0。

对于大的 $x$ 值，积分 $\\int_0^x \\sin(t^2) dt$ 会振荡但会逐渐接近某个极限值，大约是 $\\sqrt{\\pi/8}$。

总结：
1. $f(0) = 0$
2. $f'(x) = \\sin(x^2)$
3. $f''(x) = 2x\\cos(x^2)$
4. 当 $x \\to \\infty$ 时，$f(x) \\to \\sqrt{\\pi/8}$
"""
    
    renderer.render_to_image(
        llm_response, 
        output_filename="llm_response_example", 
        width=800,
        llm_name="Claude 3.5 Sonnet"
    )
    
    print("所有示例已完成，请查看 'rendered_output' 目录中的图片")

if __name__ == "__main__":
    main() 