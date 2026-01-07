# ustwienie bazowego szablonu
FROM python:3.8

# ustawienie bazowego folderu 
WORKDIR /code

# skopiowanie pliku requirements.txt do kontenera
COPY requirements.txt .

EXPOSE 5001

# uzycie menadzera pakietow dla python'a 
# do instalacji potrzebnych pakietow 
RUN pip install -r requirements.txt

# skopiowanie folderu src do folderu 
# bazowego kontenera (ustawionego za pomoca WORKDIR)
COPY src/ .

# uruchomienie aplikacji app.py w jezyku python 
# po uruchomieniu kontenera
CMD [ "python", "app1.py" ]