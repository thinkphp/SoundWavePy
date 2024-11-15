import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout,
                            QHBoxLayout, QWidget, QLabel, QSlider, QFileDialog,
                            QListWidget, QDialog)
from PyQt5.QtCore import Qt, QTimer
from pygame import mixer
import os
from datetime import timedelta

class PlaylistDialog(QDialog):
    def __init__(self, playlist, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Current Playlist")
        self.setGeometry(200, 200, 400, 300)
        self.parent = parent  # Store reference to parent for accessing its methods

        # Set the background color and styles
        self.setStyleSheet("""
            QDialog {
                background-color: #2b2b2b;
            }
            QListWidget {
                background-color: #3b3b3b;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 5px;
            }
            QListWidget::item {
                padding: 5px;
            }
            QListWidget::item:selected {
                background-color: #3498db;
            }
            QLabel {
                color: white;
                font-size: 12px;
            }
            QPushButton {
                border: none;
                padding: 8px;
                border-radius: 4px;
                font-weight: bold;
                color: white;
                background-color: #2ecc71;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """)

        layout = QVBoxLayout()

        # Instructions label
        self.instruction_label = QLabel("Double-click a song to play")
        self.instruction_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.instruction_label)

        # Create list widget
        self.list_widget = QListWidget()
        self.update_playlist(playlist)

        # Connect double-click signal
        self.list_widget.itemDoubleClicked.connect(self.play_selected_song)

        # Create play button
        self.play_button = QPushButton("Play Selected")
        self.play_button.clicked.connect(self.play_selected_song)

        layout.addWidget(self.list_widget)
        layout.addWidget(self.play_button)
        self.setLayout(layout)

    def update_playlist(self, playlist):
        """Update the playlist display"""
        self.list_widget.clear()
        for song in playlist:
            self.list_widget.addItem(os.path.basename(song))

    def play_selected_song(self):
        """Play the selected song"""
        current_item = self.list_widget.currentItem()
        if current_item:
            selected_index = self.list_widget.row(current_item)
            self.parent.play_selected_song(selected_index)
            self.parent.song_label.setText(f"Now Playing: {current_item.text()}")

class MusicPlayer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Music Player")
        self.setGeometry(100, 100, 400, 300)

        # Store reference to playlist dialog
        self.playlist_dialog = None

        # Previous styles remain the same...
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2b2b2b;
            }
            QLabel {
                color: white;
                font-size: 12px;
            }
            QPushButton {
                border: none;
                padding: 8px;
                border-radius: 4px;
                font-weight: bold;
                color: white;
            }
            QPushButton:hover {
                opacity: 0.8;
            }
            QSlider::groove:horizontal {
                border: 1px solid #999999;
                height: 8px;
                background: #4a4a4a;
                margin: 2px 0;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #3498db;
                border: 1px solid #5c5c5c;
                width: 18px;
                margin: -2px 0;
                border-radius: 9px;
            }
        """)

        # Initialize mixer
        mixer.init()

        # Initialize variables
        self.current_song_index = 0
        self.playlist = []
        self.is_playing = False
        self.current_duration = 0

        # Create timer for updating song position
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update_position)

        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Create buttons with their styles
        self.play_button = QPushButton("Play")
        self.pause_button = QPushButton("Pause")
        self.stop_button = QPushButton("Stop")
        self.playlist_button = QPushButton("Show Playlist")
        self.import_folder_button = QPushButton("Import Folder")  # New import folder button
        self.back_button = QPushButton("Back")
        self.forward_button = QPushButton("Forward")
        self.choose_button = QPushButton("Choose Song")

        # Set button styles
        self.play_button.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """)

        self.pause_button.setStyleSheet("""
            QPushButton {
                background-color: #f1c40f;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #f39c12;
            }
        """)

        self.stop_button.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)

        self.playlist_button.setStyleSheet("""
            QPushButton {
                background-color: #1abc9c;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #16a085;
            }
        """)

        self.import_folder_button.setStyleSheet("""
            QPushButton {
                background-color: #16a085;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #1abc9c;
            }
        """)

        for button in [self.back_button, self.forward_button]:
            button.setStyleSheet("""
                QPushButton {
                    background-color: #3498db;
                    min-width: 60px;
                }
                QPushButton:hover {
                    background-color: #2980b9;
                }
            """)

        self.choose_button.setStyleSheet("""
            QPushButton {
                background-color: #9b59b6;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #8e44ad;
            }
        """)

        # Connect button signals
        self.play_button.clicked.connect(self.play_music)
        self.pause_button.clicked.connect(self.pause_music)
        self.stop_button.clicked.connect(self.stop_music)
        self.playlist_button.clicked.connect(self.show_playlist)
        self.import_folder_button.clicked.connect(self.import_folder)  # Connect import folder button
        self.back_button.clicked.connect(self.play_previous)
        self.forward_button.clicked.connect(self.play_next)
        self.choose_button.clicked.connect(self.choose_file)

        # Create labels and sliders
        self.song_label = QLabel("")
        self.song_label.setAlignment(Qt.AlignCenter)
        self.song_label.setStyleSheet("font-size: 14px; color: #ffffff;")

        self.time_label = QLabel("00:00 / 00:00")
        self.time_label.setAlignment(Qt.AlignCenter)
        self.time_label.setStyleSheet("font-size: 14px; color: #ffffff;")

        self.volume_label = QLabel("Volume:")
        self.volume_label.setAlignment(Qt.AlignCenter)

        self.position_label = QLabel("Position:")
        self.position_label.setAlignment(Qt.AlignCenter)

        # Set up sliders
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setMinimum(0)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setValue(50)
        self.volume_slider.valueChanged.connect(self.set_volume)

        self.position_slider = QSlider(Qt.Horizontal)
        self.position_slider.setMinimum(0)
        self.position_slider.setMaximum(100)
        self.position_slider.setValue(0)
        self.position_slider.valueChanged.connect(self.set_position)

        # Layout setup
        nav_layout = QHBoxLayout()
        nav_layout.addWidget(self.back_button)
        nav_layout.addWidget(self.forward_button)

        # Add all widgets to layout
        layout.addSpacing(10)
        layout.addWidget(self.play_button)
        layout.addSpacing(5)
        layout.addWidget(self.pause_button)
        layout.addSpacing(5)
        layout.addWidget(self.stop_button)
        layout.addSpacing(5)
        layout.addWidget(self.playlist_button)
        layout.addSpacing(5)
        layout.addWidget(self.import_folder_button)  # Add import folder button to layout
        layout.addSpacing(10)
        layout.addLayout(nav_layout)
        layout.addSpacing(10)
        layout.addWidget(self.choose_button)
        layout.addSpacing(15)
        layout.addWidget(self.song_label)
        layout.addWidget(self.time_label)
        layout.addSpacing(10)
        layout.addWidget(self.volume_label)
        layout.addWidget(self.volume_slider)
        layout.addWidget(self.position_label)
        layout.addWidget(self.position_slider)
        layout.addSpacing(10)

    def import_folder(self):
        """Import all MP3 files from a selected folder"""
        folder = QFileDialog.getExistingDirectory(
            self,
            "Select Folder",
            "",
            QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
        )
        if folder:
            # Get all MP3 files from the selected folder
            music_files = [os.path.join(folder, f) for f in os.listdir(folder)
                         if f.lower().endswith('.mp3')]

            # Add files to playlist
            self.playlist.extend(music_files)

            # Update display
            if music_files:
                self.song_label.setText(f"Added {len(music_files)} songs from folder")
                # Update playlist dialog if it exists
                if self.playlist_dialog:
                    self.playlist_dialog.update_playlist(self.playlist)
            else:
                self.song_label.setText("No MP3 files found in selected folder")

    def show_playlist(self):
        """Show playlist dialog and create new one if it doesn't exist"""
        if not self.playlist_dialog:
            self.playlist_dialog = PlaylistDialog(self.playlist, self)
        else:
            self.playlist_dialog.update_playlist(self.playlist)
        self.playlist_dialog.show()

    def play_selected_song(self, index):
        """Play a song selected from the playlist"""
        if 0 <= index < len(self.playlist):
            self.current_song_index = index
            self.stop_music()
            self.play_music()

    def choose_file(self):
        file, _ = QFileDialog.getOpenFileName(
            self,
            "Select File",
            "",
            "MP3 Files (*.mp3);;All Files (*.*)"
        )
        if file:
            self.playlist.append(file)
            self.song_label.setText(f"Added: {os.path.basename(file)}")
            # Update playlist dialog if it exists
            if self.playlist_dialog:
                self.playlist_dialog.update_playlist(self.playlist)

    # Rest of the methods remain the same...
    def format_time(self, seconds):
        return str(timedelta(seconds=int(seconds)))[2:7]

    def play_music(self):
        if self.playlist:
            if not self.is_playing:
                mixer.music.load(self.playlist[self.current_song_index])
                mixer.music.play()
                self.is_playing = True
                self.timer.start()

                sound = mixer.Sound(self.playlist[self.current_song_index])
                self.current_duration = sound.get_length()

                self.song_label.setText(f"Now Playing: {os.path.basename(self.playlist[self.current_song_index])}")
                self.update_position()

    def pause_music(self):
        if self.is_playing:
            mixer.music.pause()
            self.is_playing = False
            self.timer.stop()
            self.song_label.setText("Music Paused")

    def stop_music(self):
        mixer.music.stop()
        self.is_playing = False
        self.timer.stop()
        self.position_slider.setValue(0)
        self.time_label.setText("00:00 / 00:00")
        self.song_label.setText("Music Stopped")

    def play_previous(self):
        if self.playlist:
            self.current_song_index = (self.current_song_index - 1) % len(self.playlist)
            self.stop_music()
            self.play_music()

    def play_next(self):
        if self.playlist:
            self.current_song_index = (self.current_song_index + 1) % len(self.playlist)
            self.stop_music()
            self.play_music()

    def set_volume(self, value):
        volume = value / 100
        mixer.music.set_volume(volume)

    def set_position(self, value):
        if self.playlist and self.is_playing:
            position = (value / 100) * self.current_duration
            try:
                mixer.music.set_pos(position)
                self.update_position()
            except:
                pass

    def update_position(self):
        if self.is_playing:
            try:
                current_pos = mixer.music.get_pos() / 1000
                total_time = self.current_duration

                current_time = self.format_time(current_pos)
                total_time_formatted = self.format_time(total_time)
                self.time_label.setText(f"{current_time} / {total_time_formatted}")

                if total_time > 0:
                    slider_pos = (current_pos / total_time) * 100
                    self.position_slider.setValue(int(slider_pos))
            except:
                pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    player = MusicPlayer()
    player.show()
    sys.exit(app.exec_())
