import subprocess
import sys

class Install():
    '''class for installing and updating dependences for the program'''
    def __init__(self):
       self.main() 

    # method for executing pip install process on the system
    def install(self, package):
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", package])

    # main method calls install() on all dependencies 
    def main(self):
        self.install('google-api-python-client')
        self.install('google-auth-httplib2')
        self.install('google-auth-oauthlib')
