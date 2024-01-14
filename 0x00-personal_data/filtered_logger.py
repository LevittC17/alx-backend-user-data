#!/usr/bin/env python3

"""
This module provides a function to obfuscate fields in a log message.
"""


import re


def filter_datum(fields, redaction, message, separator):
    """
    Obfuscate specified fields in a log message.

    Arguments:
    fields -- list of strings representing fields to obfuscate
    redaction -- string representing the obfuscation
    message -- string representing the log line
    separator -- string representing the field separator
    """
    for field in fields:
        message = re.sub(f"{field}=[^;]*", f"{field}={redaction}", message)
    return message
