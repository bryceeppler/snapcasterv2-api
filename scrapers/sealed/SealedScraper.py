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

    def setTags(self, string):
        """
        returns a list of tags from a string
        """
        tags = []
        if "pack" in string.lower():
            tags.append("pack")
        if "box" in string.lower():
            tags.append("box")
        if "bundle" in string.lower():
            tags.append("bundle")
        if "set" in string.lower():
            tags.append("set")
        if "draft" in string.lower():
            tags.append("draft")
        if "jumpstart" in string.lower():
            tags.append("jumpstart")
        if "collector" in string.lower():
            tags.append("collector")
        return tags
