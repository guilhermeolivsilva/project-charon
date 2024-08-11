"""Export classes to allow `from src.nodes import *`."""

# Base classes
from src.ast_nodes.node import Node
from src.ast_nodes.conditionals.conditional import Conditional
from src.ast_nodes.operations.operation import Operation

# Basic nodes
from src.ast_nodes.basic.CST import CST
from src.ast_nodes.basic.EMPTY import EMPTY
from src.ast_nodes.basic.EXPR import EXPR
from src.ast_nodes.basic.SEQ import SEQ

# Variables
from src.ast_nodes.variables.VAR import VAR
from src.ast_nodes.variables.VAR_DEF import VAR_DEF
from src.ast_nodes.variables.ELEMENT_ACCESS import ELEMENT_ACCESS

# Functions
from src.ast_nodes.functions.FUNC_CALL import FUNC_CALL
# from src.ast_nodes.basic.PROG import PROG

# Conditional nodes (control flow, loops etc.)
from src.ast_nodes.conditionals.DO import DO
from src.ast_nodes.conditionals.IF import IF
from src.ast_nodes.conditionals.IFELSE import IFELSE
from src.ast_nodes.conditionals.WHILE import WHILE

# Operations
from src.ast_nodes.operations.ADD import ADD
from src.ast_nodes.operations.ASSIGN import ASSIGN
from src.ast_nodes.operations.LT import LT
from src.ast_nodes.operations.SUB import SUB
