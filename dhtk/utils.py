# !/usr/local/bin/python
# -*- coding: utf-8 -*-
"""Utility functions used by all modules."""

import os
import uuid
import platform
import zipfile
import chardet
from shutil import copyfileobj
from urllib.request import urlopen, Request

import requests

from dhtk import LOGGER


def url_exists(url):
    """
    Check if an url exists and if it is available.

    :param str url:
    :return bool:
    """
    if url.startswith("file:"):
        return os.path.exists("/" + url.replace(r"///", r"/").split(r"/", 1)[1])

    try:
        response = requests.head(url)
    except requests.exceptions.ConnectionError:
        raise ConnectionError("Make shure you are connected to the server.")
    return response.ok


def download_file(uri, destination):
    """
    Download an uri to a destination.

    :param str uri:
    :param str destination:
    :return str: path of the downloaded file.
    """
    try:
        if not os.path.exists(os.path.dirname(destination)):
            os.makedirs(os.path.dirname(destination))
    except IOError:
        LOGGER.error("Could not create %s, pleas check your rights.", destination)
        return ""

    if not os.path.basename(destination):
        destination = os.path.join(destination, str(uuid.uuid4()) + uri.rsplit(".", 1)[1])

    headers = {'User-Agent': '"Mozilla/4.0 (compatible; MSIE 5.01; Windows NT 5.0)"'}
    request = Request(uri, data=None, headers=headers)

    if os.path.isdir(destination):
        destination += uri.rsplit("/", 1)[1]
    else:
        destination = os.path.join(os.path.dirname(destination),  uri.rsplit("/", 1)[1])

    response = urlopen(request)
    with open(destination, 'wb') as out_file:
        copyfileobj(response, out_file)
    response.close()
    LOGGER.info("Downloaded %s from %s", destination, uri)
    return destination


def file_creation_date(path_to_file):
    """
    Try to get the date that a file was created,

    Falling back to when it was last modified if that isn't possible.
    See http://stackoverflow.com/a/39501288/1709587 for explanation and credit.

    TODO: Test on MacOS and Windows
    """

    if platform.system() == "Windows":
        return os.path.getctime(path_to_file)

    stat = os.stat(path_to_file)
    try:
        return stat.st_birthtime
    except AttributeError:
        # We're probably on Linux. No easy way to get creation dates here,
        # so we'll settle for when its content was last modified.
        return stat.st_mtime


def unarchive_book(path, destination=None):
    title = path.rsplit("/", 1)[1].replace(".zip", "")
    archive = zipfile.ZipFile(path, 'r')

    for txt_file in archive.namelist():
        print(title)
        if txt_file.endswith(".txt"):
            raw_text = archive.read(txt_file)
            break

    detect = chardet.detect(raw_text)
    try:
        raw_text = raw_text.decode(detect["encoding"])
    except UnicodeDecodeError:
        raw_text = raw_text.decode("utf-8", errors='backslashreplace')
    if destination:
        try:
            with open(destination, "w")as out_file:
                out_file.write(destination)
        except IOError:
            LOGGER.debug("%s could not be written.", destination)

    return raw_text
