import os
import importlib.metadata
from functools import partial
import flask
import requests
from flask import Response, send_from_directory, render_template

from vanna.base import VannaBase
from auth import AuthInterface, NoAuth
from cache import Cache, MemoryCache
from api import Talk2DBAPI
import pandas as pd

def run_sql(sql: str, db_config: dict) -> pd.DataFrame:
    if db_config["type"].strip().lower() == 'hive':
        pass
        #from pyhive import hive
        #import subprocess
        #command = ['kinit', '-kt', db_config["keytab_file"], db_config["principal"]]
        #result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #cnx = hive.Connection(
        #    host = db_config["host"],
        #    port = db_config["port"],
        #    kerberos_service_name = db_config["user"],
        #    username = db_config["user"],
        #    auth = db_config["auth"],
        #    database = db_config["database"]
        #)
        #cursor = cnx.cursor()
        #cursor.execute(sql)
        #result = cursor.fetchall()
        #if db_config["type"].strip().lower() == 'hive':
        #    columns = [desc[0] for desc in cursor.description]
        #df = pd.DataFrame(result, columns=columns)
    elif db_config["type"].strip().lower() == 'dm8':
        import dmPython
        conn = dmPython.connect(
            user=db_config["user"],
            password=db_config["password"],
            server=db_config["host"],
            port=db_config["port"]
        )
        df = pd.read_sql_query(sql, conn)
    return df

class Talk2DBApp(Talk2DBAPI):
    def __init__(
        self,
        vn: VannaBase,
        cache: Cache = MemoryCache(),
        auth: AuthInterface = NoAuth(),
        debug=True,
        allow_llm_to_see_data=False,
        logo="static/images/talk2db-logo.png",
        title="欢迎使用Talk2DB！",
        subtitle="您的 SQL 查询人工智能副驾驶员。",
        show_training_data=True,
        suggested_questions=True,
        sql=True,
        table=True,
        csv_download=True,
        chart=True,
        redraw_chart=True,
        auto_fix_sql=True,
        ask_results_correct=True,
        followup_questions=True,
        summarization=True,
        function_generation=True,
        index_html_path=None,
        assets_folder=None,
        db_configurations=None,
        auth_type=None,
    ):

        # 设置auth_type
        self.auth_type = auth_type
        auth.auth_type = auth_type
        
        super().__init__(vn, cache, auth, debug, allow_llm_to_see_data, chart, db_configurations)

        self.config["logo"] = logo
        self.config["title"] = title
        self.config["subtitle"] = subtitle
        self.config["show_training_data"] = show_training_data
        self.config["suggested_questions"] = suggested_questions
        self.config["sql"] = sql
        self.config["table"] = table
        self.config["csv_download"] = csv_download
        self.config["chart"] = chart
        self.config["redraw_chart"] = redraw_chart
        self.config["auto_fix_sql"] = auto_fix_sql
        self.config["ask_results_correct"] = ask_results_correct
        self.config["followup_questions"] = followup_questions
        self.config["summarization"] = summarization
        self.config["function_generation"] = function_generation and hasattr(vn, "get_function")
        self.config["version"] = importlib.metadata.version('vanna')

        self.index_html_path = index_html_path
        self.assets_folder = assets_folder

        @self.flask_app.route("/auth/login", methods=["POST"])
        def login():
            return self.auth.login_handler(flask.request)

        @self.flask_app.route("/auth/callback", methods=["GET"])
        def callback():
            return self.auth.callback_handler(flask.request)

        @self.flask_app.route("/auth/logout", methods=["GET"])
        def logout():
            return self.auth.logout_handler(flask.request)

        @self.flask_app.route("/assets/<path:filename>")
        def proxy_assets(filename):
            if self.assets_folder:
                return send_from_directory(self.assets_folder, filename)
            else:
                return "File not found", 404

        # Proxy the /vanna.svg file to the remote server
        @self.flask_app.route("/vanna.svg")
        def proxy_vanna_svg():
            remote_url = "https://vanna.ai/img/vanna.svg"
            response = requests.get(remote_url, stream=True)

            # Check if the request to the remote URL was successful
            if response.status_code == 200:
                excluded_headers = [
                    "content-encoding",
                    "content-length",
                    "transfer-encoding",
                    "connection",
                ]
                headers = [
                    (name, value)
                    for (name, value) in response.raw.headers.items()
                    if name.lower() not in excluded_headers
                ]
                return Response(response.content, response.status_code, headers)
            else:
                return "Error fetching file from remote server", response.status_code

        @self.flask_app.route("/", defaults={"path": ""})
        @self.flask_app.route("/<path:path>")
        def hello(path: str):
            if self.index_html_path:
                directory = os.path.dirname(self.index_html_path)
                filename = os.path.basename(self.index_html_path)
                return send_from_directory(directory=directory, path=filename)
            return "Custom HTML not provided", 404

        @self.flask_app.route("/select_db", methods=["GET"])
        @self.requires_auth
        def select_db_page(user: any):
            return flask.render_template("db_select.html", db_configurations=self.db_configurations)

        @self.flask_app.route("/select_db", methods=["POST"])
        @self.requires_auth
        def select_db(user: any):
            db_select = flask.request.form['db_select']
            username = flask.request.form['username']
            password = flask.request.form['password']
            
            db_config = next((db for db in self.db_configurations if db["name"] == db_select), None)
            if not db_config:
                return '选择的数据库无效'
            
            # 更新数据库配置中的用户名和密码
            db_config['user'] = username
            db_config['password'] = password
            
            #from vanna.chromadb import ChromaDB_VectorStore
            from vanna.ollama import Ollama
            from vanna.qdrant import Qdrant_VectorStore
            from qdrant_client import QdrantClient
            from openai import OpenAI
            from vanna.openai import OpenAI_Chat
            '''
            class MyVanna(ChromaDB_VectorStore, Ollama):
                def __init__(self, config=None):
                    ChromaDB_VectorStore.__init__(self, config=config)
                    Ollama.__init__(self, config=config)
            self.vn = MyVanna(config={
                'model': db_config.get('model'),
                'ollama_host': db_config.get('ollama_host'),
                'path': db_config.get('path')
            })
            '''
            if db_config.get('llm_type') == 'vllm':
                client = OpenAI(api_key=db_config.get('vllm_key'), base_url=db_config.get('vllm_host'))
                class MyVanna(Qdrant_VectorStore, OpenAI_Chat):
                    def __init__(self, config=None):
                        Qdrant_VectorStore.__init__(self, config=config)
                        OpenAI_Chat.__init__(self, config=config)
                        if "openai_client" in (config or {}):
                            self.client = config["openai_client"]
                self.vn = MyVanna(config={
                    'client': QdrantClient(host=db_config.get('vector_host'),port=6333,api_key=None),
                    'model': db_config.get('vllm_model'),
                    'openai_client': client,
                    'fastembed_model': "jinaai/jina-embeddings-v2-base-zh",
                    'sql_collection_name': db_config.get('database') + '_sql',
                    'ddl_collection_name': db_config.get('database') + '_ddl',
                    'documentation_collection_name': db_config.get('database') + '_documentation'
                })
            else:
                class MyVanna(Qdrant_VectorStore, Ollama):
                    def __init__(self, config=None):
                        Qdrant_VectorStore.__init__(self, config=config)
                        Ollama.__init__(self, config=config)
                self.vn = MyVanna(config={
                    'client': QdrantClient(host=db_config.get('vector_host'),port=6333,api_key=None),
                    'model': db_config.get('ollama_model'),
                    'ollama_host': db_config.get('ollama_host'),
                    'fastembed_model': "jinaai/jina-embeddings-v2-base-zh",
                    'sql_collection_name': db_config.get('database') + '_sql',
                    'ddl_collection_name': db_config.get('database') + '_ddl',
                    'documentation_collection_name': db_config.get('database') + '_documentation'
                })
            
            print(f"已更新vn实例配置，使用向量存储路径: {db_config['path']}")
            print(f"更新后的vn实例ID: {id(vn)}")
            
            db_type = db_config["type"].strip().lower()
            try:
                if db_type == 'mysql':
                    self.vn.connect_to_mysql(
                        host=db_config.get('host'), 
                        dbname=db_config.get('database'), 
                        user=db_config.get('user'), 
                        password=db_config.get('password'), 
                        port=db_config.get('port')
                    )
                elif db_type == 'postgres':
                    self.vn.connect_to_postgres(
                        host=db_config.get('host'), 
                        dbname=db_config.get('database'), 
                        user=db_config.get('user'), 
                        password=db_config.get('password'), 
                        port=db_config.get('port')
                    )
                elif db_type == 'oracle':
                    self.vn.connect_to_oracle(
                        host=db_config.get('host'), 
                        dbname=db_config.get('database'), 
                        user=db_config.get('user'), 
                        password=db_config.get('password'), 
                        port=db_config.get('port')
                    )
                elif db_type == 'mssql':
                    self.vn.connect_to_mssql(
                        host=db_config.get('host'), 
                        dbname=db_config.get('database'), 
                        user=db_config.get('user'), 
                        password=db_config.get('password'), 
                        port=db_config.get('port')
                    )
                else:
                    # 使用自定义run_sql函数 并设置vn.run_sql_is_set为True
                    self.vn.run_sql = partial(run_sql, db_config=db_config)
                    self.vn.run_sql_is_set = True
                print(f"✅ 已连接到数据库: {db_config['name']}")
            except Exception as e:
                print(f"⚠️ 数据库连接出错: {str(e)}")
                return f"⚠️ 数据库连接出错: {str(e)}", 500

            try:
                file_path = db_config.get('path') + "/" + db_config.get('database') + ".txt"
                sql_path = db_config.get('path') + "/" + db_config.get('database') + ".sql"
                if os.path.exists(file_path):
                    with open(file_path, mode='r', encoding='utf-8') as file:
                        content = file.read()
                        print(f"✅ 已加载 {file_path}，长度: {len(content)} 字符")
                        
                        try:
                            #for item in content.split("----"):
                            #    train_id = self.vn.train(documentation=item)
                            from textwrap import wrap
                            for section in content.split('----'):
                                chunks = wrap(section, 800)
                                for c in chunks:
                                    train_id = self.vn.train(documentation=c)
                                    print(f"✅ 文档训练成功，ID: {train_id}")
                        except Exception as train_error:
                            print(f"⚠️ 训练过程中出错: {str(train_error)}")
                if os.path.exists(sql_path):
                    import json
                    with open(sql_path, "r", encoding="utf-8") as f:
                        training_data = json.load(f)
                    for item in training_data:
                        question = item.get("question")
                        sql = item.get("sql")
                        if question and sql:
                            self.vn.train(question=question, sql=sql)
                            print(f"✅ 已训练: {question}")
                        else:
                            print("⚠️ 跳过不完整数据:", item)

                # 验证训练是否成功
                training_data = self.vn.get_training_data()
                print(f"✅ 训练集: {str(training_data)}")
                
            except Exception as e:
                print(f"⚠️ 加载过程中出错: {str(e)}")
                import traceback
                traceback.print_exc()
            
            response = flask.make_response(flask.redirect('/'))
            return response
