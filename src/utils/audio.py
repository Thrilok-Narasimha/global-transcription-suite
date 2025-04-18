import speech_recognition as sr
import threading
import time
from datetime import datetime

class AudioProcessor:
    def __init__(self, app_instance):
        """Initialize audio processing functionality"""
        self.app = app_instance
        self.recognizer = sr.Recognizer()
        self.is_listening = False
        self.current_thread = None
    
    def adjust_noise_level(self, level):
        """Adjust noise reduction level based on slider"""
        if level == 0:
            self.recognizer.dynamic_energy_threshold = True
            self.recognizer.energy_adjustment_ratio = 1.5
        elif level == 1:
            self.recognizer.dynamic_energy_threshold = True
            self.recognizer.energy_adjustment_ratio = 1.2
        elif level == 2:
            self.recognizer.dynamic_energy_threshold = True
            self.recognizer.energy_adjustment_ratio = 1.0
        elif level == 3:
            self.recognizer.dynamic_energy_threshold = False
            self.recognizer.energy_threshold = 300
        else:
            self.recognizer.dynamic_energy_threshold = False
            self.recognizer.energy_threshold = 400
    
    def populate_mic_list(self):
        """Populate the microphone dropdown with available devices"""
        try:
            mic_list = sr.Microphone.list_microphone_names()
            return mic_list
        except Exception as e:
            print(f"Error retrieving microphone list: {e}")
            return []
    
    def start_listening(self, mic_index, auto_detect, target_language, format_filler, format_punctuation, format_caps):
        """Start the audio listening process in a separate thread"""
        if self.is_listening:
            return False
            
        self.is_listening = True
        
        # Start listening in a separate thread
        self.current_thread = threading.Thread(
            target=self.listen_and_process,
            args=(mic_index, auto_detect, target_language, format_filler, format_punctuation, format_caps)
        )
        self.current_thread.daemon = True
        self.current_thread.start()
        
        return True
    
    def stop_listening(self):
        """Stop the audio listening process"""
        self.is_listening = False
        return True
    
    def listen_and_process(self, mic_index, auto_detect, target_language, format_filler, format_punctuation, format_caps):
        """Main function to listen to audio and process in real-time"""
        from .formatting import TextFormatter
        
        # Create formatter
        formatter = TextFormatter()
        
        try:
            with sr.Microphone(device_index=mic_index) as source:
                # Adjust for ambient noise
                self.app.log("Adjusting for ambient noise...", tag='info')
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                
                # Configure based on settings
                noise_level = self.app.noise_reduction_var.get()
                self.adjust_noise_level(noise_level)
                
                # Configure phrase timeout
                phrase_timeout = 1.0
                if hasattr(self.app, 'phrase_timeout_var'):
                    phrase_timeout = self.app.phrase_timeout_var.get()
                
                self.app.log("Ready for speech", tag='info')
                
                # Main listening loop
                while self.is_listening:
                    try:
                        # Listen for audio
                        audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                        
                        # Update status
                        self.app.status_var.set("Processing speech...")
                        
                        # Recognize speech
                        if auto_detect:
                            # Auto-detect language
                            text = self.recognizer.recognize_google(audio)
                            # Detect language of text
                            try:
                                detected_lang = self.app.translator.detect(text).lang
                                self.app.log(f"Detected language: {detected_lang}", tag='info')
                            except:
                                detected_lang = 'en'  # Default to English if detection fails
                                
                            source_lang = detected_lang
                        else:
                            # Default to English as source
                            source_lang = 'en'
                            text = self.recognizer.recognize_google(audio, language=source_lang)
                        
                        # Log the recognized text
                        self.app.log(f"Recognized: {text}", tag='source')
                        
                        # Translate if target language is different
                        if source_lang != target_language:
                            try:
                                translated = self.app.translator.translate(
                                    text, src=source_lang, dest=target_language).text
                                    
                                # Apply formatting
                                if format_filler or format_punctuation or format_caps:
                                    translated = formatter.format_text(
                                        translated, 
                                        remove_fillers=format_filler,
                                        fix_punctuation=format_punctuation,
                                        fix_capitalization=format_caps,
                                        filler_words=self.app.get_filler_words()
                                    )
                                
                                # Log the translated text
                                self.app.log(translated, tag='translated')
                            except Exception as e:
                                self.app.log(f"Translation error: {e}", tag='info')
                                # Use the original text with formatting
                                formatted_text = formatter.format_text(
                                    text,
                                    remove_fillers=format_filler,
                                    fix_punctuation=format_punctuation,
                                    fix_capitalization=format_caps,
                                    filler_words=self.app.get_filler_words()
                                )
                                self.app.log(formatted_text, tag='translated')
                        else:
                            # Apply formatting
                            formatted_text = formatter.format_text(
                                text,
                                remove_fillers=format_filler,
                                fix_punctuation=format_punctuation,
                                fix_capitalization=format_caps,
                                filler_words=self.app.get_filler_words()
                            )
                            
                            # Log the formatted text
                            self.app.log(formatted_text, tag='translated')
                        
                        # Auto-save if enabled
                        if hasattr(self.app, 'transcript_file') and self.app.transcript_file and hasattr(self.app, 'auto_save_var') and self.app.auto_save_var.get():
                            self.app.save_transcript()
                            
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
                        self.app.log(f"Error: {e}", tag='info')
                        time.sleep(1)
        
        except Exception as e:
            self.app.log(f"Microphone error: {e}", tag='info')
            
        finally:
            # Ensure we update UI in the main thread
            self.app.reset_ui_after_listening()