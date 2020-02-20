#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 23:11:31 2020

@author: iqrah
"""

import ply.lex as lex

tokens = [

    'T_Identifier',
	'T_IntConstant',
	'T_DoubleConstant',
	'T_BoolConstant',
	'T_StringConstant',
	'Plus',
	'Minus',
	'Multiply',
	'Divide',
	'Modulus',
	'T_GreaterEqual',
	'Greater',
	'T_LessEqual',
	'Less',
	'T_Equal',
	'T_NotEqual',
	'Eq',
	'T_And',
	'T_Or',
	'Not',
	'Semicolon',
	'Comma',
	'Dot',
	'LeftParen',
	'RightParan',
    'LeftCurly',
	'RightCurly',
	'Comment'   
]
reserved = {
	'void' : 'T_Void',
	'int' : 'T_Int',
	'double' : 'T_Double',
	'bool' : 'T_Bool',
	'string' : 'T_String',
	'null' : 'T_Null',
	'for' : 'T_For',
	'while' : 'T_While',
	'if' : 'T_If',
	'else' : 'T_Else',
	'return' : 'T_Return',
	'break' : 'T_Break',
	'Print' : 'T_Print',
	'ReadInteger' : 'T_ReadInteger',
	'ReadLine' : 'T_ReadLine'
}
tokens += list(reserved.values())

operators = {
	'Plus' : '+',
	'Minus' : '-',
	'Multiply' : '*',
	'Divide' : '/',
	'Modulus' : '%',
	'Greater' : '>',
	'Less' : '<',
	'Eq' : '=',
	'Not' : '!',
	'Semicolon' : ';',
	'Comma' : ',',
	'Dot' : '.',
	'LeftParen' : '(',
	'RightParan' : ')',
    'LeftCurly' : '{',
	'RightCurly' : '}'
}

t_ignore = r' '
t_Plus = r'\+'
t_Minus = r'\-'
t_Multiply = r'\*'
t_Divide = r'\/'
t_Modulus = r'\%'
t_Greater = r'>'
t_Less = r'<'
t_Eq = r'='
t_Not = r'\!'
t_Semicolon = r';'
t_Comma = r','
t_Dot = r'\.'
t_LeftParen = r'\('
t_RightParan = r'\)'
t_LeftCurly = r'{'
t_RightCurly = r'}'

def t_GreaterEqual(t):
	r'>='
	t.type = 'T_GreaterEqual'
	return t

def t_LessEqual(t):
	r'<='
	t.type = 'T_LessEqual'
	return t

def t_Equal(t):
	r'=='
	t.type = 'T_Equal'
	return t

def t_NotEqual(t):
	r'\!='
	t.type = 'T_NotEqual'
	return t

def t_And(t):
	r'\&\&'
	t.type = 'T_And'
	return t

def t_Or(t):
	r'\|\|'
	t.type = 'T_Or'
	return t


def t_BoolConstant(t):
	r'(true|false)'
	t.type = 'T_BoolConstant'
	return t

def t_Identifier(t):
	r'[a-zA-Z_][a-zA-Z_0-9]*'
	if reserved.get(t.value) != None:
		t.type = reserved.get(t.value)
		return t
	if len(t.value) > 31:
		t_error(t)
		return
	t.type = 'T_Identifier'
	return t

def t_StringConstant(t): #needs to be completed
	r'"[^\n|"]*(")?'
	t.type = 'T_StringConstant'
	if t.value[-1] != '\"':
		t_error(t)
		t.lexer.lineno += 1
		return
	return t

def t_DoubleConstant(t):
	r'\d+\.\d*(E?)\+?\d+'
	t.value = float(t.value)
	t.type = 'T_DoubleConstant'
	return t

def t_IntConstant(t):
	r'\d+'
	t.value = int(t.value)
	t.type = 'T_IntConstant'
	return t

def t_Comment(t):
	r'(/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+/)|(//.*)'
	lines = t.value.count('\n')
	t.lexer.lineno += lines
	pass

def t_newline(t):
     r'\n+'
     t.lexer.lineno += len(t.value)


# Compute column.
 #     input is the input text string
 #     token is a token instance
def find_column(input, token):
	line_start = input.rfind('\n', 0, token.lexpos) + 1
	return (token.lexpos - line_start) + 1

def t_error(t):
     print("\n*** Error in line no ", t.lineno, ".\nIllegal character '%s'" % t.value)
     t.lexer.skip(1)





lexer = lex.lex()
#input_str = "12.3E+-2"
#lexer.input(input_str)

input_str = ''
file = open("/home/iqrah/Desktop/Spring_02_2020/Compilers/pp1-post(1)/pp1-post/samples/comment.frag", "r")
if file.mode == 'r':
	input_str = file.read()
lexer.input(input_str)


while True:
	t = lexer.token()
	if not t:
		break
	op_type = t.type
	if(operators.get(t.type) != None):
		op_type = "'" + operators.get(t.type) + "'"
	value = ""
	if ( t.type == "T_IntConstant" or t.type == "T_DoubleConstant" 
	or t.type == "T_BoolConstant" or t.type == "T_StringConstant"): #bool and string const
		value = "(value = " + str(t.value) + ")"
	#print(t)
	#print(t.value, "\t\tline ", t.lineno, "cols ", t.lexpos+1, "-", t.lexpos+len(str(t.value)), " ", t.type)
	print(t.value, "\t\tline ", t.lineno, "cols ", find_column(input_str, t), "-",  find_column(input_str, t)+len(str(t.value))-1, " ", op_type, value)
	