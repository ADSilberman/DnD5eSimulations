import re
import random

class Roll:
    def __init__(self, rollStr):
        self.rollStr = rollStr
        self.rollTuple = self.parse(rollStr) #(nDice, dSize)
        self.result, self.rollValues = self.roll(self.rollTuple)
        # self.rolls = []

    def parse(self, rollStr):
        self.m = re.match(r"(\d+)d(\d+)", rollStr)
        return (int(self.m.group(1)), int(self.m.group(2))) #(nDice, dSize)

    def split(self, rollStr):
        self.rolls = re.split(r"(\d+)d(\d+)",rollStr)
        pass 

    def roll(self, rollTuple):
        rollResults = tuple(random.randrange(1,rollTuple[1]) for i in range(rollTuple[0]))
        value = sum(rollResults)
        return value, rollResults

    def __repr__(self):
        return (self.rollStr + ":\n" + str(self.result) + "\n" + "(" + ",".join(map(str, self.rollValues)) + ")")

def main():
    r = Roll("3d4")
    print (r)

if __name__ == "__main__":
    main()