
from PIL import Image
import os
import re
images_folder_path = r'screenshots'
output_pdf_path = r'output.pdf'
def extract_number(file_name):
    numbers = re.findall(r'\d+', file_name)
    return int(numbers[0]) if numbers else 0
 
