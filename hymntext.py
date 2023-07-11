import requests
from bs4 import BeautifulSoup


class Hymn:
    def __init__(
        self, title: str, hymnal: str = "", hymn_index: int = 0, file: str = None
    ) -> None:
        self.title = title
        self.file = file
        self.hymnal = hymnal
        self.hymn_index = hymn_index
        self.create_verses()

    def get_num_verses(self):
        lines = read_hymn(self.file)
        return lines.count("") + 1

    def create_verses(self):
        if self.file is None:
            lines = scrape_hymn(self.hymnal, self.hymn_index)
            self.file = "words/test.txt"
        self.verses, self.refrain, self.order = read_hymn(self.file)


def read_hymn(file: str) -> list:
    verses = []
    refrain = ""
    order = []
    with open(file, "r") as f:
        lines = f.readlines()
        current_section = ""
        is_verse = False
        verse_num = 0
        for line in lines:
            line = line.strip()
            if line.startswith("Refrain:") or line.strip("\t") == "(Refrain)":
                if current_section:
                    if is_verse:
                        verses.append(current_section.strip("\t"))
                        order.append(verse_num)
                    else:
                        refrain = current_section.strip("\t")
                        order.append("refrain")
                is_verse = False
                continue
            elif line and line[0].isdigit():
                if current_section:
                    if is_verse:
                        verses.append(current_section.strip("\t"))
                        order.append(verse_num)
                    else:
                        refrain = current_section.strip("\t")
                        order.append("refrain")
                verse_num = int(line[0])
                current_section = line[2:]
                is_verse = True
            else:
                current_section += "\n" + line.strip("\t")
            # print(current_section)
        if current_section:
            if is_verse:
                verses.append(current_section.strip("\t"))
                order.append(verse_num)
            else:
                refrain = current_section.strip("\t")
                order.append("refrain")
        return verses, refrain, order


def scrape_hymn(hymnal: str, hymn_index: int):
    url = f"https://hymnary.org/hymn/{hymnal}/{hymn_index}"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    full_text = soup.find(id="text")
    line_text = full_text.find_all("p")
    with open("words/test.txt", "w") as f:
        for line in line_text:
            f.write(line.text + "\n")


def main():
    test = Hymn("O for a Thousand", "UMH", 116)
    print(test.title)
    num = 1
    for verse in test.verses:
        print(num)
        num += 1
        print(verse)
    print("Refrain")
    print(test.refrain)
    print(test.order)


if __name__ == "__main__":
    main()
