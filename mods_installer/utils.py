from termcolor import colored
def print_error(string:str=""):
    print(colored(string, 'red'))

def print_success(string:str=""):
    print(colored(string, 'green'))

def print_minor(string:str=""):
    print(colored(string, 'grey'))
