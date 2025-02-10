# NebulaGraphQAChain

## Overview
NebulaGraphQAChain is a question-answering framework based on NebulaGraph, LangChain, and DeepSeek (SiliconFlow). It enables querying and retrieving structured knowledge stored in a Nebula Graph database using an AI model.

## Environment Configuration
The following environment is used:

- **Operating System:** Ubuntu 20.04
- **Graph Database:** Nebula Graph 2025.01.13-nightly
- **Programming Language:** Python 3.10.16

## Installation & Setup
### 1. Clone the Repository
```bash
# Clone the repository to your local machine
git clone https://github.com/EvannZhongg/NebulaGraphQAChain
cd NebulaGraphQAChain
```
Or you can just download this repository and run it.

### 2. Install Dependencies
Make sure you have Python installed, then install the required dependencies:
```bash
pip install -r requirements.txt
```

### 3. Configure API Credentials
Edit `NebulaGraphQAChain.py` and `.env` to set up your API credentials and model.

#### API Configuration
Update the API URL and API Key in `.env` based on your usage:
```python
# SiliconFlow online API call method (modifiable as needed)
CHAT_API_URL=https://api.siliconflow.cn/v1/chat/completions
API_KEY=*****************************  # Replace with your API key
```

#### Model Selection
Modify the model you need (default: `deepseek-ai/DeepSeek-V3`):
```python
response = requests.post(
    CHAT_API_URL,
    headers={"Authorization": f"Bearer {API_KEY}"},
    json={
        "model": "deepseek-ai/DeepSeek-V3",  # Change to the desired model
        "messages": [{"role": "user", "content": prompt}]
    }
)
```

### 4. Configure Nebula Graph Connection
Modify the Nebula Graph connection settings in `NebulaGraphQAChain.py`:
```python
from nebula3.gclient.net import NebulaGraph

graph = NebulaGraph(
    space="YOUR_SPACE",  # Change to the Nebula Graph space you need
    username="root",
    password="nebula",
    address="127.0.0.1",
    port=9669,
    session_pool_size=30,
)
```

## Running the Application
After configuring the necessary settings, run the application:
```bash
python NebulaGraphQAChain.py
```

## Usage
### 1. Open the Web Interface
Once the script is running, open your browser and enter:
```
http://localhost:5000/
```

### 2. Start a Conversation
Enter your questions in the web interface, and the system will generate responses based on the Nebula Graph database and AI model.
![image](https://github.com/user-attachments/assets/8a1613eb-ec9a-4e2f-bce9-3876ebc80191)

### 3. Monitor Logs
You can view the backend log on the frontend page.

#### Backend Log View:
![Backend Log](https://github.com/user-attachments/assets/06deb529-0524-44bc-aed0-e108efe118e8)

#### nGQL Query Execution:
To inspect the generated nGQL queries, check the terminal:
![Query Execution](https://github.com/user-attachments/assets/fefb7d40-9737-4dc1-a3d0-266445ccc65a)

### 4. Verify Queries in Nebula Graph
Queries can be directly executed in Nebula Graph for validation:
![Nebula Graph Query](https://github.com/user-attachments/assets/72b07b88-740e-4210-aaaf-823e29bfb3d1)

## Contribution
If you wish to contribute, feel free to fork the repository and submit a pull request.

## License
This project is licensed under the MIT License.

Additionally, this project makes use of [LangChain](https://github.com/hwchase17/langchain), which is licensed under the MIT License.
