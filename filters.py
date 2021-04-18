"""
An app to apply three different image filter effects to the video stream
of a webcam in real-time.
The three effects are:
- Warming/cooling filters
- Black-and-white pencil sketch
- Cartoonizer
"""
import cv2 as cv 
import numpy as np
import time
"""
the slow dodge effect hardcoded !  
 def slow_dodge_effect(image : np.uint8, mask: np.uint8) -> np.uint8:
     """"""
     classic implementation of dodge effect
     Input : 
     image (np.mtarix): inout image
     mask (np.matrix): mask to apply in the input image 
     Returns :
     dodged image 
     Returns :
     np.matrix : dodged image 
     """"""
     height = image.shape[0]   
     width = image.shape[1]
     blend = np.zeros((width, height), np.uint8)
     for c in range(width):
         for r in range(height):
             #shifting image pixels by 8 bits, and dividing  
             #by the inverse of the mask
             result = (image[c, r] << 8 ) / (255-mask[c, r])
             #making sure it stays within the bounds
             blend[c, r] = min(255, result)
     return result

tic = time.time()
slowDodged = slow_dodge_effect('image',22)
toc = time.time()
slowdodTime= toc-tic
ratio = (slowdodTime/fastdodTime )* 100
print(f"the classic method is {0} % faster ", ratio)
"""


#Optimized dodge effect
def dodge_effect(image, mask):
    """
    better implimentation of dodge effect
    Args:
        image (np.matrix)): input image
        mask (np.matrix): mask to apply in input image
    """
    return cv.divide(image, 255 - mask, scale=256)


#Pencil Scale Transformation : 
def pencil_scale_transform(image : np.uint8)->np.uint8:
    """
    fucntion taht aplyes pencil scale transformation

    Args:
        image (np.uint8): input image

    Returns:
        np.uint8: output image
    """
    img_gray = cv.cvtColor(image, cv.COLOR_RGB2GRAY)
    invert_img = 255 - img_gray
    blurred_image = cv.GaussianBlur(invert_img, (21, 21), 0, 0)
    grey_sketch = cv.divide(img_gray, 255-blurred_image, scale=256)
    return grey_sketch

def pencil_sketch_on_canvas(rgb_image: np.uint8, canvas:int=None)->np.uint8 :
    """Pencil sketch with canvas option to prettify the output image

    Args:
        rgb_image (np.unit8): 
        canvas (int, optional): [description]. Defaults to None.

    Returns:
        numpy.unit8
    """
    gray_image = cv.cvtColor(rgb_image, cv.COLOR_RGB2GRAY)
    blurred_image = cv.GaussianBlur(gray_image, (21, 21), 0, 0)
    gray_sketch = cv.divide(gray_image, blurred_image, scale=256)
    if canvas is not None:
        gray_sketch = cv.multiply(gray_sketch, canvas, scale=1 / 256)
    return cv.cvtColor(gray_sketch, cv.COLOR_GRAY2RGB)

def apply_rgb_filters(rgb_image, *,
                      red_filter=None, green_filter=None, blue_filter=None):
    """Python function to apply an rgb filter

    Args:
        rgb_image (np.unit8): InputImage
        red_filter (str, optional): choose the filter color. Defaults to None.
        green_filter (str, optional): choose the filter color. Defaults to None.
        blue_filter (str, optional): choose the filter color. Defaults to None.

    Returns:
        np.unit8: Rgb filtred image
    """
    #Splitiing the color channeles in three variables
    c_r, c_g, c_b = cv.split(rgb_image)
    #Increasing the desired color channel
    if red_filter is not None:
        c_r = cv.LUT(c_r, red_filter).astype(np.uint8)
    if green_filter is not None:
        c_g = cv.LUT(c_g, green_filter).astype(np.uint8)
    if blue_filter is not None:
        c_b = cv.LUT(c_b, blue_filter).astype(np.uint8)
    return cv.merge((c_r, c_g, c_b))

def downscale_img(image : np.uint8, scale:float=0.5)->np.uint8:
    """a python function to downscale an image

    Args:
        image (np.unit8): image to downscale
        scale (float, optional): 2*the scale of resizing. Defaults to 0.5.

    Returns:
        np.unit8: downscaled image
    """
    return cv.resize(image, (0, 0), fx=scale, fy=scale)

# def upscale_img(img : np.unit8, scale:int=4)->np.unit8:
#      """a python function to Upscale an image
#     Args:
#         image (np.unit8): image to upscame
#         scale (int, optional): 2*the scale of resizing. Defaults to 4 .
#     Returns:
#         np.unit8: upscaled image
#     """
#     return cv.pyrUp(img, dst=scale)