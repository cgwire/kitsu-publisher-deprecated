import os

from Qt import QtCore, QtGui, QtWidgets
from PyQt5 import QtMultimediaWidgets, QtMultimedia

from gazupublisher.utils.connection import get_data_from_url, get_host
from gazupublisher.views.task_panel.PreviewWidget import PreviewWidget

class PreviewVideoWidget(PreviewWidget):
    def __init__(self, preview_file):
        PreviewWidget.__init__(self, preview_file)


    def complete_ui(self):
        self.url = os.path.join(
            get_host(),
            "movies",
            "originals",
            "preview-files",
            self.preview_file["id"] + "." + self.preview_file["extension"],
        )

        self.media_player = QtMultimedia.QMediaPlayer(
            None, QtMultimedia.QMediaPlayer.VideoSurface
        )
        self.play_button = QtWidgets.QPushButton()
        self.play_button.setEnabled(False)
        self.play_button.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_MediaPlay))
        self.play_button.clicked.connect(self.play)
        self.toolbar_widget.layout().insertWidget(0, self.play_button)

        self.position_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.position_slider.setRange(0, 0)
        self.position_slider.sliderMoved.connect(self.set_position)
        self.layout().insertWidget(0, self.position_slider)

        self.error_label = QtWidgets.QLabel()
        self.error_label.setSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum
        )
        self.layout().insertWidget(0, self.error_label)
        self.error_label.hide()

        video_widget = QtMultimediaWidgets.QVideoWidget()
        self.layout().insertWidget(0, video_widget)

        self.play_button.clicked.connect(self.play)
        self.media_player.setVideoOutput(video_widget)
        self.media_player.stateChanged.connect(self.media_state_changed)
        self.media_player.positionChanged.connect(self.position_changed)
        self.media_player.durationChanged.connect(self.duration_changed)
        self.media_player.error.connect(self.handle_error)

        self.buffer = QtCore.QBuffer()
        self.open_file(self.url)

    def fill_preview(self):
        self.open_file(self.url)

    def open_file(self, url):
        data = get_data_from_url(url)
        self.buffer.setData(data)

        if self.buffer.open(QtCore.QIODevice.ReadOnly):
            self.media_player.setMedia(
                QtMultimedia.QMediaContent(),
                self.buffer
            )
        self.play_button.setEnabled(True)

    def play(self):
        if self.media_player.state() == QtMultimedia.QMediaPlayer.PlayingState:
            self.media_player.pause()
        else:
            self.media_player.play()

    def media_state_changed(self, state):
        if self.media_player.state() == QtMultimedia.QMediaPlayer.PlayingState:
            self.play_button.setIcon(
                self.style().standardIcon(QtWidgets.QStyle.SP_MediaPause)
            )
        else:
            self.play_button.setIcon(
                self.style().standardIcon(QtWidgets.QStyle.SP_MediaPlay)
            )

    def position_changed(self, position):
        self.position_slider.setValue(position)

    def duration_changed(self, duration):
        self.position_slider.setRange(0, duration)

    def set_position(self, position):
        self.media_player.setPosition(position)

    def handle_error(self):
        self.play_button.setEnabled(False)
        self.error_label.setText("Error: " + self.media_player.errorString())
        self.error_label.show()

    def clear_setup_media_widget(self):
        for i in reversed(range(self.layout().count())):
            widget = self.layout().itemAt(i).widget()
            if widget:
                widget.setParent(None)

