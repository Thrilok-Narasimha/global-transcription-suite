# Global Professional Transcription Suite

A powerful desktop application for automatic speech transcription and translation with professional formatting capabilities.

![Application Screenshot](assets/screenshot.png)

## Features

- **Real-time transcription** with high accuracy speech recognition
- **Multi-language support** with automatic language detection
- **Professional text formatting** including removal of filler words and proper punctuation
- **Translation capabilities** to convert speech between 30+ languages
- **Transcript history management** for easy access to previous sessions
- **Export options** for saving transcripts in various formats
- **Customizable settings** for audio processing and text formatting

## Installation

### Prerequisites

- Python 3.8+
- Required packages (automatically installed with pip)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/global-transcription-suite.git
   cd global-transcription-suite
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python src/app.py
   ```

## Usage

### Basic Transcription

1. Select your microphone from the dropdown menu
2. Choose your target language
3. Click "Start Transcription" to begin
4. Speak clearly into your microphone
5. View real-time transcription results in the main panel
6. Click "Stop Transcription" when finished

### Advanced Options

- **Noise Reduction**: Adjust the slider to filter out background noise
- **Remove filler words**: Automatically remove "um", "uh", "like", etc.
- **Fix punctuation**: Automatically add proper punctuation to the transcript
- **Fix capitalization**: Ensure proper capitalization of sentences and proper nouns

### Managing Transcripts

- Save transcripts manually or enable auto-save in settings
- Access previous transcripts in the History tab
- Export transcripts to various formats for external use

## Configuration

Customize the application through the Settings panel:

- **General**: Default save location, transcript format
- **Audio**: Recording quality, energy threshold, phrase timeout
- **Formatting**: Filler words to remove, paragraph breaks, speaker identification

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Speech recognition powered by Google Speech API
- Translation services by Google Translate
- UI built with Tkinter