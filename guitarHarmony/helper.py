# -*- coding: utf-8 -*-
# @Author: Xi He
# @Date:   2020-03-08 17:16:33
# @Last Modified by:   Xi He
# @Last Modified time: 2020-03-21 12:35:49
def reverseDict(dic):
	inv_map = dict()
	for k, v in dic.items():
		inv_map[v] = inv_map.get(v, [])
		inv_map[v].append(k)
	return inv_map

def warning(message, style='WARNING'):
	CRED = '\033[91m'
	CEND = '\033[0m'
	print(CRED + style + ':' + CEND, message)

def suf(n):
	return "%d%s"%(n,{1:"st",2:"nd",3:"rd"}.get(n if n<20 else n%10,"th"))