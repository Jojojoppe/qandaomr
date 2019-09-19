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
import math
import argparse
import zxing
from os import remove

from .parser import *

def read(fi, debug):
    fo = 'out.jpg'

    # Load image and create thresholded image img_th
    img, img_gray = prepare_image(fi, debug)
    height, width = img.shape[:2]

    # Read barcodes from bottom
    bc1 = img_gray[int(height*0.92):height, int(1*width/3):int(width/2)]
    bc2 = img_gray[int(height*0.92):height, int(width/2):int(2*width/3)]
    cv2.imwrite('bc1.png', bc1)
    cv2.imwrite('bc2.png', bc2)

    reader = zxing.BarCodeReader()
    res1 = reader.decode('bc1.png').raw
    res2 = reader.decode('bc2.png').raw
    b1 = res1.split(';')
    b2 = res2.split(';')

    if debug==False:
        remove('bc1.png')
        remove('bc2.png')

    # Barcode 1 data
    b1_ver = int(b1[0])
    # Version must be 1
    if b1_ver!=1:
        exit(-1)
    b1_col = int(b1[1])
    b1_row = int(b1[2])
    b1_block_col = int(b1[3])
    b1_block_row = int(b1[4])
    b1_startx = float(b1[5])/100    # Start of first block
    b1_starty = float(b1[6])/100
    b1_pady = float(b1[7])/100      # Space between blocks
    b1_padx = float(b1[8])/100

    b2_sizex = float(b2[0])/100     # Size of bullet
    b2_sizey = float(b2[1])/100
    b2_padx = float(b2[2])/100      # Space between bullets
    b2_pady = float(b2[3])/100

    mask = np.zeros(img.shape[:2], np.uint8)
    for col in range(0, b1_col):
        py = int(b1_startx*width + b1_pady*width*col)
        sy = int(b2_padx*b1_block_col*width)
        for row in range(0, b1_row):
            px = int(b1_starty*height + b1_padx*height*row)
            sx = int(b2_pady*b1_block_row*height)

            cv2.rectangle(img, (py, px), (py+sy, px+sx), (0, 0, 255), 3)

            for block_row in range(0, b1_block_row):
                bpx = px + int(b2_pady*height*block_row)
                sbx = int(b2_sizey*height)
                sby = int(b2_sizex*width)

                colors = [0] * b1_block_col
                for block_col in range(0, b1_block_col):
                    bpy = py + int(b2_padx*width*block_col)

                    cv2.rectangle(img, (bpy, bpx), (bpy+sby, bpx+sbx), (180, 180, 0), 2)
                    cv2.rectangle(mask, (bpy, bpx), (bpy+sby, bpx+sbx), (255, 255, 255), -1)
                    colors[block_col] = cv2.mean(img_gray, mask)[0]
                    cv2.rectangle(mask, (bpy, bpx), (bpy+sby, bpx+sbx), (0, 0, 0), -1)

                ans = np.argmin(colors)
                bpy = py + int(b2_padx*width*ans)
                cv2.rectangle(img, (bpy, bpx), (bpy+sby, bpx+sbx), (255, 0, 255), 4)
                print(ans, end=',')

    print("")
    if debug:
        cv2.imwrite(fo, img)

