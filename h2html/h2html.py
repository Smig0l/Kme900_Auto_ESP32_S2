import gzip
import re
import sys
import os

# Check for the input file
if len(sys.argv) < 2:
    print("Usage: python h2html.py <path_to_c_header_file>")
    sys.exit(1)

input_file = sys.argv[1]

try:
    # Read the C header file
    with open(input_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Regex to match multiple byte arrays (captures array name and data)
    matches = re.findall(r"static const uint8_t (\w+)_gz\[\] PROGMEM =\s*{([^}]*)};", content, re.DOTALL)

    if not matches:
        print("Error: No valid byte arrays found in the file.")
        sys.exit(1)

    for name, data in matches:
        # Extract numbers and convert to bytes
        byte_data = bytes(int(num.strip()) for num in data.split(",") if num.strip().isdigit())

        # Save as a GZ file
        gz_filename = f"{name}.gz"
        with open(gz_filename, "wb") as gz_file:
            gz_file.write(byte_data)

        # Decompress and save as HTML
        html_filename = f"{name}.html"
        with gzip.open(gz_filename, "rb") as gz_file:
            html_content = gz_file.read().decode("utf-8")

        with open(html_filename, "w", encoding="utf-8") as html_file:
            html_file.write(html_content)

        # Delete the .gz file
        os.remove(gz_filename)

        print(f"Extracted {gz_filename} → {html_filename}")

    print("Extraction complete!")

except Exception as e:
    print(f"Error extracting files: {e}")
