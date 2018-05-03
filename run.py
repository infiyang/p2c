from p2c import *



f =open ('test2.py','r',encoding="utf8")
# generate the python code into AST,
# the root_node is the head node of the AST
root_node = ast.parse(f.read())

print(ast.dump(root_node))
print('#include <stdio.h> \n#include <cstring>\nint main(){\n')
print(p2c(root_node).code)
print('}')





