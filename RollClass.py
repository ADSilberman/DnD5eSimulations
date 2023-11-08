import re
import random
import math
import numpy as np
from typing import NamedTuple
# import SymPy

class OneRoll:
    def __init__(self, nDice, dSize, augStr):
        self.nDice = nDice
        self.dSize = dSize
        self.augStr = augStr
        self.augs = self.parse(self.augStr)
        #self.rollStr = rollStr
        #self.nDice, self.dSize = self.parse(rollStr) #(nDice, dSize)
        self.result, self.rollValues, self.rollFlags = self.roll(self.nDice, self.dSize, self.augs)
        # self.rolls = []

    #def parse(self, rollStr):
    #    m = re.match(r"(\d+)d(\d+)", rollStr)
    #    nDice = int(m.group(1))
    #    dSize = int(m.group(2))
    #    return nDice, dSize

    #def split(self, rollStr):
    #    self.rolls = re.split(r"(\d+)d(\d+)",rollStr)
    #    pass 
    def parse(self, augStr):
        spec = [
            ("KEEP HIGHEST",    r"kh",  r"\d+"),
            ("KEEP LOWEST",     r"kl",  r"\d+"),
            ("CRIT SUCC",       r">>",  r"\d+"),
            ("CRIT FAIL",       r"<<",  r"\d+"),
            ("REROLL UNDER",    r"rr",  r"\d+"),
            ("EXPLODE OVER",    r"ex",  r"\d+"),
            ("UNKNOWN CHAR SEQ",r"",    r".")
        ]
        regexPattern = "|".join("{1}(?P<{0}>{2})".format(elem) for elem in spec)
        matchAugs = re.findIter(regexPattern, augStr)
        for m in matchAugs:
            kind = m.lastgroup # name of last captured group
            if kind == "UNKNOWN CHAR SEQ":
                sys.exit("Unexpected character sequence \'" + m.group(kind) + "\'")
            value = int(m.group(kind))
            yield Augmentation(kind, value)

    def roll(self, nDice, dSize, augs):
        rollResults = [random.randrange(1,dSize) for i in range(nDice)]
        flags = []
        for aug in augs:
            if aug.kind == "KEEP HIGHEST":
                if aug.value == nDice:
                    newRollResults = [random.randrange(1,dSize) for i in range(nDice)]
                    if sum(newRollResults) > sum(rollResults):
                        rollResults = newrollResults
                else:
                    for i in range(nDice - aug.value):
                        rollResults.remove(min(rollResults))
            elif aug.kind == "KEEP LOWEST":
                if aug.value == nDice:
                    newRollResults = [random.randrange(1,dSize) for i in range(nDice)]
                    if sum(newRollResults) < sum(rollResults):
                        rollResults = newrollResults
                else:
                    for i in range(nDice - aug.value):
                        rollResults.remove(max(rollResults))
            elif aug.kind == "REROLL UNDER":
                for i in range(len(rollResults)):
                    if rollResults[i] <= aug.value:
                        rollResults[i] = random.randrange(1,dSize)
            elif aug.kind == "EXPLODE OVER":
                for roll in rollResults:
                    if roll >= aug.value:
                        rollResults.append(random.randrange(1,dSize))
            elif aug.kind == "CRIT SUCC":
                nSucc = 0
                for roll in rollResults:
                    if roll >= aug.value:
                        nSucc += 1
                if nSucc >= 1:
                    flags.append(Augmentation(kind = "CRIT SUCC", value = int(nSucc)))
            elif aug.kind == "CRIT FAIL":
                nFail = 0
                for roll in rollResults:
                    if roll >= aug.value:
                        nFail += 1
                if nFail >= 1:
                    flags.append(Augmentation(kind = "CRIT SUCC", value = int(nFail)))


        total = sum(rollResults)
        return total, rollResults, flags

    def __repr__(self):
        return (self.rollStr + ":\n" + str(self.result) + "\n" + "(" + ",".join(map(str, self.rollValues)) + ")\nFlags:" + self.rollflags)

class Augmentation(NamedTuple):
    kind: str
    value: str

class Roll:
    def __init__(self, rollStr, rollMax):
        self.rollStr = rollStr
        self.rollMax = rollMax

        self.rollList = self.parse(self.rollStr)
        self.resultArr = self.roll(self.rollList)


    def _spaceRepl(m):
        return " " + m.group(0) + " "

    def parse(self, rollStr):
        subStr = re.sub(r"(?:\S)[\+\-\*\/]+(?:\S)", _spaceRepl, rollStr) # format text by adding whitetext around operators if it does not currently exist
        strList = re.split(r"\s+", subStr) # split into operations, rolls, and numbers (integers or floats)

        rollIter = re.findIter(r"(\d+)d(\d+)(\S+)", subStr)
        lenRollIter = len(rollIter)
        finStr = subStr[:rollIter[0].start()]
        for i in range(lenRollIter):
            currMatch = rollIter[i]
            finStr += oneRoll(currMatch.group(1), currMatch.group(2), currMatch.group(3)).result # nDice, dSize, augmentations
            if i != lenRollIter-1:
                nextMatch = rollIter[i+1]
                finStr += subStr[currMatch.end():nextMatch.start()]
        finStr += subStr[rollIter[-1]:]

        #rollList = []
        #for elem in strList: # identify each
        #    if re.match(r"\d+d\d+", elem): rollList.append(oneRoll(elem)) # rolls (can have values/flags/modifiers afterwards)
        #    elif re.fullmatch(r"\d*\.\d*"): rollList.append(elem) #float(elem)) # number (float)
        #    elif re.fullmatch(r"\d+"): rollList.append(elem) #int(elem)) # number (int)
        #    else: sys.exit("Unexpected character sequence \'" + elem + "\'")
        #return rollList

    def roll(self, rollList, maxRolls):
        rollTotalArr = np.arange(maxRolls)
        self.rollStr
        for i in range(maxRolls):
            for r in rollList:

        return rollTotalArr


def main():
    r = Roll("3d4")
    print (r)

if __name__ == "__main__":
    main()