#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lexer import *
from grammer import *

class analysis_table(object):
    
    
    #测试用
    '''
    def ece(self):
        self.cal_firsts()
        k = 0
        for i in aaa.Firsts:
            print(non_terminal_sign_type[k])
            k+=1
            print(i)
        self.generate_table()
    '''

    #预测分析表
    def __init__(self):
        

        #定义预测分析表
        self.table = list()
        #为预测分析表分配空间
        for i in range(len(non_terminal_sign_type)):
            self.table.append(list())
            for j in range(len(non_terminal_sign_type)):
                self.table[i].append(None)
        
        #初始化
        self.non_terminal_signs = list()
        self.terminal_signs = list()
        #赋值，变成Sign 统一格式方便运算
        for i in non_terminal_sign_type:
            self.non_terminal_signs.append(Sign(i))
        for i in terminal_sign_type:
            self.terminal_signs.append(Sign(i))
        #每个非终结符的first集和follow集
        self.Firsts = list()
        self.Follows = list()

        for i in non_terminal_sign_type:
            #为每一个非终结符对应的first和follow集申请空间
            #每一个list代表一个非终结符的一个first集或follow集
            #每个first集或者follow集list中的元素是Sign对象
            #如Firsts[0]代表第一个非终结符的first集
            self.Firsts.append(list())
            self.Follows.append(list())
    
    #获得终结符位置
    def get_ts_index(self,terminal_sign):
        for i in range(len(self.terminal_signs)):
            if terminal_sign.type == self.terminal_signs[i].type:
                return i
        #查找失败
        return -1
    #获得非终结符位置
    def get_nts_index(self,non_terminal_sign):
        for i in range(len(self.non_terminal_signs)):
            if non_terminal_sign.type == self.non_terminal_signs[i].type:
                return i
        #查找失败
        return -1
    #获取first集 
    def get_First(self,non_terminal_sign):
        return self.Firsts[self.get_nts_index(non_terminal_sign)]
    #获取不含空元素的first集
    def get_First_no_empty(self,non_terminal_sign):
        temp = list()
        for i in self.get_First(non_terminal_sign):
            if not i.is_empty_sign():
                temp.append(i)
        return temp

    #判断first集中是否含空元素
    def is_empty_in_First(self,non_terminal_sign):
        for i in self.get_First(non_terminal_sign):
            if  i.is_empty_sign():
                return True
        return False

    #获取follow集
    def get_Follows(self,non_terminal_sign):
        return self.Follows[self.get_nts_index(non_terminal_sign)]

    @classmethod 
    #判断是否存在，返回bool值
    def add(cls,collection,sign):
        #collection为某个非终结符的first集或follow集
        #sign为Sign对象

        for elem in collection:
            if elem.type == sign.type:             
                return False
        else:
            collection.append(sign)
        return True
    def get_production(self,non_terminal_sign,terminal_sign):
        x = self.get_nts_index(non_terminal_sign)
        y = self.get_ts_index(terminal_sign)
        #print("x",x,"y",y)
        return self.table[x][y]



    #求first集
    def cal_firsts(self):
        flag = True #标识first集是否变化
        while flag:
            flag = False
            for production in productions:
                #$ 空‘’
                if len(production.right)==0:
                    if self.add(self.get_First(production.left),Sign('')):
                        flag =True
                #非空       
                else:
                    #终结符开头，加入到非终结符的first集中
                    if production.right[0].is_terminal_sign():
                        if self.add(self.get_First(production.left),production.right[0]):
                            flag = True
                    #非终结符开头，开始循环
                    elif production.right[0].is_non_terminal_sign():
                     
                        
                        change = False
                        for i in self.get_First_no_empty(production.right[0]):
                            if self.add(self.get_First(production.left),i):
                                change = True
                        if change :
                            flag = True

                        for i in range(len(production.right)):
                            if production.right[i].is_non_terminal_sign():
                                #如果为空
                                if self.is_empty_in_First(production.right[i]):
                                    if i == len(production.right)-1:
                                        if self.add(self.get_First(production.left),Sign('')):
                                            flag = True
                                    else:
                                        #下一个是终结符
                                        if production.right[i + 1].is_terminal_sign():####可优化
                                            if self.add(self.get_First(production.left),production.right[i + 1]):
                                                flag = True
                                        #下一个是非终结符
                                        elif production.right[i + 1].is_non_terminal_sign():
                                            change = False
                                            for j in self.get_First_no_empty(production.right[i+1]):
                                                if self.add(self.get_First(production.left),j):
                                                    change = True
                                                if change :
                                                    flag = True
                                        else:
                                            print("语法产生式错误1")
                                            return False
                                #如果不含空  ####优化           
                                else:
                                    break
                            else:
                                break
                    #错误          
                    else:
                        print("语法产生式错误2")
                        return False

    #求指定非终结符的first集
    def cal_certain_first(self,collection):
        first = list()
        #右边产生式为空
        if len(collection)==0:
            self.add(first,Sign(''))
                
        #非空       
        else:
            #终结符开头，加入到非终结符的first集中
            if collection[0].is_terminal_sign():
                self.add(first,collection[0])
                    
            #非终结符开头，开始循环
            elif collection[0].is_non_terminal_sign():
                
                for i in self.get_First_no_empty(collection[0]):
                    self.add(first,i)                 


                for i in range(len(collection)):
                    if collection[i].is_non_terminal_sign():
                        #如果为空
                        if self.is_empty_in_First(collection[i]):
                            #是最后一个
                            if i == len(collection)-1:
                                self.add(first,Sign(''))
                            #不是最后一个  
                            else:
                                #下一个是终结符
                                if collection[i + 1].is_terminal_sign():####可优化
                                    self.add(first,collection[i + 1])
                             
                                #下一个是非终结符
                                elif collection[i + 1].is_non_terminal_sign():

                                    for j in self.get_First_no_empty(collection[i+1]):
                                        self.add(first,j)
        
                                else:
                                    print("语法产生式错误1")
                                    return False
                        #如果不含空  ####优化           
                        else:
                            break
                    else:
                        break
            #错误          
            else:
                print("语法产生式错误2")
                return False
        return first


    #求follow集
    def cal_follow(self):
        first = list()
        flag = True
        while flag :
            flag =False
            #所有产生式
            for production in productions:
                #起始非终结符
                if production.left.type == grammar_start.type:
                    if self.add(self.get_Follows(production.left),Sign('pound')):
                        flag =True
                #右产生式
                for i in range(len(production.right)):
                    #是非终结符
                    if production.right[i].is_non_terminal_sign():

                        #如果是最后一个符号
                        if i == len(production.right)-1:
                            change = False
                            # 将产生式左边非终结符的 follow 集添加到这个符号的 follow 集中
                            for j in self.get_Follows(production.left):
                                if self.add(self.get_Follows(production.right[i]),j):
                                    change =True
                            if change:
                                flag = True
                        #否则继续看之后的
                        else:
                            first.clear()
                            first += self.cal_certain_first(production.right[i+1:])
                            #将first中的非空元素加入到follow中
                            hasEmpty = False
                            for f in first:
                                if not f.is_empty_sign():
                                    self.add(self.get_Follows(production.right[i]),f)
                                else:
                                    hasEmpty = True
                            #有空元素
                            if hasEmpty:
                                # 将产生式左边非终结符的 follow 集添加到这个符号的 follow 集中
                                change = False
                                for j in self.get_Follows(production.left):
                                    if self.add(self.get_Follows(production.right[i]),j):
                                        change = True
                                if change:
                                    flag = True
                    #是终结符
                    elif production.right[i].is_terminal_sign():
                        continue
                    #error
                    else:
                        print("语法产生式错误")
                        return False

    def insert_to_table(self,production,terminal):
        #形如M[A,a]的矩阵,用终结符或非终结符的序号表示.
        x = self.get_nts_index(production.left)
        y = self.get_ts_index(terminal)


        if self.table[x][y]:

            same_left = production.left.type == self.table[x][y].left.type
            if same_left:   
                same_right = True
                if len(production.right) != len(self.table[x][y].right):
                    print("非LL(1)语法")
                    return False 
                else:
                    for i in range(len(production.right)):
                        if production.right[i].type != self.table[x][y].right[i].type:
                            same_right = False
                    if same_right:
                        del self.table[x][y]
                        self.table[x].insert(y, production)
                        return True
                    else:
                        print("非LL(1)语法1")
                        return False 
            else:
                print("非LL(1)语法2")
                return False  
        else:
            del self.table[x][y]
            self.table[x].insert(y, production)
            return True
        

    def generate_table(self):
        # 对每一条产生式应用规则
        for production in productions:
            # 先求出该产生式右边部分的 first 集
            first = self.cal_certain_first(production.right)

            # 对每一个 first 集中的每一个终结符执行操作
            empty_find = False
            for i in list(first):
                if i.type == '':

                    empty_find = True
                else:
                    if not self.insert_to_table(production, i):
                        return False

            # 如果其 first 集中有空字，则对 follow 集中的每一个终结符执行操作
            if empty_find:
                for i in self.get_Follows(production.left):
                    if not self.insert_to_table(production, i):
                        return False

        return True

    def compile(self):
        # 对每一个文法元素求其 first 集
        self.cal_firsts()
        # 对每一个文法元素求其 follow 集
        self.cal_follow()
        # 根据 first 集和 follow 集生成预测分析表
        success = self.generate_table()
        return success  
        

class Stack(object):
    #定义栈及其操作
    def __init__(self):
        self.container = list()
    def top(self):
        return self.container[-1]
    def push(self,elem):

        self.container.append(elem)

    def pop(self):
        top = self.top() #记录栈顶元素，并返回
        self.container.pop()
        print(top.type)
        return top


class parser(object):

    '''
    语法分析器
    '''

    def __init__(self,tokens):

        self.tokens = tokens
        #存储词法分析结果
        self.token_terminal = list()
        #存储带值的Sign对象
        for  i in self.tokens:
            self.token_terminal.append(Sign(i.type,i.value,i.line))
            
        self.token_terminal.append(Sign('pound'))
        ###for i in self.token_terminal:
           ### print(i.type)#i.value,i.line)))


    def sytax(self):
        self.an_tables = analysis_table()
        self.an_tables.compile()
        stack = Stack()

        stack.push(Sign('pound'))
        index = 0
        flag = True
        error=False
        stack.push(Sign('program'))
        #print(stack.top().type,self.token_terminal[index].type)
        while flag:
            #print("stack           ",len(stack.container))
            if stack.top().is_non_terminal_sign():

                # 查看分析表
                ###print("      查表",stack.top().type,self.token_terminal[index].type)
                production = self.an_tables.get_production(stack.top(), self.token_terminal[index])
                #print(production)
                # 如果分析表中有产生式
                if production:
                    # 将 top 出栈
                    top = stack.pop()
                    #print(top)
                    # 反序入栈
                    for i in range(len(production.right) - 1,-1,-1):  
                        stack.push(production.right[i])
                        ###print("      逆序压入",production.right[i].type)
                # 如果分析表中存放着错误信息
                else:
                    print("<Error type B at line %s :  '%s'  reason：语法错误1 >"%(self.token_terminal[index].line,self.token_terminal[index].value))
                    error = True
                    break
            # 如果 top 是终结符
            else:
                # 如果 top = input
                ###print(stack.top().type,"终结符",self.token_terminal[index].type) 
                if stack.top().type == self.token_terminal[index].type:
                    
                    # 如果 top = #，分析成功
                    if stack.top().type == 'pound':
                        print("语法分析成功")
                        flag = False
                    # 如果 top != #
                    else:

                        stack.pop()
                        index += 1
                # 如果 top != input
                else:
                    print("<Error type B at line %s :  '%s' reason：语法错误2 >"%(self.token_terminal[index].line,self.token_terminal[index].value))
                    error = True
                    break

        if  error:
            print("语法分析： 语法有错误")
            return False
        else:
            return True



   
















lexer = Lexer()
lexer.main()

if  lexer.no_error:
    print("词法分析成功")
   
    aaa = parser(lexer.tokens)
    #aaa.compile()

    aaa.sytax()
    #print(aaa.table)


'''
print(bbb.table[0][2].right[0].type)
bbb= analysis_table()
bbb.compile()          
x =bbb.get_nts_index(Sign('expression-follow'))
for i in bbb.table[x]:
    if i != None:
        print(i.right)
'''




        





