#!/usr/bin/env python
# -*- coding: utf-8 -*-


#符号类（表示终结符和非终结符）
class Sign(object):
    def __init__(self,sign_type,sign_value = '',sign_line=-1):
        if sign_type == '':
            self.type  = None
        self.type  = sign_type  
        self.value = sign_value
        self.line = sign_line      

    def is_terminal_sign(self):

        if self.type == '':
            return True
        elif self.type in terminal_sign_type:
            return True
        return False

    def is_non_terminal_sign(self):

        if self.type in non_terminal_sign_type:          
            return True
        return False

    def is_empty_sign(self):

        return self.type == ''
        

#语法产生式类
class Production(object):
    def __init__(self, left_type, right_types):

        #Sign
        self.left = Sign(left_type)

        #list(Sign)
        self.right = list()
        for i in right_types:
            self.right.append(Sign(i))

#产生式
productions = [
        #0
        Production('program', ['define-list']),
        #1
        Production('define-list', ['define','define-list']),
        Production('define-list', []),
        #2
        Production('define', ['TYPE','ID','definetype']),
        Production('define', ['STRUCT','id','struct-define']),

        Production('id', ['ID']),
        Production('id', []),
        #3
        Production('definetype', ['var-define']),
        Production('definetype', ['func-define']),
        
        #4
        Production('var-define', ['SEMI']),
        Production('var-define', ['LB','num','RB','SEMI']),
        #5
        Production('func-define', ['LP','params','RP','LC','code-block','RC']),
        Production('struct-define', ['LC','code-block','RC','SEMI']),
        #6
        Production('params', ['param-list']),
        Production('params', []),
        #7
        Production('param-list', ['param','param-follow']),
        #8
        Production('param-follow', ['COMMA','param','param-follow']),
        Production('param-follow', []),
        Production('param-follow', ['SEMI']),
        #9
        Production('param', ['TYPE','ID','array']),
        #10
        Production('array', ['LB','RB']),
        Production('array', []),
        #11
        Production('code-block', ['LC','in-define-list','code-list','RC']),
        Production('code-block', ['in-define-list','code-list']),
        #12
        Production('in-define-list', ['in-var-define','in-define-list',]),
        Production('in-define-list', ['in-struct-define','in-define-list',]),
        Production('in-define-list', []),
        #13
        Production('in-var-define', ['TYPE','ID','in-var-define-follow']),
        Production('in-struct-define', ['STRUCT','ID','id','in-var-define-follow']),
        Production('type', ['TYPE']),
        Production('in-var-define-follow', ['EQUAL','expression','SEMI']),

        Production('in-var-define-follow', ['SEMI']),
        Production('in-var-define-follow', ['COMMA','ID','in-var-define-follow']),

        #14
        Production('code-list', ['code','code-list']),
        Production('code-list', []),
        #15
        Production('code', ['normal-statement']),
        Production('code', ['if-statement']),
        Production('code', ['while-statement']),
        Production('code', ['return-statement']),
        #16
        Production('normal-statement', ['SEMI']),
        Production('normal-statement', ['ID','normal-statement-follow']),
        #17
        Production('normal-statement-follow', ['var-follow','dot','EQUAL','expression','SEMI']),
        
        Production('normal-statement-follow', ['call-follow','SEMI']),
        #18
        Production('var-follow', ['LB','expression','RB']),
        
        Production('var-follow', []),
        #19
        Production('call-follow', ['LP','call-params','RP']),
        #20
        Production('call-params', ['call-param-list']),
        #21
        Production('call-param-list', ['expression','call-param-follow']),
        #22
        Production('call-param-follow', ['COMMA','expression','call-param-follow']),
        Production('call-param-follow', []),
        #23
        Production('if-statement', ['IF','LP','expression','RP','LC','code-list','RC','if-follow']),
        #24
        Production('if-follow', ['ELSE','LC','code-list','RC']),#if else 语句都要加{}
        Production('if-follow', []),

        #25
        Production('while-statement', ['WHILE','LP','expression','RP','while-follow']),
        #26
        Production('while-follow', ['LC','code-list','RC']),
        Production('while-follow', ['code']),
        #27
        Production('return-statement', ['RETURN','return-follow']),
        #28
        Production('return-follow', ['SEMI']),
        Production('return-follow', ['expression','SEMI']),

        #29
        Production('expression', ['add-exp','expression-follow']),
        #30
        Production('expression-follow', ['RELOP','add-exp']),
        Production('expression-follow', ['AND','add-exp']),

        Production('expression-follow', ['EQUAL','add-exp']),
        #Production('expression-follow', ['add-exp']),
        Production('expression-follow', []),
        #31
        Production('add-exp', ['term','add-exp-follow']),
        #32
        Production('add-exp-follow', ['add-op','term','add-exp-follow']),
        Production('add-exp-follow', []),
        #33
        Production('add-op', ['PLUS']),
        Production('add-op', ['MINUS']),
        #34
        Production('term', ['factor','term-follow']),
        #35
        Production('term-follow', ['mul-op','factor','term-follow']),
        Production('term-follow', []),
        #36
        Production('mul-op', ['STAR']),
        Production('mul-op', ['DIV']),
        #37
        Production('factor', ['LP','expression','RP']),
        Production('factor', ['ID','dot','id-factor-follow']),
        Production('dot', ['DOT','ID']),
        Production('dot', []),
        
        Production('factor', ['num']),
        #38
        Production('num', ['INT']),
        Production('num', ['FLOAT']),
        #39
        Production('id-factor-follow', ['var-follow']),
        Production('id-factor-follow', ['LP','args','RP']),
        
        #40
        Production('args', ['arg-list']),
        Production('args', []),
        #41
        Production('arg-list', ['expression','arg-list-follow']),
        #42
        Production('arg-list-follow', ['COMMA','expression','arg-list-follow']),
        Production('arg-list-follow', []),


        #Production('', []),
]

#终结符
terminal_sign_type = [
    'ELSE',
    'IF',
    'TYPE',
    'RETURN',
    'VOID',
    'WHILE',
    'STRUCT',

    'PLUS',
    'MINUS',
    'STAR',
    'DIV',
    'EQUAL',
    'RELOP',
    'AND', 
    'DOT',   
    'SEMI',
    'COMMA',
    'LP',
    'RP',
    'LB',
    'RB',
    'LC',
    'RC',
    'NOT',
    'ID',
    'FLOAT',
    'INT',

    'pound'
]

#非终结符
non_terminal_sign_type = [
    'program',
    'define-list',
    'define',
    'definetype',
    'var-define',
    'specifier',
    'type',
    'id',
    'dot',
    'func-define',
    'struct-define',
    'params',
    'param-list',
    'param-follow',
    'param',
    'array',
    'code-block',
    'in-define-list',
    'in-var-define',
    'in-struct-define',
    'in-var-define-follow',
    'code-list',
    'code',
    'normal-statement',
    'normal-statement-follow',
    'call-follow',
    'call-params',
    'call-param-list',
    'call-param-follow',
    'if-statement',
    'if-follow',
    'while-statement',
    'while-follow',
    'return-statement',
    'return-follow',
    'var-follow',
    'expression',
    'expression-follow',
  
    'add-exp',
    'add-exp-follow',
    'add-op',
    'term',
    'term-follow',
    'mul-op',
    'factor',
    'num',
    'id-factor-follow',
    'args',
    'arg-list',
    'arg-list-follow'
]
grammar_start = Sign('program')
if __name__ =="__main__":
    m = 0
    for production in productions:
        for i in range(len(production.right)):
            if not (production.right[i].is_non_terminal_sign() or production.right[i].is_terminal_sign()):
                print( production.right[i].type)

