import cv2
import numpy as np
from pdf2image import convert_from_path
import argparse


def pdf_to_images(document, dpi):
    image_list = []
    image_list.extend(
        list(
            map(
                lambda image: cv2.cvtColor(np.asarray(image), code=cv2.COLOR_RGB2BGR),
                convert_from_path(document, dpi=dpi),
            )
        )
    )
    return image_list


def transparency_mask(image, col, invert=False):
    h, w, c = image.shape
    image_bgra = np.concatenate([image, np.full((h, w, 1), 255, dtype=np.uint8)], axis=-1)
    if invert:
        print(col)
        print(image)
        col_mask = np.all(image <= col, axis=-1)
    else:
        col_mask = np.all(image >= col, axis=-1)
    image_bgra[col_mask, -1] = 0
    return image_bgra


def invert_image(image):
    return cv2.bitwise_not(image)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Load Image')
    parser.add_argument('--fp', dest="fp", help="filepath (pdf)")
    parser.add_argument('--i', dest="invert", help="invert image colours?")
    args = parser.parse_args()
    images = pdf_to_images(args.fp, 300)
    k = 0
    print(args.invert)
    for i in images:
        if args.invert:
            im = invert_image(i)
            im = transparency_mask(im, [25, 25, 25], True)
        else:
            im = transparency_mask(i, [230, 230, 230])
        cv2.imwrite('im_{:04}.png'.format(k), im)
        k += 1





