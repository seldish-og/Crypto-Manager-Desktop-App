class Limiter:
    drawableData = []

    @staticmethod
    def getVertexesAmount(vertexes, vertexWidth, screenWidth, horizontalMargin=0) -> int:
        if (len(vertexes) > (screenWidth - horizontalMargin) // vertexWidth):
            return (screenWidth - horizontalMargin) // vertexWidth
        else:
            return int(len(vertexes))

    @staticmethod
    def setDrawableData(data):
        Limiter.drawableData = data

    @staticmethod
    def calculateDrawableData(data, startPosition, endPosition):
        return data[startPosition:endPosition]