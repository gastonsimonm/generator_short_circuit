import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox, Slider

def update(val):
    try:
        f = float(f_box.text)
        Icc_prime_prime = float(Icc_prime_prime_box.text)
        Icc_prime = float(Icc_prime_box.text)
        Icc = float(Icc_box.text)
        Icc_double_prime = float(Icc_double_prime_box.text)
        T_prime_prime = float(T_prime_prime_box.text)
        T_prime = float(T_prime_box.text)
        T = float(T_box.text)
        
        if f <= 0 or Icc_prime_prime <= 0 or Icc_prime <= 0 or Icc <= 0 or Icc_double_prime <= 0 or T_prime_prime <= 0 or T_prime <= 0 or T <= 0:
            raise ValueError("All values must be greater than 0")
        
        w = 2 * np.pi * f
        t = np.linspace(0, 1, 1000)
        
        # Total short-circuit current (AC and DC)
        i_cc = np.sqrt(2) * (Icc_prime_prime * np.exp(-t / T_prime_prime) + Icc_prime * np.exp(-t / T_prime) + Icc) * np.sin(w * t + alpha_slider.val) + np.sqrt(2) * Icc_double_prime * np.exp(-t / T) * np.sin(alpha_slider.val)
        
        # DC short-circuit current
        f_2 = np.sqrt(2) * Icc_double_prime * np.exp(-t / T) * np.sin(alpha_slider.val)
        
        ax.clear()
        ax.plot(t, i_cc, label=r'$i_{cc}(t) = \sqrt{2} \cdot [(I^{\prime\prime}_{cc} - I^{\prime}_{cc}) \cdot e^{-\frac{t}{T^{\prime\prime}_d}} + (I^{\prime}_{cc} - I_{cc}) \cdot e^{-\frac{t}{T^{\prime}_d}} + I_{cc}] \cdot \sin(\omega t + \alpha) + \sqrt{2} \cdot I^{\prime\prime}_{cc} \cdot e^{-\frac{t}{T}} \cdot \sin(\alpha)$', color='blue')
        ax.plot(t, f_2, label=r'$i_{cc-direct}(t) = \sqrt{2} \cdot I^{\prime\prime}_{cc} \cdot e^{-\frac{t}{T}} \cdot \sin(\alpha)$', color='red', linestyle='--')
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Short-Circuit Current (A)')
        ax.set_title('GENERATOR SHORT-CIRCUIT CURRENT')
        ax.legend(fontsize=11)
        ax.grid(True)
        plt.draw()
    except ValueError as e:
        print(f"Error: {e}")

# Function to update the Alpha slider value as a fraction of π
def update_alpha_slider_label(val):
    pi_fraction = val / np.pi  # Convert the value to a fraction of π
    if np.isclose(pi_fraction, 1):
        alpha_slider.valtext.set_text(f'π')
    elif np.isclose(pi_fraction, 0):
        alpha_slider.valtext.set_text('0')
    elif pi_fraction == 0.5:
        alpha_slider.valtext.set_text(r'$\frac{1}{2}\pi$')
    elif pi_fraction == 1.5:
        alpha_slider.valtext.set_text(r'$\frac{3}{2}\pi$')
    elif pi_fraction == 2:
        alpha_slider.valtext.set_text('2π')
    else:
        alpha_slider.valtext.set_text(f'{pi_fraction:.2f}π')
    plt.draw()

fig, ax = plt.subplots(figsize=(12, 8))
fig.canvas.manager.set_window_title('GENERATOR SHORT-CIRCUIT CURRENT - GSM')
plt.subplots_adjust(left=0.1, bottom=0.3, right=0.9, top=0.9)

# Initial values
initial_text = {'f=': '50', "I''cc - I'cc=": '100', "I'cc - Icc=": '10', 'Icc=': '2', "I''cc=": '1',
                "T''d=": '0.5', "T'd=": '0.3', 'T=': '0.1'}

text_boxes = []
for i, (key, value) in enumerate(initial_text.items()):
    box = plt.axes([0.15 + (i % 4) * 0.2, 0.15 - (i // 4) * 0.06, 0.12, 0.04])
    text_box = TextBox(box, key, initial=value)
    text_box.on_submit(update)
    text_boxes.append(text_box)

f_box, Icc_prime_prime_box, Icc_prime_box, Icc_box, Icc_double_prime_box, T_prime_prime_box, T_prime_box, T_box = text_boxes

alpha_slider_ax = plt.axes([0.1, 0.03, 0.8, 0.03])
alpha_slider = Slider(alpha_slider_ax, 'Alpha', 0, 2*np.pi, valinit=np.pi/4)


alpha_slider.on_changed(update_alpha_slider_label)
alpha_slider.on_changed(update)  

update(None)  # Initial plot

plt.show()
