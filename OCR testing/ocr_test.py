import cv2
import numpy  as np
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split

def train_knn():
    digits = load_digits()
    data = digits.images
    labels = digits.target
    
    samples = data.reshape((len(data), -1)).astype(np.float32)
    
    X_train, X_test, y_train, y_test = train_test_split(samples, labels, test_size=0.2, random_state=42)
    
    knn = cv2.ml.KNearest_create()
    knn.train(X_train, cv2.ml.ROW_SAMPLE, y_train)
    
    return knn

def preprocess_cell(cell_img):
    resized = cv2.resize(cell_img, (8, 8), interpolation=cv2.INTER_AREA)
    resized = resized.astype(np.float32)
    flattened = resized.flatten().reshape(1, -1)
    return flattened

def predict_sudoku_board(image_path, knn):
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
    
    board = []
    
    for i in range(9):
        row = []
        for j in range(9):
            x1, y1 = j * cell_w, i * cell_h
            x2, y2 = (j + 1) * cell_w, (i + 1) * cell_h
    
            cell = thresh[y1:y2, x1:x2]
            
            if cv2.countNonZero(cell) < 20:
                row.append('')
                continue
            
            processed = preprocess_cell(cell)
            _, result, _, _ = knn.findNearest(processed, k=3)
            row.append(int(result[0][0]))
        board.append(row)
        
    return board


# usage
knn_model = train_knn()
sudoku_board = predict_sudoku_board("OCR testing/OCR demo.PNG", knn_model)

for row in sudoku_board:
    print(row)