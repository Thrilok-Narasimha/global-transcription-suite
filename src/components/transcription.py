import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog
import threading
import time
import os
from datetime import datetime
import speech_recognition as sr
from googletrans import Translator
from src.utils.audio import AudioProcessor
from src.utils.formatting import TextFormatter

class TranscriptionTab:
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        
        # State variables
        self.is_listening = False
        self.current_thread = None
        self.transcript_file = None
        
        # Initialize recognizer and translator
        self.recognizer = sr.Recognizer()
        self.translator = Translator()
        self.audio_processor = AudioProcessor(self.recognizer)
        self.text_formatter = TextFormatter()
        
        # Initialize language support
        self.supported_languages = self.get_supported_languages()
        self.target_language = "en"  # Default target language is English
        
        # Setup UI
        self.setup_ui()
    
    def get_supported_languages(self):
        """Get list of supported languages with their codes"""
        languages = {
            "en": "English",
            "es": "Spanish",
            "fr": "French",
            "de": "German",
            "it": "Italian",
            "pt": "Portuguese",
            "ru": "Russian",
            "zh-cn": "Chinese (Simplified)",
            "ja": "Japanese",
            "ko": "Korean",
            "ar": "Arabic",
            "hi": "Hindi",
            "bn": "Bengali",
            "ur": "Urdu",
            "tr": "Turkish",
            "vi": "Vietnamese",
            "th": "Thai",
            "id": "Indonesian",
            "ms": "Malay",
            "sv": "Swedish",
            "nl": "Dutch",
            "pl": "Polish",
            "ro": "Romanian",
            "el": "Greek",
            "he": "Hebrew",
            "fa": "Persian",
            "sw": "Swahili",
            "fi": "Finnish",
            "no": "Norwegian",
            "da": "Danish"
        }
        return languages
    
    def setup_ui(self):
        """Setup the transcription tab UI"""
        # Left panel for controls
        control_panel = ttk.Frame(self.parent)
        control_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # Right panel for transcription output
        output_panel = ttk.Frame(self.parent)
        output_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Control panel elements - use a consistent padding
        pad_y = 5
        
        # Section: Input Device
        device_frame = ttk.LabelFrame(control_panel, text="Audio Input", padding="10")
        device_frame.pack(fill=tk.X, pady=pad_y)
        
        ttk.Label(device_frame, text="Microphone:").pack(anchor=tk.W)
        self.mic_var = tk.StringVar()
        self.mic_dropdown = ttk.Combobox(device_frame, textvariable=self.mic_var, width=25)
        self.mic_dropdown.pack(fill=tk.X, pady=(5, 0))
        self.populate_mic_list()
        
        refresh_mic_btn = ttk.Button(device_frame, text="Refresh List", command=self.populate_mic_list)
        refresh_mic_btn.pack(anchor=tk.E, pady=(5, 0))
        
        # Section: Language Settings
        lang_frame = ttk.LabelFrame(control_panel, text="Language Settings", padding="10")
        lang_frame.pack(fill=tk.X, pady=pad_y)
        
        ttk.Label(lang_frame, text="Target Language:").pack(anchor=tk.W)
        self.target_lang_var = tk.StringVar(value="English")
        self.target_lang_dropdown = ttk.Combobox(lang_frame, textvariable=self.target_lang_var, width=25)
        # Populate with language names
        language_names = [name for name in self.supported_languages.values()]
        self.target_lang_dropdown['values'] = sorted(language_names)
        self.target_lang_dropdown.current(language_names.index("English"))
        self.target_lang_dropdown.pack(fill=tk.X, pady=(5, 0))
        self.target_lang_dropdown.bind("<<ComboboxSelected>>", self.on_language_change)
        
        # Automatic language detection option
        self.auto_detect_var = tk.BooleanVar(value=True)
        auto_detect_cb = ttk.Checkbutton(lang_frame, text="Auto-detect source language", 
                                       variable=self.auto_detect_var)
        auto_detect_cb.pack(anchor=tk.W, pady=(5, 0))
        
        # Section: Transcription Controls
        control_frame = ttk.LabelFrame(control_panel, text="Controls", padding="10")
        control_frame.pack(fill=tk.X, pady=pad_y)
        
        self.start_button = ttk.Button(control_frame, text="Start Transcription", 
                                    command=self.start_translation, style='Start.TButton')
        self.start_button.pack(fill=tk.X, pady=(0, 5))
        
        self.stop_button = ttk.Button(control_frame, text="Stop Transcription", 
                                   command=self.stop_translation, style='Stop.TButton',
                                   state=tk.DISABLED)
        self.stop_button.pack(fill=tk.X)
        
        # Section: Advanced Options
        advanced_frame = ttk.LabelFrame(control_panel, text="Advanced Options", padding="10")
        advanced_frame.pack(fill=tk.X, pady=pad_y)
        
        # Noise reduction level
        ttk.Label(advanced_frame, text="Noise Reduction:").pack(anchor=tk.W)
        self.noise_reduction_var = tk.IntVar(value=2)
        noise_scale = ttk.Scale(advanced_frame, from_=0, to=4, variable=self.noise_reduction_var,
                              orient=tk.HORIZONTAL)
        noise_scale.pack(fill=tk.X, pady=(5, 0))
        
        noise_labels = ttk.Frame(advanced_frame)
        noise_labels.pack(fill=tk.X, pady=(0, 5))
        ttk.Label(noise_labels, text="Low").pack(side=tk.LEFT)
        ttk.Label(noise_labels, text="High").pack(side=tk.RIGHT)
        
        # Formatting options
        formatting_frame = ttk.Frame(advanced_frame)
        formatting_frame.pack(fill=tk.X)
        
        self.format_filler_var = tk.BooleanVar(value=True)
        filler_cb = ttk.Checkbutton(formatting_frame, text="Remove filler words", 
                                  variable=self.format_filler_var)
        filler_cb.pack(anchor=tk.W)
        
        self.format_punctuation_var = tk.BooleanVar(value=True)
        punctuation_cb = ttk.Checkbutton(formatting_frame, text="Fix punctuation", 
                                       variable=self.format_punctuation_var)
        punctuation_cb.pack(anchor=tk.W)
        
        self.format_caps_var = tk.BooleanVar(value=True)
        caps_cb = ttk.Checkbutton(formatting_frame, text="Fix capitalization", 
                                variable=self.format_caps_var)
        caps_cb.pack(anchor=tk.W)
        
        # Output panel elements
        ttk.Label(output_panel, text="Professional Transcription:", 
                font=('Helvetica', 11, 'bold')).pack(anchor=tk.W)
        
        # Transcription output area with context menu
        self.log_area = scrolledtext.ScrolledText(output_panel, wrap=tk.WORD, 
                                               width=60, height=25, font=('Helvetica', 10))
        self.log_area.pack(fill=tk.BOTH, expand=True)
        self.log_area.tag_configure('source', foreground='gray')
        self.log_area.tag_configure('translated', foreground='black', font=('Helvetica', 10, 'bold'))
        self.log_area.tag_configure('info', foreground=self.app.primary_color)
        self.log_area.config(state=tk.DISABLED)
        
        # Add right-click menu for copy/clear
        self.create_context_menu(self.log_area)
        
        # Buttons below transcript
        button_frame = ttk.Frame(output_panel)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        save_button = ttk.Button(button_frame, text="Save Transcript", command=self.save_transcript)
        save_button.pack(side=tk.LEFT, padx=(0, 5))
        
        clear_button = ttk.Button(button_frame, text="Clear", command=self.clear_transcript)
        clear_button.pack(side=tk.LEFT)
        
        export_button = ttk.Button(button_frame, text="Export as Document", command=self.export_as_doc)
        export_button.pack(side=tk.RIGHT)
    
    def create_context_menu(self, widget):
        """Create right-click context menu for text widgets"""
        context_menu = tk.Menu(widget, tearoff=0)
        
        context_menu.add_command(label="Copy", command=lambda: self.copy_text(widget))
        context_menu.add_command(label="Select All", command=lambda: self.select_all_text(widget))
        context_menu.add_separator()
        context_menu.add_command(label="Clear", command=lambda: self.clear_text(widget))
        
        widget.bind("<Button-3>", lambda event: self.show_context_menu(event, context_menu))
    
    def show_context_menu(self, event, menu):
        """Show the context menu on right-click"""
        menu.post(event.x_root, event.y_root)
    
    def copy_text(self, widget):
        """Copy selected text to clipboard"""
        try:
            selected_text = widget.get(tk.SEL_FIRST, tk.SEL_LAST)
            self.parent.clipboard_clear()
            self.parent.clipboard_append(selected_text)
        except tk.TclError:
            pass  # No selection
    
    def select_all_text(self, widget):
        """Select all text in the widget"""
        widget.tag_add(tk.SEL, "1.0", tk.END)
        widget.mark_set(tk.INSERT, "1.0")
        widget.see(tk.INSERT)
        return 'break'
    
    def clear_text(self, widget):
        """Clear text from widget"""
        if widget == self.log_area:
            self.clear_transcript()
        else:
            widget.config(state=tk.NORMAL)
            widget.delete("1.0", tk.END)
            widget.config(state=tk.DISABLED)
    
    def clear_transcript(self):
        """Clear the transcript area"""
        self.log_area.config(state=tk.NORMAL)
        self.log_area.delete("1.0", tk.END)
        self.log_area.config(state=tk.DISABLED)
    
    def populate_mic_list(self):
        """Populate the microphone dropdown with available devices"""
        try:
            mic_list = sr.Microphone.list_microphone_names()
            self.mic_dropdown['values'] = mic_list
            if mic_list:
                self.mic_dropdown.current(0)
        except Exception as e:
            self.log(f"Error retrieving microphone list: {e}", tag='info')
    
    def log(self, message, tag='info'):
        """Add message to log area with formatting"""
        self.log_area.config(state=tk.NORMAL)
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        if tag == 'translated':
            self.log_area.insert(tk.END, f"[{timestamp}] {message}\n\n", tag)
        else:
            self.log_area.insert(tk.END, f"[{timestamp}] {message}\n", tag)
            
        self.log_area.see(tk.END)
        self.log_area.config(state=tk.DISABLED)
    
    def on_language_change(self, event=None):
        """Handle target language change"""
        selected_lang_name = self.target_lang_var.get()
        # Find the language code for the selected name
        for code, name in self.supported_languages.items():
            if name == selected_lang_name:
                self.target_language = code
                break
    
    def save_transcript(self):
        """Save current transcript to a file"""
        if not self.transcript_file or not os.path.exists(self.transcript_file):
            self.save_transcript_as()
            return
            
        # Get current text
        text = self.log_area.get("1.0", tk.END)
        
        # Save to file
        with open(self.transcript_file, 'w', encoding='utf-8') as file:
            file.write(text)
            
        self.log(f"Transcript saved to {self.transcript_file}", tag='info')
    
    def save_transcript_as(self):
        """Save transcript to a new file"""
        # Create a default filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_filename = f"professional_transcript_{timestamp}.txt"
        
        # Open file dialog
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialfile=default_filename
        )
        
        if not filename:
            return  # User cancelled
            
        # Get current text
        text = self.log_area.get("1.0", tk.END)
        
        # Save to file
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(text)
            
        self.transcript_file = filename
        self.log(f"Transcript saved to {filename}", tag='info')
        
        # Refresh history in history tab
        if hasattr(self.app, 'history_component'):
            self.app.history_component.load_history()
    
    def export_as_doc(self):
        """Export transcript to a document format"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_filename = f"professional_transcript_{timestamp}.txt"
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialfile=default_filename
        )
        
        if not filename:
            return
            
        # Get current text
        text = self.log_area.get("1.0", tk.END)
        
        # Add header
        header = f"PROFESSIONAL TRANSCRIPTION\n"
        header += f"Date: {datetime.now().strftime('%Y-%m-%d')}\n"
        header += f"Time: {datetime.now().strftime('%H:%M:%S')}\n"
        header += f"Target Language: {self.target_lang_var.get()}\n"
        header += "=" * 50 + "\n\n"
        
        # Save to file
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(header + text)
            
        self.log(f"Transcript exported to {filename}", tag='info')
    
    def start_translation(self):
        """Start the translation/transcription process"""
        if self.is_listening:
            return
            
        # Update button states
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        
        # Create new transcript file if auto-save is on
        settings = self.app.settings_manager.get_settings()
        if settings.get('auto_save', True):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.transcript_file = f"professional_transcript_{timestamp}.txt"
        
        # Update status
        self.app.status_var.set("Listening...")
        self.is_listening = True
        
        # Start listening in a separate thread
        self.current_thread = threading.Thread(target=self.listen_and_translate)
        self.current_thread.daemon = True
        self.current_thread.start()
        
    def stop_translation(self):
        """Stop the translation/transcription process"""
        self.is_listening = False
        self.app.status_var.set("Stopped")
        
        # Update button states
        self.stop_button.config(state=tk.DISABLED)
        self.start_button.config(state=tk.NORMAL)
        
        # Log stop event
        self.log("Transcription stopped", tag='info')
        
    def listen_and_translate(self):
        """Main function to listen to audio and translate in real-time"""
        # Get the selected microphone
        mic_index = self.mic_dropdown.current()
        
        # Handle no microphones case
        if mic_index < 0:
            self.log("No microphone selected", tag='info')
            self.stop_translation()
            return
        
        try:
            with sr.Microphone(device_index=mic_index) as source:
                # Configure audio processor
                settings = self.app.settings_manager.get_settings()
                
                # Adjust for ambient noise
                self.log("Adjusting for ambient noise...", tag='info')
                self.audio_processor.adjust_for_ambient_noise(source)
                
                # Set noise reduction based on slider
                self.audio_processor.set_noise_reduction(self.noise_reduction_var.get())
                
                # Configure energy threshold from settings
                if 'energy_threshold' in settings:
                    self.recognizer.energy_threshold = settings['energy_threshold']
                
                # Configure phrase timeout
                phrase_timeout = settings.get('phrase_timeout', 1.0)
                
                self.log("Ready for speech", tag='info')
                
                # Main listening loop
                while self.is_listening:
                    try:
                        # Listen for audio
                        audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                        
                        # Update status
                        self.app.status_var.set("Processing speech...")
                        
                        # Process the audio
                        result = self.audio_processor.process_audio(
                            audio, 
                            auto_detect=self.auto_detect_var.get(),
                            target_language=self.target_language
                        )
                        
                        if result:
                            original_text, translated_text, detected_lang = result
                            
                            # Log the recognized text
                            self.log(f"Recognized: {original_text}", tag='source')
                            
                            # Format the text based on user settings
                            formatting_options = {
                                'remove_fillers': self.format_filler_var.get(),
                                'fix_punctuation': self.format_punctuation_var.get(),
                                'fix_caps': self.format_caps_var.get(),
                                'filler_words': settings.get('filler_words', "um, uh, like, you know").split(',')
                            }
                            
                            formatted_text = self.text_formatter.format_text(
                                translated_text if translated_text else original_text,
                                **formatting_options
                            )
                            
                            # Log the formatted/translated text
                            self.log(formatted_text, tag='translated')
                            
                            # Auto-save if enabled
                            if self.transcript_file and settings.get('auto_save', True):
                                self.save_transcript()
                        
                        # Update status
                        self.app.status_var.set("Listening...")
                            
                    except sr.WaitTimeoutError:
                        # No speech detected, continue listening
                        continue
                    except sr.UnknownValueError:
                        # Speech was unintelligible
                        self.app.status_var.set("Could not understand audio")
                        time.sleep(1)
                        self.app.status_var.set("Listening...")
                    except Exception as e:
                        # Log other errors
                        self.log(f"Error: {e}", tag='info')
                        time.sleep(1)
        
        except Exception as e:
            self.log(f"Microphone error: {e}", tag='info')
            
        finally:
            # Ensure buttons are reset
            self.parent.after(0, self.reset_buttons)
    
    def reset_buttons(self):
        """Reset button states"""
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.is_listening = False
        self.app.status_var.set("Ready")