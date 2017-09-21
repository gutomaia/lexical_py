# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from re import match
import re
from io import StringIO, BytesIO
import sys

class UnknownToken(Exception):
    ''' Unknown token error when trying to tokenize a single line '''
    def __init__(self, line, column, line_code):
        self.line_code = line_code
        self.line = line
        self.column = column
        super(UnknownToken, self).__init__(self.message)

    @property
    def message(self):
        msg = 'Unknown token @({line},{column}): {0}'
        return msg.format(self.line_code.rstrip(), **vars(self))

def is_string(code):
    return (
            (sys.version_info >= (3,0) and type(code).__name__ == 'str') or
            type(code).__name__ == 'unicode'
        )

def is_bytes(code):
    return (
            (sys.version_info >= (3,0) and type(code).__name__ == 'bytes') or
            type(code).__name__ == 'str'
        )


def code_line_generator(code):
    ''' A generator for lines from a file/string, keeping the \n at end '''
    if is_string(code):
        stream = StringIO(code)
    elif is_bytes(code):
        stream = BytesIO(code)
    else:
        stream = code # Should be a file input stream, already

    while True:
        line = stream.readline()
        if line:
            yield line
        else: # Line is empty (without \n) at EOF
            break


def analyse(code, token_types):
    for line, line_code in enumerate(code_line_generator(code), 1):
        column = 1
        while column <= len(line_code):
            remaining_line_code = line_code[column - 1:]
            for ttype in token_types:
                flags = ttype.get('flags', 0)
                m = match(ttype['regex'], remaining_line_code, re.S | flags)
                if m:
                    value = m.group(0)
                    if ttype['store']:
                        yield dict(
                            type=ttype['type'],
                            value=value,
                            line=line,
                            column=column
                        )
                    column += len(value)
                    break
            else:
                raise UnknownToken(line, column, line_code)

