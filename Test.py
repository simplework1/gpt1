import cv2
import pytesseract

# Set the Tesseract executable path (required on Windows)
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Load the image
image_path = "mixed_language.png"  # Replace with your image path
image = cv2.imread(image_path)

# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Optional preprocessing
# gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

# Perform OCR with both languages
custom_config = r'--oem 3 --psm 6'  # Set OCR Engine Mode and Page Segmentation Mode
text = pytesseract.image_to_string(gray, lang='eng+hin', config=custom_config)

# Print the extracted text
print("Extracted Text:")
print(text)

# Optional: Display the image
cv2.imshow("Image", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
