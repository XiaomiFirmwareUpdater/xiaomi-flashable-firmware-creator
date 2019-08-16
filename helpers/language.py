#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""Xiaomi Flashable Firmware Creator Language Stuff"""

import json

RTL_LANGUAGES = ['ar']


def load_strings() -> dict:
    """
    loads settings into dict
    :return: dict
    """
    with open('data/translations.json', 'r') as json_file:
        translations = json.load(json_file)
    return translations
