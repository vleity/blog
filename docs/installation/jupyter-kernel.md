### 安装C内核
```shell
# 安装C内核,一下必须已安装
# gcc
# jupyter
# python3
# pip

(jupyterenv)[leo@orig01 ~]# pip install jupyter-c-kernel

# 将C内核安装到虚拟环境中去，指定虚拟环境的目录
(jupyterenv)[leo@orig01 ~]# install_c_kernel --prefix /home/leo/jupyterenv

# 启动jupyter
(jupyterenv)[leo@orig01 ~]# jupyter-lab

```

### 安装R内核
```R
# 我是用root用户安装的，非root用户能否安装？

R> install.packages(c('repr'))
R> install.packages(c('IRdisplay'))
R> install.packages(c('evaluate'))
R> install.packages(c('crayon'))
R> install.packages(c('pbdZMQ'))
R> install.packages(c('devtools'))
R> install.packages(c('uuid'))
R> install.packages(c('digest'))


install.packages(c('repr', 'IRdisplay', 'evaluate', 'crayon', 'pbdZMQ', 'devtools', 'uuid', 'digest'))


R> devtools::install_github('IRkernel/IRkernel')

# 只在当前用户下安装
R> IRkernel::installspec()
# 或者是在系统下安装
R> IRkernel::installspec(user = FALSE)


# 非root用户
# 安装到指定虚拟环境
R> IRkernel::installspec(name = 'ir', displayname = 'R 3.6' ,prefix = '/app/www/html/jupyter/env')

```

