# OMR - Optical mark regognition
# Copyright (C) 2019 Joppe Blondel
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import cv2
import numpy as np
import argparse
import urllib.request
from os import remove

from .parser import *

def create(fi, fo, col, row, bcol, brow, debug):

    transform, doc, _ = prepare_image_create(fi)
    if debug:
        cv2.imwrite('transformed.png', doc)
    height, width = doc.shape[:2]

    # Create red and green only masks
    (B, G, R) = cv2.split(doc)
    start = R-B
    end = G-B
    doc = cv2.merge([R+G-B, R+G-B, R+G-B])

    # Delete green and red squares for output
    (B, G, R) = cv2.split(cv2.imread(fi))
    out = cv2.merge([R+G-B, R+G-B, R+G-B])

    # Find coords of start and end squares
    start_c, start_h = cv2.findContours(start, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    end_c, end_h = cv2.findContours(end, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    block_start = []
    block_end = []

    # GIVEN
    b1 = [""]*9
    b1_ver = 1
    b1_col = col
    b1_row = row
    b1_block_col = bcol
    b1_block_row = brow
    b1_startx = 0.0
    b1_starty = 0.0
    b1_padx = 0.0
    b1_pady = 0.0

    b2 = [""]*4
    b2_sizex = 0.0
    b2_sizey = 0.0
    b2_padx = 0.0
    b2_pady = 0.0

    for i in range(0, len(start_c)):
        # If there is no parent
        if start_h[0][i][3]==-1:
            block_start.append(i)
            block_end.append(i)

            p_s = cv2.arcLength(start_c[i], True)
            a_s = cv2.approxPolyDP(start_c[i], 0.03* p_s, True)
            p_e = cv2.arcLength(end_c[i], True)
            a_e = cv2.approxPolyDP(end_c[i], 0.03* p_s, True)

            # Must be rectangles
            if len(a_s)!=4 or len(a_e)!=4:
                exit()

            # Find bullet size if not yet found
            if b2_sizex==0 or b2_sizey==0:
                c1 = a_s[0][0]
                c2 = a_s[2][0]
                c3 = a_s[1][0]
                b2_sizey = (float(np.linalg.norm(c1-c3))/height)*100
                b2_sizex = (float(np.linalg.norm(c2-c3))/width)*100

            # Find space between bullets if not yet found
            if b2_padx==0 or b2_pady==0:
                # TODO not neat
                b2_padx = (float(a_e[0][0][0]+3 - a_s[0][0][0])/(width*(b1_block_col-1)))*100
                b2_pady = (float(a_e[0][0][1]+1 - a_s[0][0][1])/(height*(b1_block_row-1)))*100

            cv2.drawContours(doc, [start_c[i]], 0, (0, 0, 255), 4)
            cv2.drawContours(doc, [end_c[i]], 0, (0, 255, 0), 4)

            sx = start_c[i][0][0][0]
            sy = start_c[i][0][0][1]
            ex = end_c[i][0][0][0]
            ey = end_c[i][0][0][1]
            cv2.putText(doc, str(i), (sx, sy), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), 5)
            cv2.putText(doc, str(i), (ex, ey), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 5)

    # calculate start position
    bstart = block_start[-1:][0]
    p_b = cv2.arcLength(start_c[bstart], True)
    a_b = cv2.approxPolyDP(start_c[bstart], 0.03* p_s, True)
    startx = a_b[0][0][0]
    starty = a_b[0][0][1]
    b1_startx = (float(startx)/width)*100
    b1_starty = (float(starty)/height)*100

    bnext = block_start[-2:][0]
    p_b = cv2.arcLength(start_c[bnext], True)
    a_b = cv2.approxPolyDP(start_c[bnext], 0.03* p_s, True)
    nextx = a_b[0][0][0]
    nexty = a_b[0][0][1]

    bdown = block_start[-1*b1_col-1:][0]
    p_b = cv2.arcLength(start_c[bdown], True)
    a_b = cv2.approxPolyDP(start_c[bdown], 0.03* p_s, True)
    downx = a_b[0][0][0]
    downy = a_b[0][0][1]

    b1_pady = ((downy - starty)/height)*100
    b1_padx = ((nextx - startx)/width)*100

    b1[0] = str(b1_ver)
    b1[1] = str(b1_col)
    b1[2] = str(b1_row)
    b1[3] = str(b1_block_col)
    b1[4] = str(b1_block_row)
    b1[5] = "{:10.3f}".format(b1_startx)
    b1[6] = "{:10.3f}".format(b1_starty)
    b1[7] = "{:10.3f}".format(b1_padx)
    b1[8] = "{:10.3f}".format(b1_pady)

    b2[0] = "{:10.3f}".format(b2_sizex)
    b2[1] = "{:10.3f}".format(b2_sizey)
    b2[2] = "{:10.3f}".format(b2_padx)
    b2[3] = "{:10.3f}".format(b2_pady)

    bc1 = ';'.join(b1).replace(" ", "")
    bc2 = ';'.join(b2).replace(" ", "")

    if debug:
        cv2.imwrite('doc.png', doc)

    # Create barcodes
    bc1 = bc1.replace(';','%3B')
    bc2 = bc2.replace(';','%3B')

    urllib.request.urlretrieve('http://datamatrix.kaywa.com/img.php?s=6&d=' + bc1, 'bc1.png')
    urllib.request.urlretrieve('http://datamatrix.kaywa.com/img.php?s=6&d=' + bc2, 'bc2.png')
    bc1 = cv2.imread('bc1.png')
    bc1_height, bc1_width = bc1.shape[:2]
    bc2 = cv2.imread('bc2.png')
    bc2_height, bc2_width = bc2.shape[:2]

    if debug==False:
        remove('bc1.png')
        remove('bc2.png')

    # Copy new barcodes over old ones
    oheight, owidth = out.shape[:2]
    codes = np.zeros((height, width, 3), dtype="uint8")

    h = int(0.045*height)
    w = int(h)
    sy = int(0.941*height)
    sx = int(0.396*width)
    # copy bc1 to here
    bc1 = cv2.resize(bc1, (h, w), interpolation = cv2.INTER_AREA)
    codes[sy:sy+h, sx:sx+h] = 255-bc1

    sx = int((1-0.396-0.045)*width)
    # copy bc2 to here
    bc2 = cv2.resize(bc2, (h, w), interpolation = cv2.INTER_AREA)
    codes[sy:sy+h, sx:sx+h] = 255-bc2

    invtransform = np.linalg.inv(transform)
    codes = cv2.warpPerspective(codes, invtransform, (owidth, oheight))

    cv2.imwrite(fo, cv2.bitwise_and(out, 255-codes))
