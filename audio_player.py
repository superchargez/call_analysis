import numpy as np
import pygame
import tkinter as tk
from pydub import AudioSegment
import tempfile
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# Load the audio file with PyDub
audio_data = AudioSegment.from_file(r'E:\pyprojects\audio\ptcl\AudioAnalysis\static\audio\715631816.wav')
if audio_data.channels == 2:
    audio_data = audio_data.set_channels(1)
audio_array = np.array(audio_data.get_array_of_samples())
samplingFrequency = audio_data.frame_rate
# Create a temporary file and save the audio data to it
temp_file = tempfile.NamedTemporaryFile(delete=False)
audio_data.export(temp_file.name, format="wav")
temp_file.close()  # Close the file so that Pygame can open it

# Initialize the mixer
pygame.mixer.init()

# Load the temporary file with Pygame
pygame.mixer.music.load(temp_file.name)

# Create a Tkinter window
window = tk.Tk()

# Create a new figure and subplot for the waveform plot
figure, subplot = plt.subplots()

# Create an array of time points in seconds
num_samples = len(audio_data.get_array_of_samples())
timePoints = np.arange(num_samples) / audio_data.frame_rate

# Display the waveform plot
subplot.plot(timePoints, audio_data.get_array_of_samples())

# Create a canvas to display the plot in Tkinter window
canvas = FigureCanvasTkAgg(figure, master=window)
canvas.draw()
canvas.get_tk_widget().pack()

# Create a Scale widget to act as the seek bar
seek_bar = tk.Scale(window, from_=0, to=audio_data.duration_seconds, length=500, orient='horizontal', sliderlength=10)

dragging = False  # Variable to track whether the slider is being dragged

def start_playback():
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.unpause()
    else:
        pygame.mixer.music.play(start=seek_bar.get())
        if position_entry.get() != '':
            seek_bar.set(float(position_entry.get()))

def stop_playback():
    pygame.mixer.music.stop()
    seek_bar.set(0)  # Reset the slider when stopping playback

def update_seek_bar():
    global dragging
    # Update the position of the seek bar slider to match the current position of the song
    if pygame.mixer.music.get_busy() and not dragging:
        seek_bar.set(pygame.mixer.music.get_pos() / 1000)

    # Check if the window still exists before scheduling the next call
    if window.winfo_exists():
        # Schedule the function to be called again after 1000ms (1 second)
        window.after(1000, update_seek_bar)

def seek(event):
    global dragging
    # Seek to the position selected by the user by clicking on the seek bar
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.pause()
        pygame.mixer.music.unpause()
        pygame.mixer.music.set_pos(seek_bar.get())
        pygame.mixer.music.pause()
    dragging = False

def seek_to_position():
    # Seek to the position entered in the entry widget
    if position_entry.get() != '':
        position = float(position_entry.get())
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play(start=position)
        else:
            pygame.mixer.music.pause()
            pygame.mixer.music.unpause()
            pygame.mixer.music.set_pos(position)
            pygame.mixer.music.pause()
        seek_bar.set(position)

def start_drag(event):
    global dragging
    dragging = True

# Bind the seek function to ButtonRelease-1 event (which is triggered when the user releases the left mouse button)
seek_bar.bind('<ButtonRelease-1>', seek)
seek_bar.bind('<Button-1>', start_drag)

# Create Play and Stop buttons
play_button = tk.Button(window, text='Play', command=start_playback)
stop_button = tk.Button(window, text='Stop', command=stop_playback)

# Create an Entry widget for seeking to a specific position
position_entry = tk.Entry(window)
seek_button = tk.Button(window, text='Seek', command=seek_to_position)

# Pack everything into the window
seek_bar.pack()
play_button.pack()
stop_button.pack()
position_entry.pack()
seek_button.pack()
update_seek_bar()

# Define a function to stop playback and destroy the window
def on_closing():
    pygame.mixer.music.stop()
    window.destroy()

# Set this function to be called when the window is closed
window.protocol("WM_DELETE_WINDOW", on_closing)

# Start the Tkinter event loop
window.mainloop()
