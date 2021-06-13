"""
Python Script to handle parking init when an image is 
given 
"""
from coordinates_generator import CoordinatesGenerator
from colors import *
import argparse

def main():
    args = prase_args()
    
    image = args.image

    print("image is good")
    with open('test.yaml', "w+") as file:
        header="---\n"
        file.write(header)
        genrator = CoordinatesGenerator(image, file, COLOR_RED)
        genrator.generate()

def prase_args():
    praser = argparse.ArgumentParser(description="argument Praser")
    praser.add_argument("--image", dest="image",required=True)
    return praser.parse_args()


if __name__ =="__main__":
    main()

