
# for fail throw
class LbaFailException(Exception):
    def __init__(self, desc, lba, secCnt):
        super().__init__(desc)
        self.lba = lba
        self.secCnt = secCnt
        self.exMsg = ""
        