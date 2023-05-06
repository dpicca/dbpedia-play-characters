# !/usr/local/bin/python
# -*- coding: utf-8 -*-
"""
Contains the RdfProWrapper Class.

This class downloads and installs rdfpro, for further usage.
"""

import os
import platform
import tarfile

from dhtk.utils import download_file
from .third_patry import ThirdPartyProgram


class RdfproWrapper(ThirdPartyProgram):
    """A simple installer for the rdfpro program."""

    _rdfpro_url = \
        "https://knowledgestore.fbk.eu/files/rdfpro/0.6/rdfpro-dist-0.6-bin.tar.gz"

    def __init__(self, third_party_library_path=None, use_dhtk_library=True):
        """
        Init function of the RdfproWrapper Class.

        :param str third_party_library_path:
        :param bool use_dhtk_library:
        """
        if platform.system() == "Linux":
            super().__init__(
                "rdfpro",
                "rdfpro",
                third_party_library_path,
                use_dhtk_library,
                use_external=False
            )
        elif platform.system() == "Windows":
            if not os.environ.get("JAVA_HOME"):
                raise EnvironmentError("JAVA_HOME environment variable is missing!")
            super().__init__(
                "rdfpro",
                "rdfpro.cmd",
                third_party_library_path,
                use_dhtk_library,
                use_external=False
            )
        elif platform.system() == "Darwin":
            # TODO: upstream BUG in Mac OS paths with spaces
            def get_classpath(basedir):
                classpath = os.path.join(basedir, "etc")
                lib_dir = os.path.join(basedir, "lib")
                for jar in os.listdir(lib_dir):
                    if jar.endswith(".jar"):
                        classpath += ":{}".format(os.path.join(lib_dir, jar))
                return classpath
            super().__init__(
                "rdfpro",
                "rdfpro",
                third_party_library_path,
                use_dhtk_library,
                use_external=False
            )
            os.environ["CLASSPATH"] = get_classpath(
                os.path.dirname(self.get_executable())
            )
            # TODO: remove next line
            print("export CLASSPATH={}".format(os.environ["CLASSPATH"]))
            self._executable = " ".join([
                "java",
                "-Xmx6G",
                "-Xms1G",
                "-server",
                "eu.fbk.rdfpro.tool.Main"
            ])
        else:
            raise OSError("Could not identify your OS")

    def _download_and_unpack(self, library_path):
        """
        Download and unpack rdfpro to library_path.

        :param str library_path:
        :return: None
        """
        rdfpro = download_file(self._rdfpro_url, library_path)
        tarfile.open(rdfpro).extractall(library_path)
        os.remove(rdfpro)
