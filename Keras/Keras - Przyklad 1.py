# Ładowanie potrzebych modułów
# MNIST - zbiór obrazów z odręcznie pisanymi cyframi od 0 do 9
# Sequential- model sekwencyjny sieci neuronowej
# Dense - warsta gęsta sieci
try:
    from keras.api.datasets import mnist
    from keras.api.models import Sequential
    from keras.api.layers import Dense
    from keras.api.utils import to_categorical
except:
    from keras.datasets import mnist
    from keras.models import Sequential
    from keras.layers import Dense
    from keras.utils import to_categorical
from matplotlib import pyplot as plt

# Wczytywanie danych
(X_train, y_train), (X_test, y_test) = mnist.load_data()

# Splaszczenie obrazów z28 * 28 pikseli do 784 elementowego vector'a
num_pixels = X_train.shape[1] * X_train.shape[2]
X_train = X_train.reshape((X_train.shape[0], num_pixels)).astype("float32")
X_test = X_test.reshape((X_test.shape[0], num_pixels)).astype("float32")

# Normalizacja danych o wartosciach od 0 do 255 do wartości od 0 do 1
X_train = X_train / 255
X_test = X_test / 255

# Pobranie i stworzenie listy klas dla danych
y_train = to_categorical(y_train)
y_test = to_categorical(y_test)

# Wyciągniecie liczby klas
num_classes = y_test.shape[1]

# Tworzenie modelu sieci
model = Sequential()

# Dodanie pierwszej warstwy odpowiedzialnej za odebranie danych obrazu - liczba neuronoów = liczbie pikseli
model.add(
    Dense(
        num_pixels, input_dim=num_pixels, kernel_initializer="normal", activation="relu"
    )
)

# Dodanie drugiej warstwy odpowiedzialnej za klasę - liczba neuronów = liczba klas
model.add(Dense(num_classes, kernel_initializer="normal", activation="softmax"))

# Kompilacja modelu
model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])

# Uczenie modelu danymi
# epoch - liczba iteracji
# batch_size - liczba elemenów z danych treningowych branych podczas pojedyńczego przejścia funkcji uczącej
history = model.fit(
    X_train,
    y_train,
    validation_data=(X_test, y_test),
    epochs=25,
    batch_size=50,
    verbose=1,
)

# Testowanie modelu
scores = model.evaluate(X_test, y_test, verbose=0)
print("Baseline Error: %.2f%%" % (100 - scores[1] * 100))

# wyświetlenie wykresu przedstawiającego historię uczenia sieci
plt.subplot(2, 1, 1)
plt.plot(history.history["accuracy"])
plt.plot(history.history["val_accuracy"])
plt.title("model accuracy")
plt.ylabel("accuracy")
plt.xlabel("epoch")
plt.legend(["train", "val"], loc="upper left")

plt.subplot(2, 1, 2)
plt.plot(history.history["loss"])
plt.plot(history.history["val_loss"])
plt.title("model loss")
plt.ylabel("loss")
plt.xlabel("epoch")
plt.legend(["train", "val"], loc="upper left")
plt.show()
# -----------------------------
# Zapis i odczyt modelu oraz wag
# -----------------------------
# Zapisanie całego modelu (architektura + wagi + stan optymalizatora)
model.save("mnist_1_model.keras")
# Zapisanie tylko wag
# Keras (nowsze wersje) oczekuje, że plik wag HDF5 będzie kończył się na ".weights.h5"
model.save_weights("mnist_1.weights.h5")
print("Model i wagi zapisane: mnist_1_model.keras, mnist_1.weights.h5")

# Przykład: wczytanie całego modelu
from tensorflow.keras.models import load_model

loaded_model = load_model("mnist_1_model.keras")
print("Wczytany model (cały):", loaded_model)

# Przykład: wczytanie wag do nowo zbudowanej architektury (weights-only)
# Tworzymy taką samą (prosty, gęsty) architekturę jak powyżej i ładujemy zapisane wagi.
new_model = Sequential()
new_model.add(
    Dense(
        num_pixels, input_dim=num_pixels, kernel_initializer="normal", activation="relu"
    )
)
new_model.add(Dense(num_classes, kernel_initializer="normal", activation="softmax"))
new_model.compile(
    loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"]
)
new_model.load_weights("mnist_1.weights.h5")
print("Wczytano wagi do nowej architektury.")

# Opcjonalna szybka ewaluacja wczytanych modeli (nie uczy, tylko testuje)
loss, acc = loaded_model.evaluate(X_test, y_test, verbose=0)
print(f"Loaded model - test loss: {loss:.4f}, test acc: {acc:.4f}")
loss2, acc2 = new_model.evaluate(X_test, y_test, verbose=0)
print(f"Weights-only model - test loss: {loss2:.4f}, test acc: {acc2:.4f}")
