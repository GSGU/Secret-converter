import tkinter as tk
from tkinter import ttk, font, messagebox
import random
import string
import json
import os

CIPHER_DIR = "ciphers"  # Directory to store the ciphers
RESULTS_DIR = "results"  # Directory to store the encoded results

# Ensure the directories exist
os.makedirs(CIPHER_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)

# Function to generate a random substitution cipher
def generate_cipher():
    letters = string.ascii_uppercase
    shuffled = list(letters)
    random.shuffle(shuffled)
    return dict(zip(letters, shuffled)), dict(zip(shuffled, letters))

# Function to load data from a specified file
def load_data(filename):
    with open(filename, 'r') as f:
        return json.load(f)

# Function to save data to a specified file
def save_data(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f)

# Function to list saved files in a directory
def list_files(directory):
    return [f for f in os.listdir(directory) if f.endswith('.json')]

# Function to encode text
def encode(text, cipher):
    return ''.join([cipher.get(char.upper(), char) for char in text])

# Function to decode text
def decode(text, reverse_cipher):
    return ''.join([reverse_cipher.get(char.upper(), char) for char in text])

# Load or generate the default cipher
default_cipher_data = generate_cipher()
default_cipher = default_cipher_data[0]
default_reverse_cipher = default_cipher_data[1]

# Function to handle encoding
def on_encode():
    input_text = text_input.get("1.0", tk.END).strip()
    if input_text and current_cipher:
        encoded_text = encode(input_text, current_cipher)
        result_output.delete("1.0", tk.END)
        result_output.insert(tk.END, encoded_text)

# Function to handle decoding
def on_decode():
    input_text = text_input.get("1.0", tk.END).strip()
    if input_text and current_reverse_cipher:
        decoded_text = decode(input_text, current_reverse_cipher)
        result_output.delete("1.0", tk.END)
        result_output.insert(tk.END, decoded_text)

# Function to clear input and result fields
def clear_fields():
    text_input.delete("1.0", tk.END)
    result_output.delete("1.0", tk.END)

# Function to save the current cipher
def save_current_cipher():
    name = cipher_name_entry.get().strip()
    if name:
        filename = os.path.join(CIPHER_DIR, f"{name}.json")
        save_data(filename, {'cipher': current_cipher, 'reverse_cipher': current_reverse_cipher})
        refresh_cipher_list()

# Function to rename the selected cipher
def rename_cipher():
    selected_cipher = cipher_listbox.get(cipher_listbox.curselection())
    new_name = cipher_name_entry.get().strip()
    if new_name:
        old_filename = os.path.join(CIPHER_DIR, selected_cipher)
        new_filename = os.path.join(CIPHER_DIR, f"{new_name}.json")
        
        if os.path.exists(new_filename):
            messagebox.showerror("Error", f"A cipher with the name '{new_name}' already exists. Please choose a different name.")
        else:
            os.rename(old_filename, new_filename)
            refresh_cipher_list()

# Function to delete the selected cipher
def delete_cipher():
    selected_cipher = cipher_listbox.get(cipher_listbox.curselection())
    if selected_cipher:
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{selected_cipher}'?")
        if confirm:
            os.remove(os.path.join(CIPHER_DIR, selected_cipher))
            refresh_cipher_list()

# Function to load the selected cipher
def load_selected_cipher(event):
    selected_cipher = cipher_listbox.get(cipher_listbox.curselection())
    filename = os.path.join(CIPHER_DIR, selected_cipher)
    cipher_data = load_data(filename)
    global current_cipher, current_reverse_cipher
    current_cipher = cipher_data['cipher']
    current_reverse_cipher = cipher_data['reverse_cipher']

# Function to save encoded result
def save_encoded_result():
    result_text = result_output.get("1.0", tk.END).strip()
    name = result_name_entry.get().strip()
    if result_text and name:
        filename = os.path.join(RESULTS_DIR, f"{name}.json")
        save_data(filename, {'result': result_text})
        refresh_result_list()

# Function to rename the selected result
def rename_result():
    selected_result = result_listbox.get(result_listbox.curselection())
    new_name = result_name_entry.get().strip()
    if new_name:
        old_filename = os.path.join(RESULTS_DIR, selected_result)
        new_filename = os.path.join(RESULTS_DIR, f"{new_name}.json")
        
        if os.path.exists(new_filename):
            messagebox.showerror("Error", f"A result with the name '{new_name}' already exists. Please choose a different name.")
        else:
            os.rename(old_filename, new_filename)
            refresh_result_list()

# Function to delete the selected result
def delete_result():
    selected_result = result_listbox.get(result_listbox.curselection())
    if selected_result:
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{selected_result}'?")
        if confirm:
            os.remove(os.path.join(RESULTS_DIR, selected_result))
            refresh_result_list()

# Function to load the selected result
def load_selected_result(event):
    selected_result = result_listbox.get(result_listbox.curselection())
    filename = os.path.join(RESULTS_DIR, selected_result)
    result_data = load_data(filename)
    encoded_text = result_data['result']
    
    # Decode the encoded text using the current reverse cipher
    decoded_text = decode(encoded_text, current_reverse_cipher)
    
    # Clear the result output and insert the decoded text
    result_output.delete("1.0", tk.END)
    result_output.insert(tk.END, decoded_text)

# Create the main window
root = tk.Tk()
root.title("Secret Language Encoder/Decoder")
root.geometry("800x400")  # Set window size to wider
root.configure(bg='#2E2E2E')  # Set dark gray background

# Prevent resizing the main window
root.resizable(False, False)

# Initialize current cipher variables
current_cipher = default_cipher
current_reverse_cipher = default_reverse_cipher

# Define fonts
title_font = font.Font(family="Helvetica", size=16, weight="bold")
button_font = font.Font(family="Helvetica", size=12)
text_font = font.Font(family="Courier", size=10)

# Style configuration
style = ttk.Style()
style.theme_use('clam')
style.configure("TNotebook", background="#2E2E2E", borderwidth=0)
style.configure("TNotebook.Tab", background="#424242", foreground="white", borderwidth=0)
style.map("TNotebook.Tab", background=[("selected", "#333333")], foreground=[("selected", "white")])
style.configure("TButton", background="#333333", foreground="white", borderwidth=1)
style.map("TButton", background=[("active", "#4CAF50"), ("!active", "#333333")])

# Create Notebook (Tabbed Interface)
notebook = ttk.Notebook(root)

# Title Page (Welcome Screen)
title_frame = tk.Frame(notebook, bg='#2E2E2E')
notebook.add(title_frame, text="Home")

label_welcome = tk.Label(title_frame, text="Welcome to the Secret Language Encoder/Decoder", font=title_font, bg='#2E2E2E', fg="white", pady=20)
label_welcome.pack()

label_desc = tk.Label(title_frame, text="Use this app to encode and decode text into a random secret language!\n"
                                        "Navigate through the tabs to Encode, Decode, or learn How It Works.", font=button_font, bg='#2E2E2E', fg="white")
label_desc.pack()

# Encoding/Decoding Page
encode_decode_frame = tk.Frame(notebook, bg='#2E2E2E')
notebook.add(encode_decode_frame, text="Encode/Decode")

# Input text label
label_input = tk.Label(encode_decode_frame, text="Input Text:", font=title_font, bg='#2E2E2E', fg="white")
label_input.pack(anchor="w", padx=10, pady=5)

# Text box for input
text_input = tk.Text(encode_decode_frame, height=5, width=50, font=text_font, bg="#424242", fg="white", insertbackground="white", wrap=tk.WORD)
text_input.pack(padx=10, pady=5, fill=tk.X)

# Buttons to encode, decode, and clear
frame_buttons = tk.Frame(encode_decode_frame, bg='#2E2E2E')
frame_buttons.pack(pady=10)

btn_encode = tk.Button(frame_buttons, text="Encode", command=on_encode, font=button_font, bg="#4CAF50", fg="white", padx=20, pady=10)
btn_encode.grid(row=0, column=0, padx=10)

btn_decode = tk.Button(frame_buttons, text="Decode", command=on_decode, font=button_font, bg="#2196F3", fg="white", padx=20, pady=10)
btn_decode.grid(row=0, column=1, padx=10)

# Clear button
btn_clear = tk.Button(frame_buttons, text="Clear", command=clear_fields, font=button_font, bg="#F44336", fg="white", padx=20, pady=10)
btn_clear.grid(row=0, column=2, padx=10)

# Result label
label_result = tk.Label(encode_decode_frame, text="Result:", font=title_font, bg='#2E2E2E', fg="white")
label_result.pack(anchor="w", padx=10, pady=5)

# Text box for result output
result_output = tk.Text(encode_decode_frame, height=5, width=50, font=text_font, bg="#424242", fg="white", insertbackground="white", wrap=tk.WORD)
result_output.pack(padx=10, pady=5, fill=tk.X)

# Info Page (How It Works)
info_frame = tk.Frame(notebook, bg='#2E2E2E')
notebook.add(info_frame, text="How It Works")

label_info_title = tk.Label(info_frame, text="How It Works", font=title_font, bg='#2E2E2E', fg="white", pady=20)
label_info_title.pack()

info_text = ("This app uses a random substitution cipher to encode text.\n"
             "Each letter is replaced by another randomly chosen letter.\n"
             "For example, A could become U, B could become P, and so on.\n"
             "You can encode any text using the 'Encode' button, and decode\n"
             "the secret message back to its original form using the 'Decode' button.\n\n"
             "You can also save multiple ciphers and select them as needed.")
label_info = tk.Label(info_frame, text=info_text, font=text_font, bg='#2E2E2E', fg="white", justify="left", padx=20)
label_info.pack(anchor="w")

# Cipher Management Page
cipher_management_frame = tk.Frame(notebook, bg='#2E2E2E')
notebook.add(cipher_management_frame, text="Manage Ciphers")

label_cipher_management = tk.Label(cipher_management_frame, text="Manage Ciphers", font=title_font, bg='#2E2E2E', fg="white", pady=20)
label_cipher_management.pack()

label_cipher_name = tk.Label(cipher_management_frame, text="Cipher Name:", font=button_font, bg='#2E2E2E', fg="white")
label_cipher_name.pack(padx=10, pady=5)

cipher_name_entry = tk.Entry(cipher_management_frame, font=text_font, bg="#424242", fg="white")
cipher_name_entry.pack(padx=10, pady=5, fill=tk.X)

# Frame for buttons
frame_buttons = tk.Frame(cipher_management_frame, bg='#2E2E2E')
frame_buttons.pack(pady=10)

btn_save_cipher = tk.Button(frame_buttons, text="Save Current Cipher", command=save_current_cipher, font=button_font, bg="#4CAF50", fg="white", padx=20, pady=10)
btn_save_cipher.grid(row=0, column=0, padx=5)

btn_rename_cipher = tk.Button(frame_buttons, text="Rename Selected Cipher", command=rename_cipher, font=button_font, bg="#FF9800", fg="white", padx=20, pady=10)
btn_rename_cipher.grid(row=0, column=1, padx=5)

btn_delete_cipher = tk.Button(frame_buttons, text="Delete Selected Cipher", command=delete_cipher, font=button_font, bg="#F44336", fg="white", padx=20, pady=10)
btn_delete_cipher.grid(row=0, column=2, padx=5)

label_saved_ciphers = tk.Label(cipher_management_frame, text="Saved Ciphers:", font=button_font, bg='#2E2E2E', fg="white")
label_saved_ciphers.pack(pady=5)

cipher_listbox = tk.Listbox(cipher_management_frame, font=text_font, bg="#424242", fg="white")
cipher_listbox.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

# Load saved ciphers into the listbox
def refresh_cipher_list():
    cipher_listbox.delete(0, tk.END)
    for cipher_file in list_files(CIPHER_DIR):
        cipher_listbox.insert(tk.END, cipher_file)

cipher_listbox.bind('<<ListboxSelect>>', load_selected_cipher)
refresh_cipher_list()

# Results Management Page
results_management_frame = tk.Frame(notebook, bg='#2E2E2E')
notebook.add(results_management_frame, text="Manage Results")

label_results_management = tk.Label(results_management_frame, text="Manage Encoded Results", font=title_font, bg='#2E2E2E', fg="white", pady=20)
label_results_management.pack()

label_result_name = tk.Label(results_management_frame, text="Result Name:", font=button_font, bg='#2E2E2E', fg="white")
label_result_name.pack(padx=10, pady=5)

result_name_entry = tk.Entry(results_management_frame, font=text_font, bg="#424242", fg="white")
result_name_entry.pack(padx=10, pady=5, fill=tk.X)

# Frame for result buttons
frame_result_buttons = tk.Frame(results_management_frame, bg='#2E2E2E')
frame_result_buttons.pack(pady=10)

btn_save_result = tk.Button(frame_result_buttons, text="Save Encoded Result", command=save_encoded_result, font=button_font, bg="#4CAF50", fg="white", padx=20, pady=10)
btn_save_result.grid(row=0, column=0, padx=5)

btn_rename_result = tk.Button(frame_result_buttons, text="Rename Selected Result", command=rename_result, font=button_font, bg="#FF9800", fg="white", padx=20, pady=10)
btn_rename_result.grid(row=0, column=1, padx=5)

btn_delete_result = tk.Button(frame_result_buttons, text="Delete Selected Result", command=delete_result, font=button_font, bg="#F44336", fg="white", padx=20, pady=10)
btn_delete_result.grid(row=0, column=2, padx=5)

label_saved_results = tk.Label(results_management_frame, text="Saved Results:", font=button_font, bg='#2E2E2E', fg="white")
label_saved_results.pack(pady=5)

result_listbox = tk.Listbox(results_management_frame, font=text_font, bg="#424242", fg="white")
result_listbox.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

# Load saved results into the listbox
def refresh_result_list():
    result_listbox.delete(0, tk.END)
    for result_file in list_files(RESULTS_DIR):
        result_listbox.insert(tk.END, result_file)

result_listbox.bind('<<ListboxSelect>>', load_selected_result)
refresh_result_list()

# Add Notebook (Tabs) to the root window
notebook.pack(expand=True, fill="both")

# Start the GUI loop
root.mainloop()
