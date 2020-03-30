# -*- coding: utf-8 -*-
# @Author: Xi He
# @Date:   2020-03-08 17:16:33
# @Last Modified by:   Xi He
# @Last Modified time: 2020-03-30 18:09:46

def reverseDict(dic):
    inv_map = dict()
    for k, v in dic.items():
        inv_map[v] = inv_map.get(v, [])
        inv_map[v].append(k)
    return inv_map

class CONSTANT(object):
    def __init__(self):
        pass

    @staticmethod
    def tone_to_semisteps():
        return {'C' :0, 'C#':1, 'Db':1, 'D' :2, 
                'D#':3, 'Eb':3, 'E' :4, 'F' :5, 
                'F#':6, 'G' :7, 'G#':8, 'Ab':8,
                'A' :9, 'A#':10,'Bb':10,'B' :11}
                
    @staticmethod
    def semisteps_to_tone():
        return reverseDict(CONSTANT.tone_to_semisteps())

    @staticmethod
    def tone_to_steps():
        return {'C':1, 'D':2, 'E':3, 'F':4, 'G':5, 'A':6, 'B':7}

    @staticmethod
    def steps_to_tone():
        return reverseDict(CONSTANT.tone_to_steps())

    @staticmethod
    def accidental_to_step():
        return {'b':-1, '#':1}

    @staticmethod
    def interval_to_semisteps():
        return {'P1':0,     'A1':1, 
                  'd2':0,     'm2':1,     'M2':2,     'A2':3,
                  'd3':2,     'm3':3,     'M3':4,     'A3':5, 
                  'd4':4,     'P4':5,     'A4':6, 
                  'd5':6,     'P5':7,     'A5':8,  
                  'd6':7,     'm6':8,     'M6':9,     'A6':10,
                  'd7':9,     'm7':10,    'M7':11,    'A7':12,
                  'd8':11,    'P8':12,    'A8':13, 
                  'd9':12,    'm9':13,    'M9':14,    'A9':15, 
                  'd10':14,   'm10':15,   'M10':16,   'A10':17,
                  'd11':16,   'P11':17,   'A11':18, 
                  'd12':18,   'P12':19,   'A12':20,
                  'd13':19,   'm13':20,   'M13':21,   'A13':22,
                  'd14':21,   'm14':22,   'M14':23,   }

    @staticmethod
    def semisteps_to_interval():
        return reverseDict(CONSTANT.interval_to_semisteps())

    @staticmethod
    def interval_name_mapping():
        return {'P': 'Perfect', 'd': 'Diminished',
                'm': 'Minor',   'M': 'Major',      'A': 'Augmented'}

    @staticmethod
    def chord_recipes():
        return {''         : ['P1', 'M3', 'P5'],
                'm'        : ['P1', 'm3', 'P5'],
                'dim'      : ['P1', 'm3', 'd5'],
                'aug'      : ['P1', 'M3', 'A5'],

                '7'        : ['P1', 'M3', 'P5', 'm7'],
                'm7'       : ['P1', 'm3', 'P5', 'm7'],
                'maj7'     : ['P1', 'M3', 'P5', 'M7'],
                'dim7'     : ['P1', 'm3', 'd5', 'd7'],
                'm7b5'     : ['P1', 'm3', 'd5', 'd7'],
                'mmaj7'    : ['P1', 'm3', 'P5', 'M7'],
                'aug7'     : ['P1', 'M3', 'A5', 'm7'],
                'aug-maj7' : ['P1', 'M3', 'A5', 'M7'],
                '7b5'      : ['P1', 'M3', 'd5', 'm7'],
                '7#5'      : ['P1', 'M3', 'A5', 'm7'],

                'm9'       : ['P1', 'm3', 'P5', 'm7', 'M9'],
                'add9'     : ['P1', 'M3', 'P5', 'M9'],

                'sus2'     : ['P1', 'M2', 'P5'],
                'sus4'     : ['P1', 'P4', 'P5'],

                'user'     : []
                }

    @staticmethod
    def alter_recipes():
        return {'power5'   : ['P1', 'P5'],
                'add2'     : ['M9'],
                     }


def warning(message, style='WARNING'):
    CRED = '\033[91m'
    CEND = '\033[0m'
    print(CRED + style + ':' + CEND, message)

def suf(n):
    return "%d%s"%(n,{1:"st",2:"nd",3:"rd"}.get(n if n<20 else n%10,"th"))

def eqList(lst1, lst2):
    return lst1 == lst2