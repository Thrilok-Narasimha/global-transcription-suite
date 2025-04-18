import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import os
from datetime import datetime

class HistoryTab:
    def __init__(self, parent, app_instance):
        """Initialize the History tab UI"""
        self.parent = parent
        self.app = app_instance
        self.history_files = {}  # Dictionary to map listbox indices to filenames
        
        self.setup_ui()
        self.load_history()
        
    def setup_ui(self):
        """Setup the history tab UI"""
        # Create frames
        list_frame = ttk.Frame(self.parent)
        list_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 10), expand=True, anchor=tk.W)
        
        preview_frame = ttk.Frame(self.parent)
        preview_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # History list
        ttk.Label(list_frame, text="Transcription History:", 
                font=('Helvetica', 11, 'bold')).pack(anchor=tk.W)
        
        self.history_listbox = tk.Listbox(list_frame, width=40, height=25, 
                                        font=('Helvetica', 10))
        self.history_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        history_scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, 
                                        command=self.history_listbox.yview)
        history_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.history_listbox.config(yscrollcommand=history_scrollbar.set)
        
        # Bind selection event
        self.history_listbox.bind('<<ListboxSelect>>', self.on_history_select)
        
        # List controls
        list_controls = ttk.Frame(list_frame)
        list_controls.pack(fill=tk.X, pady=(10, 0))
        
        refresh_btn = ttk.Button(list_controls, text="Refresh", command=self.load_history)
        refresh_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        delete_btn = ttk.Button(list_controls, text="Delete", command=self.delete_history_item)
        delete_btn.pack(side=tk.LEFT)
        
        # Preview area
        ttk.Label(preview_frame, text="Preview:", 
                font=('Helvetica', 11, 'bold')).pack(anchor=tk.W)
        
        self.preview_area = scrolledtext.ScrolledText(preview_frame, wrap=tk.WORD, 
                                                    width=50, height=25, font=('Helvetica', 10))
        self.preview_area.pack(fill=tk.BOTH, expand=True)
        self.preview_area.config(state=tk.DISABLED)
        
        # Preview controls
        preview_controls = ttk.Frame(preview_frame)
        preview_controls.pack(fill=tk.X, pady=(10, 0))
        
        open_btn = ttk.Button(preview_controls, text="Open Full Transcript", 
                            command=self.open_full_transcript)
        open_btn.pack(side=tk.LEFT)
        
        export_btn = ttk.Button(preview_controls, text="Export", 
                              command=self.export_history_item)
        export_btn.pack(side=tk.RIGHT)
    
    def load_history(self):
        """Load transcription history"""
        # Clear current list
        self.history_listbox.delete(0, tk.END)
        self.history_files.clear()  # Clear the mapping dictionary
    
        # Get transcript files from current directory
        transcript_files = [f for f in os.listdir(".") if f.startswith("professional_transcript_") and f.endswith(".txt")]
    
        if not transcript_files:
            self.history_listbox.insert(tk.END, "No transcripts found")
            return
        
        # Sort by date (newest first)
        transcript_files.sort(reverse=True)
    
        # Add to listbox
        for file in transcript_files:
            # Format display name: remove prefix and extension, convert timestamp to readable format
            display_name = file.replace("professional_transcript_", "").replace(".txt", "")
            try:
                # Try to parse timestamp from filename
                date_obj = datetime.strptime(display_name, "%Y%m%d_%H%M%S")
                display_name = date_obj.strftime("%Y-%m-%d %H:%M:%S")
            except ValueError:
                pass  # Use original name if parsing fails
            
            self.history_listbox.insert(tk.END, display_name)
            # Store filename in our dictionary
            index = self.history_listbox.size() - 1
            self.history_files[index] = file
    
    def on_history_select(self, event):
        """Handle selection in history list"""
        selection = self.history_listbox.curselection()
        if not selection:
            return
            
        # Get selected filename
        try:
            index = selection[0]
            filename = self.history_files.get(index)
            if not filename:
                return
        except (IndexError, tk.TclError):
            return

        # Load preview of the file
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                # Read first 2000 characters for preview
                content = file.read(2000)
                
                # Show in preview area
                self.preview_area.config(state=tk.NORMAL)
                self.preview_area.delete("1.0", tk.END)
                self.preview_area.insert(tk.END, content)
                
                # Add ellipsis if truncated
                if len(content) == 2000:
                    self.preview_area.insert(tk.END, "\n\n[...] (Preview truncated)")
                    
                self.preview_area.config(state=tk.DISABLED)
        except Exception as e:
            self.preview_area.config(state=tk.NORMAL)
            self.preview_area.delete("1.0", tk.END)
            self.preview_area.insert(tk.END, f"Error loading file: {e}")
            self.preview_area.config(state=tk.DISABLED)
    
    def delete_history_item(self):
        """Delete selected history item"""
        selection = self.history_listbox.curselection()
        if not selection:
            return
            
        # Get selected filename
        try:
            index = selection[0]
            filename = self.history_files.get(index)
            if not filename:
                return
        except (IndexError, tk.TclError):
            return
        
        if not os.path.exists(filename):
            messagebox.showerror("Error", "File not found.")
            return
            
        # Ask for confirmation
        confirm = messagebox.askyesno("Confirm Delete", 
                                      f"Are you sure you want to delete this transcript?")
        if not confirm:
            return
            
        # Delete file
        try:
            os.remove(filename)
            self.load_history()  # Refresh list
            
            # Clear preview
            self.preview_area.config(state=tk.NORMAL)
            self.preview_area.delete("1.0", tk.END)
            self.preview_area.config(state=tk.DISABLED)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete file: {e}")
    
    def open_full_transcript(self):
        """Open the full transcript file"""
        selection = self.history_listbox.curselection()
        if not selection:
            return
            
        # Get selected filename
        try:
            index = selection[0]
            filename = self.history_files.get(index)
            if not filename:
                return
        except (IndexError, tk.TclError):
            return
        
        if not os.path.exists(filename):
            messagebox.showerror("Error", "File not found.")
            return
            
        # Open the file with system default application
        try:
            import subprocess
            import platform
            
            system = platform.system()
            
            if system == 'Windows':
                os.startfile(filename)
            elif system == 'Darwin':  # macOS
                subprocess.call(('open', filename))
            else:  # Linux and other Unix-like
                subprocess.call(('xdg-open', filename))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open file: {e}")
    
    def export_history_item(self):
        """Export selected history item"""
        selection = self.history_listbox.curselection()
        if not selection:
            return
            
        # Get selected filename
        try:
            index = selection[0]
            filename = self.history_files.get(index)
            if not filename:
                return
        except (IndexError, tk.TclError):
            return
        
        if not os.path.exists(filename):
            messagebox.showerror("Error", "File not found.")
            return
            
        # Open save dialog
        export_filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialfile=os.path.basename(filename)
        )
        
        if not export_filename:
            return
            
        # Copy file to new location
        try:
            with open(filename, 'r', encoding='utf-8') as src:
                content = src.read()
                
            with open(export_filename, 'w', encoding='utf-8') as dst:
                dst.write(content)
                
            messagebox.showinfo("Success", f"Transcript exported to {export_filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export file: {e}")