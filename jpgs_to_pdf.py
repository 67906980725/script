# pip install FPDF
# python jpgs2pdf.py dir_name
# python jpgs2pdf.py collections_dir_name 1

from fpdf import FPDF
from PIL import Image
import os
import sys


def opt(folder):

    pdf = FPDF()
    imagelist = []

    for dirpath, dirnames, filenames in os.walk(folder):
        for filename in [f for f in filenames if f.endswith(".jpg")]:
            full_path = os.path.join(dirpath, filename)
            imagelist.append(full_path)

    imagelist.sort()
    for i in range(0, len(imagelist)):
        print(imagelist[i])

    for i in range(0, len(imagelist)):
        im1 = Image.open(imagelist[i])
        width, height = im1.size
        # If width > height, rotate the image.
        if width > height:
            im2 = im1.transpose(Image.ROTATE_270)
            os.remove(imagelist[i])
            im2.save(imagelist[i])
            # im.save

    print("\nFound " + str(len(imagelist)) + " image files. Converting to PDF....\n")

    for image in imagelist:
        pdf.add_page()
        pdf.image(image, 0, 0, 210, 297)                           # 210 and 297 are the dimensions of an A4 size sheet.

    folder_name = os.path.basename(folder)
    parent_folder = os.path.abspath(os.path.join(folder, ".."))
    pdf.output(folder + ".pdf", "F")

    print("PDF generated successfully!")
    

if __name__ == '__main__':
    dir = sys.argv[1]
    type = sys.argv[2]
    
    if not type:
        opt(dir)
        
    else:
        for path, dir_names, file_names in os.walk(dir):
            for dir_name in dir_names:
                opt(os.path.join(path, dir_name))
