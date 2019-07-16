#!/usr/bin/env python

import logging
import os
import subprocess
import sys

logging.basicConfig(format='Local Exec: %(message)s', level=logging.ERROR)

try:
    cmd_name = sys.argv.pop(1)
except IndexError as e:
    logging.error("No command provided")
    sys.exit(1)

try:
    cmd_arg = sys.argv.pop(1)
except Exception as e:
    logging.error("No option to command provided")
    sys.exit(1)

cmd_args = sys.argv[1:]


def get_path(arg):
    try:
        std_out = subprocess.check_output("readlink -f $(which " + arg + ")", shell=True).rstrip()
        return std_out
    except Exception as e:
        return "Error on stat operation on: " + arg


def get_env_var(arg):
    try:
        std_out = os.environ[arg]
        return std_out
    except KeyError as e:
        return "Environment variable: " + arg + " not set"


def get_sys_val(arg, *args):
    match_patterns = args
    try:
        with open(arg, 'r') as f:
            file_lines = f.read().split('\n')
    except IOError as e:
        return "Cannot read file: " + arg
    matched_lines = [x for x in file_lines if any(w in x for w in match_patterns)]
    std_out = '\n'.join(matched_lines)
    return std_out


if cmd_name == 'real_path':
    cmd_std_out = get_path(cmd_arg)
    print("%s" % cmd_std_out)

elif cmd_name == 'env_var':
    cmd_std_out = get_env_var(cmd_arg)
    print("%s" % cmd_std_out)

elif cmd_name == 'sys_value':
    cmd_std_out = get_sys_val(cmd_arg, *cmd_args)
    print("%s" % cmd_std_out)

else:
    logging.error("Unknown command")
    sys.exit(1)

#    """
#     Very Simple COMMAND reference
#    
#      "real_path"
#       USAGE: [path], path
#         path, java
#         path, ansible
#    
#      "env_var"
#        USAGE: [env_var], variable_name
#          env_var, HOME
#          env_var, LANG
#          env_var, PATH
#    
#      "sys_value" (reads proc, sys, etc)
#       USAGE: [sys_value], path, attribute
#         value, /proc/meminfo, MemFree 
#         value, /sys/devices/system/cpu/vulnerabilities/meltdown, Mitigation
#         value, /etc/java/java.conf, JAVA_HOME
#        
#      "system_stat"
#       USAGE: [system], command (all comments and whitespace are removed and a list of arrays returned)
#         system, uptime
#         system, load
#        
#    
#      "any" (all comments and whitespace are removed and a list of arrays returned)
#       USAGE: [any], cmd, arg1, arg2 ...
#         any, uname, -r
#         any, free, -h
#        
#    """
#


#                                     EXTRA REFERENCE
#######################################################################################


# Alternative method using list comprehension
# def getSysVal(arg, *args):
#    match_patterns = args
#
#    with open(arg, 'r') as f:
#       file_lines = f.read().split('\n')
#
#    matched_lines = []
#    for l in file_lines:
#        print("Checking: " + l)
#        if any(xs in l for xs in match_patterns):
#            matched_lines.append(l)
#
#    std_out =  matched_lines
#    return std_out


# cmd = "ps -A|grep 'process_name'"
# ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
# output = ps.communicate()[0]
# print output


# ls_lines = subprocess.check_output(['ls', '-l']).splitlines()


# import subprocess
# child = subprocess.Popen('command',stdout=subprocess.PIPE,shell=True)
# output = child.communicate()[0]


# import platform
# platform.uname()
# ('Linux', 'fedora.echorand', '3.7.4-204.fc18.x86_64', '#1 SMP Wed Jan 23 16:44:29 UTC 2013', 'x86_64')
# 
# platform.uname().system
# 'Linux'
# 
# platform._supported_dists
# ('SuSE', 'debian', 'fedora', 'redhat', 'centos', 'mandrake',
# 'mandriva', 'rocks', 'slackware', 'yellowdog', 'gentoo',
# 'UnitedLinux', 'turbolinux')
#


# fcntl.fcntl(
#     proc.stdout.fileno(),
#     fcntl.F_SETFL,
#     fcntl.fcntl(proc.stdout.fileno(), fcntl.F_GETFL) | os.O_NONBLOCK,
# )
# and then using select to test if the data is ready
# 
# while proc.poll() == None:
#     readx = select.select([proc.stdout.fileno()], [], [])[0]
#     if readx:
#         chunk = proc.stdout.read()
#         print chunk
# 
#
