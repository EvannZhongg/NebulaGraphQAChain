import requests
import re
import os
from dotenv import load_dotenv

load_dotenv()  # 读取 .env 文件

CHAT_API_URL = os.getenv("CHAT_API_URL")
API_KEY = os.getenv("API_KEY")

if not CHAT_API_URL or not API_KEY:
    raise ValueError("请在 .env 文件中正确配置 CHAT_API_URL 和 API_KEY")

def call_chat_api(prompt):
    """
    调用大模型 API，解析 NGQL 语句
    """
    try:
        response = requests.post(
            CHAT_API_URL,
            headers={"Authorization": f"Bearer {API_KEY}"},
            json={
                "model": "deepseek-ai/DeepSeek-V3",
                "messages": [{"role": "user", "content": prompt}]
            }
        )
        if response.status_code == 200:
            return response.json()
        else:
            print("API 调用失败:", response.status_code, response.text)
            return None
    except Exception as e:
        print(f"API 调用出错: {e}")
        return None

def parse_ngql_with_llm(ngql_query, query_result):
    """
    使用大模型解析 NGQL 语句，生成节点和边的结构化数据
    """
    # 构造提示词
    prompt = f"""
    你是一个图数据库专家，请解析以下 NGQL 查询语句，并提取节点、边及其属性：
    NGQL 查询语句：
    {ngql_query}
    查询结果：
    {query_result}

    请严格按照以下格式返回结果：
    - 节点：
      - 节点别名: 节点标签, 属性: 属性键=属性值
    - 边：
      - 边标签: 从节点 节点别名 连接到节点 节点别名

    示例：
    - 节点：
      - d: Tag name 1, 属性: properties 1=value 1
      - a: Tag name 2, 属性: oproperties 2=value 2
    - 边：
      - Edge name: 从节点 d 连接到节点 a
    """
    
    # 调用大模型
    response = call_chat_api(prompt)
    if not response:
        return None
    
    # 提取大模型的输出
    llm_output = response['choices'][0]['message']['content']
    print("大模型输出：\n", llm_output)
    
    # 解析大模型的输出
    nodes = {}
    edges = []
    
    # 解析节点
    node_pattern = re.compile(r'- (\w+): (\w+), 属性: ([^\n]+)')
    for match in node_pattern.findall(llm_output):
        node_alias, node_label, properties = match
        properties_dict = {}
        if properties.strip() != "无":
            # 解析属性键值对
            prop_pairs = properties.split(',')
            for prop in prop_pairs:
                if '=' in prop:
                    key, value = prop.split('=', 1)
                    key = key.strip()
                    value = value.strip()
                    properties_dict[key] = value
        nodes[node_alias] = {'id': node_alias, 'label': node_label, 'properties': properties_dict}
    
    # 解析边
    edge_pattern = re.compile(r'- (\w+): 从节点 (\w+) 连接到节点 (\w+)')
    for match in edge_pattern.findall(llm_output):
        edge_label, from_node, to_node = match
        edges.append({'label': edge_label, 'from': from_node, 'to': to_node})
    
    # 返回图结构
    return {'nodes': nodes, 'edges': edges}

# 示例 NGQL 查询和结果
ngql_query = """
MATCH (d:`Device_name`)-[:`contains_operating_temperature`]->(a:`Absolute_maximum_ratings`) 
WHERE d.`Device_name`.`value` == '1N4736AT-D'
RETURN a.`Absolute_maximum_ratings`.`operating_temperature`;
"""
query_result = {'a.Absolute_maximum_ratings.operating_temperature': ['-55°C to +150°C']}

# 解析 NGQL 查询
graph = parse_ngql_with_llm(ngql_query, query_result)

# 输出结果
if graph:
    print("\nNodes:")
    for node_id, node_data in graph['nodes'].items():
        print(f"  {node_id}: {node_data}")
    
    print("\nEdges:")
    for edge in graph['edges']:
        print(f"  {edge}")
