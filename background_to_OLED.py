"""
What: Script for editing any background image to darken colours to true blacks.
      Provides a way to check and adjust backgrounds for OLED panels.
Why:  OLED panel pixels turn off on true blacks, thus images with greater true black percentages reduce power consumption.
How:  Highly optimized with NumPy and usage is from command line only.
"""
import numpy as np
from PIL import Image
import argparse
import utils


def calculate_black_percentage(img, size):
    """
    Summation of number of values less than 0, summed across all rows of the image
    :param img: numpy array of image
    :param size: size of image (l x w)
    :return: percentage of image that is true black
    """
    b = np.sum(np.abs(img).sum(axis=2) == 0)
    return b/size * 100


# Currently unused, useful for checking thresholds
def calculate_thresh_percentage(img, size, th):
    b = np.sum(np.abs(img).sum(axis=2) <= th*3)
    return b/size * 100


def darken(img, th=50, lum=False):
    """
    Darkens all pixels with an average value less than threshold based on mean value of RGB or luminosity
    :param img: numpy array of image
    :param th: threshold for darkening
    :param lum: if darken based on human perceived brightness (luminosity)
    :return: a numpy array of image with all pixels below the threshold set to true black
    """
    if lum:
        img_lum = utils.calculate_luminosity(utils.transform_colour_space(img_arr))
        return np.where(img_lum < th, img, 0)
    return np.where(np.moveaxis(np.array([np.mean(img, axis=2) > th]*3), 0, -1), img, 0)


if __name__ == '__main__':
    # Argument parser
    parser = argparse.ArgumentParser(description='Load Image')
    parser.add_argument('--i', dest="input", required=True, help="image file input path", metavar="FILE")
    parser.add_argument('--o', dest="output", required=True, help="saved darkened image file output path", metavar="FILE")
    parser.add_argument('--th', dest="th", required=True, help="threshold for blacking", type=int)
    args = parser.parse_args()

    # Open input image
    image = Image.open(args.input)
    img_arr = np.array(image)[:, :, :3]
    total = image.height * image.width
    thresh = args.th

    # Calculate true black percentage before and after darkening
    perc = calculate_black_percentage(image, total)
    darkened_arr = darken(img_arr, thresh)
    perc_after = calculate_black_percentage(darkened_arr, total)

    # Display results
    print('black percentage before: ', perc)
    print('black percentage after: ', perc_after)
    darkened = Image.fromarray(darkened_arr)
    darkened.show()

    # Optional save output
    if args.output:
        darkened.save(args.output)



