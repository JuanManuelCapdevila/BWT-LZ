with open("imagen.jpg","rb") as file:
    data = file.read()
    file.close()
    with open("ejemplo.jpg","wb") as file:
        file.write(data)

