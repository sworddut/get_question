import os
import asyncio
from openai import OpenAI
from openai import AsyncOpenAI
import dotenv
from typing import List, Dict, Any

dotenv.load_dotenv()

# 同步客户端
doubao_client = OpenAI(
    # 此为默认路径，您可根据业务所在地域进行配置
    base_url="https://ark.cn-beijing.volces.com/api/v3",
    # 从环境变量中获取您的 API Key
    api_key=os.environ.get("doubao_api"),
)
qwen_client = OpenAI(
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key=os.environ.get("qwen_api"),
)
deepseek_client = OpenAI(
    api_key=os.getenv("deepseek_api"),
    base_url="https://api.deepseek.com",
)

# 异步客户端
async_doubao_client = AsyncOpenAI(
    base_url="https://ark.cn-beijing.volces.com/api/v3",
    api_key=os.environ.get("doubao_api"),
)
async_qwen_client = AsyncOpenAI(
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key=os.environ.get("qwen_api"),
)
async_deepseek_client = AsyncOpenAI(
    api_key=os.getenv("deepseek_api"),
    base_url="https://api.deepseek.com",
)

def call_doubao(prompt):
    completion = doubao_client.chat.completions.create(
        # 指定您创建的方舟推理接入点 ID，此处已帮您修改为您的推理接入点 ID
        model="doubao-1-5-thinking-pro-250415",
        messages=[
            {"role": "user", "content": prompt},
        ],
    )
    return completion.choices[0].message.content


async def async_call_doubao(prompt):
    completion = await async_doubao_client.chat.completions.create(
        model="doubao-1-5-thinking-pro-250415",
        messages=[
            {"role": "user", "content": prompt},
        ],
    )
    return completion.choices[0].message.content


def call_deepseek(prompt):
    completion = deepseek_client.chat.completions.create(
        model="deepseek-reasoner",
        messages=[
            {"role": "user", "content": prompt},
        ],
    )
    return completion.choices[0].message.content


async def async_call_deepseek(prompt):
    completion = await async_deepseek_client.chat.completions.create(
        model="deepseek-reasoner",
        messages=[
            {"role": "user", "content": prompt},
        ],
    )
    return completion.choices[0].message.content


async def async_call_deepseek_v3(prompt):
    completion = await async_deepseek_client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "user", "content": prompt},
        ],
    )
    return completion.choices[0].message.content

def call_deepseek_v3(prompt):
    completion = deepseek_client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "user", "content": prompt},
        ],
    )
    return completion.choices[0].message.content

def call_deepseek_json(prompt):
    completion = deepseek_client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "user", "content": prompt},
        ],
        response_format={"type": "json_object"}
    )
    return completion.choices[0].message.content


async def async_call_deepseek_json(prompt):
    completion = await async_deepseek_client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "user", "content": prompt},
        ],
        response_format={"type": "json_object"}
    )
    return completion.choices[0].message.content


def call_qwen(prompt):
    completion = qwen_client.chat.completions.create(
        model="qwq-32b",  # 此处以 qwq-32b 为例，可按需更换模型名称
        messages=[
            {"role": "user", "content": prompt}
        ],
        # QwQ 模型仅支持流式输出方式调用
        stream=True,
    )
    reasoning_content = ""  # 定义完整思考过程
    answer_content = ""     # 定义完整回复
    is_answering = False   # 判断是否结束思考过程并开始回复
    for chunk in completion:
  
      delta = chunk.choices[0].delta
      # 打印思考过程
      if hasattr(delta, 'reasoning_content') and delta.reasoning_content != None:
          reasoning_content += delta.reasoning_content
      else:
          # 开始回复
          if delta.content != "" and is_answering is False:
              is_answering = True
          # 打印回复过程
          # print(delta.content, end='', flush=True)
          answer_content += delta.content

    return answer_content


async def async_call_qwen(prompt):
    completion = await async_qwen_client.chat.completions.create(
        model="qwq-32b",
        messages=[
            {"role": "user", "content": prompt}
        ],
        stream=True,
    )
    reasoning_content = ""  # 定义完整思考过程
    answer_content = ""     # 定义完整回复
    is_answering = False   # 判断是否结束思考过程并开始回复
    async for chunk in completion:
        delta = chunk.choices[0].delta
        # 打印思考过程
        if hasattr(delta, 'reasoning_content') and delta.reasoning_content != None:
            reasoning_content += delta.reasoning_content
        else:
            # 开始回复
            if delta.content != "" and is_answering is False:
                is_answering = True
            # 打印回复过程
            # print(delta.content, end='', flush=True)
            answer_content += delta.content

    return answer_content


# 批量处理多个问题的函数
async def process_batch_questions(questions: List[str], model_func, batch_size=3):
    """
    使用协程批量处理多个问题
    
    Args:
        questions: 问题列表
        model_func: 异步模型调用函数 (async_call_deepseek, async_call_doubao, async_call_qwen 等)
        batch_size: 每批处理的问题数量，默认为3
        
    Returns:
        包含所有问题答案的列表
    """
    results = []
    total_questions = len(questions)
    
    for i in range(0, total_questions, batch_size):
        batch = questions[i:i+batch_size]
        print(f"处理批次 {i//batch_size + 1}/{(total_questions+batch_size-1)//batch_size}, 问题 {i+1}-{min(i+batch_size, total_questions)}")
        
        # 创建当前批次的任务
        tasks = [model_func(question) for question in batch]
        batch_results = await asyncio.gather(*tasks)
        results.extend(batch_results)
        
        print(f"批次 {i//batch_size + 1} 完成")
        
    return results


# 批量处理多个问题的函数 - Deepseek模型
async def batch_process_deepseek(questions: List[str], batch_size=3):
    return await process_batch_questions(questions, async_call_deepseek, batch_size)


# 批量处理多个问题的函数 - Doubao模型
async def batch_process_doubao(questions: List[str], batch_size=3):
    return await process_batch_questions(questions, async_call_doubao, batch_size)


# 批量处理多个问题的函数 - Qwen模型
async def batch_process_qwen(questions: List[str], batch_size=3):
    return await process_batch_questions(questions, async_call_qwen, batch_size)


# 运行批处理的辅助函数
def run_batch_process(questions: List[str], model_name: str, batch_size=3):
    """
    运行批处理函数的同步包装器
    
    Args:
        questions: 问题列表
        model_name: 模型名称 ('deepseek', 'doubao', 'qwen')
        batch_size: 每批处理的问题数量，默认为3
        
    Returns:
        包含所有问题答案的列表
    """
    if model_name.lower() == 'deepseek':
        return asyncio.run(batch_process_deepseek(questions, batch_size))
    elif model_name.lower() == 'doubao':
        return asyncio.run(batch_process_doubao(questions, batch_size))
    elif model_name.lower() == 'qwen':
        return asyncio.run(batch_process_qwen(questions, batch_size))
    else:
        raise ValueError(f"不支持的模型名称: {model_name}")