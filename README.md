# PyQt5 MP3 Player

A modern, feature-rich MP3 player built with PyQt5 and Pygame. This application provides a clean, user-friendly interface for playing and managing your music files.

![Player Screenshot](placeholder-image.png)

## Features

- **Modern Dark Theme Interface**: Sleek dark mode design with intuitive controls
- **Basic Playback Controls**:
  - Play/Pause/Stop functionality
  - Previous/Next track navigation
  - Volume control slider
- **Playlist Management**:
  - Add individual songs
  - Import entire folders of MP3 files
  - View and manage current playlist
  - Double-click songs to play from playlist
- **Progress Tracking**:
  - Real-time progress bar
  - Current time and total duration display
- **File Support**:
  - Supports MP3 audio files
  - Drag and drop functionality (planned)

## Requirements

- Python 3.x
- PyQt5
- Pygame

## Installation

1. Ensure you have Python installed on your system
2. Install required packages:
```bash
pip install PyQt5 pygame
```

## Usage

1. Run the application:
```bash
python music_player.py
```

2. Add music to your playlist:
   - Click "Choose Song" to add individual MP3 files
   - Click "Import Folder" to add all MP3 files from a directory
   - Use "Show Playlist" to view and manage your current playlist

3. Playback controls:
   - Use Play/Pause/Stop buttons for basic control
   - Adjust volume using the volume slider
   - Navigate between tracks using Back/Forward buttons
   - Use the progress slider to seek within the current track

## Controls

- **Play Button**: Start playing the current track
- **Pause Button**: Pause the current track
- **Stop Button**: Stop playback completely
- **Back Button**: Go to previous track
- **Forward Button**: Skip to next track
- **Show Playlist**: Open playlist management window
- **Import Folder**: Add all MP3 files from a selected folder
- **Choose Song**: Add individual MP3 files to playlist
- **Volume Slider**: Adjust playback volume
- **Position Slider**: Seek through the current track

## User Interface Features

- Song title display
- Current time and total duration display
- Volume control
- Progress bar with seek functionality
- Playlist management window
- Color-coded buttons for different actions

## Styling

The application features a modern dark theme with:
- Dark backgrounds (#2b2b2b for main window, #3b3b3b for playlist)
- Contrasting text colors (white)
- Color-coded buttons:
  - Green for Play (#2ecc71)
  - Yellow for Pause (#f1c40f)
  - Red for Stop (#e74c3c)
  - Blue for navigation (#3498db)
  - Purple for file selection (#9b59b6)
  - Teal for playlist management (#1abc9c)

## Contributing

Feel free to fork this project and submit pull requests for any improvements you'd like to add. Some potential areas for enhancement:

- Support for additional audio formats
- Shuffle and repeat functionality
- Equalizer
- Playlist saving/loading
- Keyboard shortcuts
- Visualization effects

## License

This project is open source and available under the MIT License.

## Credits

Built with:
- PyQt5 for the graphical interface
- Pygame for audio playback functionality
