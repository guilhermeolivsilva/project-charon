"""Implement certificate to high level program inverter."""

from src.inverters.base_inverter import BaseInverter


class CertificateToHighLevel(BaseInverter):
    """
    Invert a certificate to retrieve the original program in canonical form.

    Parameters
    ----------
    certificate : str
        The certificate produced from a `Certificator` class.
    """

    ir_to_high_level = {
        "RET_SYM": "return",
        "ASSIGN": "=",
        "NOT": "!",
        "ADD": "+",
        "SUB": "-",
        "MULT": "*",
        "DIV": "/",
        "MOD": "%",
        "LESS": "<",
        "GREATER": ">",
        "EQUAL": "==",
        "DIFF": "!=",
        "AND": "&&",
        "OR": "||",
        "LSHIFT": "<<",
        "RSHIFT": ">>",
        "BITAND": "&",
        "BITOR": "|",
    }

    def __init__(self, certificate):
        super().__init__(certificate)

    def get_program(self):
        functions = self._compute_functions_boundaries()

        ...

    def _compute_functions_boundaries(self) -> dict[str, dict[str, int]]:
        functions = {}
        start, end, current_function_id = 0, 0, 1

        for idx, item in enumerate(self.ir):
            if item["operation"] == "RET_SYM":
                end = idx

                functions[f"func_{current_function_id}"] = {
                    "start": start,
                    "end": end
                }

                start = end + 1

        return functions


def is_operand(op: str) -> bool:
    """
    Tell whether an IR token represents an operand or not.

    Parameters
    ----------
    op : str
        The IR token.

    Returns
    -------
    : bool
        Whether this token is an operand or not.
    """

    _operands = ["VAR_ADDRESS", "CST", "VAR_VALUE", "FUNC_CALL"]

    return op in _operands


def is_operation(op: str) -> bool:
    """
    Tell whether an IR token represents an operation or not.

    Parameters
    ----------
    op : str
        The IR token.

    Returns
    -------
    : bool
        Whether this token is an operation or not.
    """

    _operations = [
        "NOT",
        "ADD",
        "SUB",
        "MULT",
        "DIV",
        "MOD",
        "LESS",
        "GREATER",
        "EQUAL",
        "DIFF",
        "AND",
        "OR",
        "LSHIFT",
        "RSHIFT",
        "BITAND",
        "BITOR",
    ]

    return op in _operations


def is_terminator(op: str) -> bool:
    """
    Tell whether an IR token is an expression terminator or not.

    Parameters
    ----------
    op : str
        The IR token.

    Returns
    -------
    : bool
        Whether this token terminates an expression or not.
    """

    _terminators = [
        "ASSIGN",
        "ARG",
        "RET_SYM"
    ]

    return op in _terminators
