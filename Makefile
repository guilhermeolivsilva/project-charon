all:
	clang tinyc_compiler.c -o program.out

debug:
	clang tinyc_compiler.c -o debug_program.out -g

clean:
	rm -rf *.out *.out.dSYM

sanity:
	echo "a=b=c=2<3;" | ./program.out
	echo "{ i=1; while (i<100) i=i+i; }" | ./program.out
	echo "{ i=125; j=100; while (i-j) if (i<j) j=j-i; else i=i-j; }" | ./program.out
	echo "{ i=1; do i=i+10; while (i<50); }" | ./program.out
	echo "{ i=1; while ((i=i+10)<50) ; }" | ./program.out
	echo "{ i=7; if (i<5) x=1; if (i<10) y=2; }" | ./program.out