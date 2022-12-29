from pyparsing import nestedExpr
from django.db.models import Q
import ast

def q(tokens):
    if any(isinstance(sub, list) for sub in tokens):
        for operator in ('OR', 'AND'): # OR first since it has a lower precedence than AND
            try:
                index = tokens.index(operator)
                break
            except ValueError:
                pass
        else:
            return q(tokens[0])
        print((Q.__or__ if operator == 'OR' else Q.__and__)(
            q(tokens[:index]), q(tokens[index + 1:])))
        return (Q.__or__ if operator == 'OR' else Q.__and__)(
            q(tokens[:index]), q(tokens[index + 1:]))
    else:
        d = tokens
        if d[1] == "eq":
            return Q(**{d[0]: d[2]})
        elif d[1] == "ne":
            return ~Q(**{d[0]: d[2]})
        return Q(**{'__'.join((d[0], d[1])): d[2]})
            

def parse_search_phrase(val):
    val = '(' + val + ')'
    parsed = nestedExpr('(',')').parseString(val).asList()
    return q(parsed)


