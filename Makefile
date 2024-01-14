all:
	clang tinyc_compiler.c -o program.out

debug:
	clang tinyc_compiler.c -o debug_program.out -g

clean:
	rm -rf *.out *.out.dSYM tests/*.result

test:
	./program.out < tests/two_is_less_than_three.test > tests/two_is_less_than_three.result
	./program.out < tests/power_of_two.test > tests/power_of_two.result
	./program.out < tests/greatest_common_divisor.test > tests/greatest_common_divisor.result
	./program.out < tests/do_while.test > tests/do_while.result
	./program.out < tests/while.test > tests/while.result
	./program.out < tests/available_vars.test > tests/available_vars.result
