import string

class SealedScraper():
    def __init__(self, setName):
        self.setName=setName
        self.results = []

    def getResults(self):
        return self.results

    def comparesetNames(self, setName, setName2):
        """
        compares two set names and returns true if they are the same
        """
        # remove all punctuation from card names
        setName = setName.translate(str.maketrans('', '', string.punctuation)).lower()
        setName2 = setName2.translate(str.maketrans('', '', string.punctuation)).lower()
        if setName in setName2:
            return True
        else:
            return False
