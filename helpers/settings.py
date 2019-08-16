#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""Xiaomi Flashable Firmware Creator Settings loader"""

import json


def load_settings() -> dict:
    """
    loads settings into dict
    :return: dict
    """
    with open('data/settings.json', 'r') as json_file:
        settings = json.load(json_file)
    return settings


def update_settings(new: dict):
    """
    loads settings into dict
    :return: dict
    """
    with open('data/settings.json', 'w') as json_file:
        json.dump(new, json_file)
