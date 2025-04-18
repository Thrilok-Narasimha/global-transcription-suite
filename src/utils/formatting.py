import re

class TextFormatter:
    """Class that handles all text formatting operations"""
    
    def __init__(self):
        # Default filler words to remove
        self.default_filler_words = [
            "um", "uh", "like", "you know", "so", "actually", 
            "basically", "literally", "I mean", "right", "okay",
            "hmm", "err", "sort of", "kind of"
        ]
        
        # Common proper nouns to capitalize
        self.common_proper_nouns = [
            "i", "monday", "tuesday", "wednesday", "thursday", 
            "friday", "saturday", "sunday", "january", "february", 
            "march", "april", "may", "june", "july", "august", 
            "september", "october", "november", "december",
            "america", "europe", "asia", "africa", "australia",
            "united states", "canada", "mexico", "china", "japan",
            "india", "russia", "germany", "france", "uk", "england",
            "brazil", "australia", "italy", "spain"
        ]
    
    def format_text(self, text, remove_fillers=True, fix_punctuation=True, 
                   fix_capitalization=True, filler_words=None):
        """Apply formatting options to text"""
        if not text:
            return text
            
        if remove_fillers:
            text = self.remove_filler_words(text, filler_words)
        
        if fix_punctuation:
            text = self.fix_punctuation(text)
        
        if fix_capitalization:
            text = self.fix_capitalization(text)
        
        return text
    
    def remove_filler_words(self, text, filler_words=None):
        """Remove filler words from the text"""
        # Use custom filler words if provided, otherwise use defaults
        words_to_remove = filler_words if filler_words else self.default_filler_words
        
        # Remove each filler word
        for word in words_to_remove:
            pattern = r'\b' + re.escape(word) + r'\b'
            text = re.sub(pattern, '', text, flags=re.IGNORECASE)
        
        # Clean up extra spaces
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def fix_punctuation(self, text):
        """Fix common punctuation issues"""
        # Add period at end if missing
        if not text.endswith(('.', '!', '?')):
            text += '.'
        
        # Fix spacing after punctuation
        text = re.sub(r'([.,!?;:])(\w)', r'\1 \2', text)
        
        # Fix repeated punctuation
        text = re.sub(r'([.,!?;:])+', r'\1', text)
        
        # Fix spacing before punctuation
        text = re.sub(r'\s+([.,!?;:])', r'\1', text)
        
        # Fix quotation mark spacing
        text = re.sub(r'"(\s+)', r'" ', text)
        text = re.sub(r'(\s+)"', r' "', text)
        
        # Add spaces after commas if missing
        text = re.sub(r',([^\s])', r', \1', text)
        
        return text
    
    def fix_capitalization(self, text):
        """Fix capitalization issues"""
        # Capitalize first letter of sentences
        text = re.sub(r'(^|[.!?]\s+)([a-z])', lambda m: m.group(1) + m.group(2).upper(), text)
        
        # Fix proper nouns
        for word in self.common_proper_nouns:
            pattern = r'\b' + word + r'\b'
            text = re.sub(pattern, word.capitalize(), text, flags=re.IGNORECASE)
        
        # Fix "i" personal pronoun
        text = re.sub(r'\bi\b', 'I', text)
        
        # Fix capitalization after quotes
        text = re.sub(r'"([a-z])', lambda m: '"' + m.group(1).upper(), text)
        
        return text
    
    def get_formatted_export(self, text, metadata=None):
        """Create a formatted export with metadata"""
        header = "PROFESSIONAL TRANSCRIPTION\n"
        
        if metadata:
            for key, value in metadata.items():
                header += f"{key}: {value}\n"
        
        header += "=" * 50 + "\n\n"
        
        return header + text
    
    def detect_paragraphs(self, text, min_pause_seconds=2.0):
        """Split text into paragraphs based on pause markers"""
        # This is a placeholder - in a real implementation,
        # timestamps would be used to detect pauses
        return text
    
    def identify_speakers(self, text):
        """Identify different speakers in the transcript"""
        # This is a placeholder for speaker diarization
        # In a real implementation, this would use audio analysis
        return text