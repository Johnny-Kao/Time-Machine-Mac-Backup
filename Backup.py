#!/usr/bin/python
# -*- coding: UTF-8 -*-

import time
import os

# 固定参数
begin_time_formatted = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
start_time = time.time()

# Log路径/名称
log_name = time.strftime('%Y%m%d_%H%M%S', time.localtime()) + '.log'# YYYY/MM/DD_HHMMSS.log
log_path = 'YOUR PATH HERE'

# WIFI白名单 - 判定是否为指定局域网
wifi_list = ['YOUR WIFI SSID HERE', 'YOUR WIFI SSID HERE', 'YOUR WIFI SSID HERE']

# 备份主程序路径/不备份路径（排除清单）
exe_path = 'THE PATH OF YOUR rsync_tmbackup.sh HERE'
exclude_list_path = 'YOUR EXCLUDE TXT FILE HERE'
    # ===== Example Content Format ======== #
    # - /Users/JK/Documents/Axure User Data
    # - /Users/JK/Documents/Rsync_log

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

# Python呼叫Shell指令
def cmd_exe(cmd):
    os.system(cmd)

# 取得当前WIFI连接名称 - MAC OS
def get_ssid():
    cmd = '/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -I | sed -e "s/^  *SSID: //p" -e d'
    # return example 'GuoAP\n'
    res = os.popen(cmd).read()
    return res[:-1:]

# 调用MAC OS系统通知
def mac_notify(title, text1, text2=""):
    os.system("""
              osascript -e 'display notification "{}{}" with title "{}"'
              """.format(text1, text2, title))

# 计算指令执行时间
def timer(start_time):
    # require start time
    exp = time.time() - start_time
    return round(exp,2)

# 备份指令
def backup_cmd_execute(exe_path, exclude_list_path, remote_ip, remote_user, backup_source, backup_dest, log_path, log_name):
    cmd = exe_path + " " + backup_source + " " + remote_user + "@" + remote_ip + ":" + backup_dest + " " + exclude_list_path + ">> " + log_path + log_name + " 2>&1"
    cmd_exe(cmd)

def recovery():
    print('Please check example')
    # rsync -aP /backup/2017-04-29-080002/etc/ /etc
    # NOT YET FINISH

# 在局域网内，直接更新且标记为局域网；否则标记为公网后，判定是否强制在局域网内更新，如果否，则询问是否继续备份。
if get_ssid() in wifi_list:
    final_choice = "T"
    external_or_internal = "I"
else:
    external_or_internal = "E"
    if only_sync_in_local == "T":
        final_choice = "F"
    else:
        select = input("当前电脑不在局域网，是否继续备份？输入Y继续...")
        if select.upper() == "Y":
            final_choice = "T"
        else:
            final_choice = "F"


if final_choice == "F":
    mac_notify("备份失败","当前Wifi名称：" + get_ssid(),"。请连接指定Wifi备份。")
        
    cmd = "echo " + "\"备份失败，请连接指定Wifi备份。\"" + " >> " + log_path + log_name 
    cmd_exe(cmd)   

else:
    # 指定局域/广域IP
    if external_or_internal == "I":
        remote_ip = remote_ip_internal
    else:
        remote_ip = remote_ip_external

    print(remote_ip)
    # 开始备份
    mac_notify("备份开始","当前Wifi名称：" + get_ssid(),"\n本次备份路径数量：" + str(len(backup_path)))
    print(log_path + log_name )
    tmp_text = "备份时间开始：" + begin_time_formatted + " 本次备份路径数量：" + str(len(backup_path))
    cmd = "echo " + "\"" +tmp_text + "\"" + " >> " + log_path + log_name 
    cmd_exe(cmd)

    #项目备份
    for item in range(len(backup_path)):
        project_start_time = time.time()
        project_start_time_style = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        # mac_notify("备份进度", "本地路径：" + str(backup_path[item][0]), "\n远端路径：" + str(backup_path[item][1]))

        tmp_text = "===========================================\n" +"备份时间开始：" + project_start_time_style + " 本地路径：" + str(backup_path[item][0]) + "。远端路径：" + str(backup_path[item][1])
        cmd = "echo " + "\"" + tmp_text + "\"" + " >> " + log_path + log_name 
        cmd_exe(cmd)

        # 依序执行

        backup_cmd_execute(exe_path, exclude_list_path, remote_ip, remote_user, backup_path[item][0], backup_path[item][1], log_path, log_name)

        tmp_text = "备份时间花费时间：" + str(timer(project_start_time)) + "秒"
        cmd = "echo " + "\"" + tmp_text + "\"" + " >> " + log_path + log_name 
        cmd_exe(cmd)

    # 备份结束
    mac_notify("备份结束","备份总花费时间：" + str(timer(start_time))) + "秒"
    
    tmp_text = "===========================================\n" + "备份总花费时间：" + str(timer(start_time)) + "秒"
    cmd = "echo " + "\"" +tmp_text + "\"" + " >> " + log_path + log_name 
    cmd_exe(cmd)