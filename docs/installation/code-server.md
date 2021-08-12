> code-server是vscode的在线版编辑器，可以在任何能连接上code-server服务器的地方使用编辑器。github：`https://github.com/cdr/code-server`

> 环境：CentOS 7.6

# 1. 下载code-server

下载地址：`https://github.com/cdr/code-server/releases`

```bash
[root@localhost ~]# wget https://github.com/cdr/code-server/releases/download/3.4.1/code-server-3.4.1-linux-x86_64.tar.gz
```

# 2. 解压安装

适用 `tar` 命令解压到指定目录
```bash
[root@localhost ~]# tar -zxvf code-server-3.4.1-linux-x86_64.tar.gz -C /opt/
[root@localhost ~]# cd /opt
[root@localhost opt]# mv code-server-3.4.1-linux-x86_64 code-server
```

# 3. 配置code-server

配置ip允许外部ip访问，端口默认8080，配置用户主目录和插件目录，修改密码
```bash
[root@localhost opt]# cd code-server
[root@localhost code-server]# mkdir data extensions
[root@localhost code-server]# vim config.yaml  # 配置文件
bind-addr: 0.0.0.0:8080
auth: password
password: 123456
cert: false
user-data-dir: /opt/code-server/data/
extensions-dir: /opt/code-server/extensions/ 
```

# 4. 启动

执行code-server启动服务
```bash
[root@localhost code-server]# ./code-server --config /opt/code-server/config.yaml
***** Please use the script in bin/code-server instead!
***** This script will soon be removed!
***** See the release notes at https://github.com/cdr/code-server/releases/tag/v3.4.0
info  Using config file /opt/code-server/config.yaml
info  Using user-data-dir /opt/code-server/data
info  code-server 3.4.1 48f7c2724827e526eeaa6c2c151c520f48a61259
info  HTTP server listening on http://0.0.0.0:8080
info      - Using password from /opt/code-server/config.yaml
info      - To disable use `--auth none`
info    - Not serving HTTPS
```

> 打开浏览器，输入 http://127.0.0.1:8080 输入密码即可使用

# 5. 创建启动、重启和关闭脚本

创建pid存储文件
```bash
[root@localhost code-server]# cd bin
[root@localhost bin]# touch code-server.pid
[root@localhost bin]# chmod 666 code-server.pid
```

创建启动脚本

```bash
[root@localhost bin]# vim start.sh
```

```bash
#!/usr/bin/bash

# 判断pid是否存在
if_exists_pid(){
    if [ -s /opt/code-server/bin/code-server.pid ]; then
        return 0
    else
        return 1
    fi
}

# 停止服务
stop_server(){
    pid=$(cat /opt/code-server/bin/code-server.pid)
    kill -9 $pid && echo -n '' > /opt/code-server/bin/code-server.pid
    echo "code-server is stoped"
    return 0
}

# 启动服务
start_server(){
    nohup /opt/code-server/lib/node /opt/code-server --config /opt/code-server/config.yaml >> /opt/code-server/data/logs/code-server.log 2>/opt/code-server/data/logs/error.log &
    jobs -l | grep -e '\[[[:digit:]]\]+' | grep code-server | awk '{ print $2 }' > /opt/code-server/bin/code-server.pid
    echo 'code-server is started'
    return 0
}

# 启动
if if_exists_pid; then
    echo 'code-server is running'
else
    start_server
fi
```

创建重启脚本

```bash
[root@localhost bin]# vim restart.sh
```

```bash
#!/usr/bin/bash

# 判断pid是否存在
if_exists_pid(){
    if [ -s /opt/code-server/bin/code-server.pid ]; then
        return 0
    else
        return 1
    fi
}

# 停止服务
stop_server(){
    pid=$(cat /opt/code-server/bin/code-server.pid)
    kill -9 $pid && echo -n '' > /opt/code-server/bin/code-server.pid
    echo "code-server is stoped"
    return 0
}

# 启动服务
start_server(){
    nohup /opt/code-server/lib/node /opt/code-server --config /opt/code-server/config.yaml >> /opt/code-server/data/logs/code-server.log 2>/opt/code-server/data/logs/error.log &
    jobs -l | grep -e '\[[[:digit:]]\]+' | grep code-server | awk '{ print $2 }' > /opt/code-server/bin/code-server.pid
    echo 'code-server is started'
    return 0
}

# 重启
if if_exists_pid; then
    stop_server
    sleep 5
    start_server
else
    start_server
fi
```

创建关闭脚本

```bash
[root@localhost bin]# vim stop.sh
```

```bash
#!/usr/bin/bash

# 判断pid是否存在
if_exists_pid(){
    if [ -s /opt/code-server/bin/code-server.pid ]; then
        return 0
    else
        return 1
    fi
}

# 停止服务
stop_server(){
    pid=$(cat /opt/code-server/bin/code-server.pid)
    kill -9 $pid && echo -n '' > /opt/code-server/bin/code-server.pid
    echo "code-server is stoped"
    return 0
}

# 启动服务
start_server(){
    nohup /opt/code-server/lib/node /opt/code-server --config /opt/code-server/config.yaml >> /opt/code-server/data/logs/code-server.log 2>/opt/code-server/data/logs/error.log &
    jobs -l | grep -e '\[[[:digit:]]\]+' | grep code-server | awk '{ print $2 }' > /opt/code-server/bin/code-server.pid
    echo 'code-server is started'
    return 0
}

# 关闭
if if_exists_pid; then
    stop_server
else
    echo 'code-server is not running'
fi
```

# 6. 配置开机自启动

配置systemd服务，利用systemctl进行服务管理

```bash
[root@localhost bin]# vim /usr/lib/systemd/system/code-server.service
```

```bash
[Unit]
Description=code-server - Run VS Code on any machine anywhere and access it in the browser.

After=network.target remote-fs.target nss-lookup.target

[Service]
Type=forking
ExecStart=/opt/code-server/bin/start.sh
ExecReload=/opt/code-server/bin/restart.sh
ExecStop=/opt/code-server/bin/stop.sh
User=leo
Group=leo

[Install]
WantedBy=multi-user.target
```

重载服务配置

```bash
[root@localhost bin]# systemctl daemon-reload
```

开机自动启动


启动服务

```bash
[root@localhost bin]# systemctl enable code-server
```

```bash
[root@localhost bin]# systemctl start code-server
```

