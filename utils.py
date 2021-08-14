from PIL import ImageCms
import io
import numpy as np


def transform_colour_space(im):
    """
    Gets colour space of image and converts it to sRGB
    :param im: PIL image
    :return: PIL image converted to sRGB colour space
    """
    profile = im.info.get('icc_profile')
    if profile != 'sRGB':
        io_handle = io.BytesIO(profile)
        src = ImageCms.ImageCmsProfile(io_handle)
        srgb = ImageCms.createProfile('sRGB')
        img = ImageCms.profileToProfile(im, src, srgb)
        return img
    return im


def calculate_luminosity(img_arr):
    """
    Luminosity function: converts from sRGB to RGB then applies luminosity function
    in a vectorized implementation
    :param img_arr: NumPy image array in sRGB colour space
    :return: luminosity image matrix
    """
    # Normalize values
    img_arr /= 255
    # sRGB to RGB (linear)
    img_arr[img_arr <= 0.0404499] /= 12.92
    img_arr[img_arr > 0.0404499] = np.exp((img_arr[img_arr > 0.0404499] + 0.055) / (1 + 0.055), 2.4)
    # Clipping
    img_arr[img_arr > 1] = 1
    # RGB luminosity function
    weights = np.array([0.2126, 0.7152, 0.0722])
    luminosity = np.tensordot(img_arr, weights, axes=[2, 0])
    return luminosity


