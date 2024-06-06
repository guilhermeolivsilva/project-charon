# Project [C]haron

Project [C]haron consists in a translation validation framework of programs
written in a subset of the C language.

Translation validation is a technique to certificate whether a compiler
correctly implements the semantics of the original, high level source code when
translating it to machine code. You can learn more about it in
[Pnueli (1998)](https://doi.org/10.1007/BFb0054170).

The project offers a compiler, a virtual machine, and certificators for both
the front (i.e., the high level, [C]haron language itself) and back (the list
of instructions to be executed by the virtual machine) ends.

The project is further presented in the following sections. First, a short
discussion on the certification strategy used to validate the compiler. And
then, the [C]haron language overview.

# Translation validation

Our translation validation strategy is based on the
[Gödel numbering](https://en.wikipedia.org/wiki/G%C3%B6del_numbering): we
generate a Gödel number for each statement of both the front and back end
sources, based on its semantics. The goal is to generate two sets of numbers
that, if equal, then one can be assured that the compiler has correctly
implemented the semantics of the high level code in terms of low level code.
If the sets don't match, then the compiler has altered the semantics of the
original program during compilation.

# The [C]haron language

The [C]haron language is implemented in Python, and is derived from
[M. Feeley's Tiny-C](https://www.iro.umontreal.ca/~felipe/IFT2030-Automne2002/Complements/tinyc.c).
It is statically typed and supports integers (`long` integers as well),
floating point numbers, and user defined structures. It also supports
functions, arrays, control flow (`if`, `if/else`), and loops (`while`,
`do/while`).

The programs shown in the [Examples](#examples) section explore the
capabilities of the language.

## Grammar

The EBNF expression of the language grammar is shown below:

```
<program> ::= <function>
<function> ::= <id> "(" <parameters> ") { return " <statement> "; }"
<parameters> ::= <id>
<statement> ::= <function call>
                | "if" <parenthesis expression> <statement> ";"
                | "if" <parenthesis expression> <statement> "else" <statement> ";"
                | "while" <parenthesis expression> <statement> ";"
                | "do" <statement> "while" <parenthesis expression> ";"
                | "{" <statement> "}" ";"
                | <expression> ";"
                | ";"
<function call> ::= <name> "(" <expression> ");"
<parenthesis expression> ::= "(" <expression> ")"
<expression> ::= <comparison> | <id> "=" <expression>
<comparison> ::= <sum> | <sum> "<" <sum>
<sum> ::= <term> | <sum> "+" <term> | <sum> "-" <term>
<term> ::= <id> | <constant> | <parenthesis expression>
<id> ::= <type> <name>
<constant> ::= <int> | <float> | <long> | <struct>
<int> ::= unsigned decimal integer
<float> ::= unsigned decimal floating point number
<struct> ::= <name> "{" <type> <name> "};"
<name> ::= any non-reserved word or symbol
```

## Lexer

### Types

* **INT_TYPE**: an unsigned integer.
* **FLOAT_TYPE**: an unsigned floating point number.
* **LONG_TYPE**: an unsigned long integer (64 bits).
* **STRUCT_TYPE**: a user-defined structure.

### Reserved words

* **IF_SYM**: Represents the `if` keyword, used in conditional statements.
* **ELSE_SYM**: Represents the `else` keyword, used in if-else statements.
* **WHILE_SYM**: Represents the `while` keyword, used in while loops.
* **DO_SYM**: Represents the `do` keyword, used in the do-while loop construct.
* **RET_SYM**: Represents the `return` keyword, used in functions.

### Symbols

* **LCBRA, RCBRA**: Represents curly braces (`{`, `}`), used to define blocks of statements.
* **LBRA, RBRA**: Represents braces (`[`, `]`), used to define the length or access an element of an array.
* **LPAR, RPAR**: Represents parenthesis (`(`, `)`), used in expressions, conditionals and functions.
* **PLUS**: Represents the addition operator `+`, used in arithmetic expressions.
* **MINUS**: Represents the subtraction operator `-`, used in arithmetic expressions.
* **LESS**: Represents the less than operator `<`, used in comparison expressions.
* **SEMI**: Represents the semicolon `;`, used to terminate statements.
* **EQUAL**: Represents the equal sign `=`, used in assignment expressions.
* **DOT**: Represents the access of an attribute of a user-defined `struct`.
* **EOI**: Stands for "End of Input" and signifies the end of the input source code.

## Abstract Syntax Tree

Tiny-C works on an internal abstract syntax tree (AST) with the following terms:

* **VAR**: Represents a variable.
* **CST**: Represents a constant value.
* **ADD**: Represents addition operation.
* **SUB**: Represents subtraction operation.
* **LT**: Represents less-than comparison.
* **SET**: Represents assignment operation.
* **IF**: Represents the an `if` statement.
* **IFELSE**: Represents an `if/else` statement.
* **WHILE**: Represents a `while` loop.
* **DO**: Represents a `do/while` loop.
* **EMPTY**: Represents an empty statement or a placeholder.
* **SEQ**: Represents a sequence of statements.
* **EXPR**: Represents an expression.
* **PROG**: Represents a program.

## Virtual Machine

Tiny-C's virtual machine supports the following instructions:

* **IFETCH**: Fetches the value of the specified variable and pushes it onto the stack.
* **ISTORE**: Pops a value from the stack and stores it at the specified variable.
* **IPUSH**: Pushes a constant value onto the stack.
* **IPOP**: Pops the top value from the stack.
* **IADD**: Pops the top two values from the stack, adds them, and pushes the result back onto the stack.
* **ISUB**: Pops the top two values from the stack, subtracts the second from the top from the top, and pushes the result back onto the stack.
* **ILT**: Pops the top two values from the stack, compares them for less-than, and pushes the result (in Python terms, i.e., `True` or `False`) back onto the stack.
* **JZ**: Jumps to the specified node if the top value on the stack is `False`.
* **JNZ**: Jumps to the specified node if the top value on the stack is `True`.
* **JMP**: Unconditional jump to the specified node.
* **HALT**: Halts the execution of the virtual machine.

# Examples

All the following examples have been implemented as integration tests, and you
may find it [here](https://github.com/guilhermeolivsilva/project-charon/tree/main/tests/integration).

## Variable assignment

```
> Input
{
    a = 1;
    c = 3 < 2;
    b = c;
}

> Result
{'a': 1, 'b': False, 'c': False}
```

## Control Flow

```
> Input
{
    i = 10;
    if (i < 5) {
        x = 1;
    }
    else {
        y = 2;
    }
}

> Result
{'i': 10, 'y': 2}
```

## While

```
> Input
{
    i = 1;
    while (i < 100) {
        i = i + i;
    }
}

> Result
{'i': 128}
```

## Do/While

```
> Input
{
    i = 1;
    do { i = i + 10; }
    while (i < 50); 
}

> Result
{'i': 51}
```

## Greatest Commond Divisor

```
> Input
{
    i = 125;
    j = 100;
    while (i - j) {
        if (i < j) {
            j = j - i;
        }
        else {
            i = i - j;
        }
    } 
}

> Result
{'i': 25, 'j': 25}
```

## Fibonacci sequence

```
> Input
{
    i = 1;
    a = 0;
    b = 1;
    while (i < 10) {
        c = a;
        a = b;
        b = c + a;
        i = i + 1; 
    }
}

> Result
{'i': 10, 'a': 34, 'b': 55, 'c': 21}

# (The result is in the `b` variable.)
```
