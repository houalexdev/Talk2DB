# -*- coding: utf-8 -*-
import json
from casdoor_auth import CasdoorAuth
from auth import ConfigFileAuth
from app import Talk2DBApp
import os
#from vanna.chromadb import ChromaDB_VectorStore
from vanna.ollama import Ollama
from vanna.qdrant import Qdrant_VectorStore
from qdrant_client import QdrantClient
from openai import OpenAI
from vanna.openai import OpenAI_Chat

# Load database configurations
with open('env/config.json', 'r', encoding='utf-8') as f:
    config_data = json.load(f)
    global_config = config_data.get('global', {})
    db_configurations = config_data.get('databases', [])
    users_config = global_config.get('users', [])

current_dir = os.path.dirname(os.path.abspath(__file__))

'''
class MyVanna(ChromaDB_VectorStore, Ollama):
    def __init__(self, config=None):
        ChromaDB_VectorStore.__init__(self, config=config)
        Ollama.__init__(self, config=config)

vn = MyVanna(config={
    'model': global_config.get('model'),
    'ollama_host': global_config.get('ollama_host'),
    'path': global_config.get('path')
})
'''

if global_config.get('llm_type') == 'vllm':
    client = OpenAI(api_key=global_config.get('vllm_key'), base_url=global_config.get('vllm_host'))
    class MyVanna(Qdrant_VectorStore, OpenAI_Chat):
        def __init__(self, config=None):
            Qdrant_VectorStore.__init__(self, config=config)
            OpenAI_Chat.__init__(self, config=config)
            if "openai_client" in (config or {}):
                self.client = config["openai_client"]
    vn = MyVanna(config={
        'client': QdrantClient(host=global_config.get('vector_host'),port=6333,api_key=None),
        'model': global_config.get('vllm_model'),
        'openai_client': client,
        'fastembed_model': "jinaai/jina-embeddings-v2-base-zh"
    })
else:
    class MyVanna(Qdrant_VectorStore, Ollama):
        def __init__(self, config=None):
            Qdrant_VectorStore.__init__(self, config=config)
            Ollama.__init__(self, config=config)
    vn = MyVanna(config={
        'client': QdrantClient(host=global_config.get('vector_host'),port=6333,api_key=None),
        'model': global_config.get('ollama_model'),
        'ollama_host': global_config.get('ollama_host'),
        'fastembed_model': "jinaai/jina-embeddings-v2-base-zh"
    })

# 获取认证类型配置（默认使用casdoor）
AUTH_TYPE = os.getenv('AUTH_TYPE', 'casdoor').lower()
print(f"当前认证方式: {AUTH_TYPE}")

# 根据认证类型选择对应的认证类
if AUTH_TYPE == 'config':
    # 使用配置文件认证
    print(f"配置的用户数: {len(users_config)}")
    for user in users_config:
        print(f"- 用户: {user['user']}")
    auth = ConfigFileAuth(users_config=users_config)
elif AUTH_TYPE == 'casdoor':
    # 使用Casdoor认证
    CASDOOR_ENDPOINT = os.getenv('CASDOOR_ENDPOINT')
    CASDOOR_CLIENT_ID = os.getenv('CASDOOR_CLIENT_ID')
    CASDOOR_CLIENT_SECRET = os.getenv('CASDOOR_CLIENT_SECRET')
    
    if not all([CASDOOR_ENDPOINT, CASDOOR_CLIENT_ID, CASDOOR_CLIENT_SECRET]):
        raise ValueError("请设置以下环境变量：CASDOOR_ENDPOINT, CASDOOR_CLIENT_ID, CASDOOR_CLIENT_SECRET")
    
    auth = CasdoorAuth(
        endpoint=CASDOOR_ENDPOINT,
        client_id=CASDOOR_CLIENT_ID,
        client_secret=CASDOOR_CLIENT_SECRET
    )
else:
    raise ValueError(f"不支持的认证方式: {AUTH_TYPE}。支持的值: casdoor, config")

# 创建FlaskApp实例时传递db_configurations
Talk2DBApp(
    vn=vn,
    auth=auth,
    allow_llm_to_see_data=True,
    show_training_data=True,
    sql=True,
    table=True,
    csv_download=True,
    chart=True,
    redraw_chart=False,
    summarization=False,
    ask_results_correct=False,
    assets_folder=os.path.join(current_dir, "static"),
    index_html_path=os.path.join(current_dir, "templates/index.html"),
    debug=False,
    followup_questions=False,
    db_configurations=db_configurations,
    auth_type=AUTH_TYPE,
).run()
