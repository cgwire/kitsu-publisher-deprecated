from Qt import QtWidgets


class PreviewImageWidget(QtWidgets.QGraphicsPixmapItem):
    def __init__(self, data):
        QtWidgets.QGraphicsPixmapItem.__init__(self)
