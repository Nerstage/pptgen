#!/usr/bin/env python3

import collections
import collections.abc
from pptx import Presentation
from pptx.util import Inches, Pt


def slidehw():
    prs = Presentation()
    title_slide_layout = prs.slide_layouts[0]
    slide = prs.slides.add_slide(title_slide_layout)
    title = slide.shapes.title
    subtitle = slide.placeholders[1]

    title.text = "Hello, World"
    subtitle.text = "python-pptx was here!"

    prs.save("text.pptx")


if __name__ == "__main__":
    slidehw()
