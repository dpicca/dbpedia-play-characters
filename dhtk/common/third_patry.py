# !/usr/local/bin/python
# -*- coding: utf-8 -*-
"""Contains the ThirdPartyProgram class."""

import os
import signal
from abc import ABCMeta, abstractmethod

from appdirs import user_data_dir

import psutil


class ThirdPartyProgram(metaclass=ABCMeta):
    """
    Abstract Class for Third party programs.

    This class should be parent to any subclass adding a functionality from a third party program.
    """

    _executable = None

    def __init__(
            self,
            library_name,
            executable_name,
            third_party_library_path=None,
            use_dhtk_library=False,
            use_external=False
    ):
        """
        Init function of ThirdPartyProgram.

        :param str library_name:
        :param str executable_name:
        :param str third_party_library_path:
        :param bool use_dhtk_library:
        :param bool use_external:
        """
        library_path = ""
        if not use_dhtk_library:
            if not use_external:
                self._executable = self._find_in_path(executable_name)
        else:
            if not self._executable:
                library_path = os.path.join(user_data_dir("dhtk", "dhtk"), "lib")

                if third_party_library_path:
                    library_path = os.path.join(third_party_library_path)

                if not os.path.exists(library_path):
                    os.makedirs(library_path)
                else:
                    self._executable = self._find_in_third_party_library(
                        os.path.join(library_path, library_name),
                        executable_name
                    )

            if not self._executable:
                self._download_and_unpack(library_path)
                self._executable = self._find_in_third_party_library(
                    os.path.join(library_path, library_name),
                    executable_name
                )

        if not self._executable and not use_external:
            raise OSError(
                """"
                Could not find or install third party library %s !
                Check your write permissions for library folder %s""" % (library_name, library_path)
            )
        try:
            self.termination_signal = signal.CTRL_C_EVENT
        except AttributeError:
            self.termination_signal = signal.SIGTERM

    @staticmethod
    def _find_in_path(executable_name):
        """
        Find out if program is in PATH.

        :param str executable_name: the name of the executable
        :return: str:
        """
        def is_exe(file_path):
            """Check if file path can be executed."""
            return os.path.isfile(file_path) and os.access(file_path, os.X_OK)

        program_path, _ = os.path.split(executable_name)
        if program_path:
            if is_exe(executable_name):
                return executable_name
        else:
            for path in os.environ["PATH"].split(os.pathsep):
                path = path.strip('"')
                exe_file = os.path.join(path, executable_name)
                if is_exe(exe_file):
                    return exe_file

    @staticmethod
    def _find_in_third_party_library(library_path, executable_name):
        """
        Find out if the program is installed in the library_path.

        :param str library_path:
        :param str executable_name:
        :return str: of None if not found.
        """
        probable_executable = os.path.join(library_path, executable_name)
        if os.path.isfile(probable_executable):
            return probable_executable
        return None

    @abstractmethod
    def _download_and_unpack(self, library_path):
        """
        Implement this function for each child of this class.

        :param str library_path:
        :return None:
        """
        NotImplementedError(
            "Class %s doesn't implement _download_and_unpack()" % self.__class__.__name__)

    def get_executable(self):
        """
        Return the path of the executable of the third party program.
        """
        return self._executable

    @staticmethod
    def kill_pid(proc_pid):
        """
        Kill a process by pid.

        :param proc_pid:
        :return:
        """
        process = psutil.Process(proc_pid)
        for proc in process.children(recursive=True):
            proc.kill()
            process.kill()
