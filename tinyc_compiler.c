/* file: "tinyc.c" */

/* Copyright (C) 2001 by Marc Feeley, All Rights Reserved. */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* 
 * This is a compiler for the Tiny-C language.  Tiny-C is a
 * considerably stripped down version of C and it is meant as a
 * pedagogical tool for learning about compilers.  The integer global
 * variables "a" to "z" are predefined and initialized to zero, and it
 * is not possible to declare new variables.  The compiler reads the
 * program from standard input and prints out the value of the
 * variables that are not zero.  The grammar of Tiny-C in EBNF is:
 *
 *  <program> ::= <statement>
 *  <statement> ::= "if" <paren_expr> <statement> |
 *                  "if" <paren_expr> <statement> "else" <statement> |
 *                  "while" <paren_expr> <statement> |
 *                  "do" <statement> "while" <paren_expr> ";" |
 *                  "{" { <statement> } "}" |
 *                  <expr> ";" |
 *                  ";"
 *  <paren_expr> ::= "(" <expr> ")"
 *  <expr> ::= <test> | <id> "=" <expr>
 *  <test> ::= <sum> | <sum> "<" <sum>
 *  <sum> ::= <term> | <sum> "+" <term> | <sum> "-" <term>
 *  <term> ::= <id> | <int> | <paren_expr>
 *  <id> ::= "a" | "b" | "c" | "d" | ... | "z"
 *  <int> ::= <an_unsigned_decimal_integer>
 *
 * Here are a few invocations of the compiler:
 *
 * % echo "a=b=c=2<3;" | ./a.out
 * a = 1
 * b = 1
 * c = 1
 * % echo "{ i=1; while (i<100) i=i+i; }" | ./a.out
 * i = 128
 * % echo "{ i=125; j=100; while (i-j) if (i<j) j=j-i; else i=i-j; }" | ./a.out
 * i = 25
 * j = 25
 * % echo "{ i=1; do i=i+10; while (i<50); }" | ./a.out
 * i = 51
 * % echo "{ i=1; while ((i=i+10)<50) ; }" | ./a.out
 * i = 51
 * % echo "{ i=7; if (i<5) x=1; if (i<10) y=2; }" | ./a.out
 * i = 7
 * y = 2
 *
 * The compiler does a minimal amount of error checking to help
 * highlight the structure of the compiler.
 */


/*---------------------------------------------------------------------------*/

/* Lexer. */

enum { DO_SYM, ELSE_SYM, IF_SYM, WHILE_SYM, LBRA, RBRA, LPAR, RPAR,
       PLUS, MINUS, LESS, SEMI, EQUAL, INT, ID, EOI };

char *words[] = { "do", "else", "if", "while", NULL };

int ch = ' ';
int sym;
int int_val;
char id_name[100];

void syntax_error() {
  fprintf(stderr, "syntax error\n");
  exit(1);
}

void next_character() {
  ch = getchar(); 
}

void next_sym() {
  again: switch (ch) {
    case ' ':
    case '\n':
      next_character();
      goto again;

    case EOF:
      sym = EOI;
      break;

    case '{':
      next_character();
      sym = LBRA;
      break;

    case '}':
      next_character();
      sym = RBRA;
      break;

    case '(':
      next_character();
      sym = LPAR;
      break;

    case ')':
      next_character();
      sym = RPAR;
      break;

    case '+':
      next_character();
      sym = PLUS;
      break;

    case '-':
      next_character();
      sym = MINUS;
      break;

    case '<':
      next_character();
      sym = LESS;
      break;

    case ';':
      next_character();
      sym = SEMI;
      break;

    case '=':
      next_character();
      sym = EQUAL;
      break;

    default:
      if (ch >= '0' && ch <= '9') {
        int_val = 0; /* missing overflow check */

        while (ch >= '0' && ch <= '9') {
            int_val = int_val * 10 + (ch - '0');
            next_character();
          }
          sym = INT;
        }

      else if (ch >= 'a' && ch <= 'z') {
        int i = 0; /* missing overflow check */
        while ((ch >= 'a' && ch <= 'z') || ch == '_') {
          id_name[i++] = ch;
          next_character();
        }

        id_name[i] = '\0';
        sym = 0;

        while (words[sym] != NULL && strcmp(words[sym], id_name) != 0)
          sym++;

        if (words[sym] == NULL) {
          if (id_name[1] == '\0')
            sym = ID;
          else
            syntax_error();
        }
      }
      else
        syntax_error();
    }
}

/*---------------------------------------------------------------------------*/

/* Parser. */

enum { VAR, CST, ADD, SUB, LT, SET,
       IF1, IF2, WHILE, DO, EMPTY, SEQ, EXPR, PROG };

struct ast_node {
  int node_kind;
  struct ast_node *child_1, *child_2, *child_3;
  int node_value;
};
typedef struct ast_node ast_node;

ast_node *new_node(int k) {
  ast_node *x = (ast_node*) malloc(sizeof(ast_node));
  x->node_kind = k;
  return x;
}

ast_node *paren_expr(); /* forward declaration */

/* <term> ::= <id> | <int> | <paren_expr> */
ast_node *term() {
  ast_node *x;
  if (sym == ID) {
    x = new_node(VAR);
    x->node_value = id_name[0] - 'a';
    next_sym();
  }
  else if (sym == INT) {
    x = new_node(CST);
    x->node_value = int_val;
    next_sym();
  }
  else
    x = paren_expr();

  return x;
}

/* <sum> ::= <term> | <sum> "+" <term> | <sum> "-" <term> */
ast_node *sum() {
  ast_node *t, *x = term();
  while (sym == PLUS || sym == MINUS) {
    t = x;
    x = new_node(sym == PLUS ? ADD : SUB);
    next_sym();
    x->child_1 = t;
    x->child_2 = term();
  }
  return x;
}

/* <test> ::= <sum> | <sum> "<" <sum> */
ast_node *test() {
  ast_node *t, *x = sum();
  if (sym == LESS) {
    t = x;
    x = new_node(LT);
    next_sym();
    x->child_1 = t;
    x->child_2 = sum();
  }
  return x;
}

/* <expr> ::= <test> | <id> "=" <expr> */
ast_node *expr() {
  ast_node *t, *x;
  if (sym != ID)
    return test();
  
  x = test();
  if (x->node_kind == VAR && sym == EQUAL) {
    t = x;
    x = new_node(SET);
    next_sym();
    x->child_1 = t;
    x->child_2 = expr();
  }

  return x;
}

/* <paren_expr> ::= "(" <expr> ")" */
ast_node *paren_expr() {
  ast_node *x;

  if (sym == LPAR)
    next_sym();
  else
    syntax_error();

  x = expr();

  if (sym == RPAR)
    next_sym();
  else
    syntax_error();

  return x;
}

ast_node *statement() {
  ast_node *t, *x;

  /* "if" <paren_expr> <statement> */
  if (sym == IF_SYM) {
    x = new_node(IF1);
    next_sym();
    x->child_1 = paren_expr();
    x->child_2 = statement();

    /* ... "else" <statement> */
    if (sym == ELSE_SYM) {
      x->node_kind = IF2;
      next_sym();
      x->child_3 = statement();
    }
  }

  /* "while" <paren_expr> <statement> */
  else if (sym == WHILE_SYM) {
    x = new_node(WHILE);
    next_sym();
    x->child_1 = paren_expr();
    x->child_2 = statement();
  }

  /* "do" <statement> "while" <paren_expr> ";" */
  else if (sym == DO_SYM) {
    x = new_node(DO);
    next_sym();
    x->child_1 = statement();

    if (sym == WHILE_SYM)
      next_sym();
    else
      syntax_error();

    x->child_2 = paren_expr();

    if (sym == SEMI)
      next_sym();
    else
      syntax_error();
  }

  /* ";" */
  else if (sym == SEMI) {
    x = new_node(EMPTY);
    next_sym();
  }

  /* "{" { <statement> } "}" */
  else if (sym == LBRA) {
    x = new_node(EMPTY);
    next_sym();

    while (sym != RBRA) {
      t = x;
      x = new_node(SEQ);
      x->child_1 = t;
      x->child_2 = statement();
    }
    next_sym();
  }

  /* <expr> ";" */
  else {
    x = new_node(EXPR);
    x->child_1 = expr();

    if (sym == SEMI)
      next_sym();
    else
      syntax_error();
  }

  return x;
}

/* <program> ::= <statement> */
ast_node *program() {
  ast_node *x = new_node(PROG);

  next_sym();
  x->child_1 = statement();
  
  if (sym != EOI)
    syntax_error();

  return x;
}

/*---------------------------------------------------------------------------*/

/* Code generator. */

enum { IFETCH, ISTORE, IPUSH, IPOP, IADD, ISUB, ILT, JZ, JNZ, JMP, HALT };

typedef char code;
code object[1000], *here = object;

void add_to_code_collection(code c) {
  *here++ = c;
} /* missing overflow check */

code *create_code_hole() {
  return here++;
}

void path_source_reference(code *src, code *dst) {
  *src = dst - src;
} /* missing overflow check */

void generate_code_from_ast_node(ast_node *x) {
  code *p1, *p2;
  switch (x->node_kind) {
    case VAR:
      add_to_code_collection(IFETCH);
      add_to_code_collection(x->node_value);
      break;

    case CST:
      add_to_code_collection(IPUSH);
      add_to_code_collection(x->node_value);
      break;

    case ADD:
      generate_code_from_ast_node(x->child_1);
      generate_code_from_ast_node(x->child_2);
      add_to_code_collection(IADD);
      break;

    case SUB:
      generate_code_from_ast_node(x->child_1);
      generate_code_from_ast_node(x->child_2);
      add_to_code_collection(ISUB);
      break;

    case LT:
      generate_code_from_ast_node(x->child_1);
      generate_code_from_ast_node(x->child_2);
      add_to_code_collection(ILT);
      break;

    case SET:
      generate_code_from_ast_node(x->child_2);
      add_to_code_collection(ISTORE);
      add_to_code_collection(x->child_1->node_value);
      break;

    case IF1:
      generate_code_from_ast_node(x->child_1);
      add_to_code_collection(JZ);
      p1 = create_code_hole();
      generate_code_from_ast_node(x->child_2);
      path_source_reference(p1, here);
      break;

    case IF2:
      generate_code_from_ast_node(x->child_1);
      add_to_code_collection(JZ);
      p1 = create_code_hole();
      generate_code_from_ast_node(x->child_2);
      add_to_code_collection(JMP);
      p2 = create_code_hole();
      path_source_reference(p1, here);
      generate_code_from_ast_node(x->child_3);
      path_source_reference(p2, here);
      break;

    case WHILE:
      p1 = here;
      generate_code_from_ast_node(x->child_1);
      add_to_code_collection(JZ);
      p2 = create_code_hole();
      generate_code_from_ast_node(x->child_2);
      add_to_code_collection(JMP);
      path_source_reference(create_code_hole(), p1);
      path_source_reference(p2, here);
      break;

    case DO:
      p1 = here;
      generate_code_from_ast_node(x->child_1);
      generate_code_from_ast_node(x->child_2);
      add_to_code_collection(JNZ);
      path_source_reference(create_code_hole(), p1);
      break;

    case SEQ:
      generate_code_from_ast_node(x->child_1);
      generate_code_from_ast_node(x->child_2);
      break;

    case EXPR:
      generate_code_from_ast_node(x->child_1);
      add_to_code_collection(IPOP);
      break;

    case PROG:
      generate_code_from_ast_node(x->child_1);
      add_to_code_collection(HALT);
      break;

    case EMPTY:
      break;
  }
}

/*---------------------------------------------------------------------------*/

/* Virtual machine. */

int globals[26];

void run() {
  int stack[1000], *sp = stack;
  code *pc = object;

  again:
    switch (*pc++) {
      case IFETCH:
        *sp++ = globals[*pc++];
        goto again;

      case ISTORE:
        globals[*pc++] = sp[-1];
        goto again;

      case IPUSH:
        *sp++ = *pc++;
        goto again;

      case IPOP:
        --sp;
        goto again;

      case IADD:
        sp[-2] = sp[-2] + sp[-1];
        --sp;
        goto again;

      case ISUB:
        sp[-2] = sp[-2] - sp[-1];
        --sp;
        goto again;

      case ILT:
        sp[-2] = sp[-2] < sp[-1];
        --sp;
        goto again;

      case JMP:
        pc += *pc;
        goto again;

      case JZ:
        if (*--sp == 0)
          pc += *pc;
        else
          pc++;
        goto again;

      case JNZ:
        if (*--sp != 0)
          pc += *pc;
        else
          pc++;
        goto again;
    }
}

/*---------------------------------------------------------------------------*/

/* Main program. */

int main() {
  int i;

  generate_code_from_ast_node(program());

  for (i=0; i<26; i++)
    globals[i] = 0;

  run();

  for (i=0; i<26; i++)
    if (globals[i] != 0)
      printf("%c = %d\n", 'a'+i, globals[i]);

  return 0;
}
