#!/usr/bin/env python3

import collections
import collections.abc
from pptx import Presentation
from pptx.util import Inches, Pt
from hymntext import Hymn


def hymn_slide(title, verses):
    prs = Presentation()
    title_slide_layout = prs.slide_layouts[0]
    blank_slide_layout = prs.slide_layouts[6]
    slide1 = prs.slides.add_slide(title_slide_layout)
    slide1.shapes.title.text = title

    for v in verses:
        verse_slide = prs.slides.add_slide(blank_slide_layout)
        left = top = width = height = Inches(1)
        txBox = verse_slide.shapes.add_textbox(left, top, width, height)
        tf = txBox.text_frame
        p = tf.add_paragraph()
        p.text = v
        p.font.size = Pt(20)

    prs.save("test.pptx")


def slidehw():
    prs = Presentation()
    title_slide_layout = prs.slide_layouts[0]
    slide = prs.slides.add_slide(title_slide_layout)
    title = slide.shapes.title
    subtitle = slide.placeholders[1]

    title.text = "Hello, World"
    subtitle.text = "python-pptx was here!"

    prs.save("test.pptx")


def main():
    test = Hymn("O for a Thousand", "57.txt")
    hymn_slide(test.title, test.verses)


if __name__ == "__main__":
    main()
