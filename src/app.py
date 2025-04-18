"""
Global Professional Transcription Suite - Main Application

A professional desktop application for automatic speech transcription and translation
with professional formatting capabilities.
"""
import tkinter as tk
from tkinter import ttk
import os
from src.components.transcription import TranscriptionTab
from src.components.history import HistoryTab
from src.utils.settings import SettingsManager

class GlobalTranscriptionSuite:
    def __init__(self, root):
        self.root = root
        self.root.title("Global Professional Transcription Suite")
        self.root.geometry("1000x700")
        
        # Set app theme
        self.setup_theme()
        
        # Initialize settings manager
        self.settings_manager = SettingsManager()
        
        # Set up the UI
        self.setup_ui()
        
        # Load user settings
        self.settings_manager.load_settings()
        
    def setup_theme(self):
        """Configure the application theme and styles"""
        # Set app theme
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Custom colors
        self.primary_color = "#3498db"  # Blue
        self.secondary_color = "#2c3e50"  # Dark Blue
        self.accent_color = "#e74c3c"  # Red
        self.bg_color = "#f5f5f5"  # Light Gray
        self.text_color = "#2c3e50"  # Dark Blue
        
        # Configure styles
        self.style.configure('TFrame', background=self.bg_color)
        self.style.configure('TLabel', background=self.bg_color, foreground=self.text_color, font=('Helvetica', 10))
        self.style.configure('TButton', background=self.primary_color, foreground='white', borderwidth=0, font=('Helvetica', 10, 'bold'))
        self.style.map('TButton', background=[('active', self.secondary_color)])
        
        # Custom button styles
        self.style.configure('Start.TButton', background=self.primary_color, foreground='white', font=('Helvetica', 10, 'bold'))
        self.style.configure('Stop.TButton', background=self.accent_color, foreground='white', font=('Helvetica', 10, 'bold'))
        self.style.map('Start.TButton', background=[('active', '#2980b9')])
        self.style.map('Stop.TButton', background=[('active', '#c0392b')])
        
        # Set root background
        self.root.configure(bg=self.bg_color)
        
    def setup_ui(self):
        """Set up the main user interface"""
        # Main container
        main_container = ttk.Frame(self.root, padding="10")
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Header frame with title
        header_frame = ttk.Frame(main_container)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        # App title with styling
        title_label = ttk.Label(header_frame, text="Global Professional Transcription Suite", 
                              font=('Helvetica', 16, 'bold'), foreground=self.primary_color)
        title_label.pack(side=tk.LEFT)
        
        # Settings button
        self.settings_button = ttk.Button(header_frame, text="⚙️ Settings", command=self.open_settings)
        self.settings_button.pack(side=tk.RIGHT)
        
        # Create tabs
        self.notebook = ttk.Notebook(main_container)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Tab 1: Transcription
        transcription_tab = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(transcription_tab, text="Transcription")
        
        # Tab 2: History
        history_tab = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(history_tab, text="History")
        
        # Initialize tab components
        self.transcription_component = TranscriptionTab(transcription_tab, self)
        self.history_component = HistoryTab(history_tab, self)
        
        # Status bar
        status_frame = ttk.Frame(main_container)
        status_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.status_var = tk.StringVar(value="Ready")
        status_indicator = ttk.Label(status_frame, textvariable=self.status_var,
                                   font=('Helvetica', 9), foreground=self.primary_color)
        status_indicator.pack(side=tk.LEFT)
        
        version_label = ttk.Label(status_frame, text="v2.0", font=('Helvetica', 9))
        version_label.pack(side=tk.RIGHT)
    
    def open_settings(self):
        """Open settings dialog"""
        self.settings_manager.open_settings_dialog(self.root, self)

def main():
    """Main application entry point"""
    root = tk.Tk()
    app = GlobalTranscriptionSuite(root)
    root.mainloop()

if __name__ == "__main__":
    main()