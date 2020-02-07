This program is used to select the Area of interest in the image (jpg,png) and map them to a key.
This outputs a config xml.

Install using pip -
- numpy
- scipy
- opencv-python
- tkinter
- math
- pytesseract

Set pytesseract as system variable

python roi_tesseract.py <Destination of image file> or set the path in IMAGE_FILE_LOCATION.
Eg: python roi_tesseract.py C:\Workspace\image.png

Steps
1 - Select the region of text and press ENTER. To re-select press C and select again.
2 - Enter the name of the Key Selected.
3 - Repeat Step 1 & 2 till all the fields are selected.
4 - Press q to quit the Image.
5 - Enter the name of the document.
6 - Config file will be generated.

