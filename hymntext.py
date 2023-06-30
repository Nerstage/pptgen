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
        lines = read_hymn(self.file)
        self.verses = [""]
        curr_verse = 0
        for line in lines:
            if line == "":
                curr_verse = curr_verse + 1
                self.verses.append("")
            else:
                if self.verses[curr_verse] == "":
                    self.verses[curr_verse] = line
                else:
                    self.verses[curr_verse] = self.verses[curr_verse] + "\n" + line


def read_hymn(file: str) -> list:
    lines = []
    with open(file, "r") as f:
        for line in f:
            lines.append(line.strip())
    return lines


def scrape_hymn(hymnal: str, hymn_index: int):
    url = f"https://hymnary.org/hymn/{hymnal}/{hymn_index}"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    full_text = soup.find(id="text")
    line_text = full_text.find_all("p")
    with open("words/test.txt", "w") as f:
        for line in line_text:
            f.write(line.text)
            f.write("\n\n")


def main():
    test = Hymn("O for a Thousand", "UMH", 368)
    print(test.title)
    print(test.verses)


if __name__ == "__main__":
    main()
