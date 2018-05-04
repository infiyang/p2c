# p2c
Introduced by zicong (Fitz) 



///
This program provides a tool p2c to achieve the format conversion within python and C.



///
The file in this document includes:


'p2c' file is the core code.


'run' file is the file to realize the conversion, you can open the fild with python code in it directly and start the simple conversion.



There are also several test code for the test use:
	
'test1.py'-'test6.py' list different simple basic program in python, including print, if else, regular expression,while and for.
	
	

'testpy.py' is the simple program file in python to call the python  or compiled c code which can be called by python directly
	
	

'testc.py' is the typical method  to call the c in python
	
(1.ctypes and os module in this program is the standard module of python, if you want to run the call C function here, you need those two modules
	 
2.'.dll' file stands for the compiled file of C and can be compiled from C by GCC compiler to help us calling C.
	
 3. this test case may still need some improvements)

'fib.py' is the python program being called in testpy.

'pycall.c' and 'pycall.dll' are the file used in testc





///
Most program that executes sequentially, such as the arithmetic code, loop code, condition code, assignment code, can be converted.


But there are some places still need to be improved:

1. The 'for' statement, it may have the possibility to have difference within the runing results of python code and converted code.


2. The 'call python', you can add some codes like 'print' statement after them, and mostly they can be converted into C with usable right format.



3.The 'call C', you can use the converted c code directly, but if you add some statements after the 'call C' statements,
the printed c code might have some problems . 

4. There may be some issues in the strings variables conversion in python and c.





You can use the test files in this document to test the program

