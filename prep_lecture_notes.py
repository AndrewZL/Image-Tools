import cv2
import numpy as np
from pdf2image import convert_from_path
import argparse


def pdf_to_images(document, dpi):
    """
    Converts a pdf to a list of images in BGR matrix format (OpenCV)
    :param document: pdf filepath (String)
    :param dpi: resolution (int)
    :return: list of images in BGR matrix format
    """
    image_list = []
    image_list.extend(list(map(
                lambda image: cv2.cvtColor(np.asarray(image), code=cv2.COLOR_RGB2BGR),
                convert_from_path(document, dpi=dpi),
            )))
    return image_list


def transparency_mask(image, col, invert=False):
    """
    Creates an alpha channel for the image and sets all pixels under a colour threshold to transparent
    :param image: image in 3-channel BGR matrix format (OpenCV)
    :param col: colour threshold
    :param invert: invert image or not
    :return: image in 4-channel BGRA matrix with transparent background
    """
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
    """
    Inverts all the colours in the image
    :param image: 3-channel BGR image in matrix format (OpenCV)
    :return: 3-channel BGR image in matrix format with inverted colours
    """
    return cv2.bitwise_not(image)


def invert_bw(image):
    """
    Inverts only the blacks and whites in the image
    :param image: 3-channel BGR image in matrix format (OpenCV)
    :return: 3-channel BGR image in matrix format with inverted blacks and whites
    """
    b_mask = np.all(image <= [25, 25, 25])
    w_mask = np.all(image >= [230, 230, 230])
    image[b_mask], image[w_mask] = image[w_mask], image[b_mask]
    return image


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Load Image')
    parser.add_argument('--fp', dest="fp", help="filepath (pdf)")
    parser.add_argument('--out', dest="out", help="output folder path")
    parser.add_argument('-i', dest="invert", help="invert image colours?")
    parser.add_argument('-ibw', dest="invertbw", help="invert black/white and keep other colours equal")
    args = parser.parse_args()

    images = pdf_to_images(args.fp, 300)

    k = 0
    for i in images:
        if args.invert:
            im = invert_image(i)
            im = transparency_mask(im, [25, 25, 25], True)
        elif args.invertbw:
            im = invert_bw(i)
            im = transparency_mask(im, [25, 25, 25], True)
        else:
            im = transparency_mask(i, [230, 230, 230])
        cv2.imwrite(args.out + '/im_{:04}.png'.format(k), im)
        k += 1





