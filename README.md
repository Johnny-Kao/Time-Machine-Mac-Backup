# 自动备份脚本

## 简介

本脚本可达成MAC OS系统电脑，定期将本地指定资料夹，备份到远端服务器。

备份方式采用增量备份，使用了[Rsync-time-backup](https://github.com/laurent22/rsync-time-backup)脚本，可以依照时间点回滚回复，与Timemachine达成同样的备份效果。

## 系统环境

* MAC OS 10.11 以上
* Python3.7.0 以上
* 远端服务器与本机需先配置免密登录SSH

## 设定方式

复制备份脚本Rsync_tmbackup.sh到本地

赋予执行权限

设定远端与服务端免密登录

设定排除备份清单

设定基本参数

首次执行

添加定期备份功能

## 待开发清单

* 复原功能 - 定期、手动