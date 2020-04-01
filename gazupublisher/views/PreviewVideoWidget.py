from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QSizePolicy,
    QSlider,
    QStyle,
    QVBoxLayout,
)
from PyQt5.QtWidgets import QWidget, QPushButton
import sys


class VideoWindow(QWidget):
    def __init__(self, parent=None):
        super(VideoWindow, self).__init__(parent)

        self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        self.play_button = QPushButton()
        self.play_button.setEnabled(False)
        self.play_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.play_button.clicked.connect(self.play)

        self.position_slider = QSlider(Qt.Horizontal)
        self.position_slider.setRange(0, 0)
        self.position_slider.sliderMoved.connect(self.set_position)

        self.error_label = QLabel()
        self.error_label.setSizePolicy(
            QSizePolicy.Preferred, QSizePolicy.Maximum
        )

        control_layout = QHBoxLayout()
        control_layout.setContentsMargins(0, 0, 0, 0)
        control_layout.addWidget(self.play_button)
        control_layout.addWidget(self.position_slider)

        video_widget = QVideoWidget()
        layout = QVBoxLayout()
        layout.addWidget(video_widget)
        layout.addLayout(control_layout)
        layout.addWidget(self.error_label)

        self.setLayout(layout)

        self.media_player.setVideoOutput(video_widget)
        self.media_player.stateChanged.connect(self.media_state_changed)
        self.media_player.positionChanged.connect(self.position_changed)
        self.media_player.durationChanged.connect(self.duration_changed)
        self.media_player.error.connect(self.handle_error)
        import os

        current_file_path = os.path.dirname(os.path.realpath(__file__))
        print(current_file_path)

    def open_file(self, file_name):
        if file_name != "":
            self.media_player.setMedia(
                QMediaContent(QUrl.fromLocalFile(file_name))
            )
            self.play_button.setEnabled(True)

    def exit_call(self):
        sys.exit(app.exec_())

    def play(self):
        if self.media_player.state() == QMediaPlayer.PlayingState:
            self.media_player.pause()
        else:
            self.media_player.play()

    def media_state_changed(self, state):
        if self.media_player.state() == QMediaPlayer.PlayingState:
            self.play_button.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPause)
            )
        else:
            self.play_button.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPlay)
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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    player = VideoWindow()
    player.resize(210, 180)
    player.show()
    sys.exit(app.exec_())
