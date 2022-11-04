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
        # if there is no Set or Draft tag, add the draft tag
        if not "set" in tags and not "draft" in tags:
            tags.append("draft")
            
        return tags

    def setLanguage(self, string):
        """
        returns a string of the language of the card
        """
        if "english" in string.lower():
            return "English"
        elif "russian" in string.lower():
            return "Russian"
        elif "korean" in string.lower():
            return "Korean"
        elif "french" in string.lower():
            return "French"
        elif "german" in string.lower():
            return "German"
        elif "spanish" in string.lower():
            return "Spanish"
        elif "italian" in string.lower():
            return "Italian"
        elif "japanese" in string.lower():
            return "Japanese"
        elif "portuguese" in string.lower():
            return "Portuguese"
        elif "chinese" in string.lower():
            return "Chinese"
        else:
            return "English"

    def removeLanguage(self, string):
        # We want to remove any language from the name and return the string
        if "english" in string.lower():
            return string.replace("English", "")
        elif "russian" in string.lower():
            return string.replace("Russian", "")
        elif "korean" in string.lower():
            return string.replace("Korean", "")
        elif "french" in string.lower():
            return string.replace("French", "")
        elif "german" in string.lower():
            return string.replace("German", "")
        elif "spanish" in string.lower():
            return string.replace("Spanish", "")
        elif "italian" in string.lower():
            return string.replace("Italian", "")
        elif "japanese" in string.lower():
            return string.replace("Japanese", "")
        elif "portuguese" in string.lower():
            return string.replace("Portuguese", "")
        elif "chinese" in string.lower():
            return string.replace("Chinese", "")
        else:
            return string


