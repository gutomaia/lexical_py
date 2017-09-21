import unittest
import lexical
import re

sql_tokens = [
    dict(type='T_SELECT', regex=r'^(SELECT)', store=True, flags=re.I),
    dict(type='T_FROM', regex=r'^(FROM)', store=True, flags=re.I),
    dict(type='T_WILDCARD', regex=r'^(\*)', store=True),
    dict(type='T_LABEL', regex=r'^([a-z]+)', store=True),

    dict(type='T_ENDLINE', regex=r'^\n', store=False),
    dict(type='T_WHITESPACE', regex=r'^[ \t\r]+', store=False),
]


class SQLTest(unittest.TestCase):

    def test_select_all_fields_from_table(self):
        query = 'SELECT * FROM table'
        analysis = lexical.analyse(query, sql_tokens)
        tokens = list(analysis)
        self.assertEquals(4, len(tokens))
        self.assertEquals('T_SELECT', tokens[0]['type'])
        self.assertEquals('T_WILDCARD', tokens[1]['type'])
        self.assertEquals('T_FROM', tokens[2]['type'])
        self.assertEquals('T_LABEL', tokens[3]['type'])

    def test_select_all_fields_with_lower_case(self):
        query = 'select * from table'
        analysis = lexical.analyse(query, sql_tokens)
        tokens = list(analysis)
        self.assertEquals(4, len(tokens))
        self.assertEquals('T_SELECT', tokens[0]['type'])
        self.assertEquals('T_WILDCARD', tokens[1]['type'])
        self.assertEquals('T_FROM', tokens[2]['type'])
        self.assertEquals('T_LABEL', tokens[3]['type'])
