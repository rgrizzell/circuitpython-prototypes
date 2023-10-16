""" Generate different tones with a buzzer buzzer. """
import audiocore
import audiopwmio
import board
import os
import time

DIR = 'wav'

if __name__ == "__main__":
    out = audiopwmio.PWMAudioOut(board.GP0)
    wav_files = [f for f in os.listdir(DIR) if f.endswith('.wav')]
    for f in wav_files:
        f = f"{DIR}/{f}"
        with open(f, "rb") as o:
            wav = audiocore.WaveFile(o)
            print(f"Playing: {f}")
            out.play(wav)
            while out.playing:
                pass
            time.sleep(1)
