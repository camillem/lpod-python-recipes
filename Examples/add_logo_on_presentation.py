#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Insert an image (e.g. the logo of an event, organization or a Creative Commons
attribution) with size x,y at position x2,y2 on a number of slides in a
presentation slide deck.

Exemple:

./add_logo_on_presentation.py -i newlogo.png -r 1-8 -s 4.00 presentation_logo.odp

"""

import sys
import os
from optparse import OptionParser

# Import from lpod
from lpod.document import odf_get_document
from lpod.frame import odf_create_image_frame

# Readng image size requires a graphic library
# The standard PIL lib may have different modules names on different OS
try:
    from PIL import Image
    PIL_ok = True
except:
    PIL_ok = False
    print "No image size detection. You should install Python Imaging Library"

modified_file_suffix = "new"
pos_x = "1.50cm"
pos_y = "1.50cm"
title = "New Logo"
text = "The new logo with blue background"

def make_image_size(path, size):
    try:
        w, h = Image.open(path).size
    except IOError:
        print "error reading", path
        return None

    ratio = max( w / size, h / size)
    display_w = "%.2fcm" % (w / ratio)
    display_h = "%.2fcm" % (h / ratio)
    return display_w, display_h

if  __name__ == '__main__':
    usage = "usage: %prog -i IMAGE -r RANGE -s SIZE PRESENTATION"
    description = "Add an image on some pages of a presentation."
    parser = OptionParser(usage, description=description)
    parser.add_option("-i", "--image", dest="image", help="Image to be added",
                      action="store", type="string")
    parser.add_option("-r", "--range", dest="range", help="Range of the slides",
                      action="store", type="string")
    parser.add_option("-s", "--size", dest="size", help="max width in cm of the image",
                      action="store", type="float")

    options, source = parser.parse_args()
    if not source or not options.image or not options.range or not options.size:
        print "need options !"
        parser.print_help()
        exit(0)

    lst = options.range.split('-')
    start = int(lst[0]) - 1
    end = int(lst[1]) - 1

    file_name = source[0]

    presentation = odf_get_document(file_name)
    presentation_body = presentation.get_body()

    uri = presentation.add_file(options.image)

    width, height = make_image_size(options.image, float(options.size))

    # Create a frame for the image
    image_frame = odf_create_image_frame(
            url = uri,
            name = file_name,
            text = "",                # Text over the image object
            size = (width, height),   # Display size of image
            anchor_type = 'page',
            page_number = None,
            position = (pos_x, pos_y),
            style = None
            )
    image_frame.set_svg_title(title)
    image_frame.set_svg_description(text)

    # Append all the component
    i = start
    while True:
        slide = presentation_body.get_draw_page(position = i)
        # Create a frame for the image
        image_frame = odf_create_image_frame(
            url = uri,
            name = file_name,
            text = "",                # Text over the image object
            size = (width, height),   # Display size of image
            anchor_type = 'page',
            page_number = None,
            position = (pos_x, pos_y),
            style = None
            )
        image_frame.set_svg_title(title)
        image_frame.set_svg_description(text)

        slide.append(image_frame)
        i += 1
        if i > end:
            break

    # Finally save the result
    lst = file_name.split(".")
    lst.insert(-1, modified_file_suffix)
    new_name = '.'.join(lst)

    presentation.save(new_name)

