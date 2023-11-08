import RollClass

class Attack(RollClass.Roll):

    dSize = 20

    def __init__(self, rollStr):
        return super().__init__(rollStr)

    pass



def main():
    r = Roll("3d4")
    print (r)

if __name__ == "__main__":
    main()
