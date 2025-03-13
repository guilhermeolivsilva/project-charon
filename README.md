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

# Running programs

You can run your own programs from the terminal. Simply create a file containing
your code and invoke the `main` with

```
$ python main.py < path/to/your_code.ch
```

This projects uses the `.ch` extension just for the sake of style :)

# The [C]haron language

The [C]haron language is implemented in Python, and consists of a large subset
of the C programming language. It is statically typed and supports integers
(`int`/`short`), floating point numbers (`float`), and user defined structures
(`struct`). It also supports most of C's binary operations, as well as
functions, arrays, control flow (`if`, `if/else`), and loops (`while`,
`do/while`).

The programs shown in the [Examples](#examples) section explore the
capabilities of the language.

## Grammar

The EBNF expression of the language grammar is shown below:

```
<program> ::= <function-definition>
            | <declaration>

<function-definition> ::= <type-specifier> <declarator> {<declaration>}* <compound-statement>

<type-specifier> ::= short
                   | int
                   | float
                   | <struct-specifier>

<struct-specifier> ::= <struct> <identifier> { {<struct-declaration>}+ }
                     | <struct> { {<struct-declaration>}+ }
                     | <struct> <identifier>

<struct-declaration> ::= <type-specifier> <struct-declarator-list>

<struct-declarator-list> ::= <declarator>
                           | <struct-declarator-list> , <direct-declarator>

<direct-declarator> ::= <identifier>
                      | ( <declarator> )
                      | <direct-declarator> [ {<constant-expression>}? ]
                      | <direct-declarator> ( <parameter-type-list> )
                      | <direct-declarator> ( {<identifier>}* )

<constant-expression> ::= <logical-or-expression>

<logical-or-expression> ::= <logical-and-expression>
                          | <logical-or-expression> || <logical-and-expression>

<logical-and-expression> ::= <inclusive-or-expression>
                           | <logical-and-expression> && <inclusive-or-expression>

<inclusive-or-expression> ::= <and-expression>
                            | <inclusive-or-expression> | <and-expression>

<and-expression> ::= <equality-expression>
                   | <and-expression> & <equality-expression>

<equality-expression> ::= <relational-expression>
                        | <equality-expression> == <relational-expression>
                        | <equality-expression> != <relational-expression>

<relational-expression> ::= <shift-expression>
                          | <relational-expression> < <shift-expression>
                          | <relational-expression> > <shift-expression>

<shift-expression> ::= <additive-expression>
                     | <shift-expression> << <additive-expression>
                     | <shift-expression> >> <additive-expression>

<additive-expression> ::= <multiplicative-expression>
                        | <additive-expression> + <multiplicative-expression>
                        | <additive-expression> - <multiplicative-expression>

<multiplicative-expression> ::= <unary-expression>
                              | <multiplicative-expression> * <unary-expression>
                              | <multiplicative-expression> / <unary-expression>
                              | <multiplicative-expression> % <unary-expression>

<unary-expression> ::= <postfix-expression>
                     | <unary-operator> <unary-expression>

<postfix-expression> ::= <primary-expression>
                       | <postfix-expression> [ <expression> ]
                       | <postfix-expression> ( {<assignment-expression>}* )
                       | <postfix-expression> . <identifier>

<primary-expression> ::= <identifier>
                       | ( <expression> )

<constant> ::= <integer-constant>
             | <floating-constant>

<expression> ::= <assignment-expression>
               | <expression> , <assignment-expression>

<assignment-expression> ::= <logical-or-expression>
                          | <unary-expression> <assignment-operator> <assignment-expression>

<assignment-operator> ::= =

<unary-operator> ::= !

<parameter-type-list> ::= <parameter-list>
                        | <parameter-list> , ...

<parameter-list> ::= <parameter-declaration>
                   | <parameter-list> , <parameter-declaration>

<parameter-declaration> ::= {<type-specifier>}+ <declarator>

<declaration> ::=  {<type-specifier>}+ {<declarator>}* ;

<compound-statement> ::= { {<declaration>}* {<statement>}* }

<statement> ::= <expression-statement>
              | <compound-statement>
              | <selection-statement>
              | <iteration-statement>

<expression-statement> ::= {<expression>}? ;

<selection-statement> ::= if ( <expression> ) <statement>
                        | if ( <expression> ) <statement> else <statement>

<iteration-statement> ::= while ( <expression> ) <statement>;
```

## Lexer

The [`Lexer`](https://github.com/guilhermeolivsilva/project-charon/blob/main/src/lexer.py)
tokenizes and pre-processes the code. It also makes some basic syntax checks.

Check its attributes (namely, `conditionals`, `symbols`, `operators`, and
`types`) for a better picture of the language's capabilities. Also, look for the
`Raises` sections in its methods docstrings for a better grasp of the syntax
checks it performs.

## Abstract Syntax Tree

The language builds its Abstract Syntax Tree (AST) with the
[`AbstractSyntaxTree`](https://github.com/guilhermeolivsilva/project-charon/blob/main/src/abstract_syntax_tree.py)
class. It has operation precedence, and is generated recursively. It makes
additional syntax checks, and it is worth to check its `Raises` sections.

Also, the class implements the `print_tree` method. It is very useful as it
offers a visualization of the tree it built.

## Code Generator

This project compiles code with the `CodeGenerator` class. It takes an AST
and generates a list of instructions to be run by the [`VirtualMachine`](#virtual-machine).

## Virtual Machine

Finally, the compiled code runs in the
[`VirtualMachine`](https://github.com/guilhermeolivsilva/project-charon/blob/main/src/virtual_machine.py).
It interprets the code, instruction by instruction, and implements a local memory
and some execution registers (`program_counter`, `memory_pointer` etc.).

You can check its memory layout after the program ends running with the `print`
method. It dumps the non-null memory addresses and the state of the internal
registers.

# Examples

All the following examples have been implemented as integration tests, and you
may find it [here](https://github.com/guilhermeolivsilva/project-charon/tree/main/tests/integration).

These tests cover all of the language's functionality:

- arrays;
- control flow: `if`, `if/else`;
- `do/while` loops;
- expressions;
- functions;
- operations (mathematical and logical);
- structs;
- `while` loops.

And also some cool programs:

- compute the Fibonacci sequence;
- compute the greatest common divisor between two numbers.

There are also unit tests. These are very useful to dive deeper into additional
details of the project's features. You may find it [here](https://github.com/guilhermeolivsilva/project-charon/tree/main/tests/unit).
