# Tiny-C

This is a compiler for the Tiny-C language, developed by Marc Feeley.

Tiny-C is a considerably stripped down version of C and it is meant as a
pedagogical tool for learning about compilers.  The integer global variables
"a" to "z" are predefined and initialized to zero, and it is not possible to
declare new variables. The compiler reads the program from standard input and
prints out the value of the variables that are not zero.

The compiler does a minimal amount of error checking to help highlight its
structure.

# Grammar

The grammar of Tiny-C in EBNF is:

```
<program> ::= <statement>
<statement> ::= "if" <parenthesis_expression> <statement> |
                "if" <parenthesis_expression> <statement> "else" <statement> |
                "while" <parenthesis_expression> <statement> |
                "do" <statement> "while" <parenthesis_expression> ";" |
                "{" { <statement> } "}" |
                <expression> ";" |
                ";"
<parenthesis_expression> ::= "(" <expression> ")"
<expression> ::= <comparison> | <id> "=" <expression>
<comparison> ::= <sum> | <sum> "<" <sum>
<sum> ::= <term> | <sum> "+" <term> | <sum> "-" <term>
<term> ::= <id> | <int> | <parenthesis_expression>
<id> ::= "a" | "b" | "c" | "d" | ... | "z"
<int> ::= <an_unsigned_decimal_integer>
```

# Lexer

* **DO_SYM**: Represents the `do` keyword, used in the do-while loop construct.
* **ELSE_SYM**: Represents the `else` keyword, used in if-else statements.
* **IF_SYM**: Represents the `if` keyword, used in conditional statements.
* **WHILE_SYM**: Represents the `while` keyword, used in while loops.
* **LBRA**: Represents the left curly brace `{`, used to define the beginning of a block of statements.
* **RBRA**: Represents the right curly brace `}`, used to define the end of a block of statements.
* **LPAR**: Represents the left parenthesis `(`, used in expressions and conditionals.
* **RPAR**: Represents the right parenthesis `)`, used in expressions and conditionals.
* **PLUS**: Represents the addition operator `+`, used in arithmetic expressions.
* **MINUS**: Represents the subtraction operator `-`, used in arithmetic expressions.
* **LESS**: Represents the less than operator `<`, used in comparison expressions.
* **SEMI**: Represents the semicolon `;`, used to terminate statements.
* **EQUAL**: Represents the equal sign `=`, used in assignment expressions.
* **INT**: Represents an integer literal, such as `1`, `2`, `42`, etc.
* **ID**: Represents an identifier, typically a variable name (e.g., `a`, `b`, `c`).
* **EOI**: Stands for "End of Input" and signifies the end of the input source code.

# Abstract Syntax Tree

Tiny-C works on an internal abstract syntax tree (AST) with the following terms:

* **VAR**: Represents a variable.
* **CST**: Represents a constant value.
* **ADD**: Represents addition operation.
* **SUB**: Represents subtraction operation.
* **LT**: Represents less-than comparison.
* **SET**: Represents assignment operation.
* **IF1**: Represents the first part of an if statement.
* **IF2**: Represents the second part of an if statement.
* **WHILE**: Represents a while loop.
* **DO**: Represents a do-while loop.
* **EMPTY**: Represents an empty statement or a placeholder.
* **SEQ**: Represents a sequence of statements.
* **EXPR**: Represents an expression.
* **PROG**: Represents a program.

# Virtual Machine

Tiny-C's virtual machine supports the following instructions:

* **IFETCH**: Fetches the value at the specified memory address and pushes it onto the stack.
* **ISTORE**: Pops a value from the stack and stores it at the specified memory address.
* **IPUSH**: Pushes a constant value onto the stack.
* **IPOP**: Pops the top value from the stack.
* **IADD**: Pops the top two values from the stack, adds them, and pushes the result back onto the stack.
* **ISUB**: Pops the top two values from the stack, subtracts the second from the top from the top, and pushes the result back onto the stack.
* **ILT**: Pops the top two values from the stack, compares them for less-than, and pushes the result (1 for true, 0 for false) back onto the stack.
* **JZ**: Jumps to the specified address if the top value on the stack is zero.
* **JNZ**: Jumps to the specified address if the top value on the stack is not zero.
* **JMP**: Unconditional jump to the specified address.
* **HALT**: Halts the execution of the virtual machine.

# Examples

Assign the result of `2<3` to `a`, `b`, and `c`.

```
% echo "a=b=c=2<3;" | ./program.out
a = 1
b = 1
c = 1
```

Compute the smallest power of 2 that is greater than 100.

```
% echo "{ i=1; while (i<100) i=i+i; }" | ./program.out
i = 128
```

Find the Greatest Common Divisor between `i` and `j`.

```
echo "{ i=125; j=100; while (i-j) if (i<j) j=j-i; else i=i-j; }" | ./program.out
i = 25
j = 25
```

Simple `do-while` example.

```
% echo "{ i=1; do i=i+10; while (i<50); }" | ./program.out
i = 51
```

A more complex version of the previous loop (only using `while`).

```
% echo "{ i=1; while ((i=i+10)<50); }" | ./program.out
i = 51
```

A simple program to highlight the available variables (`a` through `z`).

```
% echo "{ i=7; if (i<5) x=1; if (i<10) y=2; }" | ./program.out
i = 7
y = 2
```