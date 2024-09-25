import PyPDF2
import pandas as pd
import re

# Step 1: Extract text from PDF
def extract_pdf_text(pdf_path):
    with open(pdf_path, 'rb') as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        pdf_text = ""
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            pdf_text += page.extract_text()
    return pdf_text

# Step 2: Parse the extracted text to get relevant data (Athlete, Country, Total Score)
def parse_athlete_data(pdf_text):
    athletes_data = []
    # Regular expression to match "Athlete", "Country", and "Total Score"
    pattern = re.compile(r'Athlete:\s(.*?)\nCountry:\s(.*?)\n.*?Total\s(\d+)')
    
    # Find all matches
    matches = pattern.findall(pdf_text)
    
    # Extract data from matches
    for match in matches:
        athlete, country, total_score = match
        athletes_data.append([athlete, country, total_score])
    
    return athletes_data

# Step 3: Convert parsed data into an Excel file
def save_to_excel(data, output_file):
    # Create a pandas DataFrame
    df = pd.DataFrame(data, columns=["Athlete", "Country", "Total Score"])
    
    # Save DataFrame to an Excel file
    df.to_excel(output_file, index=False)
    print(f"Data successfully saved to {output_file}")

# Main function
def main(pdf_path, output_file):
    # Step 1: Extract text
    pdf_text = extract_pdf_text(pdf_path)
    
    # Step 2: Parse the text
    athletes_data = parse_athlete_data(pdf_text)
    
    # Step 3: Save to Excel
    save_to_excel(athletes_data, output_file)

# Specify the PDF input and Excel output file paths
if __name__ == "__main__":
    pdf_path = "ShootUp.pdf"  # Replace with the path to your PDF file
    output_file = "output.xlsx"  # Replace with the desired output Excel file name
    main(pdf_path, output_file)

