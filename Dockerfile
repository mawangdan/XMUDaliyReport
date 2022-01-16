# 基于镜像基础
FROM python:3.8.8-alpine


# 安装node,保证环境中有JS环境
RUN wget https://nodejs.org/dist/v10.15.3/node-v10.15.3-linux-x64.tar.xz
RUN xz -d node-v10.15.3-linux-x64.tar.xz
RUN tar -xvf node-v10.15.3-linux-x64.tar

# 添加软链接
RUN ln -s /node-v10.15.3-linux-x64/bin/node /usr/local/bin/node
RUN ln -s /node-v10.15.3-linux-x64/bin/npm /usr/local/bin/npm

# 设置代码文件夹工作目录
WORKDIR /src
# 复制当前代码文件到容器中
ADD ./src .
ADD requirements.txt .
# 安装所需的包
RUN pip install -r requirements.txt
# Run app.py when the container launches
CMD ["python", "main.py"]