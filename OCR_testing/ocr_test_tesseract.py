import numpy as np
import pytesseract
import cv2

tests = [
    {
        "image_path": "OCR testing/OCR test(1).PNG",
        "correct_board": [[5, 6, '', '', '', 7, '', '', ''],
                          ['', 9, '', 6, 8, 3, '', '', 4],
                          ['', 4, '', '', 1, 5, '', 8, 7],
                          [6, '', '', '', '', 2, '', 7, 9],
                          ['', 3, '', '', '', '', 1, '', 2],
                          ['', '', '', 7, 6, 4, '', 3, ''],
                          [9, 2, '', 8, '', 1, '', '', ''],
                          [4, '', 3, 2, 5, 6, '', '', 1],
                          [8, '', '', '', 4, 9, '', 2, '']]
    },
    {
        "image_path": "OCR testing/OCR test(2).PNG",
        "correct_board": [['', '', '', 4, 6, '', '', 3, ''],
                          [3, 9, '', '', '', 1, 7, '', 5],
                          [2, 8, 4, '', '', '', '', 9, ''],
                          [5, '', '', 8, 7, '', 6, 1, 3],
                          [8, 3, 1, '', 9, '', '', '', ''],
                          ['', '', 2, 5, 1, '', '', 8, ''],
                          ['', 6, '', '', '', '', '', '', 9],
                          [4, '', 5, '', 2, 6, 3, '', ''],
                          ['', '', '', '', 4, 7, 5, 6, 1]]
    },
    {
        "image_path": "OCR testing/OCR test(3).PNG",
        "correct_board": [[9, 6, '', '', '', '', '', '', ''],
                          ['', '', 5, 4, '', '', '', 2, ''],
                          [4, '', '', '', 6, '', '', 8, ''],
                          ['', '', 3, 5, '', '', '', 1, ''],
                          ['', '', 4, '', '', 7, 8, '', ''],
                          ['', '', '', '', '', '', '', '', ''],
                          ['', '', 8, 1, '', '', 3, '', ''],
                          ['', 3, 9, '', 5, '', 7, '', ''],
                          ['', '', '', 6, '', '', 9, '', '']]
    },
    {
        "image_path": "OCR testing/OCR test(4).PNG",
        "correct_board": [['', '', 3, 2, '', '', '', 1, ''],
                          ['', 1, '', '', 6, 9, '', 7, 5],
                          ['', 9, 6, '', 7, 5, 3, '', 2],
                          ['', 6, '', '', 5, '', '', '', 8],
                          ['', 8, '', '', 3, 6, 2, 4, 9],
                          ['', 7, '', 9, '', '', '', '', ''],
                          ['', '', 1, '', '', 7, '', 9, ''],
                          ['', '', '', '', '', '', 5, 2, 7],
                          [8, 2, 7, '', 9, '', 1, 6, 3]]
    },
    {
        "image_path": "OCR testing/OCR test(5).PNG",
        "correct_board": [['', '', '', '', 1, '', '', '', 8],
                          [4, '', 3, 9, '', 2, '', '', ''],
                          ['', 9, 1, '', '', '', 4, '', ''],
                          [8, 3, 6, '', 4, 9, 5, 1, ''],
                          [2, '', '', '', '', '', 8, 7, ''],
                          ['', 7, 9, 8, 2, 5, 6, 4, ''],
                          ['', '', '', '', 9, 7, 2, '', 6],
                          [3, '', '', '', '', '', 9, '', ''],
                          ['', 6, '', 1, '', 8, '', '', 4]]
    },
    {
        "image_path": "OCR testing/OCR test(6).PNG",
        "correct_board": [['', '', '', '', '', '', 4, '', ''],
                          [7, 3, '', 5, 9, '', '', '', ''],
                          ['', '', '', 7, '', '', 5, 3, ''],
                          ['', 2, '', '', 7, '', 3, '', ''],
                          ['', '', 3, 2, 5, 6, 8, 9, ''],
                          [8, '', 1, '', '', '', '', 2, ''],
                          ['', '', '', '', 1, '', 6, '', 7],
                          ['', 6, '', 4, '', '', 9, '', ''],
                          ['', '', '', 6, '', 3, '', 5, 4]]
    }
]

def ocr_sudoku_board(image_path):
    img = cv2.imread(image_path)

    #Preprocessing
    #Brightness
    brightness_factor = 2.5
    brightened = np.clip(img * brightness_factor, 0, 255).astype(np.uint8)

    #Grayscale
    gray = cv2.cvtColor(brightened, cv2.COLOR_BGR2GRAY)

    blurred = cv2.GaussianBlur(gray, (3, 3), 0)

    #Threshold
    thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 2)
 
    inverted = cv2.bitwise_not(thresh)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    opened = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    contrast = clahe.apply(opened)
    
    kernel_sharp = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    sharpened = cv2.filter2D(contrast, -1, kernel_sharp)
    
    # split into grid
    height, width = sharpened.shape
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
            if cv2.countNonZero(cell) <80:
                row.append('')
                continue

            digit = pytesseract.image_to_string(cell, config=custom_config)
            digit = digit.strip()

            if len(digit) == 1 and digit in '123456789':
                row.append(int(digit))
            else:
                row.append('')
        board.append(row)

    return board

def compare_boards(predicted, ground_truth):
    total_cells = 81
    correct = 0

    for i in range(9):
        for j in range(9):
            if predicted[i][j] == ground_truth[i][j]:
                correct += 1

    accuracy = (correct / total_cells) * 100
    print(f"OCR result: {correct}/{total_cells} correct cells — {accuracy:.2f}% accuracy")
    return accuracy

accuracies = []

for test in tests:
    print(f"\nTesting image: {test['image_path']}")
    board = ocr_sudoku_board(test["image_path"])
    #prints recieved board in console
    # for row in board:
    #     print(row)
    acc = compare_boards(board, test["correct_board"])
    accuracies.append(acc)

average_accuracy = sum(accuracies) / len(accuracies)
print(f"\nAverage OCR accuracy across {len(tests)} boards: {average_accuracy:.2f}%")