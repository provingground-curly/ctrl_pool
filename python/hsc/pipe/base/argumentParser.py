import argparse, os, getpass
from .camera import parseInstrument
from lsst.pipe.base import ArgumentParser

class SubaruArgumentParser(ArgumentParser):

    def __init__(self, *args, **kwargs):
        self.defaultToUserName = kwargs.pop("defaultToUserName", True)
        ArgumentParser.__init__(self, *args, **kwargs)
        self.add_argument('--rerun', type=str, default=None, help='Desired rerun (overrides --output)',
                          action="store", dest="rerun")

    def _fixPaths(self, namespace):
        if namespace.rerun and namespace.output:
            argparse.ArgumentTypeError("Please specify --output or --rerun, but not both")
        if self.defaultToUserName and namespace.rerun is None and namespace.output is None:
            namespace.rerun = getpass.getuser()
        ArgumentParser._fixPaths(self, namespace)
        if namespace.rerun:
            root = namespace.input
            namespace.output = os.path.join(root, "rerun", namespace.rerun)
