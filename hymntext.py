class Hymn:
    def __init__(
        self, title: str, file: str, hymnal: str = "", hymn_index: int = 0
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


def main():
    test = Hymn("O for a Thousand", "57.txt")
    print(test.title)
    print(test.verses)


if __name__ == "__main__":
    main()
