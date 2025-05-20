#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Markdown和LaTeX渲染示例 - 演示如何渲染LLM输出的混合内容
"""

from md_latex_renderer import MdLatexRenderer
import json
import os

def main():
    # 创建渲染器实例
    renderer = MdLatexRenderer(output_dir="rendered_output")
    
    # 示例1: 渲染简单的LLM回答
    llm_response1 = "首先，我们需要计算球面 \\(x^2 + y^2 + z^2 = 2z\\) 外侧的曲面积分：\n\n\\[\n\\iint_\\Sigma \\left[ x(y^2 + z) \\, dy \\, dz + y(z^2 + x) \\, dz \\, dx + z(x^2 + y) \\, dx \\, dy \\right]\n\\]\n\n我们使用高斯散度定理将曲面积分转换为三重积分。首先确定矢量场 \\( \\mathbf{F} = (P, Q, R) \\)，其中 \\( P = x(y^2 + z) \\)，\\( Q = y(z^2 + x) \\)，\\( R = z(x^2 + y) \\)。计算矢量场的散度：\n\n\\[\n\\text{div} \\, \\mathbf{F} = \\frac{\\partial P}{\\partial x} + \\frac{\\partial Q}{\\partial y} + \\frac{\\partial R}{\\partial z} = (y^2 + z) + (z^2 + x) + (x^2 + y) = x^2 + y^2 + z^2 + x + y + z\n\\]\n\n接下来，将球面方程标准化为 \\( x^2 + y^2 + (z - 1)^2 = 1 \\)，即球心在 \\((0, 0, 1)\\)，半径为1的球体。应用高斯定理，曲面积分转换为三重积分：\n\n\\[\n\\iiint_\\Omega (x^2 + y^2 + z^2 + x + y + z) \\, dV\n\\]\n\n将积分分解为：\n\n\\[\n\\iiint_\\Omega (x^2 + y^2 + z^2) \\, dV + \\iiint_\\Omega x \\, dV + \\iiint_\\Omega y \\, dV + \\iiint_\\Omega z \\, dV\n\\]\n\n由于积分区域关于 \\(z\\) 轴对称，\\(x\\) 和 \\(y\\) 的积分结果为零。剩余部分为：\n\n\\[\n\\iiint_\\Omega (x^2 + y^2 + z^2) \\, dV + \\iiint_\\Omega z \\, dV\n\\]\n\n变换坐标系 \\(z' = z - 1\\)，积分区域变为单位球体。计算各部分积分：\n\n1. 对于 \\( \\iiint_\\Omega (x^2 + y^2 + z^2) \\, dV \\)，变换后展开并积分：\n   \\[\n   \\iiint_{x^2 + y^2 + z'^2 \\leq 1} (x^2 + y^2 + z'^2 + 2z' + 1) \\, dV'\n   \\]\n   结果为 \\( \\frac{32\\pi}{15} \\)。\n\n2. 对于 \\( \\iiint_\\Omega z \\, dV \\)，变换后积分：\n   \\[\n   \\iiint_{x^2 + y^2 + z'^2 \\leq 1} (z' + 1) \\, dV'\n   \\]\n   结果为 \\( \\frac{4\\pi}{3} \\)。\n\n总积分结果为：\n\n\\[\n\\frac{32\\pi}{15} + \\frac{4\\pi}{3} = \\frac{52\\pi}{15}\n\\]\n\n最终答案：\n\n\\[\n\\boxed{\\dfrac{52}{15}\\pi}\n\\]"
    renderer.render_to_image(llm_response1, output_filename="llm_wave_equation", llm_name="deepseek r1")
    
    print("所有示例已完成，请查看 'rendered_output' 目录中的图片")

if __name__ == "__main__":
    main()
