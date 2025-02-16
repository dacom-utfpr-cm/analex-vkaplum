import string 

def alpha_transition(target_state):
    return { k : target_state for k in string.ascii_lowercase }

def num_transition(target_state):
    return { str(k) : target_state for k in range(10) }

def alpha_underline_transition(target_state):
    d = alpha_transition(target_state)
    d["_"] = target_state
    return d

def alphanum_transition(target_state):
    d = { k : target_state for k in string.ascii_lowercase }
    d.update( num_transition(target_state) )
    return d

def alphanum_underline_transition(target_state):
    d = alphanum_transition(target_state)
    d["_"] = target_state
    return d

def isspace_transition(target_state):
    whitespace_chars = [' ', '\t', '\n', '\r', '\f', '\v']
    return { k : target_state for k in whitespace_chars }

moore_transitions = {
    "START" : {
        "<" : "LESS",
        ">" : "GREATER",
        "+" : "FINAL_PLUS",
        "-" : "FINAL_MINUS",
        "*" : "FINAL_TIMES",
        "/" : "SLASH_STATE",
        "[" : "FINAL_LBRACKETS",
        "]" : "FINAL_RBRACKETS",
        "{" : "FINAL_LBRACES",
        "}" : "FINAL_RBRACES",
        "&" : "AND1_STATE",
        "|" : "OR1_STATE",
        "=" : "EQ_STATE",
        "!" : "NOT_STATE",
        ";" : "FINAL_SEMICOLON",
        "," : "FINAL_COMMA",
        **alpha_underline_transition("ID_START"),
        "i" : "I_STATE",
        "e" : "E_STATE",
        "f" : "F_STATE",
        "r" : "R_STATE",
        "v" : "V_STATE",
        "w" : "W_STATE",
        **isspace_transition("START"),
        "(" : "FINAL_LPAREN",
        ")" : "FINAL_RPAREN",
        **num_transition("NUM"),
    },
    "LESS" : {
        "=" : "FINAL_LESSOREQUAL"
    },
    "EQ_STATE" : {
        "=" : "FINAL_EQUALS"
    },
    "NOT_STATE" : {
        "=" : "FINAL_DIFFERENT"
    },
    "SLASH_STATE" : {
        "*" : "COMMENT_STATE",
    },
    "COMMENT_STATE" : {
        **isspace_transition("COMMENT_STATE"),
        " " : "COMMENT_STATE",
        "!" : "COMMENT_STATE",
        "&" : "COMMENT_STATE",
        "(" : "COMMENT_STATE",
        ")" : "COMMENT_STATE",
        "*" : "ASTERISK_STATE",
        "+" : "COMMENT_STATE",
        "," : "COMMENT_STATE",
        "-" : "COMMENT_STATE",
        "/" : "COMMENT_STATE",
        **alphanum_underline_transition("COMMENT_STATE"),
        ";" : "COMMENT_STATE",
        "<" : "COMMENT_STATE",
        "=" : "COMMENT_STATE",
        ">" : "COMMENT_STATE",
        "[" : "COMMENT_STATE",
        "]" : "COMMENT_STATE",
        "_" : "COMMENT_STATE",
        "{" : "COMMENT_STATE",
        "|" : "COMMENT_STATE",
        "}" : "COMMENT_STATE"
    },
    "ASTERISK_STATE" : {
        **isspace_transition("COMMENT_STATE"),
        " " : "COMMENT_STATE",
        "!" : "COMMENT_STATE",
        "&" : "COMMENT_STATE",
        "(" : "COMMENT_STATE",
        ")" : "COMMENT_STATE",
        "*" : "COMMENT_STATE",
        "+" : "COMMENT_STATE",
        "," : "COMMENT_STATE",
        "-" : "COMMENT_STATE",
        "/" : "FINAL_COMMENT",
        **alphanum_underline_transition("COMMENT_STATE"),
        ";" : "COMMENT_STATE",
        "<" : "COMMENT_STATE",
        "=" : "COMMENT_STATE",
        ">" : "COMMENT_STATE",
        "[" : "COMMENT_STATE",
        "]" : "COMMENT_STATE",
        "_" : "COMMENT_STATE",
        "{" : "COMMENT_STATE",
        "|" : "COMMENT_STATE",
        "}" : "COMMENT_STATE"        
    },
    "AND1_STATE" : {
        "&" : "FINAL_AND"
    },
    "OR1_STATE" : {
        "|" : "FINAL_OR"
    },
    "GREATER" : {
        "=" : "FINAL_GREATEROREQUAL"
    },
    "I_STATE" : {
        **alphanum_underline_transition("ID_BODY"),
        "f" : "IF_COMPLETO",
        "n" : "IN_STATE"
    },
    "IF_COMPLETO" : {
        **alphanum_underline_transition("ID_BODY"),
    },
    "E_STATE" : {
        **alphanum_underline_transition("ID_BODY"),
        "l" : "EL_STATE"
    },
    "EL_STATE" : {
        **alphanum_underline_transition("ID_BODY"),
        "s" : "ELS_STATE"        
    },
    "ELS_STATE" : {
        **alphanum_underline_transition("ID_BODY"),
        "e" : "ELSE_COMPLETO"        
    },
    "ELSE_COMPLETO" : {
        **alphanum_underline_transition("ID_BODY")
    },
    "ID_START" : {
        **alphanum_underline_transition("ID_BODY")
    },
    "ID_BODY" : {
        **alphanum_underline_transition("ID_BODY")
    },
    "NUM" : {
        **num_transition("NUM")
    },
    "IN_STATE" : {
        **alphanum_underline_transition("ID_BODY"),
        "t" : "INT_COMPLETO"
    },
    "INT_COMPLETO" : {
        **alphanum_underline_transition("ID_BODY")
    },
    "F_STATE" : {
        **alphanum_underline_transition("ID_BODY"),
        "l" : "FL_STATE"
    },
    "FL_STATE" : {
        **alphanum_underline_transition("ID_BODY"),
        "o" : "FLO_STATE"
    },
    "FLO_STATE" : {
        **alphanum_underline_transition("ID_BODY"),
        "a" : "FLOA_STATE"
    },
    "FLOA_STATE" : {
        **alphanum_underline_transition("ID_BODY"),
        "t" : "FLOAT_COMPLETO"
    },
    "FLOAT_COMPLETO": {
        **alphanum_underline_transition("ID_BODY")
    },
    "R_STATE" : {
        **alphanum_underline_transition("ID_BODY"),
        "e" : "RE_STATE"
    },
    "RE_STATE" : {
        **alphanum_underline_transition("ID_BODY"),
        "t" : "RET_STATE"
    },
    "RET_STATE" : {
        **alphanum_underline_transition("ID_BODY"),
        "u" : "RETU_STATE"
    },
    "RETU_STATE" : {
        **alphanum_underline_transition("ID_BODY"),
        "r" : "RETUR_STATE"
    },
    "RETUR_STATE" : {
        **alphanum_underline_transition("ID_BODY"),
        "n" : "RETURN_COMPLETO"
    },
    "RETURN_COMPLETO" : {
        **alphanum_underline_transition("ID_BODY"),
    },
    "V_STATE" : {
        **alphanum_underline_transition("ID_BODY"),
        "o" : "VO_STATE"
    },
    "VO_STATE" : {
        **alphanum_underline_transition("ID_BODY"),
        "i" : "VOI_STATE"
    },
    "VOI_STATE" : {
        **alphanum_underline_transition("ID_BODY"),
        "d" : "VOID_COMPLETO"
    },
    "VOID_COMPLETO" : {
        **alphanum_underline_transition("ID_BODY"),
    },
    "W_STATE" : {
        **alphanum_underline_transition("ID_BODY"),
        "h" : "WH_STATE"
    },
    "WH_STATE" : {
        **alphanum_underline_transition("ID_BODY"),
        "i" : "WHI_STATE"
    },
    "WHI_STATE" : {
        **alphanum_underline_transition("ID_BODY"),
        "l" : "WHIL_STATE"
    },
    "WHIL_STATE" : {
        **alphanum_underline_transition("ID_BODY"),
        "e" : "WHILE_COMPLETO"
    },
    "WHILE_COMPLETO" : {
        **alphanum_underline_transition("ID_BODY"),
    }
}

moore_recover = {
    "LESS" : "FINAL_LESS",
    "GREATER" : "FINAL_GREATER",
    "EQ_STATE" : "FINAL_ATTRIBUTION",
    "NOT_STATE" : "FINAL_NOT",
    "SLASH_STATE" : "FINAL_DIVIDE",
    "I_STATE" : "FINAL_IDENTIFIER",
    "IF_COMPLETO" : "FINAL_IF",
    "E_STATE" : "FINAL_IDENTIFIER",
    "EL_STATE" : "FINAL_IDENTIFIER",
    "ELS_STATE" : "FINAL_IDENTIFIER",
    "ELSE_COMPLETO" : "FINAL_ELSE",
    "ID_START" : "FINAL_IDENTIFIER",
    "ID_BODY" : "FINAL_IDENTIFIER",
    "NUM" : "FINAL_NUM",
    "IN_STATE" : "FINAL_IDENTIFIER",
    "INT_COMPLETO" : "FINAL_INT",
    "F_STATE" : "FINAL_IDENTIFIER",
    "FL_STATE" : "FINAL_IDENTIFIER",
    "FLO_STATE" : "FINAL_IDENTIFIER",
    "FLOA_STATE" : "FINAL_IDENTIFIER",
    "FLOAT_COMPLETO" : "FINAL_FLOAT",
    "R_STATE" : "FINAL_IDENTIFIER",
    "RE_STATE" : "FINAL_IDENTIFIER",
    "RET_STATE" : "FINAL_IDENTIFIER",
    "RETU_STATE" : "FINAL_IDENTIFIER",
    "RETUR_STATE" : "FINAL_IDENTIFIER",
    "RETURN_COMPLETO" : "FINAL_RETURN",
    "V_STATE" : "FINAL_IDENTIFIER",
    "VO_STATE" : "FINAL_IDENTIFIER",
    "VOI_STATE" : "FINAL_IDENTIFIER",
    "VOID_COMPLETO" : "FINAL_VOID",
    "W_STATE" : "FINAL_IDENTIFIER",
    "WH_STATE" : "FINAL_IDENTIFIER",
    "WHI_STATE" : "FINAL_IDENTIFIER",
    "WHIL_STATE" : "FINAL_IDENTIFIER",
    "WHILE_COMPLETO" : "FINAL_WHILE"
}

moore_output = {
    "FINAL_LESS" : "LESS",
    "FINAL_LESSOREQUAL" : "LESS_EQUAL",
    "FINAL_GREATER" : "GREATER",
    "FINAL_GREATEROREQUAL" : "GREATER_EQUAL",
    "FINAL_IF" : "IF",
    "FINAL_ELSE" : "ELSE",
    "FINAL_IDENTIFIER" : "ID",
    "ERROR" : "INVALID",
    "FINAL_LPAREN" : "LPAREN",
    "FINAL_RPAREN" : "RPAREN",
    "FINAL_PLUS" : "PLUS",
    "FINAL_MINUS" : "MINUS",
    "FINAL_TIMES" : "TIMES",
    "FINAL_DIVIDE" : "DIVIDE",
    "FINAL_LBRACKETS" : "LBRACKETS",
    "FINAL_RBRACKETS" : "RBRACKETS",
    "FINAL_LBRACES" : "LBRACES",
    "FINAL_RBRACES" : "RBRACES",
    "FINAL_EQUALS" : "EQUALS",
    "FINAL_ATTRIBUTION" : "ATTRIBUTION",
    "FINAL_SEMICOLON" : "SEMICOLON",
    "FINAL_COMMA" : "COMMA",
    "FINAL_NOT" : "NOT",
    "FINAL_DIFFERENT" : "DIFFERENT",
    "FINAL_COMMENT" : "COMMENT",
    "FINAL_AND" : "AND",
    "FINAL_OR" : "OR",
    "FINAL_NUM" : "NUMBER",
    "FINAL_INT" : "INT",
    "FINAL_FLOAT" : "FLOAT",
    "FINAL_RETURN" : "RETURN",
    "FINAL_VOID" : "VOID",
    "FINAL_WHILE" : "WHILE",
}

if __name__ == "__main__":
    import pprint
    pprint.pprint(moore_transitions)