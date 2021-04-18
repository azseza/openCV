"""Python script to make a cartoonized photo
@uthor: azseza
Methodology : azseza
1.First, apply a bilateral filter to reduce the color palette of the image.
2.Then, convert the original color image into grayscale.
3.After that, apply a median blur to reduce image noise.
4.Use adaptive thresholding to detect and emphasize the edges in an edge mask.
5.Finally, combine the color image from step 1 with the edge mask from step 4.
"""

import cv2 as cv
import numpy as np

#Using a bilateral filter :
# A bilateral filter smoothens the flat regions while sharpening the edges.
# We first neet to resize the input image with the helper function resize() 

image = cv.imread('images/trump.png')

def bilateral_filter(image: np.uint8, num_bilaterals:int=5, num_pyrups:int=5)->np.uint8:
    """Function that applyes a biletarel filter :
    1- Downsample the image using multiple pyrDown calls
    2-apply multiple bilateral filters
    3-upsample it to the original size
    Args:
        image (np.unit8): 

    Returns:
        np.unit8: filtred Image
    """
    #downsample the image  :: 
    downsamled_image = image
    for _ in range(num_pyrups):
        downsamled_image = cv.pyrDown(image)
    for _ in range(num_bilaterals):
        global filterd_small_img
        filterd_small_img = cv.bilateralFilter(downsamled_image, 9,
                                            9, 7)
    filtered_normal_img = filterd_small_img
    for _ in range(num_pyrups):
        filtered_normal_img = cv.pyrUp(filtered_normal_img)
    return filtered_normal_img

#Detecting and emphasizing permanent edges
def emphasize_edges(image : np.uint8) -> np.uint8 : 
    """Function that detectes and emphesizes edges
    """
    #We first reduce the noise of the image with a median blur
    img_grey = cv.cvtColor(image, cv.COLOR_RGB2GRAY)
    img_blur = cv.medianBlur(img_grey, 7)
    #And then we apply threshhold 
    grey_edges = cv.threshold(img_blur, 255, 
                            cv.ADAPTIVE_THRESH_MEAN_C, 
                            cv.THRESH_BINARY, 9)
    return grey_edges

def cartoonize(image: np.uint8)->np.uint8:
    """function to cartoonize an image that combines
    the eges emphesizes and the biliateral filters
    * the number of pyrUps is 5 
    * the number of bilaterals is 5
    as sited in the function definition
    Args:
        image (np.unit8): input image

    Returns:
        np.unit8: [description]
    """
    #Reducing the color palette of the input image
    reduced_img = bilateral_filter(image)
    #making sure the downsampled image has the same dims as the input image
    try:
        assert reduced_img.shape == image.shape
    except  AssertionError:
        reduced_img = cv.resize(reduced_img, image.shape[:2])
    #converting to grayscale, and bluring the image 
    grey_edges = emphasize_edges(image)
    #combine downscaled image with grey edges 
    rbg_edges = cv.cvtColor(grey_edges, cv.COLOR_GRAY2RGB)
    outputs = cv.bitwise_and(reduced_img, rbg_edges)
    return outputs

#testing 
in_img = cv.imread('images/trump.png')
out_img = cartoonize(in_img)
cv.imshow('original', in_img)
cv.imshow('cartooned', out_img)
cv.waitKey(0)
