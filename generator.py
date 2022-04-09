import numpy as np
from scipy.io.wavfile import write
import scipy.signal
import matplotlib.pyplot as plt
from scipy.fft import fft
import pandas as pd


class Generator:
    def __init__(self, xmin, xmax, zakres):
        self.t = np.linspace(xmin, xmax, zakres)

    def sine(self, f, amp):
        y = np.int16(amp * np.sin(2 * np.pi * f * self.t) * 32767)
        data = {"t": self.t, "y": y}
        pd.DataFrame(data).to_csv("function.csv", index=False, sep="\t")

    def square(self, f, amp):
        y = np.int16(amp * scipy.signal.square(2 * np.pi * f * self.t) * 32767)
        data = {"t": self.t, "y": y}
        pd.DataFrame(data).to_csv("function.csv", index=False, sep="\t")

    def sawtooth(self, f, amp):
        y = np.int16(amp * scipy.signal.sawtooth(2 * np.pi * f * self.t) * 32767)
        data = {"t": self.t, "y": y}
        pd.DataFrame(data).to_csv("function.csv", index=False, sep="\t")

    def triangle(self, f, amp):
        y = np.int16(amp * scipy.signal.sawtooth(2 * np.pi * f * self.t, 0.5) * 32767)
        data = {"t": self.t, "y": y}
        pd.DataFrame(data).to_csv("function.csv", index=False, sep="\t")

    def white_noise(self, amp):
        y = np.int16(amp * np.sin((2*np.pi*np.random.rand(len(self.t))) * self.t) * 32767)
        data = {"t": self.t, "y": y}
        pd.DataFrame(data).to_csv("function.csv", index=False, sep="\t")

    def show_plot(self, f):
        dane = pd.read_csv(r"function.csv", sep="\t")
        y = np.array(dane["y"])
        plt.plot(self.t, y)
        plt.xlim(0, (1/f)*5)
        plt.show()

    def ttf(self, function):
        n = len(self.t)
        dt = self.t[1] - self.t[0]
        yf = 2.0 / n * np.abs(fft(function)[0:n // 2])
        xf = np.fft.fftfreq(n, d=dt)[0:n // 2]
        return xf, yf

    def show_ttf(self):
        dane = pd.read_csv(r"ttf.csv", sep="\t")
        xf = np.array(dane["x"])
        yf = np.array(dane["y"])
        plt.plot(xf, yf)
        plt.grid()
        plt.xlim(0, 5000)
        plt.show()

    def save_ttf(self, function):
        x, y = self.ttf(function)
        data = {"x": x, "y": y}
        pd.DataFrame(data).to_csv("ttf.csv", index=False, sep="\t")

    def save_function_to_wav(self, name):
        dane = pd.read_csv(r"function.csv", sep="\t")
        y = np.int16(dane["y"])
        write(name, 44100, y)
