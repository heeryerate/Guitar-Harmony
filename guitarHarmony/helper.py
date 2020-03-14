# -*- coding: utf-8 -*-
# @Author: Xi He
# @Date:   2020-03-08 17:16:33
# @Last Modified by:   Xi He
# @Last Modified time: 2020-03-08 17:24:56
def reverseDict(dic):
	inv_map = dict()
	for k, v in dic.items():
		inv_map[v] = inv_map.get(v, [])
		inv_map[v].append(k)
	return inv_map