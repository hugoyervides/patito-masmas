
<p align="center">
  <img src="https://repository-images.githubusercontent.com/252045115/c91d1d00-9d59-11ea-8764-883372e77436" width="450" height="230" />
</p>

# Introduction
Patito ++ is a procedural language that facilitates complex matrix operations such as multiplication, addition, subtraction, transposition, inverse, and determinants.  
The manipulation of dimensioned elements is as simple as if it were a sum of two variables, only with two-dimensional arrays, saving development time when developing an application that depended heavily on these operations.


##  :beginner: About
Thanks to the use of the Python programming language as the basis for the virtual machine, the language is capable of performing matrix operations in a simple and fast way, with extra functionalities such as console writing of the matrix in an orderly and easy-to-understand way. without having to go through it by hand, thanks to this and the implemented grammar, it is very easy to write code in Patito ++, making it a very high-level language very similar to the Spanish language.

Patito ++ bases most of its grammar on a C / C ++ style grammar, making changes to make inference, reading and understanding the code easier, which will have the basic modules of a programming language, such as:  
  
- Management of functions or modules  
- Global and local variables  
- Declaration of different types of variables (Integers, Floats, Strings, Characters)  
- 1 and 2-dimensional arrangements  
- Logical operations (*, +, -) between dimensioned variables  
- Unary complex operations (Inverse, transpose, determinant) to dimensioned variables  
- Evaluation of mathematical (+, -, *, /) and logical (|, &) expressions, and the priority implementation of these expressions  
- Virtual machine  
- Member functions (write, read)


###  :hammer: Build with

* [Python](https://www.python.org/) -  :snake: The Python Programing Language
* [Ply](https://www.dabeaz.com/ply/) - Python Lex-Yacc
* [NumPy](https://numpy.org/) - NumPy
* [pandas](https://pandas.pydata.org/) - Pandas


## :zap: Installation and Requirements 
This part of the guide will get you started on Patito ++ compiler and Virtual Machine



### :notebook: Pre-Requisites
Below you can find the requirements in order to run both the compiler and virtual machine
```
Python 3
pip 3
Pandas
Numpy
```
###   :penguin: Installation for Linux Debian/Ubuntu
In order the Patito ++ Compiler and Virtual Machine you will need to install the following dependencies first
- Python 3
- Pip 3
- Pandas
- Numpy

First we will install Python 3 and Pip in our system
```
$ sudo apt-get update
$ sudo apt-get install python3
$ sudo apt-get install python-pip
```
Then we will need to clone the repository
```
$ git clone https://github.com/hugoyervides/patito-masmas.git
```
Navigate to the repository folder with cd
```
$ cd patito-masmas
```
Install requirements file
```
$ pip install
```

##  :running: Getting started
This guide will help you get started in Patito ++ with basic examples and explanation of how to structure your code and how to use the diferent implemented functions and modules
####  :nut_and_bolt: Compile
Once you have the repository in your system you can compile Patito ++ code with the following command
```
$ python compile.py <file.dpp> <output_file.ext>
```
-	The input file can be in any file extension, the compiler wont check, but its recommended to use dpp extension for Patito ++ code files
-	The user has to specify the output file for the quadruples, in this example we use output_file.ext, but you can name the file whatever you want
-	You will have two output files, one named the same as the second parameter and other that stores the constants that will be called c_<name_of_your_output>
####  :rocket: Run
Once you have compiled your first Patito ++ code, you can now run in using the Patito Virtual Machine, to do that you will need to run the patito_vm.py file and pass as an argument the name of your output file
```
$ python patito_vm.py <output_file.ext>
```
###  :computer:Code structure
All code in Patito ++ must start with the keyword "programa" followed by the name of the program and a semicolon.

```
programa <program_name>;
```
### :floppy_disk: Global Variable declaration
Next we will need to declare the global variables that our code will use, this can me done with the var keyboard followed by the variable type and names separated by commas and ends with a semicolon
```
var
	int intvar, intvar2[4][4];
	float floatvar, floatvar2;
	char charvar, charvar2;
```
In Patito++ you can declare as much variables as you like, but remember that the only variable types allowed are:
-	INT
-	FLOAT
-	CHAR

### :package: Functions
Declaring functions in Patito ++ is very similar to the function declaration in C/C++.
We first have to let the parser know that we are going to declare a new function with the keyword "funcion" followed by return type, name, parameters, local variables and block of code enclosed in {}
```
funcion int my_function(int number)
var
	int local_var_to_function;
{
	.. code ..
	return(number + 1);
}
```
Note that we can declare variables exclusive for functions, remember that these will only work when we are inside the function scope, they will not work outside of it.
Please note that the type of parameters a function can accept are the ones accepted during variable declaration
-	INT
-	FLOAT
-	CHAR

By default the return statement is enabled on all functions but doing it with a void function will generate a compilation error.
### :star: Main function
This is the core of our code, where we will need to put all the code that the virtual machine will evaluate first during execution, its important to have this part in the code otherwise the compilation process will file to compile a code without this function.
To declare this function is very similar to the normal function declaration, with the only difference that this function does not have parameters and a local memory for declaration (uses the global).
We start with the keyword "principal" followed by () and the block of code enclosed in {}
```
principal(){
	...code...
}
```
###   :inbox_tray: Console I/O
In Patito ++ we have two keywords to get and display data to the console (escribe and lee)
"Escribe" will help us to display a variable to the console just like print in Python, works by calling the "module" followed by the variables you can to display or even a text enclosed in "".
In Patito ++ you can even display a matrix without having to navigate thru each one of the elements, to do this is as simple as calling the module with the name of the variable without the [][]
```
escribe("Hello, World!");
escribe(array);
escribe(1, value);
```
As you can see, we can use one "escribe" call to display multiple variables separated by a comma.
### :pencil: Comments
When developing a large or complex code, its must to include comments in it to make it easier for other developers to understand you code, in Patito ++ you can use the character %% to let the Compiler know that its a commend and it should be ignored
```
principal(){
	%% This is a comment
	escribe( 1 * 1 );
}
```
### :dart: if, else statement
In Patito ++ we can declare a statement very easy similar to most programing languages, we start with the keyword "si" followed by an expression that MUST return a boolean value (otherwise will cause a compilation error) and the keyword "entonces"
```
si ( 1 > 3 ) entonces{
	escribe("1 es mayor a 3!!"):
}
```
We can also declare an else if we want to, just add the "sino" keyword at the end of the } 
```
si ( 1 > 3 ) entonces{
	escribe("1 es mayor a 3!!");
}sino{
	escribe("1 no es mayor a 3?");
}
```
###   :curly_loop: While Loop
Patito ++ suports the use of two types of loops, the first one is the "While like loop", its similar to other programing languages, we first have to use the keyword "mientras" followed by the boolean expression and the keyword "haz"
```
mientras( 1 > 3 ) haz {
	escribe("1 es mayor a 3!");
}
```
Don't try this, it will generate an infinite loop

### :loop:For Loop
The other type of loop is the "For like loop" does the same as the mientras loop but this loop will let us assign a value to a previous declared variable and use a int constant to determine when to end.
```
desde i = 0 hasta 5 hacer {
	escribe(i);
}
```
Please note that we can't use an expression in the assignation and the end of the range, it can only be an assignation and a integer constant.
###   :1234: Arithmetic operations
Patito ++ supports arithmetic operations (obviously) just like any other language and following the same precedence and association of them.
We can combine arithmetic and logic operations if we use the operations >=, <=, etc.
Example.
```
principal(){
	final_value = 3 * i / 15 + ( 587 * final_value );
	second_value = sumNumber( 1 , 3 ) + 5 * 8;
}
```
Note that we can also include function calls inside the expression and they will evaluate them first and then proceed to the next operation.
In Patito ++ we can also perform + , - and * of matrices, following the basic rules (sum two matrices of the same size) otherwise it will produce a compilation error.
```
funcion void sumaMat()
var:
	int mat1[5][5], mat2[5][5];
{
	escribe(mat1 + mat2);
}
```
Make sure to fill the matrices with data first.
Here you can find a table with valid and invalid arithmetic operations that can be done in Patito ++
| OPERAND 1| OPERAND 2 | OPERATION | RESULT |
|-----|----|---|------|
| INT | INT| *, +, - | INT |
| INT | INT | / | FLOAT|
| FLOAT | FLOAT | *, +, -, / | FLOAT
| INT | FLOAT | *, +, -, / | FLOAT
| CHAR | CHAR | *, +, -, / | ERROR
| INT| CHAR | *, +, -, / | ERROR
| FLOAT| CHAR | *, +, -, / | ERROR
| INT_ARR| INT_ARR | *, +, - | INT_ARR
| INT  | INT_ARR  | *, +, -, / | ERROR
| FLOAT | INT_ARR  | *, +, -, / | ERROR
| CHAR | INT_ARR  | *, +, -, / | ERROR


### :space_invader: Logic operations
Just like any other language, Patito ++ supports this logic operations
-	AND (&&)
-	OR (||)
-	\>= <=
-	\> <
-	==
```
principal(){
	mientras ((3 > 1) && ( 2 < 5 )) haz{
		....
	}
}
```
| OPERAND 1| OPERAND 2 | OPERATION | RESULT |
|-----|----|---|------|
| INT | INT| > , < , == | BOOL|
| FLOAT | FLOAT |  > , < , ==  | BOOL
| INT | FLOAT |  > , < , ==  | BOOL
| CHAR | CHAR |  > , < , ==  | ERROR
| INT| CHAR |  > , < , == | ERROR
| FLOAT| CHAR |  > , < , ==  | ERROR
| INT_ARR| INT_ARR |  > , < , ==  | ERROR
| INT  | INT_ARR  | > , < , ==  | ERROR
| FLOAT | INT_ARR  |  > , < , ==  | ERROR
| CHAR | INT_ARR  |  > , < , ==  | ERROR

###  :bar_chart: Special matrix operations
One of the most helpful things Patito ++ can do is perform the following unary operations to bi dimensional variables like

-	Transpose (¡)
-	Determinant ($)
-	Inverse (?)
```
principal(){

	%% Capturar la matriz

	capturar();

	%% Desplegar determinante

	escribe("Determinate:");

	escribe(arreglo$);

	%% Desplegar inversa

	escribe("Inversa:");

	escribe(arreglo?);

	%% Desplegar transpuesta

	escribe("Transpuesta:");

	escribe(arreglo¡);

}
```
Output of each operation will be
| OPERATION| OUTPUT | 
|-----|----|
| DETERMINANT | FLOAT| 
| TRANSPOSE | INT_ARR |
| INVERSE | INT_ARR|



## :books:Project Structure
###  :file_folder:  File Structure
Below you will find a complete map of each module and where its located, and its job during compilation and virtual machine run time 

```
.
├── code_examples
│   ├── array_operations.dpp
│   ├── array_special.dpp
│   └── fibonacci.dpp
├── compiler
│   ├── parser.py
│   └── scanner.py
├── data_structures
│   ├── constant_table.py
│   ├── fun_table.py
│   ├── quadruples.py
│   ├── semantic.py
│   ├── var_table.py
│   └── vm_memory.py
├── handlers
│   ├── fun_handler.py
│   ├── operations.py
│   ├── stacks.py
│   └── var_table_handler.py
├── ply
│   ├── lex.py
│   └── yacc.py
├── compile.py
├── patito_vm.py
├── requirements.txt
└── README.md
```
###  :page_with_curl:  File Description

| No | File Name | Details 
|----|------------|-------|
| 1  | array_operations.dpp| Basic example code using array operations in Patito ++
| 2 | array_special.dpp | Basic example code using unary array operations in Patito ++
| 3 | fibonacci.dpp | Recursive Fibonacci algorithm coded in Patito ++
| 4 | parser.py | Grammar rules and neuralgic point declaration
| 5 | scanner.py | Lex and regular expressions
| 6 | constant_table.py |  Data structure that stores and serves all the constants during compiling
|  7 |  fun_table.py | Data structure that stores and serves functions during compiling
| 8 | quadruples.py |  Data structure that stores and serves quadruples during compiling
| 9 | semantic.py |  Data structure used to verify correct semantic operations during compilation
| 10| var_table.py | Data structure used to store and manipulate variables declarated during compilation
| 11 |  vm_memory.py | Data structure used by Virtual Machine to handle read/write memory operations
|  12 |  fun_handler.py |  Module in charge of handling all operations on functions and function table during compilation
|  13 |  operations.py |  Module in charge of handling operations performed on virtual machine during code execution
| 14|  stacks.py | The core module during compilation, handles neuralgic points and all other handlers
| 15| var_table_handler.py | Module in charge of handling variables during compilation
| 16| compile.py | Main file used to compile Patito ++ code
| 17| patito_vm.py |  Virtual machine used to run compiled Patito ++ code




## :star2: Authors

* **Victor Hugo Oyervides** - *Initial work* - [hugoyervides](https://github.com/hugoyervides)
* **Obed Gonzalez Moreno** - *Initial work* - [obedgm](https://github.com/obedgm)

##  :lock: License
Add a license here, or a link to it.
