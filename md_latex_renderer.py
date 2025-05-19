import os
import time
import matplotlib.pyplot as plt
import matplotlib

# Configure matplotlib to use LaTeX rendering
matplotlib.rcParams.update({
    'text.usetex': True,
    'font.family': 'serif',
    'font.serif': ['Computer Modern Roman'],
    'mathtext.fontset': 'cm',
    'axes.unicode_minus': False
})

class MdLatexRenderer:
    """简化版的Markdown和LaTeX渲染器，只使用matplotlib"""
    
    def __init__(self, output_dir="rendered_output", dark_mode=False):
        """
        初始化渲染器
        
        Args:
            output_dir: 输出图片的目录
            dark_mode: 是否使用暗色模式
        """
        self.output_dir = output_dir
        self.dark_mode = dark_mode
        
        # 创建输出目录
        os.makedirs(output_dir, exist_ok=True)
    
    def render_to_image(self, content, output_filename=None, width=800, height=None, padding=20, llm_name=""):
        """
        渲染Markdown和LaTeX混合内容为图片
        
        Args:
            content: Markdown和LaTeX混合内容
            output_filename: 输出文件名（不含路径和扩展名）
            width: 图片宽度
            height: 图片高度（如果为None，则自动计算）
            padding: 内边距
            llm_name: LLM模型名称，显示在左上角
            
        Returns:
            生成的图片路径
        """
        if output_filename is None:
            # 使用时间戳作为文件名
            output_filename = f"rendered_{int(time.time())}"
        
        # 确保文件名没有扩展名
        output_filename = os.path.splitext(output_filename)[0]
        output_path = os.path.join(self.output_dir, f"{output_filename}.png")
        
        # 获取当前时间戳
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        
        try:
            # 创建图像
            dpi = 100
            fig_width = width / dpi
            
            # 将内容分成多行
            lines = content.split('\n')
            # 估算需要的高度
            estimated_height = len(lines) * 0.3 + 6  # 给标题和边距预留额外空间
            fig_height = max(15, estimated_height)
            
            if height is not None:
                fig_height = height / dpi
                
            fig = plt.figure(figsize=(fig_width, fig_height), dpi=dpi)
            ax = fig.add_subplot(111)
            ax.axis('off')
            
            # 设置背景色
            if self.dark_mode:
                ax.set_facecolor('#1e1e1e')
                fig.patch.set_facecolor('#1e1e1e')
                text_color = '#f8f8f8'
            else:
                ax.set_facecolor('white')
                fig.patch.set_facecolor('white')
                text_color = '#333333'
            
            # 添加标题和内容
            y_pos = 0.98
            if llm_name:
                ax.text(0.05, y_pos, llm_name, fontsize=18, weight='bold', transform=ax.transAxes, color=text_color)
                y_pos -= 0.04
            
            # 添加时间戳
            ax.text(0.95, y_pos, current_time, fontsize=10, transform=ax.transAxes, 
                   horizontalalignment='right', color='gray')
            y_pos -= 0.06
            
            # 添加内容（将过长的内容分多次添加，避免超出边界）
            max_line_length = 100  # 每行最大字符数
            content_lines = []
            
            for line in lines:
                # 处理过长的行
                while len(line) > max_line_length:
                    content_lines.append(line[:max_line_length])
                    line = line[max_line_length:]
                content_lines.append(line)
            
            # 每次添加一块文本
            chunk_size = 30  # 每次添加的行数
            for i in range(0, len(content_lines), chunk_size):
                chunk = '\n'.join(content_lines[i:i + chunk_size])
                ax.text(0.05, y_pos, chunk, fontsize=10, transform=ax.transAxes,
                      verticalalignment='top', wrap=True, color=text_color)
                y_pos -= min(0.25, len(content_lines[i:i + chunk_size]) * 0.008)  # 根据文本块大小调整位置
            
            # 保存图像
            plt.tight_layout()
            
            # 创建目录（如果不存在）
            output_dir = os.path.dirname(output_path)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)
                
            fig.savefig(output_path, format='png', bbox_inches='tight', pad_inches=0.5)
            plt.close(fig)
            print(f"图片已保存至 {output_path}")
            return output_path
        except Exception as e:
            print(f"生成图像时出错: {str(e)}")
            return None 