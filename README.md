# NebulaGraphQAChain
A question-answering framework based on NebulaGraphQAChain (langchain) and deepseek (siliconflow)

Configuration environment used：

Ubuntu 20.04

Nebula Graph 2025.01.13-nightly

Python 3.10.16

After downloading the code, enter the code file:NebulaGraphQAChain.py

Fill in the API url and API key based on your needs:
```
#The example uses the siliconflow online API call method, which can be modified by yourself
CHAT_API_URL = "https://api.siliconflow.cn/v1/chat/completions"  
API_KEY = "sk-********************************"  # Replace with your API key
```
Select the model to use (default is deepseek-ai/DeepSeek-V3):
```
response = requests.post(
            CHAT_API_URL,
            headers={"Authorization": f"Bearer {API_KEY}"},
            json={
                "model": "deepseek-ai/DeepSeek-V3",  # Modify the model you need
                "messages": [{"role": "user", "content": prompt}]
            }
        )
```
Configure the Nebula Graph space to be connected:
```
graph = NebulaGraph(
    space="SPACE",  #Change to the space you need to use
    username="root",
    password="nebula",
    address="127.0.0.1",
    port=9669,
    session_pool_size=30,
)
```
Run the code after making all the changes:
```
python NebulaGraphQAChain.py
```

Open your browser and enter the URL:
```
http://localhost:5000/
```
Enter the question-answering dialogue system
![image](https://github.com/user-attachments/assets/866cdc78-450b-47a4-9c3a-0917af8f0f6d)

