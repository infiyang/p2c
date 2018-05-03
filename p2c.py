import ast
import os
class p2c:
    def __init__(self, root_node):
# "code" is to store the converted c code
        self.code = ""
# "variables" is to store the variables names in the whole program
        self.variables = []
        for node in ast.walk(root_node):
            if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
# walk through the AST and record the variables
                self.variables.append(node.id)
        self.variables.append('lib')
        self.variables = set(self.variables)
        
        self.variables.remove('lib')
# start the convertion
        self.Module(root_node)
# if node is Name type node, call the name function
# if the node attribute "ctx" is store, it means to assign a value to the node
# and the corresponding c code is "node's variable name ="
# if the "ctx" attribute is not store, it means return the variable name
    def Name(self, node):
        if isinstance(node.ctx, ast.Store): 
            return node.id + "="
        else:
            return node.id

# if the node type is positive number, then return the number
    def Num(self, node):
        return str(node.n)
    
#negative number, then return the number or -x
    def UnaryOp (self, node):
        if isinstance(node.op, ast.USub):
            op='-'
            if isinstance (node.operand, ast.Num):
                return  '('+op + self.Num(node.operand)+')'
            elif isinstance (node.operand, ast.Name):
                return  '('+op + self.Name(node.operand)+')'
            elif isinstance (node.operand, ast.UnaryOp):
                return   '('+op+ self.UnaryOp(node.operand)+')'
            
            
                
            
                
        if isinstance(node.op, ast.UAdd):
            op=""
            if isinstance (node.operand, ast.Num):
                return  op + self.Num(node.operand)
            elif isinstance (node.operand, ast.Name):
                return  op + self.Name(node.operand.str)
            elif isinstance (node.operand, ast.UnaryOp):
                
                return  op + self.UnaryOp(node.operand)
            
            
            
                
            
# if the node type is assign, then the node.value will be assigned to node.targets
    def Assign(self, node):
        if node.targets[0].id=='lib':
            return getattr(self, str(type(node.value))[13:-2])(node.value)
        else:
            return getattr(self, str(type(node.targets[0]))[13:-2])(node.targets[0]) + getattr(self, str(type(node.value))[13:-2])(node.value)
            
                
# if unary op type, then code will be name+op+values
    def AugAssign(self, node):
        if isinstance(node.op, ast.Add):
            op = '+'
        elif isinstance(node.op, ast.Sub):
            op = '-'
        elif isinstance(node.op, ast.Mult):
            op = '*'
        else:
            op = '/'
        return self.Name(node.target) + node.target.id  + op + self.Num(node.value)


# if node is return, then code will be "return + the code generated after it 
    def Return(self, node):
        return 'return ' + getattr(self, str(type(node.value))[13:-2])(node.value)

# if node is binary op, the code will be "left code + op + right code"
    def BinOp(self, node):
        if isinstance(node, ast.Name):
            return self.Name(node)
        elif isinstance(node, ast.UnaryOp):
            return self.UnaryOp(node)
        elif isinstance(node, ast.Num):
            return self.Num(node)
        if isinstance(node.op, ast.Add):
            op = '+'
        elif isinstance(node.op, ast.Sub):
            op = '-'
        elif isinstance(node.op, ast.Mult):
            op = '*'
        else:
            op = '/'
        return '(' + self.BinOp(node.left) + op + self.BinOp(node.right) + ')'
      
    def Compare(self, node):
        # compare op， return left code+ op+ right code
        if isinstance(node.ops[0], ast.Lt):
            ops = '<'
        elif isinstance(node.ops[0], ast.Eq):
            ops = '=='
        elif isinstance(node.ops[0], ast.Gt):
            ops = '>'
        elif isinstance(node.ops[0], ast.GtE):
            ops = '>='
        elif isinstance(node.ops[0], ast.LtE):
            ops = '<='
        elif isinstance(node.ops[0], ast.NotEq):
            ops = '!='
        return getattr(self, str(type(node.left))[13:-2])(node.left) + ops + getattr(self, str(type(node.comparators[0]))[13:-2])(node.comparators[0])

    def While(self, node):
        # the 1st line will be the condition of while
        code = 'while(' + getattr(self, str(type(node.test))[13:-2])(node.test) + '){\n'
        #  the while content will be include in next few lines
        for children in node.body:
            code += getattr(self, str(type(children))[13:-2])(children) + ';\n'
        # add }
        code += '}'
        return code

    def If(self, node):
        # the 1st line will be the condition of if
        code = 'if(' + getattr(self, str(type(node.test))[13:-2])(node.test) + '){\n'
        for children in node.body:
            # the if content will be include in next few lines
            code += getattr(self, str(type(children))[13:-2])(children) + ';\n'
        # if there is no else , then just }
        if len(node.orelse) == 0:
            return code + '}'
        else:
            code += '}else \n'
        # if if there is else, then call if recursively
            for children in node.orelse:
            #code += '}else '
                code += getattr(self, str(type(children))[13:-2])(children)+';'
                code +='\n'
        return code

    def For(self, node):
        # the 1st line will be the condition of for
        var = node.target.id
# some like for x in range(1,3):
        if isinstance(node.iter, ast.Call):
            code = 'for(' + getattr(self, str(type(node.target))[13:-2])(node.target)
            if len(node.iter.args) == 2:
                 code += getattr(self, str(type(node.iter.args[0]))[13:-2])(node.iter.args[0])
            else:
                code += '0'
            code += ';' + var + '<' + getattr(self, str(type(node.iter.args[-1]))[13:-2])(node.iter.args[-1]) + ';' + var + '++){\n'

        
            for children in node.body:
                code += getattr(self, str(type(children))[13:-2])(children) + '; \n'
            code += '}'
            return code
# some like  for x in abcdef
        elif isinstance(node.iter, ast.Str):
            code ='char '+var+ 'c[] ="'+node.iter.s
            code+='";\nfor (int '+var +'=0;'
            code+= var + '<=strlen('+var+'c); '+var+'++){\n'
            for children in node.body:
                if isinstance(children, ast.Expr):
                    code+= 'printf("%c\\'
                    code+='n",'+var+'c['+var+']);'
                else:
                    code += getattr(self, str(type(children))[13:-2])(children) + ';\n'
            code += '}'
            return code


        
    def Str(self, node):
        # the string, return "string"
        return '"' + node.s + '"'
    
    def Expr(self, node):
        # print
        code = []
        #global arg
        #if node.Expr.func.id=='print':
        for arg in node.value.args:
            if isinstance(arg, ast.Str):
                code.append('printf(' + self.Str(arg) + ')')
            else:
                code.append('printf("%f",' + getattr(self, str(type(arg))[13:-2])(arg) + ')')
            
        #else:
            
            #code.append(node.value.func.id+self.Num(arg))
        code = ";\n".join(code)
        return code
         # import and from ..import, 
         # determine if is opening ctypes/os for calling C or just calling python
    def Import(self, node):
        if node.names[0].name=='ctypes':
            return ""
        if node.names[0].name=='os':
            return ""
        else:
            file = open(node.names[0].name + '.py',encoding="utf8").read()
            return p2c(ast.parse(file)).code
            
        
    def ImportFrom(self,node):
        if node.module=='ctypes':
            return ""
        if node.module =='os':
            return ""
        else:    
        
            file =open(node.module +'.py',encoding="utf8").read()
            return p2c(ast.parse(file)).code

    def Call(self, node):
        if node.func.value.value.id == 'ctypes':
            filename = node.args[0].s.split('.')[0]
            file = open(filename + '.c').read()
            return file


    def Module(self, root_node):
# function flag is used to record the whole python code and judge whether it is the function type,
# if it is then return false                                                                                                                                                                                                                                                             
        function_flag = False
        if isinstance(root_node.body[0], ast.FunctionDef):               
# if it has function type, then generate the definition of c function：
# self.FunctionDef(root_node.body[0]) to record the c fnction definition in the code                                                                                                                            
            self.FunctionDef(root_node.body[0])
            root_node = root_node.body[0]
            function_flag = True
# or it will generate int main
        #else:
            #self.code += '#include <stdio.h>\n int main(){\n'
# define every variables                                                                                                                                 
        for var in self.variables:
            self.code += 'double ' + var + ';\n'
# walk through the node, and call the corresponding method
# like  if the node type is add                                                                                                                              
# then getattr() will call BinOp() and return the c code 
        for node in root_node.body:
            if isinstance(node, ast.Import):
                self.code = getattr(self, str(type(node))[13:-2])(node) + '\n' + self.code
            elif isinstance(node, ast.ImportFrom):
                self.code = getattr(self, str(type(node))[13:-2])(node) + '\n' + self.code
            else:
                self.code += getattr(self, str(type(node))[13:-2])(node) + ';\n'
# if not function, pass or add return 0 at the end of it
        if not function_flag:
            pass
            #self.code += 'return 0;\n'
# if it is function, add double at the begin of the whole code
        else:
            self.code = 'double ' + self.code
        #self.code += '}'
        #print(self.code)
#return the function definition of c code
    def FunctionDef(self, root_node):
        self.code += root_node.name + "(){\n"
