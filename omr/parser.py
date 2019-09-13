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

SQUARE_TOLERANCE = 0.2
PLACE_TOLERANCE = 5
DIV_TOLERANCE = 0.1
A4_SCALE = 1.41

def has_square_parent(hierarchy, squares, parent):
    if hierarchy[parent][3] == -1:
        return False
    if hierarchy[parent][3] in squares:
        return True
    return has_square_parent(hierarchy, squares, hierarchy[parent][3])

def count_children(hierarchy, parent, inner=False):
    if parent == -1:
        return 0
    elif not inner:
        return count_children(hierarchy, hierarchy[parent][2], True)
    return 1 + count_children(hierarchy, hierarchy[parent][0], True) + count_children(hierarchy, hierarchy[parent][2], True)

def get_angle(p1, p2):
    x_diff = p2[0] - p1[0]
    y_diff = p2[1] - p1[1]
    return math.degrees(math.atan2(y_diff, x_diff))

def prepare_image_create(f):
    img = cv2.imread(f)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, img_th = cv2.threshold(img_gray, 127, 255, 0)
    i_cont, i_hier = cv2.findContours(img_th, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    height, width = img.shape[:2]

    # Get corner squares
    squares = []
    square_indices = []
    square_midX = []
    square_midY = []
    black = 0
    i = 0
    j = 0
    for c in i_cont:
        peri = cv2.arcLength(c, True)
        area = cv2.contourArea(c)
        approx = cv2.approxPolyDP(c, 0.03* peri, True)
        if len(approx)==4:
            if width*height*(500/2180952)<area<width*height*(10000/2180952):
                approx_area = math.fabs((peri/4) ** 2)
                if 1-SQUARE_TOLERANCE<approx_area/area<SQUARE_TOLERANCE+1 and has_square_parent(i_hier[0], square_indices, i) is False:

                    # Check if right lower corner
                    if count_children(i_hier[0], i) < 2:
                        black = j
                        #cv2.drawContours(img, [c], 0, (255, 0, 0), 8)
                    #else:
                        #cv2.drawContours(img, [c], 0, (0, 0, 255), 8)

                    squares.append(approx)
                    square_indices.append(i)

                    j += 1

                    # Find center
                    M = cv2.moments(c)
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])
                    square_midX.append(cX)
                    square_midY.append(cY)
                    #cv2.circle(img, (cX, cY), 10, (0, 255, 255), -1)
        i += 1

    if j!=4:
        print("Found more or less than 4 corners: " + str(j))

    # Right bottom corner
    sq1 = np.array([square_midX[black], square_midY[black]])
    i_sq1 = black

    # Find smallest biggest and mid
    i_max = 0
    max = 0
    i_min = 0
    min = 0
    i_mid = 0
    for i in range(0,4):
        if i==i_sq1:
            continue
        p = np.array([square_midX[i], square_midY[i]])
        dist = np.linalg.norm(sq1-p)
        if dist>max:
            max = dist
            i_max = i
        if dist<min or min==0:
            min = dist
            i_min = i

    for i in range(0, 4):
        if i!=i_max and i!=i_min and i!=i_sq1:
            i_mid = i
            break

    i_sq2 = i_max
    i_sq3 = i_min
    i_sq4 = i_mid

    sq2 = np.array([square_midX[i_sq2], square_midY[i_sq2]])
    sq3 = np.array([square_midX[i_sq3], square_midY[i_sq3]])
    sq4 = np.array([square_midX[i_sq4], square_midY[i_sq4]])

    # Write numbers on image
    #font                   = cv2.FONT_HERSHEY_SIMPLEX
    #fontScale              = 5
    #fontColor              = (0,255,0)
    #lineType               = 10
    #cv2.putText(img,'1', (sq1[0], sq1[1]), font, fontScale, fontColor, lineType)
    #cv2.putText(img,'2', (sq2[0], sq2[1]), font, fontScale, fontColor, lineType)
    #cv2.putText(img,'3', (sq3[0], sq3[1]), font, fontScale, fontColor, lineType)
    #cv2.putText(img,'4', (sq4[0], sq4[1]), font, fontScale, fontColor, lineType)

    src = np.array([
        sq2,
        sq4,
        sq1,
        sq3], dtype="float32")
    w = width
    h = height
    if w>h:
        w=int(h/A4_SCALE)
    else:
        h=int(w*A4_SCALE)
    dst = np.array([
        [0, 0],
        [w, 0],
        [w, h],
        [0, h]], dtype = "float32")

    transform = cv2.getPerspectiveTransform(src, dst)
    img = cv2.warpPerspective(img, transform, (width, height))
    img = img[0:h, 0:w]
    img_gray = cv2.warpPerspective(img_gray, transform, (width, height))
    img_gray = img_gray[0:h, 0:w]
    return transform, img, img_gray

def prepare_image(f, debug):
    img = cv2.imread(f)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, img_th = cv2.threshold(img_gray, 127, 255, 0)
    i_cont, i_hier = cv2.findContours(img_th, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    height, width = img.shape[:2]

    # Get corner squares
    squares = []
    square_indices = []
    square_midX = []
    square_midY = []
    black = 0
    i = 0
    j = 0
    for c in i_cont:
        peri = cv2.arcLength(c, True)
        area = cv2.contourArea(c)
        approx = cv2.approxPolyDP(c, 0.03* peri, True)
        if len(approx)==4:
            if width*height*(500/2180952)<area<width*height*(10000/2180952):
                approx_area = math.fabs((peri/4) ** 2)
                if 1-SQUARE_TOLERANCE<approx_area/area<SQUARE_TOLERANCE+1 and has_square_parent(i_hier[0], square_indices, i) is False:

                    # Check if right lower corner
                    if count_children(i_hier[0], i) < 2:
                        black = j
                        cv2.drawContours(img, [c], 0, (255, 0, 0), 8)
                    else:
                        cv2.drawContours(img, [c], 0, (0, 0, 255), 8)

                    squares.append(approx)
                    square_indices.append(i)

                    j += 1

                    # Find center
                    M = cv2.moments(c)
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])
                    square_midX.append(cX)
                    square_midY.append(cY)
                    cv2.circle(img, (cX, cY), 10, (0, 255, 255), -1)
                else:
                    cv2.drawContours(img, [c], 0, (0, 255, 0), 4)
        i += 1

    if debug:
        cv2.imwrite('conrners.jpg', img)

    if j!=4:
        print("Found more or less than 4 corners: " + str(j))

    # Right bottom corner
    sq1 = np.array([square_midX[black], square_midY[black]])
    i_sq1 = black

    # Find smallest biggest and mid
    i_max = 0
    max = 0
    i_min = 0
    min = 0
    i_mid = 0
    for i in range(0,4):
        if i==i_sq1:
            continue
        p = np.array([square_midX[i], square_midY[i]])
        dist = np.linalg.norm(sq1-p)
        if dist>max:
            max = dist
            i_max = i
        if dist<min or min==0:
            min = dist
            i_min = i

    for i in range(0, 4):
        if i!=i_max and i!=i_min and i!=i_sq1:
            i_mid = i
            break

    i_sq2 = i_max
    i_sq3 = i_min
    i_sq4 = i_mid

    sq2 = np.array([square_midX[i_sq2], square_midY[i_sq2]])
    sq3 = np.array([square_midX[i_sq3], square_midY[i_sq3]])
    sq4 = np.array([square_midX[i_sq4], square_midY[i_sq4]])

    # Write numbers on image
    font                   = cv2.FONT_HERSHEY_SIMPLEX
    fontScale              = 5
    fontColor              = (0,255,0)
    lineType               = 10
    cv2.putText(img,'1', (sq1[0], sq1[1]), font, fontScale, fontColor, lineType)
    cv2.putText(img,'2', (sq2[0], sq2[1]), font, fontScale, fontColor, lineType)
    cv2.putText(img,'3', (sq3[0], sq3[1]), font, fontScale, fontColor, lineType)
    cv2.putText(img,'4', (sq4[0], sq4[1]), font, fontScale, fontColor, lineType)

    src = np.array([
        sq2,
        sq4,
        sq1,
        sq3], dtype="float32")
    w = width
    h = height
    if w>h:
        w=int(h/A4_SCALE)
    else:
        h=int(w*A4_SCALE)
    dst = np.array([
        [0, 0],
        [w, 0],
        [w, h],
        [0, h]], dtype = "float32")

    if debug:
        cv2.imwrite('temp.jpg', img)

    transform = cv2.getPerspectiveTransform(src, dst)
    img = cv2.warpPerspective(img, transform, (width, height))
    img = img[0:h, 0:w]
    img_gray = cv2.warpPerspective(img_gray, transform, (width, height))
    img_gray = img_gray[0:h, 0:w]
    return img, img_gray

