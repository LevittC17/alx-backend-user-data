#!/usr/bin/env python3
"""
This module provides a function to obfuscate fields in a log message.
"""

import re
from typing import List


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    Obfuscate specified fields in a log message using regular expressions.

    Arguments:
    fields (List[str]): A list of strings representing fields to obfuscate.
    redaction (str): A string representing the obfuscation.
    message (str): A string representing the log line.
    separator (str): A string representing the field separator.

    Returns:
    str: The obfuscated log message.
    """
    for field in fields:
        message = re.sub(
            f"{field}=[^{separator}]*",
            f"{field}={redaction}",
            message)
    return message
