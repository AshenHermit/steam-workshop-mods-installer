import os
from typing import List
from pathlib import Path
import argparse

from mods_installer.game import Game

class ModDownloaderCLI:
    def __init__(self) -> None:
        self.CWD = Path(os.getcwd())
        self.game = Game(self.CWD)

    def on_startup(self):
        self.game.check_mods_for_defects()

    def install_mods(self, args):
        for q in args.queries:
            self.game.install_mod_from_query(q)
        
    def remove_mods(self, args):
        for q in args.queries:
            rm_empty_folders = not args.dont_remove_empty_folders
            self.game.remove_mod_from_query(q, rm_empty_folders)

    def remove_all_mods(self, args):
        rm_empty_folders = not args.dont_remove_empty_folders
        self.game.remove_all_mods(rm_empty_folders)

    def update_mods(self, args):
        self.game.update_mods()

    def print_log(self, args):
        self.game.print_log()

    def make_parser(self):
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers()

        parser_install = subparsers.add_parser("install", help="installs mods from url or using just an id")
        parser_install.add_argument("queries", help="links to a mod or mod ids", nargs="+")
        parser_install.set_defaults(func=self.install_mods)

        parser_remove = subparsers.add_parser("remove", help="removes mods")
        parser_remove.add_argument("queries", help="links to a mod or mod ids", nargs="+")
        parser_remove.add_argument("-RE", "--dont-remove-empty-folders", action='store_true', help="when use this flag, empty folders will not be removed")
        parser_remove.set_defaults(func=self.remove_mods)

        parser_remove_all = subparsers.add_parser("remove-all", help="removes all mods registered in config file")
        parser_remove_all.add_argument("-RE", "--dont-remove-empty-folders", action='store_true', help="when use this flag, empty folders will not be removed")
        parser_remove_all.set_defaults(func=self.remove_all_mods)

        parser_update = subparsers.add_parser("update", help="updates mods registered in config file")
        parser_update.set_defaults(func=self.update_mods)

        parser_log = subparsers.add_parser("log", help="prints known info about mods")
        parser_log.set_defaults(func=self.print_log)

        return parser

    def run(self):
        self.on_startup()

        parser = self.make_parser()
        args = parser.parse_args()
        if hasattr(args, "func"):
            print()
            args.func(args)
        else:
            parser.print_help()

def main():
    cli = ModDownloaderCLI()
    cli.run()

if __name__ == '__main__':
    main()