all:
	clang tinyc_compiler.c -o program.out

clean:
	rm -f *.out