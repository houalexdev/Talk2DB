# 使用官方Python镜像作为基础
FROM python:3.10-slim-bookworm

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=main.py \
    FLASK_ENV=production

# 配置国内Debian镜像源
RUN echo "deb http://mirrors.ustc.edu.cn/debian bookworm main contrib non-free" > /etc/apt/sources.list && \
    echo "deb http://mirrors.ustc.edu.cn/debian bookworm-updates main contrib non-free" >> /etc/apt/sources.list && \
    echo "deb http://mirrors.ustc.edu.cn/debian-security bookworm-security main contrib non-free" >> /etc/apt/sources.list

# 安装系统依赖（包括一些数据库客户端库）
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    default-libmysqlclient-dev \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 复制requirements.txt文件
COPY requirements.txt .

# 配置pip源
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
# 安装Python依赖
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# 复制项目文件
COPY static /app/static/
COPY templates /app/templates/
COPY *.py /app/

# 创建环境配置目录
RUN mkdir -p /app/env/global

# 设置环境变量（可以在运行容器时通过-e参数覆盖）
ENV CASDOOR_ENDPOINT="******************************" \
    CASDOOR_CLIENT_ID="******************************" \
    CASDOOR_CLIENT_SECRET="******************************"

# 暴露应用端口
EXPOSE 8084

# 运行应用
CMD ["python", "main.py"]