class Limiter:
    drawableData = []
    vertexesOffset = 0

    @staticmethod
    def getVertexesAmount(vertexes, vertexWidth, screenWidth, horizontalMargin=0) -> int:
        if (len(vertexes) > (screenWidth - horizontalMargin) // vertexWidth + 1):
            return (screenWidth - horizontalMargin) // vertexWidth + 1
        else:
            return int(len(vertexes))

    @staticmethod
    def setDrawableData(data):
        Limiter.drawableData = data

    @staticmethod
    def calculateDrawableData(data, startPosition, endPosition):
        return data[startPosition:endPosition]