# -*- coding: utf-8 -*-
"""
Created on Wed Jul 18 17:12:33 2018

@author: kaolafm
"""

import random
from datetime import datetime 

def readFile(filepath):
    result = []
    with open(filepath, 'r', encoding = 'utf-8', errors = 'ignore') as f:
        for line in f.readlines():
            line = line.strip()
            if line == '':
                continue
            result.append(line)
    result.append('')
    return result
                

def generateCorpus(total):
    mycount = 0
    with open('corpus.json', 'a', encoding = 'utf-8', errors = 'ignore') as fw:
        head = '''
{
  "rasa_nlu_data": {
    "regex_features": [],
    "entity_synonyms": [],
    "common_examples": [
'''
        fw.write(head)
        with open('config.txt','r', encoding = 'utf-8', errors = 'ignore') as fr:
            lines = fr.readlines()
            for line in lines:
                data = []
                entity_name = {}
                line = line.strip()
                linelist = line.split('|')
                tmpintent = linelist[0]
                components = linelist[1].split('#')
                for i in range(len(components)):
                    if '@' in components[i]:
                        entity_name[str(i)] = components[i].split('@')[0] 
                        data.append(readFile(components[i].split('@')[1]))
                    else:
                        data.append(readFile(components[i]))
                tmptotal = total / len(lines)
                for count in range(int(tmptotal)):
                    tmpcon = ''
                    text = '   "text": "'
                    intent = '        "intent": "' + tmpintent + '",\n'
                    entities = '        "entities": [\n'
                    e_i = 0
                    pos = 0
                    for i in range(len(data)):
                        if i > 0:
                            text += ' '
                            pos += 1
                        tmptext = data[i][random.randint(0,len(data[i]) - 1)]
                        pos += len(tmptext)
                        text += tmptext
                        if str(i) in entity_name.keys():
                            start = pos - len(tmptext)
                            end = pos
                            if e_i > 0:
                                entities += ',\n'
                            entities += '            {"end": ' + str(end) + ', "entity": "' + entity_name[str(i)] + '", "start": ' + str(start) + ', "value": "' + tmptext + '"}'
                            e_i += 1
                    entities += '\n        ]\n'
                    text += '",\n'
                    if count > 0:
                        tmpcon += ',\n'
                    tmpcon += '    {' + text + intent + entities + '    }'
                    fw.write(tmpcon)
                    mycount += 1
                    if mycount % 1000 == 0:
                        print('已生成 ' + str(mycount) + ' 条数据')
                    
        tail = '''
    ]
  }
}
        '''
        fw.write(tail)
            
t1 = datetime.now()     
generateCorpus(1000000)
t2 = datetime.now()
print('总用时 ' + str((t2 - t1).seconds) + ' 秒')