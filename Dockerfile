# 使用官方 Python 基础镜像，这里我们使用 3.9 版本
FROM python:3.11

# 设置工作目录为 /app，也就是容器中的项目工作目录
WORKDIR /app

# 设置环境变量，该环境变量表示 Python 将以非缓冲模式运行，这样可以在 Docker 日志中看到 Python 的各种输出
ENV PYTHONUNBUFFERED=1


COPY ./requirements.txt /app/requirements.txt


# 在容器中安装依赖
RUN pip install --no-cache-dir -r /app/requirements.txt

# 复制 requirements.txt 文件到容器中（如果你有这个文件）
COPY . /app

EXPOSE 8000
# 容器启动后执行的命令，这里使用 Uvicorn 运行 FastAPI，绑定到 0.0.0.0：80
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
