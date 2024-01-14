#!/usr/bin/env python3
"""
This module provides a function to obfuscate fields in a log message.
"""

import logging
import re
from typing import List, Tuple


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class that filters specified
    fields in log records.
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        Initialize the RedactingFormatter with a list of fields
        to abfuscate

        Arguments:
        fields (List[str]): A list of strings representing
            fields to abfuscate
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the specified log record by obfuscating fields.

        This method applies the filter_datum function to the formatted
        log record to replace the values
        of specified fields with the redaction string.

        Arguments:
        record (logging.LogRecord): The log record to format.

        Returns:
        str: The formatted and obfuscated log message.
        """
        original_format = super().format(record)
        return filter_datum(self.fields, self.REDACTION,
                            original_format, self.SEPARATOR)


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


PII_FIELDS: Tuple[str, ...] = ("name", "email", "phone", "ssn", "password")


def get_logger() -> logging.Logger:
    """
    Create a logger object with specific configuration.

    The logger is named "user_data", logs up to INFO level,
    does not propagate messages, and has a StreamHandler with
    RedactingFormatter as the formatter.

    Returns:
    logging.Logger: The configured logger object.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    # Create a StreamHandler with RedactingFormatter
    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(PII_FIELDS)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger
