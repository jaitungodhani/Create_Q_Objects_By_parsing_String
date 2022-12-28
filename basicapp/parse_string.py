from pyparsing import nestedExpr
from django.db.models import Q
import ast

def q(query, tokens):
    if isinstance(tokens, list):
        for operator in ('OR', 'AND'): # OR first since it has a lower precedence than AND
            try:
                index = tokens.index(operator)
                break
            except ValueError:
                pass
        else:
            return q(query, tokens[0])
        return (Q.__or__ if operator == 'OR' else Q.__and__)(
            q(query, tokens[:index]), q(query, tokens[index + 1:]))
    else:
        d = query[int(tokens)]
        if d['operator'] == "eq":
            return Q(**{d['field']: d['value']})
        elif d['operator'] == "ne":
            return ~Q(**{d['field']: d['value']})
        return Q(**{'__'.join((d['field'], d['operator'])): d['value']})

def get_query(parsed_list, query = {}, k = 0):
    if isinstance(parsed_list,list):
        res=False
        for i in parsed_list:
            k += 1
            if type(i) is list:
                res = True
                get_query(i, query, k)
        if not res:
            query[k]={"id": k,"field":parsed_list[0], "operator":parsed_list[1], "value":parsed_list[2]}
    return query

def parse_search_phrase(val):

    """
    converted (start_date gt 2022-12-01) AND ((distance gt 20) OR (distance lt 60)) to 
    [[['start_date', 'gt', '2022-12-01'], 'AND', [['distance', 'gt', '20'], 'OR', ['distance', 'lt', '60']]]] by using parsing

    then create query for this:
    {5: {'id': 5, 'field': 'start_date', 'operator': 'gt', 'value': '2022-12-01'}, 8: {'id': 8, 'field': 'distance', 'operator': 'gt', 'value': '20'},
     10: {'id': 10, 'field': 'distance', 'operator': 'lt', 'value': '60'}} by using get_query method

    then create logic query:-
    [[5, 'AND', [8, 'OR', 10]]]

    Then by using q function got Q object string
    """

    val = '(' + val + ')'
    parsed = nestedExpr('(',')').parseString(val).asList()

    query = get_query(parsed)   
   
    for i in query:                        # this is for creating [[5, 'AND', [8, 'OR', 10]]]
        filter_list = [query[i]["field"], query[i]["operator"], query[i]["value"]]
        parsed = str(parsed).replace(str(filter_list), str(i))
        tokens = ast.literal_eval(parsed)

    return q(query, tokens)

