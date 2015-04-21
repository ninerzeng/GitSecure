import re
import os
import subprocess

#	mysql or mysqli ( <any argument> , <any argument> <any string argument> )
regex = r"""\bmysql(i)?(_connect)?\([^,]{2,25}?,[^,]{2,25}?,\s*[\'\"][^\'\"]+[\'\"]\s*\)"""
#regex = r"""test"""

cmd = "grep -E \"" + regex + "\" test.txt"

process = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
temp = process.communicate()

print temp
