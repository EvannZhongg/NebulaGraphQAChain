import json
import requests
from flask import Flask, request, jsonify, Response, send_from_directory
from queue import Queue
import sys

# ========== 1. Monkey-Patch print 函数，用来捕获所有控制台输出到队列 ==========

log_queue = Queue()
original_print = print  # 先保存原生 print

def custom_print(*args, **kwargs):
    """
    自定义的 print 函数，会将日志同时写入到原生 print 和 log_queue。
    """
    message = " ".join(str(a) for a in args)
    # 放入日志队列，供 SSE 输出给前端
    log_queue.put(message)
    # 继续调用原生 print，以便在后端控制台也能看到
    original_print(*args, **kwargs)

# 覆盖全局 print
print = custom_print


# ========== 2. 以下为 NebulaGraphQAChain 相关逻辑 ==========

from langchain.chains import NebulaGraphQAChain
from langchain_community.graphs import NebulaGraph
from langchain_core.runnables import Runnable
from langchain_core.prompt_values import StringPromptValue  # 导入 StringPromptValue

# 配置你的 API 信息
CHAT_API_URL = "https://api.siliconflow.cn/v1/chat/completions"
API_KEY = "sk-********************************"  # 替换为你的 API 密钥

def call_chat_api(prompt):
    """
    调用 Chat Completions API
    """
    try:
        response = requests.post(
            CHAT_API_URL,
            headers={"Authorization": f"Bearer {API_KEY}"},
            json={
                "model": "deepseek-ai/DeepSeek-R1",  # 选择你的模型
                "messages": [{"role": "user", "content": prompt}]
            }
        )
        if response.status_code == 200:
            data = response.json()
            print("API 返回数据:", data)  # 这里的 print 也会被捕获
            result = data["choices"][0]["message"]["content"]
            if not result:
                print("收到空的响应内容")
                raise ValueError("Received empty response from API")
            return result
        else:
            print(f"API 调用失败: {response.status_code} {response.text}")
            return None
    except Exception as e:
        print(f"API 调用出错: {e}")
        return None

# 自定义 LLM 类，实现 Runnable 接口
class CustomChatModel(Runnable):
    def __init__(self):
        super().__init__()

    def invoke(self, input, config: dict = None, **kwargs):
        """
        实现 Runnable 的 invoke 方法
        """
        # 如果输入是 StringPromptValue 类型，提取字符串内容
        if isinstance(input, StringPromptValue):
            input = input.to_string()  # 使用 to_string() 方法获取字符串内容
        
        # 确保输入是字符串
        if not isinstance(input, str):
            raise ValueError(f"Expected input to be a string, got {type(input)} instead.")
        
        result = call_chat_api(input)
        if result is None:
            raise ValueError("API 调用未返回有效响应")
        return result

# 初始化 NebulaGraph 连接
graph = NebulaGraph(
    space="SPACE",  #更改为需要使用的图空间
    username="root",
    password="nebula",
    address="127.0.0.1",
    port=9669,
    session_pool_size=30,
)

# 初始化自定义的 LLM 对象
llm = CustomChatModel()

# 创建问答链，并设置 allow_dangerous_requests=True
chain = NebulaGraphQAChain.from_llm(
    llm, 
    graph=graph, 
    verbose=True, 
    allow_dangerous_requests=True  # 确认了解风险
)


# ========== 3. Flask 后端路由逻辑，用以配合前端对话可视化 ==========

app = Flask(__name__)

@app.route("/")
def serve_index():
    """
    返回前端页面 index.html
    """
    return send_from_directory("templates", "index.html")

@app.route("/logs")
def stream_logs():
    """
    SSE 日志流，让前端持续获得后端的所有 print 输出
    """
    def event_stream():
        while True:
            log = log_queue.get()
            # SSE 协议：以 data: 开头，一条消息以 \n\n 分割
            yield f"data: {log}\n\n"

    return Response(event_stream(), mimetype="text/event-stream")

@app.route("/ask", methods=["POST"])
def ask():
    """
    接收前端的问题，通过 chain.run(question) 获得回答
    并返回 JSON 数据给前端
    """
    data = request.get_json()
    question = data.get("question", "").strip()

    if not question:
        return jsonify({"success": False, "error": "问题不能为空"}), 400

    # 将收到的问题也写入日志
    print(f"用户提问: {question}")

    try:
        answer = chain.run(question)  # 这里的 print 也会被记录
        print(f"回答: {answer}")
        return jsonify({"success": True, "response": answer})
    except Exception as e:
        error_msg = f"后端执行出错: {e}"
        print(error_msg)
        return jsonify({"success": False, "error": error_msg}), 500

if __name__ == "__main__":
    # 启动 Flask 服务
    app.run(host="0.0.0.0", port=5000, debug=True)
