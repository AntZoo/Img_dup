#!/usr/bin/env python
# coding: utf-8

from PIL import Image as pImage
import numpy

import os
import sys


class Image:
    """Take an information from image file"""

    BLOCK_SIZE = 20
    TRESHOLD = 20

    def __init__(self, filename):
        self.filename = filename
        img = pImage.open(self.filename)
        small = img.resize((Image.BLOCK_SIZE, Image.BLOCK_SIZE),
                            pImage.BILINEAR)
        self.t_data = numpy.array(
            [sum(list(x)) / 3 for x in small.getdata()]
        )
        del img, small

    def __repr__(self):
        return self.filename

    def __mul__(self, other):
        return sum(1 for x in self.t_data - other.t_data if abs(x) > Image.TRESHOLD)


class ImageList:
    """List of images information, built from directory.
    All files must be *.jpg"""
    def __init__(self, blackdir, colordir):
        self.blackdir = blackdir
        self.colordir = colordir
        self.blackimages = \
            [Image(os.path.join(self.blackdir, filename)) \
                for filename in os.listdir(self.blackdir)
                    if filename.endswith('.jpg')]
        self.colorimages = \
            [Image(os.path.join(self.colordir, filename)) \
                for filename in os.listdir(self.colordir)
                    if filename.endswith('.jpg')]

    def __repr__(self):
        return ('\n'.join((x.filename for x in self.simages)) + '\n'.join((x.filename for x in self.cimages)))

    def html(self):
        res = ['<html><body>']
        for img in self.blackimages:
            res += ['<img src="' + os.path.abspath(img.filename) + '" width="200"/>' + \
                str(os.path.basename(img.filename))]
            distances = sorted([(img * x, x) for x in self.colorimages])
            res += [
                '<img src="' + os.path.abspath(x.filename) + '" width="200"/>' + \
                str(os.path.basename(x.filename)) + ' <i>|' + str(dist) + '|</i>'
                for dist, x in distances if dist < 220]
            res += ['<hr/>']
        res += ['</body></html>']

        return '\n'.join(res)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("The script is run as such:")
        print("         python img.py originals_directory dir_to_compare")
        print("For example:")
        print("         python img.py /Users/anton/cb /Users/anton/rgb")
    else:
        il = ImageList(sys.argv[1], sys.argv[2])
        print(il.html())
