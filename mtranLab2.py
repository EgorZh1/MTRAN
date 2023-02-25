import re


def tokenize(code):
    token_specification = [
    ('INCLUDE',     r'#include'), 
    ('HEADER',      r'<.*?>'),  
    ('NAMESPACE',   r'using\s+namespace\s+std;'), 
    ('TYPE',        r'int|float'),
    ('KEYWORD',     r'cin|cout|main|return|break|case|switch|default|endl|pow'),
    
    ('NAME',          r'[a-zA-Z0-9_.]+'),
    ('FLOAT',       r'\d+\.\d+'),
    ('INT',         r'\d+'),
    ('STREAM',      r'<<|>>'), 
    ('STRING',      r'"[^"]*"'), 
    ('OP',          r'[+\-*/=]'),      
    ('PUNCT',       r'[,.:;(){}]'),  
    ('WHITESPACE',  r'\s+'),    
    ('MISMATCH',    r'')
    
    ]
    errors = []
    veriables= {}
    t=0
    dataType=''
    ver=0
    #
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        #print("----------------")
        #print("kind=",kind)
        #print("value=",value)
        #print("----------------")
        if kind == 'WHITESPACE':
            pass
        elif kind == 'NAME':
            if re.match(r'^[0-9][a-zA-Z0-9_.]*$',value):
                if re.match(r'^\d+\.\d+$',value):
                    yield 'FLOATNEW', value
                elif re.match(r'^\d+$',value):
                    yield 'INTNEW', value
                else:
                    errors+=('MISMATCH_ID',value)
                    yield 'ТЫ ЧТО НАТВОРИЛ, СМОТРИ СЮДА =>', value
            elif t == 1:
                veriables[ver] = {'Тип данных':f'{dataType}','Переменная':f'{value}'}
                ver+=1
                yield kind, value
            elif t == 0:
                gg=0
                for i in range(len(veriables)):
                    if value == veriables[i]['Переменная']:
                        gg+=1
                if gg == 0:
                    errors+=('MISMATCH_ID',value)
                    yield 'ТЫ ЧТО НАТВОРИЛ, СМОТРИ СЮДА =>', value
                else:
                    yield kind, value
            else:
                print("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF")
                yield kind, value
        elif kind == 'TYPE':
            if t == 0:
                t=1
                dataType=value
            yield kind, value
        elif kind == 'PUNCT':
            if value == ';':
                t=0
            elif value == '{':
                t=0
            yield kind, value
        elif kind == 'MISMATCH':
            errors+=(kind,value)
            print(errors)
            print("_______________")
            print(veriables)
            #raise RuntimeError(f'{value!r} unexpected')
        else:
            yield kind, value

with open('IncorrectLex.txt', 'r') as file:
    code = file.read()

for token in tokenize(code):
    print(token)
