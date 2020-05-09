class CommonNote:
    def __init__(self, high, weight, isCommon, isNote):
        self.high = high
        self.weight = weight
        self.isCommon = isCommon
        self.isNote = isNote

    def __eq__(self, other):
        if self.isNote == other.isNote and self.weight == other.weight and self.high == other.high:
            return True
        else:
            return False


class notation:
    def __init__(self, author, title, url):
        self.author = author
        self.title = title
        self.url = url
