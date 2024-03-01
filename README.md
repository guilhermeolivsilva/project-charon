# Tiny-C

This is a Python implementation of
[M. Feeley's Tiny-C language](https://www.iro.umontreal.ca/~felipe/IFT2030-Automne2002/Complements/tinyc.c),
originally developed in C.

Tiny-C is a considerably stripped down version of C and it is meant as a
pedagogical tool for learning about compilers. The language supports
variables from `a` to `z`. The compiler reads the program from standard input
and prints out the value of the variables that have been used.

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

* **IF_SYM**: Represents the `if` keyword, used in conditional statements.
* **ELSE_SYM**: Represents the `else` keyword, used in if-else statements.
* **WHILE_SYM**: Represents the `while` keyword, used in while loops.
* **DO_SYM**: Represents the `do` keyword, used in the do-while loop construct.
* **LBRA, RBRA**: Represents curly braces (`{`, `}`), used to define blocks of statements.
* **LPAR, RPAR**: Represents parenthesis (`(`, `)`), used in expressions and conditionals.
* **PLUS**: Represents the addition operator `+`, used in arithmetic expressions.
* **MINUS**: Represents the subtraction operator `-`, used in arithmetic expressions.
* **LESS**: Represents the less than operator `<`, used in comparison expressions.
* **SEMI**: Represents the semicolon `;`, used to terminate statements.
* **EQUAL**: Represents the equal sign `=`, used in assignment expressions.
* **INT**: Represents an integer literal.
* **ID**: Represents an identifier, typically a variable name (e.g., `a`, `b`, `c`).
* **EOI**: Stands for "End of Input" and signifies the end of the input source code.

[!NOTE] 
Notice that valid a program in Tiny-C must specified between curly brackets.

[!NOTE]
Input integers must be in the `[0-9]` range.

# Abstract Syntax Tree

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

# Virtual Machine

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
may find it [here](https://github.com/guilhermeolivsilva/tinyc/tree/main/tests/integration).

## Variable assignment

```
> Input
{
    a = 1;
    c = 3 < 2;
    b = c;
}

> Result
a = 1
b = False
c = False
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
i = 10
y = 2
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
i = 128
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
i = 51
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
i = 25
j = 25
```
