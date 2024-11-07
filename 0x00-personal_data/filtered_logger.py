#!/usr/bin/env python3
""" 0. Regex-ing """
from re import sub
from typing import List


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """ returns the log message obfuscated """
    for field in fields:
        m = sub(rf'{field}=[^{separator}]*', f'{field}={redaction}', message)
    return m
