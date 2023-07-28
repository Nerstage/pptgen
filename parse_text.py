import logging


def parse_music(text):
    entries = list()
    date = None
    lines = text.strip().split("\n")
    for line in lines:
        title = None
        key = None
        hymnal = None
        num = None
        tag = None
        if not line:
            continue
        elif line[4] == "-":
            date = line
            continue
        else:
            if line[0].isdigit():
                if line[3].isdigit():
                    num = int(line[0:4])
                    line = line[5:]
                else:
                    num = int(line[0:3])
                    line = line[4:]
        try:
            key_start_index = line.index("(")
            title = line[: key_start_index - 1]
            try:
                key_end_index = line.index(")")
                key = line[key_start_index + 1 : key_end_index]
                if len(key) > 3:
                    line = line[key_start_index:].strip()
            except:
                logging.warning(f"Entry on {date} for {title} is missing information.")
        except:
            title = line.strip()
            logging.warning(f"Entry on {date} for {title} is missing information.")
        else:
            line = line[key_end_index + 1 :].strip()
        if line:
            if line.find("Bluegrass") != -1:
                hymnal = "Bluegrass"
                line = line[line.index("]") + 1 :].strip()
            elif line.find("Praise Chorus Book") != -1:
                hymnal = "Praise Chorus Book"
                line = line[line.index("]") + 1 :].strip()
            elif line.find("Hymns and Choruses") != -1:
                hymnal = "Hymns and Choruses"
                line = line[line.index("]") + 1 :].strip()
            elif line.find("Judson Hymnal") != -1:
                hymnal = "Judson Hymnal"
                line = line[line.index("]") + 1 :].strip()
        if hymnal == None and num != None:
            if num < 2000:
                hymnal = "United Methodist Hymnal"
            elif num < 3000:
                hymnal = "The Faith We Sing"
            elif num < 4000:
                hymnal = "Worship & Song"
        if line:
            if line.find("Offertory") != -1:
                tag = "Offertory"
            elif line.find("Prelude") != -1:
                tag = "Prelude"
            elif line.find("Postlude") != -1:
                tag = "Postlude"
            elif line.find("Communion") != -1:
                tag = "Communion"
        entry = {
            "date": date,
            "title": title,
            "key": key,
            "hymnal": hymnal,
            "num": num,
            "tag": tag,
        }
        entries.append(entry)

    return entries


text_document = """
Test Entries Here
"""

entries = parse_music(text_document)

for i in entries:
    print(i)
