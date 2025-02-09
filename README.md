# NebulaGraphQAChain
A question-answering framework based on NebulaGraphQAChain (langchain) and deepseek (siliconflow)

After downloading the code, enter the code file:NebulaGraphQAChain.py

Fill in the API url and API key based on your needs:
```
#The example uses the siliconflow online API call method, which can be modified by yourself
CHAT_API_URL = "https://api.siliconflow.cn/v1/chat/completions"  
API_KEY = "sk-********************************"  # Replace with your API key
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
![image](https://github.com/user-attachments/assets/81880e15-0654-4221-b0af-b5dcfd28490d)
