import cv2
import numpy  as np
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split

labels = [
    [5, 6, '', '', '', 7, '', '', ''],
    ['', 9, '', 6, 8, 3, '', '', 4],
    ['', 4, '', '', 1, 5, '', 8, 7],
    [6, '', '', '', '', 2, '', 7, 9],
    ['', 3, '', '', '', '', 1, '', 2],
    ['', '', '', 7, 6, 4, '', 3, ''],
    [9, 2, '', 8, '', 1, '', '', ''],
    [4, '', 3, 2, 5, 6, '', '', 1],
    [8, '', '', '', 4, 9, '', 2, '']
]

def extract_digit(cell):
    contours, _ = cv2.findContours(cell, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return None
    
    largest = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(largest)
    digit = cell[y:y+h, x: x+w]
    if digit.shape[0] < 5 or digit.shape[1] < 5:
        return None
    
    digit = cv2.resize(digit, (20, 20), interpolation=cv2.INTER_AREA)
    padded = cv2.copyMakeBorder(digit, 4, 4, 4, 4, cv2.BORDER_CONSTANT, value=0)
    padded = padded / 255.0
    
    return padded.flatten().astype(np.float32)

def train_knn(image_path, labels):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 2)
    kernel = np.ones((2, 2), np.uint8)
    thresh = cv2.dilate(thresh, kernel, iterations=1)
    
    height, width = thresh.shape
    cell_h, cell_w = height // 9, width // 9
    
    samples = []
    responses = []
    
    for i in range(9):
        for j in range(9):
            label = labels[i][j]
            if label == '':
                continue
                
            x1, y1 = j * cell_w, i * cell_h
            x2, y2 = (j + 1) * cell_w, (i + 1) * cell_h
            cell = thresh[y1:y2, x1:x2]
            digit = extract_digit(cell)
            
            if digit is not None:
                samples.append(digit)
                responses.append(int(label))
            
    
    knn = cv2.ml.KNearest_create()
    knn.train(np.array(samples), cv2.ml.ROW_SAMPLE, np.array(responses))
    return knn


def predict_sudoku_board(image_path, knn):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 2)
    kernel = np.ones((2, 2), np.uint8)
    thresh = cv2.dilate(thresh, kernel, iterations=1)
    
    height, width = thresh.shape
    cell_h, cell_w = height // 9, width // 9
    
    board = []
    
    for i in range(9):
        row = []
        for j in range(9):
            x1, y1 = j * cell_w, i * cell_h
            x2, y2 = x1 + cell_w, y1 + cell_h
            cell = thresh[y1:y2, x1:x2]
            digit = extract_digit(cell)
            cv2.imwrite(f'debug/{i}_{j}.png', cell)
            
            if cv2.countNonZero(cell) < 30:
                row.append('')
                continue
                
            if digit is not None:
                _, result, _, _ = knn.findNearest(digit.reshape(1, -1), k=3)
                row.append(int(result[0][0]))
            else:
                row.append('')
        board.append(row)
    return board

# usage

image_path = "OCR testing/OCR demo.PNG"
knn_model = train_knn(image_path, labels)
sudoku_board = predict_sudoku_board("OCR testing/OCR demo.PNG", knn_model)

for row in sudoku_board:
    print(row)