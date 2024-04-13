from django.shortcuts import render
import pytesseract
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
import io
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
import easyocr
import re
from django.shortcuts import render

def extract_aadhar_info(image):
    # Initialize EasyOCR reader
    reader = easyocr.Reader(['en'])

    # Load the image of the Aadhar card
    result = reader.readtext(image)

    # Define regular expressions for pattern matching
    aadhar_pattern = r'\b\d{4} \d{4} \d{4}\b'
    phone_pattern = r'\d{10}'
    dob_pattern = r'\b\d{2}/\d{2}/\d{4}\b'
    name_pattern = r'To:\s*(.+)'
    gender_pattern = r'MALE|FEMALE|male|female|Male|Female'

    # Initialize variables to store extracted information
    aadhar_number = None
    phone_number = None
    dob = None
    name = None
    gender = None

    for i in range(len(result)):
        text = result[i][1]
        if re.search(aadhar_pattern, text) and not aadhar_number:
            aadhar_number = re.search(aadhar_pattern, text).group()
        elif re.search(phone_pattern, text) and not phone_number:
            phone_number = re.search(phone_pattern, text).group()
        elif re.search(dob_pattern, text) and not dob:
            dob = re.search(dob_pattern, text).group()
        elif re.search(gender_pattern, text, re.IGNORECASE) and not gender:
            gender = re.search(gender_pattern, text).group()
        elif re.search(name_pattern, text) and not name:
            name = re.search(name_pattern, text).group(1)
            break

    return aadhar_number, phone_number, dob, name, gender

def process_image(request):
    if request.method == 'POST' and request.FILES['image']:
        image = Image.open(request.FILES['image'])

        # Save the uploaded image to the media folder
        image_io = io.BytesIO()
        image.save(image_io, format='JPEG')
        image_file = InMemoryUploadedFile(image_io, None, 'image.jpg', 'image/jpeg', image_io.tell(), None)
        image_file.seek(0)

        # Extract information using OCR directly from the image
        aadhar_number, phone_number, dob, name, gender = extract_aadhar_info(image)

        # Pass the extracted information to the result template
        return render(request, 'aadhar_result_long.html', {'aadhar_number': aadhar_number, 'phone_number': phone_number,
                                               'dob': dob, 'name': name, 'gender': gender})

    return render(request, 'aadhar_upload_long.html')

def result(request):
    return render(request, 'aadhar_result_long.html')
# Create your views here.
