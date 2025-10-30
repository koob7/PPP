# Implementacja obsługi ładowania i predykcji modelu
import cv2
import numpy as np
import sys
from PyQt6.QtGui import QImage
from tensorflow.keras.models import load_model, Sequential
from tensorflow.keras import layers


def qimage_to_array(image: QImage):
    """
    Funkcja konwertująca obiekt QImage do numpy array
    """
    image = image.convertToFormat(QImage.Format.Format_Grayscale8)
    ptr = image.bits()
    ptr.setsize(image.sizeInBytes())
    numpy_array = np.array(ptr).reshape(image.height(), image.width(), 1)

    # wykorzystanie bibloteki OpenCV do wyświetlenia obrazu po konwersji
    cv2.imshow("Check if the function works!", numpy_array)
    return numpy_array


def predict(image: QImage, model):
    """
    Funkcja wykorzystująca załadowany model sieci neuronowej do predykcji znaku na obrazie

    Należy dodać w niej odpowiedni kod do obsługi załadowanego modelu
    """
    # Konwersja QImage -> numpy array (grayscale)
    arr = qimage_to_array(image)

    # Zmiana rozmiaru do 28x28 (MNIST)
    try:
        resized = cv2.resize(arr, (28, 28), interpolation=cv2.INTER_AREA)
    except Exception:
        # Jeśli arr ma inny wymiar, spróbuj spłaszczyć do 2D
        resized = cv2.resize(arr.reshape(arr.shape[0], arr.shape[1]), (28, 28))

    # Upewnij się, że mamy kanał (H,W,1)
    if resized.ndim == 2:
        resized = resized.reshape(28, 28, 1)

    # Normalizacja do zakresu [0,1]
    x = resized.astype("float32") / 255.0
    x = np.expand_dims(x, axis=0)  # (1,28,28,1)

    if model is None:
        return "brak modelu"

    # Próba użycia modelu do predykcji. Jeśli model oczekuje spłaszczonego wektora,
    # spróbujemy przepastwić wejście i ponowić predykcję.
    try:
        preds = model.predict(x, verbose=0)
    except Exception:
        try:
            preds = model.predict(x.reshape((1, 28 * 28)), verbose=0)
        except Exception:
            return "błąd predykcji"

    prob = float(np.max(preds))
    cls = int(np.argmax(preds, axis=1)[0])
    return f"{cls} ({prob*100:.1f}%)"


def get_model():
    # Przykład: wczytanie całego modelu

    loaded_model = load_model("mnist_2_model.keras")
    print("Wczytany model (cały):", loaded_model)

    return loaded_model
