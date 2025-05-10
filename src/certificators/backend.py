"""Certificator for the frontend representation of [C]haron programs."""

from copy import deepcopy
from typing import Union

from typing_extensions import override

from src.certificators.abstract_certificator import AbstractCertificator
from src.utils import (
    get_certificate_symbol,
    primes_list,
    INSTRUCTIONS_CATEGORIES,
)


class BackendCertificator(AbstractCertificator):
    """
    Certificate the backend representation of some program.

    Parameters
    ----------
    program : dict[str, dict]
        A dictionary with bytecodes and struct metadata generated from some
        Abstract Syntax Tree representation of a program.
    """

    def __init__(self, program: dict[str, dict]) -> None:
        super().__init__()

        # Input
        self.program = deepcopy(program)
        self.bytecode_list = self.program["code"]

        self.register_to_bytecode_dependencies = {}

        self.environment = {
            "functions": {},
            "variables": {},
            "stash": {}
        }

        # Tell whether a bytecode has been accounted for in the certification
        # process or not. Maps the ID of `bytecode_list` to `True` if already
        # certificated, or `False` otherwise.
        self.bytecode_status: dict[int, bool] = {
            bytecode["bytecode_id"]: False
            for bytecode in self.bytecode_list
        }

        # Compute the primes associated with the defined functions, and the
        # primes and identify the types of variables.
        self._compute_register_to_bytecode_dependencies()
        self._preprocess_conditionals()
        self._preprocess_functions()
        self._preprocess_variables()

        self.bytecode_handlers = {
            # Instructions that might implement more than 1 operation, or
            # require special handling
            "CONSTANT": self._handle_constant,
            "MOV": self._handle_mov,
            "JAL": self._handle_function_call,
            "JZ": self._handle_control_flow,

            # 1:1 instructions
            **{
                binop: self._handle_simple_instruction
                for binop in INSTRUCTIONS_CATEGORIES["binops"]
            },
            **{
                unop: self._handle_simple_instruction
                for unop in INSTRUCTIONS_CATEGORIES["unops"]
            },
            **{
                misc: self._handle_simple_instruction
                for misc in INSTRUCTIONS_CATEGORIES["misc"]
            },
        }

    def _compute_register_to_bytecode_dependencies(self) -> None:
        """
        Compute the dependency relation between a register and bytecode IDs.

        This will map a register to the first bytecode ID of each operation
        upon which it depends on. For example, if a register depends on a
        variable to be computed, it will be mapped to the bytecode ID of the
        `CONSTANT` instruction that first obtains the variable's base address.
        """

        for bytecode in self.program["code"]:
            # We don't care about bytecodes that do not write in a temporary
            # register
            if "register" not in bytecode["metadata"]:
                continue

            register = bytecode["metadata"]["register"]

            # Ignore special registers (the same apply for the repetitions of
            # this check)
            if isinstance(register, str):
                continue

            instruction = bytecode["instruction"]
            bytecode_id = bytecode["bytecode_id"]

            if instruction in ["CONSTANT", "MOV"]:
                self.register_to_bytecode_dependencies[register] = [bytecode_id]

            elif instruction in INSTRUCTIONS_CATEGORIES["binops"]:
                lhs_register = bytecode["metadata"]["lhs_register"]
                if isinstance(lhs_register, int):
                    bytecode_ids_lhs_depends_on = (
                        self.register_to_bytecode_dependencies[lhs_register]
                    )
                else:
                    bytecode_ids_lhs_depends_on = []

                rhs_register = bytecode["metadata"]["rhs_register"]
                if isinstance(rhs_register, int):
                    bytecode_ids_rhs_depends_on = (
                        self.register_to_bytecode_dependencies[rhs_register]
                    )
                else:
                    bytecode_ids_rhs_depends_on = []


                self.register_to_bytecode_dependencies[register] = [
                    *bytecode_ids_lhs_depends_on,
                    *bytecode_ids_rhs_depends_on
                ]

            elif instruction in [
                *INSTRUCTIONS_CATEGORIES["unops"], 
                *INSTRUCTIONS_CATEGORIES["type_casts"],
                *["LOAD", "LOADF"]
            ]:
                value_register = bytecode["metadata"]["value"]
                if isinstance(value_register, int):
                    bytecode_ids_value_depends_on = (
                        self.register_to_bytecode_dependencies[value_register]           
                    )
                    self.register_to_bytecode_dependencies[register] = (
                        bytecode_ids_value_depends_on
                    )

    def _preprocess_functions(self) -> None:
        """
        Compute the function prime associated with each function.

        This method will map the function's ID to a unique prime number.
        """

        _functions_ids = range(1, len(self.program["functions"]) + 1)
        self.environment["functions"] = {
            function_id: {"prime": prime}

            for function_id, prime in zip(
                _functions_ids, primes_list(len(_functions_ids))
            )
        }

    def _preprocess_variables(self) -> None:
        """
        Compute the variable prime associated with each variable.

        This method will map the variable's base address to a unique prime
        number. The primes are in ascending order and are assigned to variables
        according to their addresses also in ascending order.
        """

        temp_variables = {}

        for bytecode_idx, bytecode in enumerate(self.bytecode_list):
            # Mark any type-casts as done, as they're handled below
            if bytecode["instruction"] in INSTRUCTIONS_CATEGORIES["type_casts"]:
                bytecode_id = bytecode["bytecode_id"]
                self.bytecode_status[bytecode_id] = True

            try:
                next_bytecode_idx = bytecode_idx + 1
                next_bytecode = self.bytecode_list[next_bytecode_idx]

                is_variable = (
                    bytecode["instruction"] == "CONSTANT"
                    and next_bytecode["instruction"] == "ADD"
                    and next_bytecode["metadata"]["rhs_register"] == "zero"
                )

                if not is_variable:
                    continue

                # Try to infer the variable type
                var_type = None

                # Find the *actual* variable register (right now, we have the
                # register with the base address of it)
                var_base_address_register = next_bytecode["metadata"]["register"]
                var_base_address = bytecode["metadata"]["value"]

                var_address_register, var_address = None, None

                _to_analyze = self.bytecode_list[next_bytecode_idx:]
                for _idx, temp_bytecode in enumerate(_to_analyze):
                    temp_bytecode_idx = _idx + next_bytecode_idx

                    # We can only know the offset if it is constant
                    # (that comes right before `ADD`)
                    can_tell_var_offset = (
                        temp_bytecode["instruction"] == "ADD"
                        and temp_bytecode["metadata"]["lhs_register"] == var_base_address_register
                        and self.bytecode_list[temp_bytecode_idx - 1]["instruction"] == "CONSTANT"
                    )

                    if can_tell_var_offset:
                        var_offset = self.bytecode_list[temp_bytecode_idx - 1]["metadata"]["value"]
                        
                        var_address = hex(int(var_base_address, 16) + var_offset)
                        var_address_register = temp_bytecode["metadata"]["register"]

                        break

                # If there isn't any `ADD` instruction computed with the base
                # address, then the base address is already the actual address.
                if var_address_register is None:
                    var_address_register = var_base_address_register
                    var_address = var_base_address

                following_bytecode_idx = next_bytecode_idx + 1
                following_bytecode = self.bytecode_list[following_bytecode_idx]

                # 1. First attempt: by checking if it is being read from
                #    - just a `LOAD`: integer
                #    - just a `LOADF`: float
                #    - `LOAD` followed by `TRUNC`: short
                if following_bytecode["instruction"] == "LOAD":
                    var_type = (
                        "short"

                        # The type-cast to short should be right after `LOAD`
                        if self.bytecode_list[following_bytecode_idx + 1]["instruction"] == "TRUNC"
                        else "int"
                    )

                elif following_bytecode["instruction"] == "LOADF":
                    var_type = "float"

                # 2. Second attempt: by checking how a value is written to it
                #    - just a `STORE`: integer
                #    - just a `STOREF`: float
                #    - `STORE` preceeded by `TRUNC`: short

                for _idx, temp_bytecode in enumerate(self.bytecode_list[following_bytecode_idx:]):
                    temp_bytecode_idx = _idx + following_bytecode_idx

                    if temp_bytecode["instruction"] == "STORE" and temp_bytecode["metadata"]["register"] == var_address_register:
                        var_type = (
                            "short"
                            if self.bytecode_list[temp_bytecode_idx - 1]["instruction"] == "TRUNC"
                            else "int"
                        )
                        break

                    if temp_bytecode["instruction"] == "STOREF" and temp_bytecode["metadata"]["register"] == var_address_register:
                        var_type = "float"
                        break

                if var_type is None:
                    continue

                if var_base_address in temp_variables:
                    temp_variables[var_base_address]["addresses"][var_address] = var_type

                else:
                    temp_variables[var_base_address] = {
                        "addresses": {var_address: var_type}
                    }

            except IndexError:
                break

            except KeyError:
                continue


        variables = {
            key: {
                "addresses": temp_variables[key]["addresses"],
                "prime": var_prime
            }
            for key, var_prime in zip(
                sorted(temp_variables.keys(), key=lambda x: int(x, 16)),
                primes_list(len(temp_variables.keys()))
            )
        }

        self.environment["variables"] = variables

    def _preprocess_conditionals(self) -> None:
        """
        Parse the bytecode list and preprocess all the conditional jumps.

        This method will mark the beginning of every expression that predicate
        conditionals (in the form of `JZ` bytecodes that *do not* evaluate the
        `zero` register) by adding a "pending symbol" to the environment stash.
        """

        insertion_points = []

        for bytecode in self.program["code"]:
            is_conditional = (
                bytecode["instruction"] == "JZ"
                and bytecode["metadata"]["conditional_register"] != "zero"
            )

            if not is_conditional:
                continue

            register = bytecode["metadata"]["conditional_register"]

            bytecode_ids_it_depends_on = self.register_to_bytecode_dependencies[register]
            insertion_points.append(min(bytecode_ids_it_depends_on) - 1)

        for point in insertion_points:
            self.environment["stash"][point] = [str(get_certificate_symbol("COND"))]

    @override
    def certificate(self, **kwargs) -> str:
        """
        Certificate the backend code.

        This method iterates over the machine code and annotate each bytecode
        with its relative position and contents.

        Returns
        -------
        computed_certificate : str
            The computed certificate.

        Raises
        ------
        ValueError
            Raised if there are unprocessed bytecodes (i.e., not marked as done
            in `self.bytecode_status`).
        """

        computed_exponents = []

        for idx, bytecode in enumerate(self.bytecode_list):
            bytecode_id = bytecode["bytecode_id"]

            # Skip instructions that have already been handled.
            if bytecode_id is not None and self.bytecode_status[bytecode_id]:
                continue

            # First, check if there are any pending exponents for this index
            if idx in self.environment["stash"]:
                pending_exponent = self.environment["stash"][idx]
                computed_exponents.extend(pending_exponent)

            # ...then handle this bytecode
            exponent = self._certificate_instruction(
                bytecode=bytecode,
                bytecode_idx=idx
            )

            computed_exponents.extend(exponent)

        # Assert all the instructions have been accounted for
        _err_msg = "Certification failed: there are uncertificated instructions."
        if not(all(self.bytecode_status.values())):
            print("Instruction IDs with missing certificates:")
            print([
                bytecode_id
                for bytecode_id, status in self.bytecode_status.items()
                if not status
            ])

            print("------")
            print("\n".join(computed_exponents))
            print("------")
            raise ValueError(_err_msg)

        self.computed_certificate = [
            f"{positional_prime}^({exponent})"
            for positional_prime, exponent in zip(
                primes_list(len(computed_exponents)),
                computed_exponents
            )
        ]

        # self.computed_certificate = "*".join(self.computed_certificate)
        # self.computed_certificate = "*".join(
        #     sorted(
        #         self.computed_certificate.split("*"),
        #         key=lambda x: int(x.split("^")[0])
        #     )
        # )

        return self.computed_certificate

    def _certificate_instruction(
        self,
        bytecode: dict[str, dict],
        bytecode_idx: int
    ) -> list[str]:
        """
        Compute the certificate of an instruction.

        This method dispatches the adequate certification method for the given
        instruction.

        Parameters
        ----------
        bytecode : dict[str, dict]
            The bytecode to certificate.
        bytecode_idx : int
            The index of this `bytecode` in `self.bytecode_list`.

        Returns
        -------
        exponent : list[str]
            The exponent that encodes the operation this instruction implements.

        Raises
        ------
        RuntimeError
            Raised if the certificator can't find the adequate handler for a
            given bytecode.
        """

        instruction = bytecode["instruction"]

        try:
            bytecode_handler = self.bytecode_handlers[instruction]
            exponent = bytecode_handler(
                bytecode=bytecode,
                bytecode_idx=bytecode_idx
            )

        except KeyError as e:
            print(f"Handler for {instruction} has not been implemented yet")
            print(bytecode)
            print(e)
            raise RuntimeError

        return exponent

    def _handle_constant(
        self,
        bytecode: dict[str, dict],
        bytecode_idx: int
    ) -> list[str]:
        """
        Handle a `CONSTANT` bytecode.

        This bytecode might mean 4 things:

        1. If followed by `ADD r_add r_constant zero; LOAD(F) r_var r_add`, it
        is loading the value of a variable into a register;
        2. If followed by `ADD r_add r_constant zero`, it is loading the address
        of a variable into a register;
        3. If followed by `STORE(F) r_constant arg`, it is a function parameter.
        4. It is a simple constant that will be used in an expression.

        So we must handle it accordingly.

        Parameters
        ----------
        bytecode : dict[str, dict]
            The `CONSTANT` bytecode.
        bytecode_idx : int
            The index of this `bytecode` in `self.bytecode_list`.

        Returns
        -------
        exponent : list[str]
            The encoding of the operation this `CONSTANT` implements.
        """

        # Figure out what operation it implements
        next_bytecode = self.bytecode_list[bytecode_idx + 1]
        next_bytecode_idx = bytecode_idx + 1

        # Cases 1 or 2: variable value/address
        is_variable = (
            next_bytecode["instruction"] == "ADD"
            and next_bytecode["metadata"]["rhs_register"] == "zero"
        )

        is_parameter = (
            next_bytecode["instruction"] in ["STORE", "STOREF"]
            and next_bytecode["metadata"]["value"] == "arg"
        )

        if is_variable:
            return self._handle_variable(
                bytecode=bytecode,
                bytecode_idx=bytecode_idx
            )

        # Case 3: function parameter
        elif is_parameter:
            return self._handle_parameter(
                bytecode=bytecode,
                bytecode_idx=bytecode_idx
            )
        
        # Case 4: just a constant
        constant_value = bytecode["metadata"]["value"] + 1 # Avoid exp. identity
        symbol = get_certificate_symbol("CST")
        exponent = f"({symbol})^({constant_value})"

        # Mark the involved bytecode as done.
        self.bytecode_status[bytecode["bytecode_id"]] = True

        return [exponent]

    def _handle_variable(
        self,
        bytecode: dict[str, dict],
        bytecode_idx: int,
    ) -> list[str]:
        """
        Handle a variable use case.

        This method will return the appropriate encoding exponent depending on
        the variable kind (simple, struct/array, or array with dynamic
        indexing), and whether it is being read from or written to.

        Parameters
        ----------
        bytecode : dict[str, dict]
            The initial bytecode that implements this variable usage.
        bytecode_idx : int
            The index of this `bytecode` in `self.bytecode_list`.

        Returns
        -------
        exponent : list[str]
            The encoding xponent of this variable usage.
        """

        # Speculate if this is an array or struct and compute the exponent and
        # the number of bytecodes that implemented it based on the following
        # bytecodes
        next_bytecode_idx = bytecode_idx + 1

        exponent, bytecodes_to_mark_as_done = self._speculate_data_structure(
            bytecode=bytecode,
            bytecode_idx=bytecode_idx,
        )

        # If not an array or struct, certificate as a simple variable.
        if not all([exponent, bytecodes_to_mark_as_done]):
            following_bytecode_idx = next_bytecode_idx + 1
            following_bytecode = self.bytecode_list[following_bytecode_idx]

            context = (
                "value" if following_bytecode["instruction"] in ["LOAD", "LOADF"]
                else "address"
            )
            symbol = get_certificate_symbol(f"VAR_{context.upper()}")
            var_prime = self._get_variable_prime(bytecode)

            exponent = (
                f"({symbol})"
                + f"^({var_prime})"
                + "^(2)"
                + "^(1)"
            )

            # Mark the involved bytecodes as done.
            if context == "address":
                # Mark `CONSTANT` and `ADD` as done.
                bytecodes_to_mark_as_done = 2

            else:
                # Mark `CONSTANT`, `ADD`, and `LOAD` as done.
                bytecodes_to_mark_as_done = 3

                # If this variable is `short`-typed, also mark the type cast as done.
                if self.bytecode_list[bytecode_idx + 3]["instruction"] == "TRUNC":
                    bytecodes_to_mark_as_done += 1

        exponents = [exponent]
        
        # Handle usage of parameter
        var_address = bytecode["metadata"]["value"]
        is_parameter = (
            self.environment["variables"]
                            [var_address].get("parameter", False)
        )

        if is_parameter:
            param_symbol = get_certificate_symbol("PARAM")
            exponents.append(param_symbol)

        for idx in range(bytecode_idx, bytecode_idx + bytecodes_to_mark_as_done):
            bytecode_id = self.bytecode_list[idx]["bytecode_id"]
            self.bytecode_status[bytecode_id] = True

        return exponents
    
    def _get_variable_prime(self, bytecode) -> int:
        """
        Get the prime number that uniquely represents a variable.

        This number is obtained from the certificator environment. This
        environment maps the variable's base address to its unique prime nubmer.

        This method is intended to be used exclusively with `CONSTANT` bytecode.

        Parameters
        ----------
        bytecode : dict[str, dict]
            The `CONSTANT` bytecode. This bytecode contains the base address
            of the variable of interest.

        Returns
        -------
        : int
            The variable prime.
        """

        # The `CONSTANT` bytecode has the variable address as its value.
        var_address = bytecode["metadata"]["value"]
        return self.environment["variables"][var_address]["prime"]
    
    def _speculate_data_structure(
        self,
        bytecode: dict[str, dict],
        bytecode_idx: int,
    ) -> tuple[Union[str, None], Union[int, None]]:
        """
        Speculate if this variable is a data structure (array/struct).

        This is an _speculation_ because we can't tell if a variable is actually
        an array or struct beforehand. To do so, we must check if a specific
        sequence of bytecodes is observed near it.

        Parameters
        ----------
        bytecode : dict[str, dict]
            The initial bytecode that implements this variable usage.
        bytecode_idx : int
            The index of this `bytecode` in `self.bytecode_list`.

        Returns
        -------
        exponent : str or None
            The exponent (that will compose the certificate) of this data
            structure. Returns `None` if this is not a data structure.
        bytecodes_to_mark_as_done : int or None
            The number of bytecodes, including `bytecode`, that will be marked
            as done in `self.bytecode_status`. Returns `None` if this is not
            a data structure.
        """

        following_bytecode_idx = bytecode_idx + 1
        following_bytecode = self.bytecode_list[following_bytecode_idx]

        # The pattern for access to array or struct elements will always begin
        # with `CONSTANT` (`bytecode`, that we already know that it is) + `ADD`
        # (following_bytecode) to get the address of the indexing variable or
        # the index of the element being accessed.
        following_bytecode_is_add = following_bytecode["instruction"] == "ADD"

        # Early return
        if not following_bytecode_is_add:
            return (None, None)
        
        var_prime = self._get_variable_prime(bytecode)

        # Check if it is an access to a struct attribute or to an array element
        # using a constant for index.
        is_static_array_or_struct = True

        # Prevent the speculation of going out of bounds or accessing an
        # unexisting attribute
        try:
            speculated_base_address_register = bytecode["metadata"]["register"]
            speculated_var_address_register = following_bytecode["metadata"]["register"]

            # Pattern:
            # 1. Following bytecode: `CONSTANT` (it has the offset size)
            following_bytecode_idx = following_bytecode_idx + 1
            following_bytecode = self.bytecode_list[following_bytecode_idx]

            speculated_offset_register = following_bytecode["metadata"]["register"]

            # TODO: divide `speculated_index` by the size of the variable type
            speculated_index = following_bytecode["metadata"]["value"]

            is_static_array_or_struct = (
                is_static_array_or_struct
                and following_bytecode["instruction"] == "CONSTANT"
            )

            # 2. Following bytecode: `ADD` (to add the base address from
            # `bytecode` to the `offset`)
            following_bytecode_idx = following_bytecode_idx + 1
            following_bytecode = self.bytecode_list[following_bytecode_idx]

            is_static_array_or_struct = (
                is_static_array_or_struct
                and following_bytecode["instruction"] == "ADD"
                and following_bytecode["metadata"]["lhs_register"] == speculated_var_address_register
                and following_bytecode["metadata"]["rhs_register"] == speculated_offset_register
            )

            # If all the conditions held, return the adequate exponent and
            # number of bytecodes already accounted for
            if is_static_array_or_struct:
                following_bytecode_idx = following_bytecode_idx + 1
                following_bytecode = self.bytecode_list[following_bytecode_idx]

                context = (
                    "value" if following_bytecode["instruction"] in ["LOAD", "LOADF"]
                    else "address"
                )
                symbol = get_certificate_symbol(f"VAR_{context.upper()}")

                exponent = (
                    f"({symbol})"
                    + f"^({var_prime})"
                    + f"^(2)^({speculated_index + 1})"
                )

                # Account for:
                #  - 2 bytecodes to obtain the variable base address
                #  - 1 bytecode to obtain the offset size
                #  - 1 bytecode to obtain the accessed item address
                bytecodes_to_mark_as_done = 4

                # Account for the `LOAD`, if this is a var. value case.
                if context == "value":
                    bytecodes_to_mark_as_done += 1

                return (exponent, bytecodes_to_mark_as_done)

        except (IndexError, KeyError):
            pass

        # Check if it is an access an array element using another variable for
        # index.
        is_dinamically_accessed_array = True

        try:
            # Pattern:
            # 1. First bytecode: `CONSTANT`, with the base address of the array
            following_bytecode_idx = bytecode_idx + 1
            following_bytecode = self.bytecode_list[following_bytecode_idx]

            speculated_base_address_register = bytecode["metadata"]["register"]

            # 2. Following bytecode: `ADD`, with `lhs=speculated_base_address_register`
            # and `rhs=zero`
            speculated_var_address_register = following_bytecode["metadata"]["register"]

            is_dinamically_accessed_array = (
                is_dinamically_accessed_array
                and following_bytecode["instruction"] == "ADD"
                and following_bytecode["metadata"]["lhs_register"] == speculated_base_address_register
                and following_bytecode["metadata"]["rhs_register"] == "zero"
            )

            # 3. Following bytecode: `CONSTANT`, with the base address of the
            # indexing variable.
            following_bytecode_idx = following_bytecode_idx + 1
            following_bytecode = self.bytecode_list[following_bytecode_idx]

            # This is the base address
            speculated_index_var_base_address_register = following_bytecode["metadata"]["register"]
            speculated_index_var_prime = self._get_variable_prime(following_bytecode)

            is_dinamically_accessed_array = (
                is_dinamically_accessed_array
                and following_bytecode["instruction"] == "CONSTANT"
            )

            # 4. Following bytecode: `ADD`, with `lhs=speculated_index_var_base_address_register`
            # and `rhs=zero`
            following_bytecode_idx = following_bytecode_idx + 1
            following_bytecode = self.bytecode_list[following_bytecode_idx]

            # This is the actual address
            speculated_index_var_address_register = following_bytecode["metadata"]["register"]

            is_dinamically_accessed_array = (
                is_dinamically_accessed_array
                and following_bytecode["instruction"] == "ADD"
                and following_bytecode["metadata"]["lhs_register"] == speculated_index_var_base_address_register
                and following_bytecode["metadata"]["rhs_register"] == "zero"
            )

            # 5. Following bytecode: `LOAD`, fetching data from
            # `speculated_index_address_register`
            following_bytecode_idx = following_bytecode_idx + 1
            following_bytecode = self.bytecode_list[following_bytecode_idx]
            
            speculated_index_var_value_register = following_bytecode["metadata"]["register"]

            is_dinamically_accessed_array = (
                is_dinamically_accessed_array
                and following_bytecode["instruction"] == "LOAD"
                and following_bytecode["metadata"]["value"] == speculated_index_var_address_register
            )

            # 6. Following bytecode: `CONSTANT` (it has the type size)
            following_bytecode_idx = following_bytecode_idx + 1
            following_bytecode = self.bytecode_list[following_bytecode_idx]

            speculated_type_size_register = following_bytecode["metadata"]["register"]

            is_dinamically_accessed_array = (
                is_dinamically_accessed_array
                and following_bytecode["instruction"] == "CONSTANT"
            )

            # 7. Following bytecode: `MULT` (to compute the memory offset)
            following_bytecode_idx = following_bytecode_idx + 1
            following_bytecode = self.bytecode_list[following_bytecode_idx]

            speculated_offset_register = following_bytecode["metadata"]["register"]

            is_dinamically_accessed_array = (
                is_dinamically_accessed_array
                and following_bytecode["instruction"] == "MULT"
                and following_bytecode["metadata"]["lhs_register"] == speculated_index_var_value_register
                and following_bytecode["metadata"]["rhs_register"] == speculated_type_size_register
            )

            # 8. Following bytecode: `ADD` (to add the base address from
            # `bytecode` to the `offset`)
            following_bytecode_idx = following_bytecode_idx + 1
            following_bytecode = self.bytecode_list[following_bytecode_idx]

            is_dinamically_accessed_array = (
                is_dinamically_accessed_array
                and following_bytecode["instruction"] == "ADD"
                and following_bytecode["metadata"]["lhs_register"] == speculated_var_address_register
                and following_bytecode["metadata"]["rhs_register"] == speculated_offset_register
            )

            # If all the conditions held, return the adequate exponent and
            # number of bytecodes already accounted for
            if is_dinamically_accessed_array:
                following_bytecode_idx = following_bytecode_idx + 1
                following_bytecode = self.bytecode_list[following_bytecode_idx]

                context = (
                    "value" if following_bytecode["instruction"] in ["LOAD", "LOADF"]
                    else "address"
                )
                symbol = get_certificate_symbol(f"VAR_{context.upper()}")
                
                exponent = (
                    f"({symbol})"
                    # + f"^({var_prime})"
                    + f"^(VAR PRIME)"
                    # + f"^(3)^({speculated_index_var_prime})"
                    + f"^(3)^(INDEX VAR PRIME)"
                )

                # Account for:
                #  - 2 bytecodes to obtain the variable base address
                #  - 3 bytecodes to load the value from the index variable
                #  - 1 bytecode to obtain the type size
                #  - 2 bytecodes to compute the element address (`ADD` and `MULT`)
                bytecodes_to_mark_as_done = 8

                # Account for the `LOAD`, if this is a var. value case.
                if context == "value":
                    bytecodes_to_mark_as_done += 1

                return (exponent, bytecodes_to_mark_as_done)

        except (IndexError, KeyError):
            return (None, None)

        return (None, None)
   
    def _handle_parameter(
        self,
        bytecode: dict[str, dict],
        bytecode_idx: int
    ) -> list[str]:
        """
        Handle function parameter definition.

        The only case that will land in this handler is the set of instructions
        that transmit data from the `arg` register to a variable within the
        function scope. This is the equivalent of "defining" such variable.
        
        As variable definitions do not have an intrinsic certificate, we simply
        flag this variable as a parameter in the certificator environment. The
        certificator will always emit the `PARAM` symbol after any uses of this
        variable.

        Parameters
        ----------
        bytecode : dict[str, dict]
            The initial bytecode that implements this parameteer.
        bytecode_idx : int
            The index of this `bytecode` in `self.bytecode_list`.

        Returns
        -------
        exponent : list[str]
            The encoding exponent of this parameter.
        """

        # Mark this variable as a parameter in the environment. The `CONSTANT`
        # bytecode has the variable address as its value.
        var_address = bytecode["metadata"]["value"]
        self.environment["variables"][var_address]["parameter"] = True

        # Mark this `CONSTANT` and the `STORE` as done.
        bytecodes_to_mark_as_done = 2

        for idx in range(bytecode_idx, bytecode_idx + bytecodes_to_mark_as_done):
            bytecode_id = self.bytecode_list[idx]["bytecode_id"]
            self.bytecode_status[bytecode_id] = True

        return []

    def _handle_mov(
        self,
        bytecode: dict[str, dict],
        bytecode_idx: int
    ) -> list[str]:
        """
        Handle a `MOV` bytecode.

        This bytecode might implement a `return` statement or the passing of an
        argument to a function.

        Parameters
        ----------
        bytecode : dict[str, dict]
            The `MOV` bytecode.
        bytecode_idx : int
            The index of this `bytecode` in `self.bytecode_list`.

        Returns
        -------
        exponent : list[str]
            The adequate encoding exponent.

        Raises
        ------
        ValueError
            Raised if this `MOV` does not match any known patterns.
        """

        # Case 1: it is a `return` statement
        is_return = (bytecode["metadata"]["register"] == "ret_value")

        if is_return:
            return self._handle_return(
                bytecode=bytecode,
                bytecode_idx=bytecode_idx
            )
        
        # Case 2: it is a function argument
        is_function_argument = (bytecode["metadata"]["register"] == "arg")

        if is_function_argument:
            return self._handle_function_argument(
                bytecode=bytecode,
                bytecode_idx=bytecode_idx
            )
        
        # There are no other known use cases for `MOV` that have not already
        # been covered.
        err_msg = f"Unknown use case of MOV instruction: {bytecode}."
        raise ValueError(err_msg)
        
    def _handle_return(
        self,
        bytecode: dict[str, dict],
        bytecode_idx: int
    ) -> list[str]:
        """
        Handle the `return` statement of a function.

        Parameters
        ----------
        bytecode : dict[str, dict]
            The bytecode to certificate.
        bytecode_idx : int
            The index of this `bytecode` in `self.bytecode_list`.

        Returns
        -------
        exponent : list[str]
            The encoding exponent.
        """

        # Produce the exponent
        symbol = get_certificate_symbol("RET_SYM")
        exponent = f"{symbol}"

        # Mark this bytecode and the next -- `JR` -- as done.
        current_bytecode_id = bytecode["bytecode_id"]
        self.bytecode_status[current_bytecode_id] = True

        next_bytecode_id = self.bytecode_list[bytecode_idx + 1]["bytecode_id"]
        self.bytecode_status[next_bytecode_id] = True

        return [exponent]

    def _handle_function_argument(
        self,
        bytecode: dict[str, dict],
        bytecode_idx: int
    ) -> list[str]:
        """
        Handle the passing of a value as an argument to a function call.

        This method simply handles the `MOV` bytecode that has `arg` as its
        destination.

        Parameters
        ----------
        bytecode : dict[str, dict]
            The bytecode to certificate.
        bytecode_idx : int
            The index of this `bytecode` in `self.bytecode_list`.

        Returns
        -------
        exponent : list[str]
            The encoding exponent.
        """

        # Produce the certificate
        symbol = get_certificate_symbol("ARG")
        exponent = f"{symbol}"

        # Mark this bytecode as done
        bytecode_id = bytecode["bytecode_id"]
        self.bytecode_status[bytecode_id] = True

        return [exponent]
    
    def _handle_function_call(
        self,
        bytecode: dict[str, dict],
        bytecode_idx: int
    ) -> list[str]:
        """
        Handle the function call operation.

        This method handles both the "jump and link" (`JAL`) and "obtain the
        returned value" (`MOV`, with `ret_value` as its source) bytecodes.

        Parameters
        ----------
        bytecode : dict[str, dict]
            The bytecode to certificate.
        bytecode_idx : int
            The index of this `bytecode` in `self.bytecode_list`.

        Returns
        -------
        exponent : list[str]
            The encoding exponent.

        Raises
        ------
        ValueError
            Raised if this `JAL` does not match any known patterns.
        """

        # Assert the function call follows the expected pattern
        next_bytecode_idx = bytecode_idx + 1
        next_bytecode = self.bytecode_list[next_bytecode_idx]

        is_function_call = (
            bytecode["instruction"] == "JAL"
            and next_bytecode["instruction"] == "MOV"
            and next_bytecode["metadata"]["value"] == "ret_value"
        )

        if not is_function_call:
            err_msg = f"Invalid function call near bytecode {bytecode}."
            raise ValueError(err_msg)

        # Produce the certificate
        symbol = get_certificate_symbol("FUNC_CALL")

        function_id = bytecode["metadata"]["value"]
        function_prime = self.environment["functions"][function_id]["prime"]

        exponent = f"({symbol})^({function_prime})"

        # Mark this bytecode and the next -- `MOV` -- as done.
        current_bytecode_id = bytecode["bytecode_id"]
        self.bytecode_status[current_bytecode_id] = True

        next_bytecode_id = self.bytecode_list[bytecode_idx + 1]["bytecode_id"]
        self.bytecode_status[next_bytecode_id] = True

        return [exponent]

    def _handle_control_flow(
        self,
        bytecode: dict[str, dict],
        bytecode_idx: int
    ) -> list[str]:
        """
        Handle control flow constructs.

        This method will identify what construct a conditional jump (i.e., the
        `JZ` bytecode) implements and handle it accordingly.

        Parameters
        ----------
        bytecode : dict[str, dict]
            The bytecode to certificate.
        bytecode_idx : int
            The index of this `bytecode` in `self.bytecode_list`.

        Returns
        -------
        exponent : list[str]
            The encoding exponent.

        Raises
        ------
        ValueError
            Raised if this `JZ` does not match any known patterns.
        """

        # Identify the construct
        _control_flow = self._identify_control_flow(
            bytecode=bytecode,
            bytecode_idx=bytecode_idx
        )

        # Call the adequate handler
        if _control_flow == "if":
            return self._handle_if(
                bytecode=bytecode,
                bytecode_idx=bytecode_idx
            )

        elif _control_flow == "if_else":
            return self._handle_if_else(
                bytecode=bytecode,
                bytecode_idx=bytecode_idx
            )

        elif _control_flow == "while":
            return self._handle_while(
                bytecode=bytecode,
                bytecode_idx=bytecode_idx
            )

        err_msg = f"Invalid conditional jump implemented by bytecode {bytecode}."
        raise ValueError(err_msg)

    def _identify_control_flow(
        self,
        bytecode: dict[str, dict],
        bytecode_idx: int
    ) -> str:
        """
        Identify the control flow construct this `JZ` bytecode implements.

        The derivation rules to derive the control flow construct from the
        conditional jump are:

        1. `IF`: the conditional jump lands on a bytecode that is not preceeded
        by some other conditional jump.
        2. `IF/ELSE`: the conditional jump lands on a bytecode that *is*
        preceeded by some other conditional jump. This other bytecode will have
        the program counter jump *forward*.
        3. `WHILE`: the conditional jump lands on a bytecode that *is*
        preceeded by some other conditional jump. This other bytecode will have
        the program counter jump *backwards*.

        Parameters
        ----------
        bytecode : dict[str, dict]
            The `JZ` bytecode.
        bytecode_idx : int
            The index of this `bytecode` in `self.bytecode_list`.

        Returns
        -------
        control_flow_construct : str
            The control flow construct this bytecode implements.
        """

        jump_size = bytecode["metadata"]["jump_size"]
        
        bytecode_to_land_on_idx = bytecode_idx + jump_size
        bytecode_preceeding_landing_spot_idx = bytecode_to_land_on_idx - 1
        bytecode_preceeding_landing_spot = (
            self.bytecode_list[bytecode_preceeding_landing_spot_idx]
        )

        if bytecode_preceeding_landing_spot["instruction"] != "JZ":
            return "if"

        other_conditional_jump_size = (
            bytecode_preceeding_landing_spot["metadata"]["jump_size"]
        )

        if other_conditional_jump_size < 0:
            return "while"
        
        return "if_else"

    def _handle_if(
        self,
        bytecode: dict[str, dict],
        bytecode_idx: int
    ) -> str:
        """
        Handle a `IF` control flow from a `JZ` bytecode.

        This method will add the `IF_END` symbol to the stash.

        Parameters
        ----------
        bytecode : dict[str, dict]
            The `JZ` bytecode.
        bytecode_idx : int
            The index of this `bytecode` in `self.bytecode_list`.

        Returns
        -------
        exponent : list[str]
            The encoding exponent.
        """

        # Add the `IF_END` symbol to the stash
        jump_size = bytecode["metadata"]["jump_size"]
        idx_to_stash_at = bytecode_idx + jump_size
        if_end_symbol = [str(get_certificate_symbol("IF_END"))]
        self.environment["stash"][idx_to_stash_at] = if_end_symbol

        # Produce the exponent
        symbol = get_certificate_symbol("IF")
        exponent = f"{symbol}"

        # Mark this bytecode as done
        bytecode_id = bytecode["bytecode_id"]
        self.bytecode_status[bytecode_id] = True

        return [exponent]

    def _handle_if_else(
        self,
        bytecode: dict[str, dict],
        bytecode_idx: int
    ) -> str:
        """
        Handle a `IF/ELSE` control flow from a `JZ` bytecode.

        This method will add the `IF_END` and `ELSE_END` symbols to the stash.

        Parameters
        ----------
        bytecode : dict[str, dict]
            The `JZ` bytecode.
        bytecode_idx : int
            The index of this `bytecode` in `self.bytecode_list`.

        Returns
        -------
        exponent : list[str]
            The encoding exponent.
        """

        # Add the `IF_END` symbol to the stash
        if_jump_size = bytecode["metadata"]["jump_size"]
        idx_to_stash_if_end_at = bytecode_idx + if_jump_size
        if_end_symbol = [str(get_certificate_symbol("IF_END"))]
        self.environment["stash"][idx_to_stash_if_end_at] = if_end_symbol

        # Add the `ELSE_END` symbol to the stash
        else_bytecode = self.bytecode_list[bytecode_idx + if_jump_size - 1]
        else_jump_size = else_bytecode["metadata"]["jump_size"]
        idx_to_stash_else_end_at = bytecode_idx + if_jump_size - 1 + else_jump_size
        else_end_symbol = [str(get_certificate_symbol("IF_END"))]
        self.environment["stash"][idx_to_stash_else_end_at] = else_end_symbol

        # Produce the exponent
        symbol = get_certificate_symbol("IF")
        exponent = f"{symbol}"

        # Mark both jump bytecodes as done
        if_bytecode_id = bytecode["bytecode_id"]
        self.bytecode_status[if_bytecode_id] = True

        else_bytecode_id = else_bytecode["bytecode_id"]
        self.bytecode_status[else_bytecode_id] = True

        return [exponent]

    def _handle_while(
        self,
        bytecode: dict[str, dict],
        bytecode_idx: int
    ) -> str:
        """
        Handle a `WHILE` control flow from a `JZ` bytecode.

        This method will add the `WHILE_END` symbol to the stash.

        Parameters`
        ----------
        bytecode : dict[str, dict]
            The `JZ` bytecode.
        bytecode_idx : int
            The index of this `bytecode` in `self.bytecode_list`.

        Returns
        -------
        exponent : list[str]
            The encoding exponent.
        """

        # Add the `WHILE_END` symbol to the stash
        jump_size = bytecode["metadata"]["jump_size"]
        idx_to_stash_while_end_at = bytecode_idx + jump_size
        while_end_symbol = [str(get_certificate_symbol("WHILE_END"))]
        self.environment["stash"][idx_to_stash_while_end_at] = while_end_symbol

        # Produce the exponent
        symbol = get_certificate_symbol("WHILE")
        exponent = f"{symbol}"

        # Mark both jump bytecodes as done
        if_bytecode_id = bytecode["bytecode_id"]
        self.bytecode_status[if_bytecode_id] = True

        jump_to_predicate_bytecode_idx = bytecode_idx + jump_size - 1
        jump_to_predicate_bytecode = self.bytecode_list[jump_to_predicate_bytecode_idx]
        jump_to_predicate_bytecode_id = jump_to_predicate_bytecode["bytecode_id"]
        self.bytecode_status[jump_to_predicate_bytecode_id] = True

        return [exponent]

    def _handle_simple_instruction(
        self,
        bytecode: dict[str, dict],
        bytecode_idx: int
    ) -> list[str]:
        """
        Handle a simple bytecode.

        A bytecode is _simple_ if it does not require pattern matching in order
        to identify what operation it implements.

        Parameters
        ----------
        bytecode : dict[str, dict]
            The simple bytecode to certificate.
        bytecode_idx : int
            The index of this `bytecode` in `self.bytecode_list`.

        Returns
        -------
        exponent : list[str]
            The encoding exponent.
        """

        instruction = bytecode["instruction"]

        # Produce the exponent
        symbol = get_certificate_symbol(instruction)
        exponent = f"{symbol}"

        # Mark this bytecode as done
        bytecode_id = bytecode["bytecode_id"]
        self.bytecode_status[bytecode_id] = True

        return [exponent]
