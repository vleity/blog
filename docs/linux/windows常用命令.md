

## 查看端口占用

```basic
> netstat -aon | findstr 445
  TCP    0.0.0.0:445            0.0.0.0:0              LISTENING       4
  TCP    127.0.0.1:57445        127.0.0.1:57446        ESTABLISHED     9864
  TCP    127.0.0.1:57446        127.0.0.1:57445        ESTABLISHED     9864
  TCP    127.0.0.1:65445        127.0.0.1:65446        ESTABLISHED     41020
  TCP    127.0.0.1:65446        127.0.0.1:65445        ESTABLISHED     41020
  TCP    172.20.218.86:445      172.20.218.86:52569    ESTABLISHED     4
  TCP    172.20.218.86:52569    172.20.218.86:445      ESTABLISHED     4
  TCP    [::]:445               [::]:0                 LISTENING       4
```



## 查看进程

```basic
tasklist /FI "PID eq 4"
```

