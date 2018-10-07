#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from functools import reduce

file_name = "/home/shi/git/bingyan-C-interpreter/source.c"
with open(file_name,'r') as f:
    content = f.read()

#print(content[210:])

TOKEN_STYLE = [
    'KEY_WORDS',
    'OPERATOR',
    'SEPARATOR',
    'INT',      #整数
    'FLOAT',    #浮点数
    'ID',      #标识符

    'DIGIT_CONSTANT',  
    'STRING_CONSTANT',
    'CHAR_CONSTANT'
]





DETAIL_TOKEN = {
    '1':'INT',
    '2': 'FLOAT',
    '3 ':'ID',        #标识符
    #类型
    'int':'TYPE',
    'float':'TYPE',
    #运算符
    '>':'RELOP',
    '<':'RELOP',
    '>=':'RELOP',
    '<=':'RELOP',
    '==':'RELOP',
    '!=':'RELOP',
    #运算
    '+':'PLUS',
    '-':'MINUS',
    '*':'STAR',
    '/':'DIV',
    '=':'EQUAL',
    '&&':'AND',
    '||':'OR',
    '.':'DOT',
    '!':'NOT',    
    # 分隔符  
    ';': 'SEMI',
    ',':'COMMA',
    '(':'LP',
    ')':'RP',
    '[':'LB',
    ']':'RB',
    '{':'LC',
    '}':'RC',
    #关键字
    'for':'FOR',
    'struct':'STRUCT',
    'return':'RETURN',
    'if':'IF',
    'else':'ELSE',
    'while':'WHILE',
    'void':'VOID',

    #add
    '++':'DOPLUS',
    '--':'DOMINUS',
    '-=':'EQMINUS'

}
#关键字
keywords = ( 'int' ,'float','for','if','else','while','void','struct', 'typedef',
        'do', 'double,','enum' ,'extern','goto',
         'long','return', 'signed','sizeof','static'        )
#keywords = ('auto','break','case','char','const' ,'continue' ,'default' ,'do',
 #        'double,','else','enum' ,'extern','float','for','goto','if',
    #     'int' ,'long', 'register' ,'return', 'short', 'signed','sizeof','static',
       #  'struct','switch','typedef','union','unsigned','void','volatile','while')
#运算符        
operaters = ('=', '&','&&','||', '<', '>', '++', '--', '+', '-', '*', '/', '>=', '<=', '!=','|')

# 分隔符
delimiters = ('(', ')', '{', '}', '[', ']', ',', '\"', ';')


class Token(object):
    '''
    0:关键字
    1:运算符
    2:分隔符
    其他,如 整数，浮点数，标识符等
    '''
    #token 生成
    def __init__(self,line,type,value):
        if type in [0,1,2]:
            self.type = DETAIL_TOKEN[value]
        else:
            self.type = TOKEN_STYLE[type]

        self.value = value
        self.line =  line 

class Lexer(object):
    
    #词法分析器
    NOERROR = True    
    def __init__(self):
        self.tokens = []
        self.no_error =True

    #判断空字符
    def isblanki(self,index):       
        return (
            content[index] == ' 'or 
            content[index] == '\n'or
            content[index] == '\t'

        )

    #跳过空字符或者跳指定位置
    def skip(self,index,line):        
        while index <len(content) and self.isblanki(index) != False:
            
            if content[index] =='\n':
                line += 1
               # print("LINE",str(line))
            index += 1
        return index,line

    #判断是否为关键字    
    def iskey(self,value):        
        if value in keywords:
            return True
        return False

    #16进制转换为10进制
    def change16(self,num):        
        self.num = num
        self.total = 0

        for i in range(0,len(self.num)-2): 
         
            if self.num[len(self.num)-i-1].isalpha():
                
            
                self.total += (ord(self.num[len(self.num)-i-1].lower())-87)*16**i
            else:        
                self.total += int(self.num[len(self.num)-i-1])*16**i 
        return self.total

    #8进制转换为10进制
    def change8(self,num):        
        self.num = num
        self.total = 0
        for i in range(0,len(self.num)-1):
     
            if (int( num[len( num)-i-1])>=8):
                return False       
            self.total += int(self.num[len(self.num)-i-1])*8**i 
        return self.total



    def main(self):
        i = 0
        line = 1
        i ,line = self.skip(i,line)
        
        while i<len(content):      

            i ,line = self.skip(i,line)  
            if i<len(content) and content[i] == '#':                
                while content[i] not in ['\n','\r'] and i<len(content):
                    i += 1
                i += 1
                line += 1
                print("已忽略头文件")
                continue
            elif i<len(content) and content[i] == '\n':

                i += 1
                line +=1

            #以字母或下划线开头
            elif i<len(content) and (content[i].isalpha() or content[i] == '_'):                
                temp = ''
                while i<len(content) and (content[i].isalpha() or content[i].isdigit() or content[i] == '_'):
                    #全部读取
                    temp += content[i]
                    i += 1

                #0，关键字
                if self.iskey(temp):                    
                    self.tokens.append(Token(line,0,temp))


                #5,标识符    
                else:                    
                    self.tokens.append(Token(line,5,temp))
                if i<len(content) and content[i] == '.':
                    self.tokens.append(Token(line,1,content[i])) 
                    i += 1
                else:
                    pass

              # #   .25E256  

            #以数字开头  
            elif i<len(content) and content[i].isdigit():
                num = ''

                #以0开头
                if content[i] == '0': 

                    #16进制                   
                    if i<len(content) and content[i+1].lower() == "x":                        
                        i=i+2
                        num += '0x'
                        while i<len(content) and (content[i].isdigit() or content[i].lower() in ('a','b','c','d','e','f')):
                            num += content[i]                                                       
                            i += 1  
                        num = self.change16(num)                       
                        self.tokens.append(Token(line,3,num))
                        if content[i].isalpha():
                            #错误处理1
                            NOERROR = False
                            print("<Error type A at line %s :  '%s'   INT_UNDEFINED reason:不合法的十六进制 如：0xx63,0x5gf >"%(line,num))
                            self.no_error = False
                            #break

                    #8进制        
                    elif i<len(content) and content[i+1].isdigit():                        
                        while i<len(content) and content[i].isdigit():
                            num += content[i]
                            i += 1                        
                        num = self.change8(num)
                        if num == False:
                            NOERROR = False
                            print("<Error type A at line %s :  '%s'   INT_UNDEFINED reason:不合法的八进制数，如: 0936 >"%(line,num)) 
                            self.no_error = False                       
                        self.tokens.append(Token(line,3,num))
                        if content[i].isalpha():
                            #错误处理1
                            NOERROR = False
                            print("<Error type A at line %s :  '%s'   INT_UNDEFINED reason:不合法的八进制数，如: 0936s>"%(line,num))
                            self.no_error = False
                            #break

                    #以0.开头,一定是浮点数
                    elif i<len(content) and content[i+1] =='.': 
                        tempnum = i
                        i += 2
                        num = '0.'

                        #如 0.a
                        if not content[i].isdigit():                            
                            NOERROR = False
                            print("Error type A at line %s :  '%s'   eg.'0.a'"%(line,num)) 
                            self.no_error = False
                            #break
                        haveE = False
                        havePL = False
                        haveMI = False
                        #后期可以做成一个函数

                        while i<len(content) and (content[i].isdigit() or content[i].lower() =='e'
                                                    or content[i] == '+' or content[i] == '-'):
                            
                            num += content[i]
                            i += 1
                        if '+' in num:
                            havePL = True
                        if '-' in num:
                            haveMI =True
                        if 'e' in num or 'E' in num:
                        
                            haveE = True  

                        findplus = num.find('+')
                        findminus = num.find('-')
                        finde   = num.lower().find('e')
                        if haveE:#含e浮点数 以0.开头
                           
                            if havePL and (findplus - finde == 1) and content[tempnum+finde+2].isdigit() and not haveMI:
                                #0.3e+2
                                Index = int(reduce(lambda x,y: x + y,num[findplus:]))                                
                                num = str(float(str(reduce(lambda x,y: x+y,num[0:finde])))*(10**Index))
                                print("0.3e+2=",num)  
                            elif haveMI and (findminus - finde == 1) and content[tempnum+finde+2].isdigit() and not havePL:
                                #0.3e-2
                                Index = int(reduce(lambda x,y: x + y,num[findminus:]))                                
                                num = str(float(str(reduce(lambda x,y: x+y,num[0:finde])))*(10**Index))
                                print("0.3e-2=",num )
                            elif content[tempnum+finde+1].isdigit() and not haveMI and not havePL:
                                #0.3e2
                                Index = int(reduce(lambda x,y: x + y,num[finde+1:]))                                
                                num = str(float(str(reduce(lambda x,y: x+y,num[0:finde])))*(10**Index))
                                print("0.3e2=",num )
                                
                            else:
                                NOERROR = False
                                print("<Error type A at line %s :  '%s'   FLOAT_UNDEFINED>"%(line,num))
                                self.no_error = False
                                #break
                        elif haveMI or havePL:#不含e浮点数，如0.256  ps:暂时不考虑 0.3-5 这种形式
                            NOERROR = False
                            print("<Error type A at line %s :  '%s'   FLOAT_UNDEFINED>"%(line,num))
                            self.no_error = False
                            #break
                        else:
                            
                            pass
                            
                        
                       
                        self.tokens.append(Token(line,4,num)) 

                    elif content[i+1] != ' ' and content[i+1] not in delimiters and content[i+1] not in operaters :
                  
                                             
                        #错误处理2
                        NOERROR = False
                        print("<Error type A at line %s :  '%s'   NUM_UNDEFINED reason:数字之后不是空格、分隔符、运算符>"%(line,num))
                        self.no_error = False
                        i+=1
                    else:
                        #整数0
                        num += content[i]
                        self.tokens.append(Token(line,3,num))
                        i += 1

                else: 
                    #不是以0开头的数
                    
                    tempnum = i

                    haveE = False
                    havePL = False
                    haveMI = False
                    Points = 0
                    while i<len(content) and (content[i].isdigit() or content[i].lower() =='e'
                                                or content[i] == '+' or content[i] == '-'or content[i] == '.'):
                        if content[i] == '.':
                            Points += 1
                        num += content[i]
                        i += 1
                    if Points == 0:
                        #整数
                        for ele in num:
                            if ele in ('e','-','='):
                                NOERROR = False
                                print("<Error type A at line %s :  '%s'   INT_UNDEFINE reason: '2e6' or '2-6' >"%(line,num))

                                self.no_error = False

                        
                        self.tokens.append(Token(line,3,num))                        

                    if Points > 1 or num[i-tempnum -1]== '.':
                        NOERROR = False
                        print("<Error type A at line %s :  '%s'   FLOAT_UNDEFINE reason: '30.' or '23.32.3' >"%(line,num))
                        #break
                    elif Points == 1:
                        if '+' in num:
                            havePL = True
                        if '-' in num:
                            haveMI =True
                        if 'e' in num or 'E' in num:
                        
                            haveE = True  

                        findplus = num.find('+')
                        findminus = num.find('-')
                        finde   = num.lower().find('e')
                        if haveE:#含e浮点数 
                        
                            if havePL and (findplus - finde == 1) and content[tempnum+finde+2].isdigit() and not haveMI:
                                #1.3e+2
                                Index = int(reduce(lambda x,y: x + y,num[findplus:]))                                
                                num = str(float(str(reduce(lambda x,y: x+y,num[0:finde])))*(10**Index))
                                print("0.3e+2=",num)  
                            elif haveMI and (findminus - finde == 1) and content[tempnum+finde+2].isdigit() and not havePL:
                                #1.3e-2
                                Index = int(reduce(lambda x,y: x + y,num[findminus:]))                                
                                num = str(float(str(reduce(lambda x,y: x+y,num[0:finde])))*(10**Index))
                                print("0.3e-2=",num )
                            elif content[tempnum+finde+1].isdigit() and not haveMI and not havePL:
                                #1.3e2
                                Index = int(reduce(lambda x,y: x + y,num[finde+1:]))                                
                                num = str(float(str(reduce(lambda x,y: x+y,num[0:finde])))*(10**Index))
                                print("0.3e2=",num )
                                
                            else:
                                NOERROR = False
                                print("<Error type A at line %s :  '%s'   FLOAT_UNDEFINED>"%(line,num))
                                self.no_error = False
                                #break
                        elif haveMI or havePL:#不含e浮点数，如2.256  ps:暂时不考虑 2.3-5 这种形式
                            NOERROR = False
                            print("<Error type A at line %s :  '%s'   FLOAT_UNDEFINED>"%(line,num))
                            self.no_error = False
                            #break
                        else:
                          
                            pass
                        
                    
                        self.tokens.append(Token(line,4,num)) 

                    if content[i] != ' ' and content[i] not in delimiters and content[i] not in operaters :
                      
                                            
                        NOERROR = False
                        print("<Error type A at line %s :  '%s'   NUM_UNDEFINED reason:数字之后不是空格、分隔符、运算符>"%(line,num))
                        self.no_error = False
                        i+=1

                        ####################################

            
            elif i<len(content) and (content[i] in operaters or content[i] == '!'):
                if i<len(content) and content[i] == '#':
                    self.tokens.append(Token(line,1,content[i]))
                    i += 1
                    i,line = self.skip(i,line)

                #以某个运算符开头
                elif i<len(content) and content[i] == '/':
                    #可能是 /  //  /**/                    
                    if i+1<len(content) and content[i] + content[i+1] == '//':

                        #处理注释//
                        while content[i] not in ['\n','\r'] and i<len(content):
                            i += 1
                        i += 1
                        line += 1
                        
                    elif i+1<len(content) and content[i] + content[i+1] == '/*':
                     
                        i += 1 
                        comment = False                 
                        #处理注释/* */
                        while i+1<len(content)and content[i] + content[i+1] != '*/':

                            
                            templine = line
                            i,line = self.skip(i,line)
                            if content[i] + content[i+1] == '/*':
                                NOERROR = False
                                print(i,"hhh",content[i] + content[i+1])
                                print("<Error type A at line %s :    COMMENT_UNDEFINED reason:/*  */ 不允许嵌套>"%(line))
                                self.no_error = False
                                i+=1
                                #break                        
                            if templine == line:
                                i += 1
                        if i+1<len(content) and content[i] + content[i+1] == '*/':
                            comment = True
                        i += 2
                        if comment:
                            pass
                            #print("已过滤注释'/**/'",line)

                        else:
                            NOERROR = False
                            print("<Error type A at line %s :   COMMENT_UNDEFINED reason: 缺少 */ >"%(line))
                            self.no_error = False
                        continue                    
                    else:                       
                        self.tokens.append(Token(line,1,content[i]))
                        i += 1
                    i,line = self.skip(i,line)

                elif i<len(content) and content[i] == '-':#自减 减赋值  减              
                    if content[i + 1] == '-':
                        self.tokens.append(Token(line,1,'--'))
                        i += 2
                    elif content[i + 1] == '=':
                        self.tokens.append(Token(line,1,'-='))
                        i += 2

                    else:
                        self.tokens.append(Token(line,1,'-'))
                        i += 1
                    i,line = self.skip(i,line)

                elif i<len(content) and content[i] == '+':#自加 加赋值  减              
                    if content[i + 1] == '+':
                        self.tokens.append(Token(line,1,'++'))
                        i += 2
                    elif content[i + 1] == '=':
                        self.tokens.append(Token(line,1,'+='))
                        i += 2

                    else:
                        self.tokens.append(Token(line,1,'+'))
                        i += 1
                    i,line = self.skip(i,line)
                elif i<len(content) and content[i] in ['>','<','=','!']:
                    op = content[i]
                    i += 1                    
                    if content[i] == '=':
                        op += content[i]
                        i += 1
                        
                    self.tokens.append(Token(line,1,op))
                    i,line = self.skip(i,line)
                elif i<len(content) and content[i] == '&':

                    if content[i + 1] == '&':
                        self.tokens.append(Token(line,1,'&&'))
                        i += 2
                    else:
                        self.tokens.append(Token(line,1,'&'))
                        i += 1
                    i,line = self.skip(i,line)
                elif i<len(content) and content[i] == '|':

                    if content[i + 1] == '|':
                        self.tokens.append(Token(line,1,'||'))
                        i += 2
                    else:   
                        print("<Error type A at line %s :  '%s'   UNKNOWEN_CHARACTER reason: 未知字符 >"%(line,content[i]))
                        self.no_error = False                     
                        i += 1
                    i,line = self.skip(i,line)


   

                
                else:
                  #i,line = self.skip(i,line)
                    op = ''
                    op += content[i]
                    i += 1  
                    self.tokens.append(Token(line,1,op))
                    i,line = self.skip(i,line)
              
            elif i<len(content) and content[i] in delimiters:
                self.tokens.append(Token(line,2,content[i]))
                i+=1            
                
            else:
                
                if i<len(content):
                    NOERROR = False 
                    print("<Error type A at line %s :  '%s'   UNKNOWEN_CHARACTER reason: 未知字符 >"%(line,content[i]))
                    self.no_error = False
                i+=1


        if not self.no_error:
            print("词法分析: 词法有错误")     

            

                


        #for i in range (0,len(self.tokens)):  

            #print(self.tokens[i].value,self.tokens[i].type)


        print("TOLAL",line,"LINE")  


if __name__ == '__main__':
    lexer = Lexer()
    lexer.main()

    for i in range (0,len(lexer.tokens)):  
    
        print(lexer.tokens[i].type,lexer.tokens[i].value ,lexer.tokens[i].line)







    
