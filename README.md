# Talk2DB

Talk2DB是一个智能SQL查询助手，使用人工智能技术将自然语言转换为SQL查询，并提供数据可视化功能。

## 功能特点

- **自然语言转SQL**：通过AI将用户的自然语言问题转换为SQL查询
- **多数据库支持**：支持MySQL、PostgreSQL、Oracle、MSSQL等多种数据库
- **数据可视化**：自动生成数据图表，直观展示查询结果
- **智能训练**：通过用户反馈不断优化SQL生成质量
- **多模型支持**：支持Ollama、OpenAI等多种LLM模型
- **向量存储**：使用Qdrant进行高效的向量存储和检索
- **响应式界面**：基于Svelte的现代化前端界面

## 技术栈

- **后端**：Python、Flask
- **前端**：Svelte、TypeScript、Tailwind CSS
- **数据库**：支持多种数据库系统
- **AI**：Vanna、Ollama、OpenAI
- **向量存储**：Qdrant
- **部署**：Docker

## 快速开始

### 环境要求

- Python 3.8+
- Node.js 16+
- Docker (可选)

### 安装步骤

1. **克隆仓库**

```bash
git clone https://github.com/houalexdev/talk2db.git
cd talk2db  
```

2. **安装后端依赖**

```bash
pip install -r requirements.txt
```

3. **安装前端依赖**

```bash
cd frontend
npm install
```

4. **构建前端**

```bash
npm run build
```

5. **配置数据库**

编辑 `env/config.json` 文件，添加数据库配置：

```json
{
  "db_configurations": [
    {
      "name": "示例数据库",
      "type": "mysql",
      "host": "localhost",
      "port": 3306,
      "database": "example_db",
      "user": "root",
      "password": "password",
      "model": "llama3",
      "ollama_host": "http://localhost:11434",
      "vector_host": "localhost",
      "path": "./env/tpch"
    }
  ]
}
```

6. **启动应用**

```bash
# 回到项目根目录
cd ..
python main.py
```

应用将在 `http://localhost:5000` 启动。

### 使用Docker部署

1. **构建Docker镜像**

```bash
docker-compose build
```

2. **启动容器**

```bash
docker-compose up -d
```

## 使用指南

1. **访问应用**：打开浏览器，访问 `http://localhost:5000`

2. **选择数据库**：在登录页面选择要连接的数据库，并输入凭据

3. **提问**：在聊天界面输入自然语言问题，例如 "显示所有销售额大于1000的订单"

4. **查看结果**：系统会生成SQL查询，执行并显示结果，同时提供数据可视化图表

5. **反馈**：对生成的SQL和结果进行反馈，帮助系统不断改进

6. **查看历史**：在侧边栏查看历史查询记录

7. **管理训练数据**：在训练数据页面管理和添加训练数据

## 项目结构

```
Talk2DB/
├── env/                  # 环境配置
│   ├── tpch/             # TPCH数据集
│   └── config.json       # 数据库配置
├── frontend/             # 前端代码
│   ├── src/              # 源代码
│   └── static/           # 静态资源
├── static/               # 静态资源
├── templates/            # HTML模板
├── api.py                # API接口
├── app.py                # 应用主文件
├── auth.py               # 认证模块
├── cache.py              # 缓存模块
├── casdoor_auth.py       # Casdoor认证
├── docker-compose.yml    # Docker配置
├── Dockerfile            # Dockerfile
├── main.py               # 主入口
└── requirements.txt      # 依赖文件
```

## 配置选项

在 `app.py` 中，`Talk2DBApp` 类支持以下配置选项：

- `vn`: VannaBase实例
- `cache`: 缓存实例
- `auth`: 认证实例
- `debug`: 调试模式
- `allow_llm_to_see_data`: 是否允许LLM查看数据
- `logo`:  logo路径
- `title`: 页面标题
- `subtitle`: 页面副标题
- `show_training_data`: 是否显示训练数据
- `suggested_questions`: 是否显示建议问题
- `sql`: 是否显示SQL
- `table`: 是否显示表格
- `csv_download`: 是否允许CSV下载
- `chart`: 是否显示图表
- `redraw_chart`: 是否允许重绘图表
- `auto_fix_sql`: 是否自动修复SQL
- `ask_results_correct`: 是否询问结果是否正确
- `followup_questions`: 是否生成后续问题
- `summarization`: 是否生成摘要
- `function_generation`: 是否生成函数
- `index_html_path`: 自定义HTML路径
- `assets_folder`: 资源文件夹
- `db_configurations`: 数据库配置
- `auth_type`: 认证类型

## 贡献指南

1. **Fork 仓库**
2. **创建特性分支** (`git checkout -b feature/amazing-feature`)
3. **提交更改** (`git commit -m 'Add some amazing feature'`)
4. **推送到分支** (`git push origin feature/amazing-feature`)
5. **打开 Pull Request**

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 联系方式

- 项目链接: [https://github.com/houalexdev/talk2db](https://github.com/houalexdev/talk2db)
- 问题反馈: [https://github.com/houalexdev/talk2db/issues](https://github.com/houalexdev/talk2db/issues)  
