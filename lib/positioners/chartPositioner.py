class ChartPositioner:
    paddingVertical = 120
    paddingHorizontal = 120
    maximalHorizontalPadding = 300

    @staticmethod
    def setPaddingVertical(padding) -> None:
        ChartPositioner.paddingVertical = padding

    @staticmethod
    def setPaddingHorizontal(padding) -> None:
        ChartPositioner.paddingHorizontal = padding