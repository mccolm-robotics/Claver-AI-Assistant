def setTextureOffset(offset, index):
    numberOfRows = 4
    column = index % numberOfRows
    row = index // numberOfRows
    offset[0] = column / numberOfRows
    offset[1] = row / numberOfRows

offset = [0, 0]
for i in range(16):
    setTextureOffset(offset, i)
    print(offset)