import os
import time
import json
import asyncio
from call_llm import run_batch_process, batch_process_deepseek, batch_process_doubao, batch_process_qwen

def main():
    """
    演示如何使用批量处理功能同时处理多个问题
    """
    # 示例问题列表
    questions = [
        "1+1等于多少?",
        "2+2等于多少?",
        "3+3等于多少?",
        "4+4等于多少?",
        "5+5等于多少?",
        "6+6等于多少?",
        "7+7等于多少?",
        "8+8等于多少?",
        "9+9等于多少?"
    ]
    
    print("开始批量处理问题...")
    
    # 设置批处理大小
    batch_size = 3  # 每次处理3个问题
    
    # 使用三个模型并行处理问题
    start_time = time.time()
    
    # 方法1: 使用asyncio.run直接运行并行任务
    deepseek_results, doubao_results, qwen_results = parallel_process_all_models(questions, batch_size)
    
    end_time = time.time()
    total_time = end_time - start_time
    
    # 显示结果
    print("\n=== 处理结果 ===")
    for i, question in enumerate(questions):
        print(f"\n问题 {i+1}: {question}")
        print(f"DeepSeek: {deepseek_results[i][:100]}..." if len(deepseek_results[i]) > 100 else f"DeepSeek: {deepseek_results[i]}")
        print(f"Doubao: {doubao_results[i][:100]}..." if len(doubao_results[i]) > 100 else f"Doubao: {doubao_results[i]}")
        print(f"Qwen: {qwen_results[i][:100]}..." if len(qwen_results[i]) > 100 else f"Qwen: {qwen_results[i]}")
    
    print(f"\n总共处理了 {len(questions)} 个问题，耗时 {total_time:.2f} 秒")
    
    # 将结果保存为JSON
    results = []
    for i, question in enumerate(questions):
        results.append({
            "question": question,
            "deepseek_ans": deepseek_results[i],
            "doubao_ans": doubao_results[i],
            "qwen_ans": qwen_results[i]
        })
    
    with open("batch_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=4)
    
    print("结果已保存到 batch_results.json")

def parallel_process_all_models(questions, batch_size=3):
    """
    并行处理所有模型的问题
    
    Args:
        questions: 问题列表
        batch_size: 每批处理的问题数量
        
    Returns:
        三个模型的结果列表的元组 (deepseek_results, doubao_results, qwen_results)
    """
    async def run_all_models():
        # 创建三个模型的任务
        print("开始并行处理所有模型的问题...")
        deepseek_task = batch_process_deepseek(questions, batch_size)
        doubao_task = batch_process_doubao(questions, batch_size)
        qwen_task = batch_process_qwen(questions, batch_size)
        
        # 并行运行所有任务
        deepseek_results, doubao_results, qwen_results = await asyncio.gather(
            deepseek_task, doubao_task, qwen_task
        )
        
        return deepseek_results, doubao_results, qwen_results
    
    # 使用asyncio.run运行异步函数
    return asyncio.run(run_all_models())


if __name__ == "__main__":
    # 解决Windows上的asyncio警告
    if os.name == 'nt':
        # 设置策略以避免"Event loop is closed"警告
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    main()
