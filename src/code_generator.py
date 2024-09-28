"""Implement a code generator for the virtual machine."""

from typing import Union

from src.ast_nodes.basic.PROG import PROG
from src.ast_nodes.functions.FUNC_DEF import FUNC_DEF
from src.ast_nodes.variables.STRUCT_DEF import STRUCT_DEF
from src.ast_nodes.variables.VAR_DEF import VAR_DEF


class CodeGenerator:
    """
    Code Generator that generates instructions for the virtual machine from
    Abstract Syntax Tree (AST) Nodes.

    This class also keeps track of the structs defined in the source code that
    have been instantiated -- structs that have been defined, but not
    instantiated, are ignored.

    Parameters
    ----------
    root : PROG
        The root of an Abstract Syntax Tree generated by the 
        `src.abstract_syntax_tree.AbstractSyntaxTree`. class
    """

    def __init__(self, root: PROG) -> None:
        self.root: PROG = root
        self.program: dict[str, Union[list, dict]] = {
            "structs": {},
            "functions": {},
            "global_vars": [],
            "code": []
        }
        self.register: int = 0

    def __str__(self) -> str:
        """
        Implement a string representation of a CodeGenerator object.

        This method is intended to be used with `codegen_obj.print()`.

        Returns
        -------
        _str : str
            The string representation of a CodeGenerator object.
        """

        _str: str = ""
        indent: int = 1

        structs = self.program["structs"]
        if structs:
            structs_str = "Structs:"

            for struct_name, struct_attributes in structs.items():
                structs_str += "\n"
                structs_str += "  " * indent
                structs_str += f"{struct_name}: {', '.join(struct_attributes)}"

            _str += structs_str

        # Add some line breaks if there were structs added to `_str`
        if _str:
            _str += "\n\n"

        _str += "Code:"

        # Print the global variables
        for instruction in self.program["global_vars"]:
            _str += "\n"
            _str += str(instruction)

        # Add a line break after the global vars, if any
        if len(_str) > len("Code:"):
            _str += "\n"

        functions = self.program["functions"]
        for function_name, function_indices in functions.items():
            _str += "\n"
            _str += f"{function_name}:"

            start_index = function_indices["start"]
            end_index = function_indices["end"]

            for index in range(start_index, end_index):
                instruction = self.program["code"][index]
                _str += "\n"
                _str += "  " * indent
                _str += str(instruction)

            _str += "\n"

        return _str

    def print(self) -> None:
        """Print this CodeGenerator object."""

        print(self)

    def generate_code(self) -> dict[str, dict]:
        """
        Generate code from a the root of an Abstract Syntax Tree.

        The generated program will also be stored in the `self.program`
        attribute. 
        
        Returns
        -------
        program : dict[str, dict]
            A dictionary with bytecodes and struct metadata generated from some
            Abstract Syntax Tree representation of a program.
        """

        self.parse_struct_definitions()
        self.parse_global_variables()
        self.parse_functions()

        # Add the HALT instruction at the end of the generated code.
        self.program["code"].append({
            "instruction": "HALT",
            "metadata": {}
        })

        return self.program

    def parse_struct_definitions(self) -> None:
        """
        Parse struct definitions and add it to the generated program.

        For structs, we only keep track of the types used by the struct, and
        the the order they appear in.
        """

        struct_def_nodes: list[STRUCT_DEF] = [
            node for node in self.root.children
            if isinstance(node, STRUCT_DEF) and node.is_active()
        ]

        for struct_def in struct_def_nodes:
            struct_type = struct_def.get_type()
            struct_attributes = struct_def.get_attribute_types()

            self.program["structs"][struct_type] = struct_attributes

    def parse_global_variables(self) -> None:
        """
        Generate code for global variables and add it to the generated program.
        """

        global_var_def_nodes: list[VAR_DEF] = [
            node for node in self.root.children
            if isinstance(node, VAR_DEF)
        ]

        for global_var_def in global_var_def_nodes:
            self.register, code = global_var_def.generate_code(
                register=self.register
            )
            self.program["global_vars"].extend(code)

    def parse_functions(self) -> None:
        """
        Generate code for each function and add it to the generated program.
        """

        index: int = len(self.program["code"])

        function_def_nodes: list[FUNC_DEF] = [
            node for node in self.root.children
            if isinstance(node, FUNC_DEF)
        ]

        for function_def in function_def_nodes:
            function_name = function_def.get_function_name()
            function_indices = {
                "start": index
            }

            print(self.register)

            self.register, function_code = function_def.generate_code(
                register=self.register
            )
            self.program["code"].extend(function_code)

            index += len(function_code)

            function_indices["end"] = index
            self.program["functions"][function_name] = function_indices

    def get_program(self) -> dict[str, dict]:
        """
        Get the generated program.

        Returns
        -------
        program : dict[str, dict]
            The generated program.
        """

        return self.program
