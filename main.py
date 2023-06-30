#!/usr/bin/env python3

import collections
import collections.abc
from pptx import Presentation
from pptx.util import Inches, Pt
from hymntext import Hymn


def hymn_slide(title: str, verses: list, hymnal: str = "", hymn_index: int = 0) -> None:
    prs = Presentation("template.pptx")
    prs = append_title_slide(prs, title, hymnal=hymnal, hymn_index=hymn_index)
    for v in verses:
        prs = append_word_slide(prs, v)
    prs.save("test.pptx")


def append_title_slide(
    prs: Presentation, title: str, hymnal: str = "", hymn_index: int = 0
) -> Presentation:
    title_slide_layout = prs.slide_layouts[0]
    slide = prs.slides.add_slide(title_slide_layout)
    slide.shapes.title.text = title
    if hymnal != "":
        if hymn_index != 0:
            subtitle = hymnal + " #" + str(hymn_index)
        else:
            subtitle = hymnal
        slide.placeholders[1].text = subtitle

    return prs


def append_word_slide(
    prs: Presentation,
    words: str,
    left: float = 1,
    top: float = 1,
    width: float = 1,
    height: float = 1,
) -> Presentation:
    blank_slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_slide_layout)
    txBox = slide.shapes.add_textbox(
        Inches(left), Inches(top), Inches(width), Inches(height)
    )
    tf = txBox.text_frame
    p = tf.add_paragraph()
    p.text = words
    p.font.size = Pt(20)
    return prs


def main():
    test = Hymn("O for a Thousand", "UMH", 57)
    hymn_slide(test.title, test.verses, test.hymnal, test.hymn_index)


if __name__ == "__main__":
    main()
