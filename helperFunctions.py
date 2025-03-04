#grids element list in respective Frame in Square
def packInSquare(elementList : list, lengthSquare: int,  xPadding: int, ):
    for rows in range(lengthSquare):
        for columns in range(lengthSquare):
            elementList[columns*lengthSquare+rows].grid(column= rows, row= columns, padx= xPadding)

