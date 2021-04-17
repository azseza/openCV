"""Python script to make a cartoonized photo
@uthor: azseza
Methodology : azseza
1.First, apply a bilateral filter to reduce the color palette of the image.
2.Then, convert the original color image into grayscale.
3.After that, apply a median blur to reduce image noise.
4.Use adaptive thresholding to detect and emphasize the edges in an edge mask.
5.Finally, combine the color image from step 1 with the edge mask from step 4.
"""
import filters
import cv2 as cv
import numpy as np
#Using a bilateral filter :
# A bilateral filter smoothens the flat regions while sharpening the edges.
# We first neet to resize the input image with the helper function resize() 

image = cv.imread('images/trump.png')

def bilateral_filter(image: np.unit8)->np.unit8:
    """Function that applyes a biletarel filter :
    1- Downsample the image using multiple pyrDown calls
    2-apply multiple bilateral filters
    3-upsample it to the original size
    Args:
        image (np.unit8): 

    Returns:
        np.unit8: filtred Image
    """
    #downsamle the image  :: 
    downsamled_image = image
    for _ in range(5):
        downsamled_image = cv.pyrDown(image)
    for _ in range(5):
        global filterd_small_img
        filterd_small_img = cv.bilateralFilter(downsamled_image, 9,
                                            9, 7)
    filtered_normal_img = filterd_small_img
    for _ in range(5):
        filtered_normal_img = cv.pyrUp(filtered_normal_img)
    return filtered_normal_img

#Detecting and emphasizing permanent edges


