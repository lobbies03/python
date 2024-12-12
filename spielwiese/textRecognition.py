import cv2
import pytesseract
img = cv2.imread('IMG_1045.jpeg') # Adding custom options
custom_config = r'--oem 3 --psm 6'
string = pytesseract.image_to_string(img, config=custom_config)
print(string)