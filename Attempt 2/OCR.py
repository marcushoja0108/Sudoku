import pytesseract
import cv2

def run_ocr(image_path):
    # image_path = "OCR testing/OCR demo.PNG"
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 2)
    inverted = cv2.bitwise_not(thresh)
    
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    dilated = cv2.dilate(inverted, kernel)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    contrast = clahe.apply(dilated)
    
    height, width = contrast.shape
    cell_h, cell_w = height // 9, width // 9
    
    custom_config = r"--psm 10 -c tessedit_char_whitelist=123456789"
    
    board = []
    
    for i in range(9):
        row = []
        for j in range(9):
            x1, y1 = j * cell_w, i * cell_h
            x2, y2 = (j + 1) * cell_w, (i + 1) * cell_h
    
            cell = thresh[y1:y2, x1:x2]
    
            cell = cv2.resize(cell,(100, 100), interpolation=cv2.INTER_LINEAR)
            cell = cv2.copyMakeBorder(cell, 10, 10, 10, 10, cv2.BORDER_CONSTANT, value=0)
    
            # OCR
            if cv2.countNonZero(cell) <50:
                row.append('')
                continue
    
            digit = pytesseract.image_to_string(cell, config=custom_config)
            digit = digit.strip()
    
            if len(digit) == 1 and digit in '123456789':
                row.append(int(digit))
            else:
                row.append('')
        board.append(row)
        
    nested_board = [[[['' for _ in range(3)] for _ in range(3)] for _ in range(3)] for _ in range(3)]
    for i in range(9):
        for j in range(9):
            value = board[i][j]
            box_row, box_col = i // 3, j // 3
            cell_row, cell_col = i % 3, j % 3
            nested_board[box_row][box_col][cell_row][cell_col] = value

    print("\n🧾 OCR Flat Board (9x9):")
    for row in board:
        print(" ".join(str(cell) if cell != '' else '.' for cell in row))
    return nested_board