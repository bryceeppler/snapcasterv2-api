import string
import re

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
        if not "set" in tags and not "draft" in tags and not "collector" in tags:
            tags.append("draft")
            
        return tags

    def setLanguage(self, string):
        """
        Returns a string containing the language of the set

        These are the possible languages for MTG printings
        English, Russian, Korean, French, German, 
        Spanish, Italian, Japanese, Portuguese, Chinese,
        Chinese Traditional, Chinese Simplified

        If we find any of these in the given string (case insensitive), 
        we return the language. If we don't find any of these, we return
        English
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
        """
        Removes the language from the string, and returns the string without
        the language.

        These are the possible languages for MTG printings
        English, Russian, Korean, French, German,
        Spanish, Italian, Japanese, Portuguese, Chinese,
        Chinese Traditional, Chinese Simplified

        Check if any of these are in the string (case insensitive), and if they
        are, remove them from the string and return the string without the language.
        """
        englishExpression = re.compile(r"english", re.IGNORECASE)
        russianExpression = re.compile(r"russian", re.IGNORECASE)
        koreanExpression = re.compile(r"korean", re.IGNORECASE)
        frenchExpression = re.compile(r"french", re.IGNORECASE)
        germanExpression = re.compile(r"german", re.IGNORECASE)
        spanishExpression = re.compile(r"spanish", re.IGNORECASE)
        italianExpression = re.compile(r"italian", re.IGNORECASE)
        japaneseExpression = re.compile(r"japanese", re.IGNORECASE)
        portugueseExpression = re.compile(r"portuguese", re.IGNORECASE)
        chineseExpression = re.compile(r"chinese", re.IGNORECASE)
        
        string = englishExpression.sub("", string)
        string = russianExpression.sub("", string)
        string = koreanExpression.sub("", string)
        string = frenchExpression.sub("", string)
        string = germanExpression.sub("", string)
        string = spanishExpression.sub("", string)
        string = italianExpression.sub("", string)
        string = japaneseExpression.sub("", string)
        string = portugueseExpression.sub("", string)
        string = chineseExpression.sub("", string)
        
        return string

