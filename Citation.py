import re
from enum import Enum


class Source(Enum):
    DWB = 1
    GWB = 2
    ADE = 3
    UNDEFINED = -1


SOURCE_NAMES: dict[Source, str] = {
        Source.DWB: "Deutsches Wörterbuch von Jacob Grimm und Wilhelm Grimm",
        Source.GWB: "Goethe-Wörterbuch",
        Source.ADE: "Grammatisch-Kritisches Wörterbuch der Hochdeutschen Mundart"
    }


class Citation:
    def __init__(self):
        self.word: str = ""
        self.dict_name: str = ""
        self.version: str = ""
        self.website: str = ""
        self.date: str = ""
        self.start_page: str = ""
        # tag
        self.source:Source = Source.UNDEFINED

    def parse(self, part1: str, part2: str):
        # word
        word_match = re.search(r"„(.+?)“", part1)
        if word_match:
            self.word = word_match.groups()[0]
        # handle dwb
        if "," in self.word:
            self.word, pos = self.word.split(",")
            if re.search(r"n.|m.|f.", pos):
                self.word = self.word[0].upper() + self.word[1:].lower()
            else:
                self.word = self.word.upper()
        # source
        for item in SOURCE_NAMES.items():
            reg = fr"({item[1]}.*)(, Version)"
            dict_name_match = re.search(reg, part1)
            if dict_name_match:
                self.dict_name = dict_name_match.group(0)
                self.source = item[0]
                break
        # version
        version_match = re.search(r"Version \d+/\d+", part1)
        if version_match:
            self.version = version_match.group(0)
        # website
        website_match = re.search(r"<(.*)>", part1)
        if website_match:
            self.website = website_match.group(1)
        # date
        date_match = re.search(r"\d+\.\d+.\d+", part1)
        if date_match:
            self.date = date_match.group(0)
        # start page
        self.start_page = part2

    def __str__(self):
        if self.source == Source.UNDEFINED:
            return ""
        # pure_dict_name_len
        l = len(SOURCE_NAMES[self.source])
        if self.source == Source.GWB or self.source == Source.DWB:
            return f"„{self.word}“. In: <em>{self.dict_name[0:l]}</em>{self.dict_name[l:]}, {self.version}. {self.start_page}. {self.website}. Stand: {self.date}."
        elif self.source == Source.ADE:
            return f"„{self.word}“. In: Johann Christoph Adelung(Hrsg.): <em>{self.dict_name[0:l]}</em>{self.dict_name[l:]}, {self.version}. {self.start_page}. {self.website}. Stand: {self.date}."

if __name__ == "__main__":
    c = Citation()
    c.parse("„Schalk“, Goethe-Wörterbuch, digitalisierte Fassung im Wörterbuchnetz des Trier Center for Digital Humanities, Version 01/23, <https://www.woerterbuchnetz.de/GWB?lemid=S00934>, abgerufen am 02.01.2024.", "Bd. 7, Sp. 824")
    print(c)
