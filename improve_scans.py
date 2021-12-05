import numpy as np
import pdf2image
import cv2
import matplotlib.pyplot as plt
from tqdm import tqdm

images = pdf2image.convert_from_path('CTCI.pdf', dpi=300)

new_images = []
length = len(images)
tq = tqdm(total=length)
for im in images:
    new_images.append(cv2.cvtColor(np.asarray(im), code=cv2.COLOR_RGB2GRAY))
    tq.update(1)


def good_contour(cc):
    x, y, w, h = cv2.boundingRect(cc)
    if w < 10 or h < 10:
        return False
    if w > 2000:
        return False
    return True


k = 0
length = len(new_images)
tq = tqdm(total=length)
for i in new_images[10:-12]:
    plt.clf()
    tq.update(1)
    ret, thresh = cv2.threshold(i, 170, 255, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(thresh, 1, 2)
    ih, iw = i.shape[:2]
    size = ih * iw
    contours = [cont for cont in contours if good_contour(cont)]
    min_x = iw
    min_y = ih
    max_x = 0
    max_y = 0
    for cc in contours:
        x, y, w, h = cv2.boundingRect(cc)
        if x < min_x:
            min_x = x
        if y < min_y:
            min_y = y
        if x + w > max_x:
            max_x = x + w
        if y + h > max_y:
            max_y = y + h
    cropped = i[min_y:max_y, min_x:max_x]
    plt.imshow(cropped)
    cv2.imwrite('images/page{}.jpg'.format(k), cropped)
    k += 1
