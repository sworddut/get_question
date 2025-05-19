import os
from openai import OpenAI
import dotenv

dotenv.load_dotenv()

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

def call_doubao(prompt):
    completion = doubao_client.chat.completions.create(
        # 指定您创建的方舟推理接入点 ID，此处已帮您修改为您的推理接入点 ID
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