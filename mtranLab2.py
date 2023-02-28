import re


def tokenize(code):
    token_specification = [
    ('INCLUDE',     r'#include'), 
    ('HEADER',      r'<.*?>'),  
    ('NAMESPACE',   r'using\s+namespace\s+std;'), 
    ('TYPE',        r'int|float'),
    ('KEYWORD',     r'cin|cout|main|return|break|case|switch|default|endl|for|while|pow'),
    
    ('NAME',        r'[a-zA-Z0-9_.]+'),
    ('STREAM',      r'<<|>>'), 
    ('STRING',      r'"[^"]*"'), 
    ('OP',          r'[+\-*/=<>!]'),      
    ('PUNCT',       r'[,.:;(){}]'),  
    ('WHITESPACE',  r'\s+'),    
    ('MISMATCH',    r'')
    
    ]
    errors = []
    veriables= {}
    keywords = []
    operations = []
    t=0
    dataType=''
    ver=0
    curVer=''
    aply=0
    oper=0
    vivod=0
    idver=0
    
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        
        if kind == 'WHITESPACE':
            pass
        elif kind == 'NAME':
            if re.match(r'^[0-9][a-zA-Z0-9_.]*$',value):
                if re.match(r'^\d+\.\d+$',value):
                    if aply == 1 and oper != 1:
                        veriables[idver] = {'Тип данных':f'{dataType}','Переменная':f'{curVer}','Значение':f'{value}'}
                        aply=0
                    yield 'FLOATNEW', value
                elif re.match(r'^\d+$',value):
                    if aply == 1 and oper != 1:
                        veriables[idver] = {'Тип данных':f'{dataType}','Переменная':f'{curVer}','Значение':f'{value}'}
                        aply=0
                    yield 'INTNEW', value
                else:
                    errors+=('MISMATCH_ID',value)
                    yield 'ТЫ ЧТО НАТВОРИЛ, СМОТРИ СЮДА =>', value
            elif t == 1:
                curVer=value
                ver+=1
                idver=ver
                veriables[idver] = {'Тип данных':f'{dataType}','Переменная':f'{value}','Значение':'0'}
                yield kind, value
            elif t == 0:
                gg=0
                keys = list(veriables.keys())
                for key, val in veriables.items():
                    if val['Переменная'] == value:
                        idver= keys.index(key)+1
                        gg+=1
                if gg == 0:
                    errors+=('MISMATCH_ID',value)
                    yield 'ТЫ ЧТО НАТВОРИЛ, СМОТРИ СЮДА =>', value
                else:
                    curVer=value
                    yield kind, value
            else:
                pass
        elif kind == 'TYPE':
            if t == 0:
                t=1
                dataType=value
            yield kind, value
        elif kind == 'PUNCT':
            if value == ',':
                t=1
            else:
                t=0
            oper=0
            aply=0
            yield kind, value
        elif kind == 'OP':
            operations+=(value)
            if value == '=':
                aply=1
            else:
                if value == '<' or value == '>' or value == '!':
                    oper=1
                aply=0
            
            yield kind, value
        elif kind == 'KEYWORD':
            keywords+=(kind,value)
            yield kind, value
        elif kind == 'MISMATCH':
            errors+=(kind,value)
            print("______ERRORS______")
            for i in range(len(errors)):
                if i==len(errors)-1 or i == len(errors)-2:
                    pass
                else:
                    print("|",errors[i]," "*(13-len(errors[i])),"|")
                    if i%2 != 0:
                        print("------------------")
            print("___________________________Stored_Veriables___________________________")
            for key in veriables:
                print("| ",veriables[key])
            print()
            nonoperation = list(set(operations))
            print("____Operations____")
            for i in range(len(nonoperation)):
                print("|        ",nonoperation[i]," "*(6-len(nonoperation[i])),"|")
                print("------------------")
            print()
            print("____Key_Words_____")
            nonduplicate = list(set(keywords))
            for i in range(len(nonduplicate)):
                if nonduplicate[i] != 'KEYWORD':
                    print("|     ",nonduplicate[i]," "*(9-len(nonduplicate[i])),"|")
                    print("------------------")
        else:
            yield kind, value

with open('IncorLexC++.txt', 'r') as file:
    code = file.read()

for token in tokenize(code):
    print(token)
