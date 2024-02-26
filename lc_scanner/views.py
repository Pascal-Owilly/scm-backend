import PyPDF2
import re

def extract_lc_info(pdf_path):
    lc_info = {}

    # Open the PDF file
    with open(pdf_path, 'rb') as pdf_file:
        # Create a PDF reader object
        pdf_reader = PyPDF2.PdfFileReader(pdf_file)

        # Loop through each page of the PDF
        for page_num in range(pdf_reader.numPages):
            # Extract text from the page
            page_text = pdf_reader.getPage(page_num).extractText()

            # Search for key data points using regular expressions
            issuing_bank_match = re.search(r'Issuing Bank: (.+)', page_text)
            if issuing_bank_match:
                lc_info['Issuing Bank'] = issuing_bank_match.group(1).strip()

            beneficiary_match = re.search(r'Beneficiary: (.+)', page_text)
            if beneficiary_match:
                lc_info['Beneficiary'] = beneficiary_match.group(1).strip()

            # Add more patterns and data points to extract as needed

    return lc_info

# Example usage:
pdf_path = 'letter_of_credit.pdf'
lc_info = extract_lc_info(pdf_path)
print(lc_info)

