# Implementacja obsługi ładowania i predykcji modelu
import cv2
import numpy as np
from PyQt6.QtGui import QImage
from tensorflow.keras.models import load_model


def qimage_to_array(image: QImage):
    """Konwertuje QImage na tablicę numpy w skali szarości (H, W)."""
    gray = image.convertToFormat(QImage.Format.Format_Grayscale8)
    ptr = gray.bits()
    ptr.setsize(gray.sizeInBytes())
    return np.array(ptr).reshape(gray.height(), gray.width())


def preprocess(image: QImage):
    """
    Przygotowuje rysunek do kształtu MNIST: binarizacja, kadrowanie
    do bounding boxu, skalowanie z proporcjami do ~20x20 i osadzenie
    na płótnie 28x28.
    """
    arr = qimage_to_array(image)

    # Binarizacja (rysujesz białym na czarnym), odszumienie progowe
    _, binary = cv2.threshold(arr, 30, 255, cv2.THRESH_BINARY)

    # Bounding box nieczarnych pikseli
    coords = cv2.findNonZero(binary)
    if coords is None:
        return None

    x, y, w, h = cv2.boundingRect(coords)
    cropped = binary[y : y + h, x : x + w]

    # Skalowanie z zachowaniem proporcji do maks 20x20 (jak MNIST)
    target = 20
    scale = target / max(w, h)
    new_w, new_h = max(1, int(w * scale)), max(1, int(h * scale))
    resized = cv2.resize(cropped, (new_w, new_h), interpolation=cv2.INTER_AREA)

    # Osadzenie na płótnie 28x28, centralnie
    canvas = np.zeros((28, 28), dtype=np.uint8)
    y_off = (28 - new_h) // 2
    x_off = (28 - new_w) // 2
    canvas[y_off : y_off + new_h, x_off : x_off + new_w] = resized

    # Normalizacja do [0,1] i dodanie wymiaru kanału oraz batcha
    x = canvas.astype("float32") / 255.0
    x = np.expand_dims(x, axis=(0, 3))  # (1, 28, 28, 1)
    return x


def predict(image: QImage, model):
    """
    Funkcja wykorzystująca załadowany model sieci neuronowej do predykcji znaku na obrazie

    Należy dodać w niej odpowiedni kod do obsługi załadowanego modelu
    """
    if model is None:
        return "brak modelu"

    x = preprocess(image)
    if x is None:
        return "brak rysunku"

    preds = model.predict(x, verbose=0)

    prob = float(np.max(preds))
    cls = int(np.argmax(preds, axis=1)[0])
    return f"{cls} ({prob*100:.1f}%)"


def get_model():
    # Używamy konwolucyjnego modelu z przykładu 2, lepiej pasuje do 28x28x1
    try:
        loaded_model = load_model(".\mnist_2_model.keras")
    except Exception:
        # Fallback na prosty dense model, jeśli CNN nie jest dostępne
        loaded_model = load_model(".\mnist_1_model.keras")

    print("Wczytany model (cały):", loaded_model)
    return loaded_model
