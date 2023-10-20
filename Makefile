all:
	clang tinyc_compiler.c -o program.out

debug:
	clang tinyc_compiler.c -o debug_program.out -g

clean:
	rm -rf *.out *.out.dSYM