# !/usr/local/bin/python
# -*- coding: utf-8 -*-
"""DHTK library."""

import logging

LOGGER = logging.getLogger(__name__)

# TODO: remove in production version substitute with nullHandler
LOGGER.setLevel(logging.INFO)
_HANDLER = logging.StreamHandler()
_HANDLER.setLevel(logging.INFO)
_HANDLER.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
LOGGER.addHandler(_HANDLER)

# LOGGER.addHandler(logging.NullHandler())

#LOGGER.debug("DHTK")
__all__ = ("catalogs", "metadata", "LOGGER")
