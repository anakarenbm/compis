#!/usr/bin/python3
from memory.memory import Memory
from lexer.lexer import lexer, tokens
from parser.parser_helper import ParserHelper
from quadruple.quadruple_helper import *
from quadruple.quadruple import *
from semantic_cube.semantic_cube import Cube
from semantic_cube.semantic_cube_helper import (
    code_to_type,
    token_to_code,
    type_to_init_value,
    scope_to_code,
    code_to_scope,
)
from error.error_helper import ErrorHelper

parser_helper = ParserHelper()
quad_helper = QuadrupleHelper()
error_helper = ErrorHelper()
semantic_cube = Cube()
memory = Memory()


def p_program(p):
    """program : PROGRAM ID program1"""


def p_program1(p):
    """program1 : script program2
        | program2"""


def p_program2(p):
    """program2 : htmltag program2
        | empty"""


def p_script(p):
    """script : SCRIPT snp_script_start block"""


def p_block(p):
    """block : OBRACE declareBlock block1 CBRACE"""


def p_block1(p):
    """block1 : statement block1
        | module block1
        | empty"""


def p_simpleBlock(p):
    """simpleBlock : OBRACE simpleBlock1 CBRACE"""


def p_simpleBlock1(p):
    """simpleBlock1 : statement simpleBlock1
        | empty"""


def p_voidModuleBlock(p):
    """voidModuleBlock : snp_save_void_type snp_save_type_to_module_table OBRACE declareBlock snp_add_quad_cont_to_table voidModuleBlock1 CBRACE"""


def p_voidModuleBlock1(p):
    """voidModuleBlock1 : statement voidModuleBlock1
        | empty"""


def p_returnModuleBlock(p):
    """returnModuleBlock : COLON type snp_save_type_to_module_table OBRACE declareBlock snp_add_quad_cont_to_table returnModuleBlock1 CBRACE"""


def p_returnModuleBlock1(p):
    """returnModuleBlock1 : statement returnModuleBlock1
        | SPIT expression"""


def p_declareBlock(p):
    """declareBlock : declare declareBlock
        | empty"""


def p_declare(p):
    """declare : type ID snp_add_var snp_push_solitary_operand
        | type ID snp_add_var initializeSlices
        | initialize"""


def p_initialize(p):
    """initialize : type initialize1 snp_add_assignation_quad initialize2"""


def p_initialize1(p):
    """initialize1 : ID snp_add_var snp_push_pending_operand EQ snp_push_pending_token value
        | ID snp_add_var initializeSlices EQ constSlices"""


def p_initialize2(p):
    """initialize2 : COMMA initialize1 initialize2
        | empty"""


def p_initializeSlices(p):
    """initializeSlices : initializeSlices1D
        | initializeSlices2D"""


def p_initializeSlices1D(p):
    """initializeSlices1D : OBRACK CTEI CBRACK"""


def p_initializeSlices2D(p):
    """initializeSlices2D : OBRACK CTEI CBRACK OBRACK CTEI CBRACK"""


def p_constSlices(p):
    """constSlices : constSlice1D
        | constSlice2D"""


def p_constSlice1D(p):
    """constSlice1D : OBRACK value constSlice1D1 CBRACK"""


def p_constSlice1D1(p):
    """constSlice1D1 : COMMA value constSlice1D1
        | empty"""


# TODO: FIX 2D SLICE
def p_constSlice2D(p):
    """constSlice2D : OBRACK constSlice1D COMMA CBRACK
        | OBRACK constSlice1D CBRACK"""


def p_type(p):
    """type : STR snp_save_type
        | INT snp_save_type
        | DOUBLE snp_save_type
        | BOOL snp_save_type"""


def p_statement(p):
    """statement : assignment
        | condition
        | cycle
        | doCycle
        | call
        | writing"""


def p_assignment(p):
    """assignment : ID snp_push_pending_operand assignmentSlice EQ snp_push_pending_token expression snp_add_assignation_quad"""


def p_assignmentSlice(p):
    """assignmentSlice : assignmentSlice1D
        | assignmentSlice2D
        | empty"""


def p_assignmentSlice1D(p):
    """assignmentSlice1D : OBRACK expression CBRACK"""


def p_assignmentSlice2D(p):
    """assignmentSlice2D : OBRACK expression CBRACK OBRACK expression CBRACK"""


def p_expression(p):
    """expression : exp expression1 snp_check_precedence_and_create_quadruple_for_rel"""


# ASSOCIATIVE => "or|and"
def p_expression1(p):
    """expression1 : REL snp_push_pending_token exp
        | ASSOCIATIVE snp_push_pending_token exp
        | empty"""
    # TODO add single expression. Do we allow if(True) ???


# Reference: Mathematical Expressions
# snp_check_precedence_and_create_quadruple => STEP 4
def p_exp(p):
    """exp : term snp_check_precedence_and_create_quadruple_for_sign exp1"""


# Reference: Mathematical Expressions
# snp_push_pending_token => STEP 2
def p_exp1(p):
    """exp1 : SIGN snp_push_pending_token exp exp1
        | empty"""


def p_term(p):
    """term : factor snp_check_precedence_and_create_quadruple_for_op term1"""


# Reference: Mathematical Expressions
# snp_push_pending_token => STEP 3
def p_term1(p):
    """term1 : OP snp_push_pending_token term term1
        | empty"""


def p_factor(p):
    """factor : OPAREN snp_push_pending_token expression CPAREN snp_clean_stack_until_false_bottom
        | factor1"""


def p_factor1(p):
    """factor1 : value
        | SIGN value"""


def p_value(p):
    """value : ID snp_checks_for_previous_declaration snp_push_pending_operand
        | valueSlice
        | call
        | CTEI snp_save_type_int snp_push_pending_operand
        | CTED snp_save_type_double snp_push_pending_operand
        | CTESTR snp_save_type_str snp_push_pending_operand
        | FALSE snp_save_type_bool snp_push_pending_operand
        | TRUE snp_save_type_bool snp_push_pending_operand"""


def p_valueSlice(p):
    """valueSlice : valueSlice1D
        | valueSlice2D"""


def p_valueSlice1D(p):
    """valueSlice1D : ID OBRACK expression CBRACK"""


def p_valueSlice2D(p):
    """valueSlice2D : ID OBRACK expression CBRACK OBRACK expression CBRACK"""


def p_condition(p):
    """condition : IF OPAREN expression CPAREN snp_conditional_statement_1 simpleBlock condition1 snp_conditional_statement_2"""


def p_condition1(p):
    """condition1 : ELSE snp_conditional_statement_3 simpleBlock
        | empty"""


def p_cycle(p):
    """cycle : LOOP snp_while_1 OPAREN expression CPAREN snp_conditional_statement_1 simpleBlock snp_while_3"""


def p_doCycle(p):
    """doCycle : DO snp_while_1 simpleBlock LOOP OPAREN expression CPAREN snp_do_while_gotot"""


def p_module(p):
    """module : DEF ID snp_add_module OPAREN arguments CPAREN snp_add_params_count_to_table module1 snp_end_module"""


def p_module1(p):
    """module1 : voidModuleBlock
        | returnModuleBlock"""


def p_call(p):
    """call : ID call1
        | predef"""


def p_call1(p):
    """call1 : OPAREN params CPAREN"""


def p_params(p):
    """params : expression params1"""


def p_params1(p):
    """params1 : COMMA params
        | empty"""


def p_predef(p):
    """predef : predef_avg
        | predef_find_max
        | predef_find_min
        | predef_median
        | predef_mode
        | predef_find_mult_slice
        | predef_pow
        | predef_randoms
        | predef_sort_slice
        | predef_suck_csv
        | predef_zeros"""


def p_predef_avg(p):
    """predef_avg : AVG OPAREN ID CPAREN"""


def p_predef_find_max(p):
    """predef_find_max : FIND_MAX OPAREN ID COMMA predef_find_max_args CPAREN"""


def p_predef_find_max_args(p):
    """predef_find_max_args : ID
        | CTEI"""


def p_predef_find_min(p):
    """predef_find_min : FIND_MIN OPAREN ID COMMA predef_find_min_args CPAREN"""


def p_predef_find_min_args(p):
    """predef_find_min_args : ID
        | CTEI"""


def p_predef_find_mult_slice(p):
    """predef_find_mult_slice : MULTIPLY_1DSLICE OPAREN ID COMMA predef_find_mult_slice_args CPAREN"""


def p_predef_find_mult_slice_args(p):
    """predef_find_mult_slice_args : ID
        | CTEI"""


def p_predef_median(p):
    """predef_median : MEDIAN OPAREN ID CPAREN"""


def p_predef_mode(p):
    """predef_mode : MODE OPAREN ID CPAREN"""


def p_predef_pow(p):
    """predef_pow : POW OPAREN predef_pow_args COMMA predef_pow_args CPAREN"""


def p_predef_pow_args(p):
    """predef_pow_args : ID
        | CTEI"""


def p_predef_randoms(p):
    """predef_randoms : RANDOMS OPAREN predef_randoms_args CPAREN"""


def p_predef_randoms_args(p):
    """predef_randoms_args : ID
        | CTEI"""


def p_predef_zeros(p):
    """predef_zeros : ZEROS OPAREN predef_zeros_args CPAREN"""


def p_predef_zeros_args(p):
    """predef_zeros_args : ID
        | CTEI"""


def p_predef_sort_slice(p):
    """predef_sort_slice : SORT_SLICE OPAREN ID COMMA predef_sort_slice_option CPAREN"""


def p_predef_sort_slice_option(p):
    """predef_sort_slice_option : MAX
        | MIN"""


def p_predef_suck_csv(p):
    """predef_suck_csv : SUCK_CSV OPAREN predef_suck_csv_args CPAREN"""


def p_predef_suck_csv_args(p):
    """predef_suck_csv_args : ID
        | CTESTR"""


def p_writing(p):
    """writing : EVAL snp_push_pending_token OPAREN expression CPAREN snp_add_eval_quad"""


# snp_add_var is the equivalent of snp #2 and #3 from Intermediate code actions
# for module definitions
def p_arguments(p):
    """arguments : type ID snp_add_var snp_counts_params arguments1
        | empty"""


# snp_add_var is the equivalent of snp #2 and #3 from Intermediate code actions
# for module definitions
def p_arguments1(p):
    """arguments1 : COMMA type ID snp_add_var snp_counts_params arguments1
        | empty"""


def p_tag(p):
    """tag : H1 snp_open_html_tag
        | H2 snp_open_html_tag
        | DIV snp_open_html_tag
        | P snp_open_html_tag
        | TABLE snp_open_html_tag
        | TR snp_open_html_tag
        | TH snp_open_html_tag"""


def p_html_class(p):
    """html_class : CLASS COLON CTESTR
        | empty"""


# gorritos <^ ^>
def p_htmlscript(p):
    """htmlscript : OEVALSCRIPT snp_push_eval_pending_token expression CEVALSCRIPT snp_add_eval_quad"""


def p_empty(p):
    """empty :"""


# TODO : Add a nice error to the error queue here
# Cannot use error_helper since program needs to exit.
# Othwerwise it doesn't know where to go next (aka se cicla)
# Reference: https://github.com/dabeaz/ply/blob/dca6c606d63d4729a395f30953456b0f00d4f443/ply/lex.py#L66
def p_error(p):
    # For debbuging
    # print("Type: ", p.type)
    # print("Value: ", p.value)
    # print("Line #", p.lineno)
    # print("lexpos? #", p.lexpos)
    print("Syntax error at '%s'" % p)
    exit(1)


# --- HTML ---


def p_htmltag(p):
    """htmltag : tag OBRACE html_block CBRACE snp_close_html_tag"""


def p_html_block(p):
    """html_block : html_statement html_block
    | htmltag html_block
    | empty"""


def p_html_statement(p):
    """html_statement : html_assignment
    | html_condition
    | htmlscript
    | html_cycle
    | html_do_cycle
    | html_call
    | writing"""


def p_html_assignment(p):
    """html_assignment : INITCODEHTML ID EQ expression CCODEHTML"""


def p_html_condition(p):
    """html_condition : INITCODEHTML IF OPAREN expression CPAREN snp_conditional_statement_1 CCODEHTML html_block html_condition1_else html_end_condition"""
    # For debbuging
    print("p_html_condition(p)")


def p_html_condition1_else(p):
    """html_condition1_else : HTMLELSE snp_conditional_statement_3 html_block
    | empty"""


def p_html_end_condition(p):
    """html_end_condition : HTMLEND snp_conditional_statement_2"""


def p_html_cycle(p):
    """html_cycle : INITCODEHTML LOOP snp_while_1 OPAREN expression CPAREN CCODEHTML snp_conditional_statement_1 html_block html_end_cycle snp_while_3"""


def p_html_end_cycle(p):
    """html_end_cycle : ENDCODEHTML ENDLOOP CCODEHTML"""


def p_html_do_cycle(p):
    """html_do_cycle : INITCODEHTML DO CCODEHTML snp_while_1 html_block html_end_do_cycle"""


def p_html_end_do_cycle(p):
    """html_end_do_cycle : ENDCODEHTML ENDLOOP OPAREN expression CPAREN CCODEHTML snp_do_while_gotot"""


def p_html_call(p):
    """html_call : INITCODEHTML ID OPAREN params CPAREN CCODEHTML"""


# --- SEMANTIC NEURAL POINTS ---

# --- PROCEDURE/MODULE SEMANTIC ACTIONS---

# Start of script global scope (adds global scope to directory)
def p_snp_script_start(p):
    """snp_script_start : empty"""
    # global parser_helper.procedure_directory, parser_helper.curr_scope, parser_helper.curr_type
    # Set current values for global script
    parser_helper.curr_scope = "global_script"
    parser_helper.curr_type = "void"
    # Add global script to the directory
    parser_helper.procedure_directory[parser_helper.curr_scope] = {
        "type": parser_helper.curr_type,
        "scope_type": scope_to_code.get("global"),
        "params_count": 0,
        "starting_quad": -1,
        "var_table": {},
    }  # TODO : add more info later on


# Start of the module (add module to directory)
def p_snp_add_module(p):
    """snp_add_module : empty"""
    # global parser_helper.procedure_directory, parser_helper.curr_scope
    module_name = p[-1]  # get the last symbol read (left from this neural point)
    # Check if module already exists and add it to the directory
    # debbuging
    # print("parser_helper.procedure_directory", parser_helper.procedure_directory, "module_name:", module_name)
    if module_name in parser_helper.procedure_directory:
        error_message = f"Module {module_name} has already been declared"
        error_helper.add_error(0, error_message)
    else:
        parser_helper.procedure_directory[module_name] = {
            "type": parser_helper.curr_type,
            "scope_type": scope_to_code.get("local"),
            "params_count": 0,
            "starting_quad": -1,
            "var_table": {},
        }  # TODO : add more info later on
        parser_helper.curr_scope = module_name


# Save the last type defined
def p_snp_save_type_to_module_table(p):
    """snp_save_type_to_module_table : empty"""
    parser_helper.procedure_directory[parser_helper.curr_scope][
        "type"
    ] = parser_helper.curr_type


# Save the last type defined
def p_snp_save_type(p):
    """snp_save_type : empty"""
    parser_helper.curr_type = p[-1]


# Save the last type as void (for modules)
def p_snp_save_void_type(p):
    """snp_save_void_type : empty"""
    parser_helper.curr_type = "void"


# End of the module deltes the var table
# snp #7 in Intermediate Code Actions for Module Definition
def p_snp_end_module(p):
    """snp_end_module : empty"""
    curr_module_type = parser_helper.procedure_directory[parser_helper.curr_scope][
        "type"
    ]
    # debbuging
    # print(f"CURR SCOPE: {parser_helper.curr_scope}")
    # print(f"TABLE: {parser_helper.procedure_directory}")
    # print("CURR TYPEEEE",curr_module_type)
    parser_helper.procedure_directory[parser_helper.curr_scope]["var_table"].clear()
    memory.reset_local_vars()
    parser_helper.curr_scope = "global_script"
    if curr_module_type is "void":  # VOID MODULE
        # Delete var table for the module that ended
        quad_helper.add_quad(token_to_code.get("ENDPROC"), -1, -1, -1)
    else:  # RETURNING MODULE
        return_value = quad_helper.pop_operand()
        return_type = code_to_type.get(quad_helper.pop_type())
        if return_type != curr_module_type:
            # print(return_type, curr_module_type)
            error_helper.add_error(301, f"Error in line {p.lexer.lineno}")
        else:
            quad_helper.add_quad(
                token_to_code.get("RET"), return_value, -1, "memory address"
            )


# --- VARIABLE SEMANTIC ACTIONS ---

# Adds a variable defined to the current scope variable table
def p_snp_add_var(p):
    """snp_add_var : empty"""
    var_name = p[-1]  # get the last symbol read (left from this neural point)
    # For debbuging
    # Check if var already exists and add it to the table in currect scope
    if parser_helper.is_var_in_current_scope(var_name):
        error_message = f"Variable {var_name} has already been declared"
        error_helper.add_error(0, error_message)
    else:
        scope_type = parser_helper.get_scope_type(parser_helper.curr_scope)
        var_memory_address = memory.set_addr(scope_type, parser_helper.curr_type)
        parser_helper.procedure_directory[parser_helper.curr_scope]["var_table"][
            var_name
        ] = {
            "type": parser_helper.curr_type,
            "memory_address": var_memory_address,
        }  # TODO : add more info later on
    # For debbuging
    # print(
    #     f"var_name {var_name}, current_scope, {parser_helper.curr_scope}, SCOPE TYPE: {scope_type}"
    # )
    # print("ProcDir for curr_scope:", parser_helper.procedure_directory, "\n")


# ---  ESTATUTOS SECUENCIALES ---
def p_snp_add_eval_quad(p):
    """snp_add_eval_quad : empty"""
    quad_helper.add_quad(quad_helper.pop_token(), -1, -1, quad_helper.pop_operand())


# --- MATHEMATICAL EXPRESSIONS (INTERMEDIATE REPRESENTATION) ---
def p_snp_push_pending_operand(p):
    """snp_push_pending_operand : empty"""
    operand_id = p[-2] if p[-1] == None else p[-1]
    quad_helper.push_operand(operand_id)

    if parser_helper.is_var_in_current_scope(operand_id):
        type = parser_helper.procedure_directory[parser_helper.curr_scope]["var_table"][
            operand_id
        ]["type"]
        quad_helper.push_type(type)
    else:
        quad_helper.push_type(parser_helper.curr_type)
    # For debbuging
    # print("OPERAND", quad_helper.top_operand())
    # print("TYPE", quad_helper.top_type())


def p_snp_save_type_int(p):
    """snp_save_type_int : empty"""
    parser_helper.curr_type = "int"


def p_snp_save_type_double(p):
    """snp_save_type_double : empty"""
    parser_helper.curr_type = "double"


def p_snp_save_type_str(p):
    """snp_save_type_str : empty"""
    parser_helper.curr_type = "str"


def p_snp_save_type_bool(p):
    """snp_save_type_bool : empty"""
    parser_helper.curr_type = "bool"


def p_snp_push_pending_token(p):
    """snp_push_pending_token : empty"""
    token = p[-1]
    quad_helper.push_token(token)
    # debbuging
    # print("pushed token", quad_helper.top_token())


def p_snp_push_solitary_operand(p):
    """snp_push_solitary_operand : empty"""

    """
    Variables declared without a corresponding initialization are zero-valued.
    For example, the zero value for an int is 0
    """
    operand_id = p[-2]
    type = parser_helper.procedure_directory[parser_helper.curr_scope]["var_table"][
        operand_id
    ]["type"]
    default_initial_value = type_to_init_value.get(type)
    operator = token_to_code.get("=")

    quad_helper.add_quad(operator, default_initial_value, -1, operand_id)


def p_snp_add_assignation_quad(p):
    """snp_add_assignation_quad : empty"""
    add_quadruple_assignation()


def add_quadruple_assignation():
    right_operand = quad_helper.pop_operand()  # TODO: type int
    right_operand_type = quad_helper.pop_type()
    left_operand = quad_helper.pop_operand()  # TODO: type str
    left_operand_type = quad_helper.pop_type()
    token = quad_helper.pop_token()

    if semantic_cube.is_in_cube(right_operand_type, left_operand_type, token):  # baila?
        quad_helper.add_quad(token, right_operand, -1, left_operand)  # assignation
    else:
        error_helper.add_error(301)
    # For debbuging
    # print(
    #     "Semantic Cube Checked: ",
    #     "right: ",
    #     right_operand_type,
    #     "left: ",
    #     left_operand_type,
    #     "token: ",
    #     token,
    # )


# sign => "+|-"
def p_snp_check_precedence_and_create_quadruple_for_sign(p):
    """snp_check_precedence_and_create_quadruple_for_sign : empty"""
    top = quad_helper.top_token()
    add = token_to_code.get("+")
    sub = token_to_code.get("-")
    is_sign = (top is add) or (top is sub)
    if is_sign:
        add_quadruple_expression()


# op => "*|/"
def p_snp_check_precedence_and_create_quadruple_for_op(p):
    """snp_check_precedence_and_create_quadruple_for_op : empty"""

    top = quad_helper.top_token()
    division = token_to_code.get("/")
    product = token_to_code.get("*")
    is_op = (top is division) or (top is product)

    if is_op:
        add_quadruple_expression()


# rel => "is|not|>=|<=|>|<"
def p_snp_check_precedence_and_create_quadruple_for_rel(p):
    """snp_check_precedence_and_create_quadruple_for_rel : empty"""

    top = quad_helper.top_token()
    eq = token_to_code.get("is")
    noteq = token_to_code.get("not")
    get = token_to_code.get(">=")
    let = token_to_code.get("<=")
    gt = token_to_code.get(">")
    lt = token_to_code.get("<")

    is_rel = (
        (top is eq)
        or (top is noteq)
        or (top is get)
        or (top is let)
        or (top is gt)
        or (top is lt)
    )

    if is_rel:
        add_quadruple_expression()


def p_snp_clean_stack_until_false_bottom(p):
    """snp_clean_stack_until_false_bottom : empty"""
    # CPAREN ", "stack should pop until finding ')' or '(' ")
    quad_helper.pop_token()


def add_quadruple_expression():
    right_operand = quad_helper.pop_operand()  # TODO: type int
    right_operand_type = quad_helper.pop_type()
    # TODO: TESTTTT
    left_operand = quad_helper.pop_operand()  # TODO: type str
    left_operand_type = quad_helper.pop_type()
    false_bottom = token_to_code.get("(")
    # debbuging
    # print("quad_helper.top_token()", quad_helper.top_token())
    if quad_helper.top_token() is false_bottom:
        print("false bottom:", quad_helper.top_token())
        quad_helper.pop_token()
        token = quad_helper.pop_token()
    else:
        token = quad_helper.pop_token()
    # token = quad_helper.pop_token()

    # debbuging HERE
    # print(right_operand, left_operand, token)
    if semantic_cube.is_in_cube(right_operand_type, left_operand_type, token):  # baila?
        # add the result (temp var) to the operand stack
        result_type = semantic_cube.cube[right_operand_type, left_operand_type, token]
        # add the quad
        quad_helper.add_quad(token, left_operand, right_operand, quad_helper.temp_cont)
        # expression
        quad_helper.push_operand(quad_helper.temp_cont)
        # add the result type (temp var) to the type stack
        quad_helper.push_type(code_to_type.get(result_type))
        # increase counter for temp/result vars
        quad_helper.temp_cont = quad_helper.temp_cont + 1
    else:
        error_helper.add_error(301)


def p_snp_checks_for_previous_declaration(p):
    """snp_checks_for_previous_declaration : empty"""
    var = p[-1]
    is_decalred = parser_helper.is_var_in_current_scope(
        var
    ) or parser_helper.is_var_in_global_scope(var)
    if not is_decalred:
        error_helper.add_error(302, f"{var} doesn't exist")


# --- NON-LINEAR STATEMENTS (INTERMEDIATE REPRESENTATION) ---

# --- CONDITIONALS ---

# Actions to produce intermediate representation for non-linear statements using quadruples
# snp for single IF
# Equivalent to snp_while_2
def p_snp_conditional_statement_1(p):
    """snp_conditional_statement_1 : empty"""
    top_type_code = quad_helper.pop_type()
    result = quad_helper.pop_operand()

    # Check if top_oper's type is type bool(1)
    if code_to_type.get(top_type_code) is "bool":
        # debbuging
        quad_helper.add_quad(token_to_code.get("GOTOF"), result, -1, "pending")
        quad_helper.push_jump(quad_helper.quad_cont - 1)
        # debbuging
        # print("Jump", quad_helper.quad_cont)
    else:
        error_helper.add_error(
            0, "Type Missmatch: Expression is not a bool"
        )  # TODO define code and custom error message


def p_snp_conditional_statement_2(p):
    """snp_conditional_statement_2 : empty"""
    end = quad_helper.pop_jump()
    cont = quad_helper.quad_cont
    quad_helper.fill(end, cont)


def p_snp_conditional_statement_3(p):
    """snp_conditional_statement_3 : empty"""
    quad_helper.add_quad(token_to_code.get("GOTO"), -1, -1, "pending")
    false = quad_helper.pop_jump()
    count = quad_helper.quad_cont
    quad_helper.push_jump(count - 1)
    # debbuging
    # print(count-1, false)
    # print(quad_helper.top_jump())
    quad_helper.fill(false, count)


# LOOPS


def p_snp_while_1(p):
    """snp_while_1 : empty"""
    count = quad_helper.quad_cont
    quad_helper.push_jump(count)


def p_snp_while_3(p):
    """snp_while_3 : empty"""
    end = quad_helper.pop_jump()
    ret = quad_helper.pop_jump()
    quad_helper.add_quad(token_to_code.get("GOTO"), -1, -1, ret)
    count = quad_helper.quad_cont
    quad_helper.fill(end, count)


def p_snp_do_while_gotot(p):
    """snp_do_while_gotot : empty"""
    top_type_code = quad_helper.pop_type()
    result = quad_helper.pop_operand()
    ret = quad_helper.pop_jump()

    # Check if top_oper's type is type bool(1)
    if code_to_type.get(top_type_code) is "bool":
        quad_helper.add_quad(token_to_code.get("GOTOT"), result, -1, ret)
    else:
        error_helper.add_error(
            0, "Type Missmatch: Expression is not a bool"
        )  # TODO define code and custom error message


###Intermediate Code Actions for a Module Definition
def p_snp_counts_params(p):
    """snp_counts_params : empty"""
    parser_helper.curr_module_param_counter = (
        parser_helper.curr_module_param_counter + 1
    )


# snp_add_params_count_to_table is snp #4 in Intermediate Code Actions for Module Definition
def p_snp_add_params_count_to_table(p):
    """snp_add_params_count_to_table : empty"""
    # add counter value to table
    parser_helper.procedure_directory[parser_helper.curr_scope][
        "params_count"
    ] = parser_helper.curr_module_param_counter
    # clears counter
    parser_helper.curr_module_param_counter = 0
    # debbuging
    # counter = parser_helper.procedure_directory[parser_helper.curr_scope][
    #     "params_count"
    # ]
    # print(f"current scope: {parser_helper.curr_scope} counter: {counter}")


# snp #6 in Intermediate Code Actions for Module Definition
def p_snp_add_quad_cont_to_table(p):
    """snp_add_quad_cont_to_table : empty"""
    parser_helper.procedure_directory[parser_helper.curr_scope][
        "starting_quad"
    ] = quad_helper.quad_cont
    # debbuging
    # print("I start from: ", parser_helper.procedure_directory[parser_helper.curr_scope]["starting_quad"])


# --- HTML ---


def p_snp_open_html_tag(p):
    """snp_open_html_tag : empty"""
    html_tag = p[-1].upper()
    quad_helper.push_tag(token_to_code.get(html_tag))
    quad_helper.add_quad(token_to_code.get("eval"), -1, -1, token_to_code.get(html_tag))
    # For debbuging
    # print("Html tag: ", html_tag)
    # print("Top tag: ", quad_helper.top_tag())


def p_snp_close_html_tag(p):
    """snp_close_html_tag : empty"""
    html_tag = quad_helper.pop_tag() + 1
    quad_helper.add_quad(token_to_code.get("eval"), -1, -1, html_tag)


def p_snp_push_eval_pending_token(p):
    """snp_push_eval_pending_token : empty"""
    quad_helper.push_token("eval")
    # For debbuging
    # print("Top token: ", quad_helper.top_token())


import ply.yacc as yacc

parser = yacc.yacc()
