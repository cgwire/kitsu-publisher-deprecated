import os
import importlib

from Qt import QtCore, QtGui, QtWidgets

from kitsupublisher.working_context import get_current_binding

QtMultimedia = importlib.import_module(get_current_binding() + ".QtMultimedia")
QtMultimediaWidgets = importlib.import_module(
    get_current_binding() + ".QtMultimediaWidgets"
)

from kitsupublisher.utils.connection import get_file_data_from_url
from kitsupublisher.views.task_panel.PreviewWidget import PreviewWidget
from kitsupublisher.exceptions import MediaNotSetUp


class SliderNoScroll(QtWidgets.QSlider):
    """
    Classic slider with scroll disabled.
    """

    def __init__(self, *args):
        QtWidgets.QSlider.__init__(self, *args)

    def wheelEvent(self, event):
        event.ignore()


class CustomVideoWidget(QtMultimediaWidgets.QVideoWidget):
    """
    QVideoWidget to contain the preview. SizeHint overridden to match the panel
    width.
    """

    def __init__(self, parent):
        QtMultimediaWidgets.QVideoWidget.__init__(self, parent)
        self.parent = parent
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        self.setStyleSheet("QLabel { background-color: black }")

    def sizeHint(self):
        ratio = 16.0 / 9
        return QtCore.QSize(
            self.parent.desired_geometry.width(),
            self.parent.desired_geometry.width() / ratio,
        )


class PreviewVideoWidget(PreviewWidget):
    def __init__(self, parent, preview_file):
        PreviewWidget.__init__(self, parent, preview_file)

    def complete_ui(self):
        """
        Complete the interface with the widgets needed for a video.
        """
        self.timer_label = QtWidgets.QLabel()

        self.toolbar_widget.layout().insertWidget(0, self.timer_label)

        self.duration = None
        self.fps = None

        self.play_button = QtWidgets.QPushButton()
        self.play_button.setEnabled(False)
        self.play_button.setIcon(
            self.style().standardIcon(QtWidgets.QStyle.SP_MediaPlay)
        )
        self.play_button.clicked.connect(self.play)
        self.play_button.setFixedSize(QtCore.QSize(30, 30))
        self.toolbar_widget.layout().insertWidget(0, self.play_button)

        self.position_slider = SliderNoScroll(QtCore.Qt.Horizontal)
        self.position_slider.setRange(0, 0)
        self.position_slider.setSingleStep(10)
        self.position_slider.setFixedWidth(self.parent.desired_geometry.width())
        self.position_slider.setFixedHeight(15)
        self.position_slider.sliderMoved.connect(self.set_position)
        self.toolbar_widget.layout().setAlignment(QtCore.Qt.AlignCenter)
        self.preview_vertical_layout.insertWidget(0, self.position_slider)

        self.error_label = QtWidgets.QLabel()
        self.error_label.setSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum
        )
        self.preview_vertical_layout.insertWidget(0, self.error_label)
        self.error_label.hide()

        self.setup_video_player()

    def setup_video_player(self):
        self.preview_url = os.path.join(
            "movies",
            "originals",
            "preview-files",
            self.preview_file["id"] + "." + self.preview_file["extension"],
        )
        self.open_file(self.preview_url)

        self.media_player = QtMultimedia.QMediaPlayer(
            None, QtMultimedia.QMediaPlayer.StreamPlayback
        )

        self.video_widget = CustomVideoWidget(self.parent)
        self.preview_vertical_layout.insertWidget(0, self.video_widget)

        self.media_player.setVideoOutput(self.video_widget)
        self.media_player.stateChanged.connect(self.media_state_changed)
        self.media_player.positionChanged.connect(self.position_changed)
        self.media_player.durationChanged.connect(self.duration_changed)
        self.media_player.mediaStatusChanged.connect(self.status_changed)
        self.media_player.error.connect(self.handle_error)
        self.media_player.setVolume(50)
        self.media_player.setMedia(QtMultimedia.QMediaContent(), self.buffer)
        self.play_button.setEnabled(True)


    def open_file(self, url):
        """
        Open the video file from the url.
        """
        try:
            self.buffer = QtCore.QBuffer()
            with get_file_data_from_url(url) as data:
                self.data = data.content
                self.buffer.setData(self.data)
                self.buffer.open(QtCore.QIODevice.ReadOnly)
        except:
            raise MediaNotSetUp()

    def play(self):
        """
        Play/pause the player.
        """
        if self.media_player.state() == QtMultimedia.QMediaPlayer.PlayingState:
            self.media_player.pause()
        else:
            self.media_player.play()

    def media_state_changed(self):
        if self.media_player.state() == QtMultimedia.QMediaPlayer.PlayingState:
            self.play_button.setIcon(
                self.style().standardIcon(QtWidgets.QStyle.SP_MediaPause)
            )
        else:
            self.play_button.setIcon(
                self.style().standardIcon(QtWidgets.QStyle.SP_MediaPlay)
            )

    def position_changed(self, position):
        position /= 1000

        if not self.position_slider.isSliderDown():
            self.position_slider.setValue(position)

        self.update_duration_info(position)

    def update_duration_info(self, current_info):
        if current_info or self.duration:
            currentTime = QtCore.QTime(
                (current_info / 3600) % 60,
                (current_info / 60) % 60,
                current_info % 60,
                (current_info * 1000) % 1000,
            )
            totalTime = QtCore.QTime(
                (self.duration / 3600) % 60,
                (self.duration / 60) % 60,
                self.duration % 60,
                (self.duration * 1000) % 1000,
            )

            format = "hh:mm:ss" if self.duration > 3600 else "mm:ss"
            tStr = (
                currentTime.toString(format)
                + " / "
                + totalTime.toString(format)
            )
        else:
            tStr = ""

        self.timer_label.setText(tStr)

    def duration_changed(self, duration):
        self.duration = duration / 1000
        self.position_slider.setRange(0, self.duration)

    def status_changed(self, status):
        if status == QtMultimedia.QMediaPlayer.EndOfMedia:
            self.set_position(0)
            self.play()

    def set_position(self, position):
        self.media_player.setPosition(position * 1000)

    def handle_error(self):
        self.play_button.setEnabled(False)
        self.error_label.setText("Error: " + self.media_player.errorString())
        self.error_label.show()

    def get_height(self):
        """
        Return the height of the widget.
        """
        return (
            self.toolbar_widget.height()
            + self.video_widget.sizeHint().height()
            + self.position_slider.height()
            + self.preview_vertical_layout.spacing()
        )

    def clear_setup_media_widget(self):
        """
        Clear all the children widgets.
        """
        for i in reversed(range(self.preview_vertical_layout.count())):
            widget = self.preview_vertical_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()
