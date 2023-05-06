# !/usr/local/bin/python
# -*- coding: utf-8 -*-
"""Catalog module for the Project Gutenberg "http://www.gutenberg.org/"."""

from .book import GutenbergBook
from .search_triplet_store import GutenbergSearchTripletStore
from .text_repository import GutenbergTextRepository

__all__ = ("search_triplet_store", "text_repository",)
