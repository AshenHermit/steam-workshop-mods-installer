from setuptools import setup, find_packages
from pathlib import Path
 
def get_requirements():
    requirements_path = (Path(__file__)/'../requirements.txt').resolve()
    requirements = requirements_path.read_text(encoding='utf-8')
    requirements = requirements.split("\n")
    requirements = list(map(lambda x: x.strip(), requirements))
    return requirements

setup(
    name='steam workshop mods installer',
    version='0.2',
    description='A small handy application for installing mods from steam workshop',
    author='hermit',
    author_email='nameless.voice.x@gmail.com',
    packages = find_packages(),
    install_requires = ["setuptools", "pathlib"],
    requires = get_requirements(),
    entry_points = {
        'console_scripts': [
            'smod = mods_installer.cli:main',
        ],
    },
)