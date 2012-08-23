#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# ok lpod 1.0
"""
Basic Accessibility test: check, for every picture in a document, if there is:
- a title (svg_title),
- a description (svg_description)
or, at least, some caption text.
See planes.odt file and result of the script.
"""
import os
# Import from lpod
from lpod.document import odf_get_document

filename = "planes.odt"

# For convenience we use some remote access to the document
#from urllib2 import urlopen
#filename = urlopen("http://arsaperta.org/planes.odt")
doc = odf_get_document(filename)

# We want the images of the document.
body = doc.get_body()
images = body.get_images()

nb_images = len(images)
nb_title = 0
nb_description = 0
nb_caption = 0

for image in images:
    uri = image.get_url()
    filename = uri.split("/")[-1]
    print "Image filename:", filename
    frame = image.get_parent()
    name = frame.get_name()
    title = frame.get_svg_title()
    description = frame.get_svg_description()
    if title:
        nb_title += 1
    if description:
        nb_description += 1
    print "Name: %s, title: %s, description: %s" %(name, title, description)
    link = frame.get_parent()
    if link.get_tag() == u'draw:a':
        caption = link.get_attribute("office:name")
        if caption:
            nb_caption +=1
            print "Caption: %s" % caption
print
print "The document displays %s pictures:" % nb_images
print " - pictures with a title: %s" % nb_title
print " - pictures with a description: %s" % nb_description
print " - pictures with a caption: %s" % nb_caption

expected_result = """
Image filename: 100000000000013B000000D3AAA93FCC.jpg
Name: graphics2, title: Spitfire, general view, description: Green spitfire in a hall, view from left front.
Image filename: 100000000000013B000000D31365BB6C.jpg
Name: graphics3, title: Spitfire, detail, description: None
Image filename: 100000000000013B000000D367502732.jpg
Name: graphics1, title: None, description: None
Caption: Thunderbolt

The document displays 3 pictures:
 - pictures with a title: 2
 - pictures with a description: 1
 - pictures with a caption: 1
"""
