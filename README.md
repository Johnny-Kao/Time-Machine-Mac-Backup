# 自动备份脚本

## 简介

本脚本可达成MAC OS系统电脑，定期将本地指定资料夹，备份到远端服务器。

备份方式采用增量备份，使用了[Rsync-time-backup](https://github.com/laurent22/rsync-time-backup)脚本，可以依照时间点回滚回复，与Timemachine达成同样的备份效果。

## 系统环境

* MAC OS 10.11 以上
* Python3.7.0 以上
* 远端服务器与本机需先配置免密登录SSH

## 设定方式

1. 复制专案到本地

`git clone https://github.com/Johnny-Kao/Time-Machine-Mac-Backup.git`

2. 复制备份脚本Rsync_tmbackup.sh到本地

`cp Time-Machine-Mac-Backup/rsync_tmbackup.sh /usr/local/bin/rsync_tmbackup.sh`

3. 赋予执行权限

`chmod +x /usr/local/bin/rsync_tmbackup.sh`

4. 设定远端与服务端免密登录

[Linux SSH免密登录](https://www.jb51.net/article/163093.htm)

5. 设定排除备份清单 - 参考项目中档案Exclude.txt格式

设定基本参数 - 修改Backup.py

```
# Log路径/名称
log_path = 'YOUR PATH HERE'

# WIFI白名单 - 判定是否为指定局域网
wifi_list = ['YOUR WIFI SSID HERE', 'YOUR WIFI SSID HERE', 'YOUR WIFI SSID HERE']

# 备份主程序路径/不备份路径（排除清单）
exe_path = '/usr/local/bin/rsync_tmbackup.sh'
exclude_list_path = 'YOUR EXCLUDE TXT FILE HERE'

# 远端服务器ip/远端服务器使用者（需要设定远端免密登录）
only_sync_in_local = "F" # 是否强制局域网更新？ T/F
remote_ip_internal = 'INTERNAL IP - EX. 192.168.0.1' # 局域网IP
remote_ip_external = 'EXTERNAL IP - EX. 143.10.10.10' # 公网IP
remote_user = 'YOUR NAS REMOTE SERVER NAME'

# 备份路径[本地，远端]
backup_path = [
    ['LOCAL SOURCE, EX. ~/Downloads','REMOTE DEST, EX. /volume3/NAS/MacAirBackup/Downloads/'],
    ['LOCAL SOURCE, EX. ~/Downloads','REMOTE DEST, EX. /volume3/NAS/MacAirBackup/Downloads/']
]
```

首次执行

`python3 Backup.py`

首次运行请先参考log档案

```
# 你会发现log中含有下列的指令，如果你有10个备份路径，log中就会有10个指令。请依照您的设定，依序在本机执行。

ssh -p 22 远端服务器账户@远端服务器IP 'mkdir -p -- "/volume3/NAS/MacAirBackup/Downloads" ; touch "/volume3/NAS/MacAirBackup/Downloads/backup.marker"'

```

添加定期备份功能

`crontab -e`



## 待开发清单

* 复原功能 - 定期、手动