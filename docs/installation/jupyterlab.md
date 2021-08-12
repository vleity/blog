# jupyterlab 3.0.12

# 虚拟环境

```
[root@orig_02 ~]# useradd jupyter
[root@orig_02 ~]# cd /opt
[root@orig_02 opt]# virtualenv --python /usr/bin/python3 jupyter 
Already using interpreter /usr/bin/python3
Using base prefix '/usr'
  No LICENSE.txt / LICENSE found in source
New python executable in /opt/jupyter/bin/python3
Also creating executable in /opt/jupyter/bin/python
Installing setuptools, pip, wheel...
done.
[root@orig_02 opt]# chown jupyter:jupyter -R jupyter/
```

# pip 安装 jupyterlab

```
[root@orig_02 opt]# su - jupyter
[jupyter@orig_02 ~]$ mkdir ~/.pip/
[jupyter@orig_02 ~]$ vim ~/.pip/pip.conf
[global]
index-url = https://pypi.tuna.tsinghua.edu.cn/simple
[install]
trusted-host = https://pypi.tuna.tsinghua.edu.cn

[jupyter@orig_02 ~]$ cd /opt/jupyter/
[jupyter@orig_02 jupyter]$ . bin/activate
(jupyter) [jupyter@orig_02 jupyter]$ pip install ipython jupyterlab
```

# 配置 jupyterlab

## 创建数据目录，存放 notebook

```
(jupyter) [jupyter@orig_02 jupyter]$ mkdir ~/jupyter_data
```

## 创建密钥

```
(jupyter) [jupyter@orig_02 jupyter]$ ipython
Python 3.6.8 (default, Apr  2 2020, 13:34:55)
Type 'copyright', 'credits' or 'license' for more information
IPython 7.16.1 -- An enhanced Interactive Python. Type '?' for help.

In [1]: from jupyter_server.auth import passwd

In [2]: passwd()
Enter password:
Verify password:
Out[2]: 'sha1:ad6c32a53587:eb16047e02c0820d114b84ffe6621d280840c10b'
```

## 生成jupyterlab配置文件

```
(jupyter) [jupyter@orig_02 jupyter]$ jupyter lab --generate-config
Writing default config to: /home/jupyter/.jupyter/jupyter_lab_config.py
(jupyter) [jupyter@orig_02 jupyter]$ vim /home/jupyter/.jupyter/jupyter_lab_config.py
# notebook目录
c.ServerApp.notebook_dir = '/home/jupyter/jupyter_data'
# 将ip设置为0.0.0.0，允许远程访问
c.ServerApp.ip = '0.0.0.0'
# 这里的密码填写上面生成的密钥
c.ServerApp.password = 'sha1:ad6c32a53587:eb16047e02c0820d114b84ffe6621d280840c10b' 
# 禁止用host的浏览器打开jupyter
c.ServerApp.open_browser = False 
# 监听端口设置为8888或其他
c.ServerApp.port = 8888
# 允许远程访问 
c.ServerApp.allow_remote_access = True
```

## 启动服务

```
(jupyter) [jupyter@orig_02 jupyter]$ jupyter-lab
```

## systemd 管理

```
vim /usr/lib/systemd/system/jupyterlab.service
```

```
[Unit]
Description=jupyterlab
After=network.target

[Service]
User=jupyter
Group=jupyter
Type=simple
# ExecStartPre=
ExecStart=/opt/jupyter/bin/python /opt/jupyter/bin/jupyter-lab
# ExecReload=
# ExecStop=

PrivateTmp=True

[Install]
WantedBy=multi-user.target
```

```
systemctl daemon-reload
systemctl enable jupyterlab
```

