import os
from typing import List
from pathlib import Path
import argparse

from mods_installer.game import Game

class ModDownloaderCLI:
    def __init__(self) -> None:
        self.CWD = Path(os.getcwd())
        self.game = Game(self.CWD)

    def install_mod(self, args):
        queries = args.queries
        self.game.install_mods_from_queries(queries)

    def update_mods(self, args):
        self.game.update_mods()

    def print_log(self, args):
        self.game.print_log()

    def make_parser(self):
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers()

        parser_install = subparsers.add_parser("install", help="installs mods from url or using just an id")
        parser_install.add_argument("queries", help="links to a mod or mod ids", nargs="+")
        parser_install.set_defaults(func=self.install_mod)

        parser_update = subparsers.add_parser("update", help="updates mods registered in config file")
        parser_update.set_defaults(func=self.update_mods)

        parser_log = subparsers.add_parser("log", help="prints known info about mods")
        parser_log.set_defaults(func=self.print_log)

        return parser

    def run(self):
        parser = self.make_parser()
        args = parser.parse_args()
        if hasattr(args, "func"):
            args.func(args)
        else:
            parser.print_help()

def main():
    cli = ModDownloaderCLI()
    cli.run()

if __name__ == '__main__':
    main()