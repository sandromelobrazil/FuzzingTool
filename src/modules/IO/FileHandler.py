from modules.IO.OutputHandler import outputHandler as oh
import os
from datetime import datetime

class FileHandler:
    """Class that handle with the files
       Singleton Class
    """
    __instance = None

    @staticmethod
    def getInstance():
        if FileHandler.__instance == None:
            FileHandler()
        return FileHandler.__instance

    """
    Attributes:
        wordlistFile: The wordlist file
        proxiesFile: The proxies file
        outputFile: The output file
    """
    def __init__(self):
        """Class constructor"""
        if FileHandler.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            FileHandler.__instance = self
        self.__wordlistFile = None
        self.__proxiesFile = None
        self.__outputFile = None
    
    def readData(self, dataFileName: str):
        '''Reads the default data of the requests.

        @type dataFileName: str
        @param dataFileName: The filename
        @returns list: The content into data file
        '''
        try:
            dataFile = open('../input/'+dataFileName, 'r')
            return [data.rstrip('\n') for data in dataFile]
        except FileNotFoundError:
            oh.errorBox("File '"+dataFileName+"' not found.")

    def getProxiesFile(self):
        """The proxiesFile getter

        @returns file: The proxies file
        """
        return self.__proxiesFile

    def openProxies(self, proxiesFileName: str):
        """Open the proxies file

        @type proxiesFileName: str
        @param proxiesFileName: The name of the proxies file
        """
        try:
            self.__proxiesFile = open('../input/'+proxiesFileName, 'r')
        except FileNotFoundError:
            oh.errorBox("File '"+proxiesFileName+"' not found.")

    def readProxies(self):
        """Read the proxies from a file
        
        @returns list: The list with proxies dictionary
        """
        proxies = []
        for line in self.__proxiesFile:
            line = line.rstrip("\n")
            proxies.append({
                'http://': 'http://'+line,
                'https://': 'http://'+line
            })
        self.__close(self.__proxiesFile)
        return proxies

    def openWordlist(self, wordlistFileName: str):
        """Open the wordlist file

        @type wordlistFileName: str
        @param wordlistFileName: The name of the wordlist file
        """
        try:
            self.__wordlistFile = open('../input/'+wordlistFileName, 'r')
        except FileNotFoundError:
            oh.errorBox("File '"+wordlistFileName+"' not found. Did you put it in the correct directory?")

    def getWordlistContentAndLength(self):
        """Get the wordlist content, into a list, and the number of lines in file

        @returns (wordlist, length): The tuple with the wordlist and the number of lines
        """
        wordlist = []
        length = 0
        for line in self.__wordlistFile:
            line = line.rstrip("\n")
            wordlist.append(line)
            length += 1
        self.__close(self.__wordlistFile)
        return (wordlist, length)

    def writeOnOutput(self, outputContent: list):
        """Write the vulnerable input and response content into a file

        @param type: list
        @param outputContent: The list with probably vulnerable content
        """
        if outputContent:
            self.__openOutput()
            for content in outputContent:
                for key, value in content.items():
                    self.__outputFile.write(key+': '+str(value)+'\n')
                self.__outputFile.write('\n')
            self.__close(self.__outputFile)
            global outputHandler
            oh.infoBox('Results saved.')

    def __openOutput(self):
        """Opens the output file 
           for store the probably vulnerable response data
        """
        now = datetime.now()
        time = now.strftime("%Y-%m-%d_%H:%M")
        try:
            self.__outputFile = open('../output/'+time+'.txt', 'w')
        except FileNotFoundError:
            os.system('mkdir ../output')
            self.__outputFile = open('../output/'+time+'.txt', 'w')
        finally:
            oh.infoBox(f'Saving results on \'{time}.txt\' ...')

    def __close(self, file: object):
        """Closes the file

        @type file: object
        @param file: The file
        """
        file.close()

fileHandler = FileHandler.getInstance()