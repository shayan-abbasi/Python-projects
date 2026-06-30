import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk, messagebox


class TransferFunction:
    def __init__(self, K, order, zeta=None, wn=None, tau=None):
        self.K = K
        self.order = order
        self.zeta = zeta
        self.wn = wn
        self.tau = tau

    def get_description(self):
        if self.order == 1:
            return f"G(s) = {self.K} / ({self.tau}s + 1)"
        else:
            a = self.K * self.wn ** 2
            b = 2 * self.zeta * self.wn
            c = self.wn ** 2
            return f"G(s) = {a:.2f} / (s² + {b:.2f}s + {c:.2f})"

    def get_system_type(self):
        if self.order == 1:
            return "First Order System"
        if self.zeta == 0:
            return "Undamped"
        elif self.zeta < 1:
            return "Underdamped"
        elif self.zeta == 1:
            return "Critically Damped"
        else:
            return "Overdamped"


class StepResponse:
    def __init__(self, tf):
        self.tf = tf

    def compute(self):
        tf = self.tf

        if tf.order == 1:
            t_end = 5 * tf.tau
        else:
            if tf.zeta >= 1:
                t_end = 10 / (tf.zeta * tf.wn)
            else:
                t_end = max(20 / tf.wn, 10 / (tf.zeta * tf.wn + 0.001))

        t = np.linspace(0, t_end, 1000)

        if tf.order == 1:
            y = tf.K * (1 - np.exp(-t / tf.tau))

        else:
            z = tf.zeta
            w = tf.wn
            K = tf.K

            if z == 0:
                y = K * (1 - np.cos(w * t))

            elif z < 1:
                wd = w * np.sqrt(1 - z ** 2)
                phi = z / np.sqrt(1 - z ** 2)
                y = K * (1 - np.exp(-z * w * t) * (np.cos(wd * t) + phi * np.sin(wd * t)))

            elif z == 1:
                y = K * (1 - (1 + w * t) * np.exp(-w * t))

            else:
                s1 = -w * (z - np.sqrt(z ** 2 - 1))
                s2 = -w * (z + np.sqrt(z ** 2 - 1))
                y = K * (1 + (s2 * np.exp(s1 * t) - s1 * np.exp(s2 * t)) / (s1 - s2))

        return t, y


class Analyzer:
    def __init__(self, t, y, tf):
        self.t = t
        self.y = y
        self.tf = tf
        self.y_final = tf.K

    def rise_time(self):
        y10 = 0.1 * self.y_final
        y90 = 0.9 * self.y_final
        t10 = None
        t90 = None
        for i in range(len(self.y)):
            if t10 is None and self.y[i] >= y10:
                t10 = self.t[i]
            if t90 is None and self.y[i] >= y90:
                t90 = self.t[i]
        if t10 is None or t90 is None:
            return None
        return t90 - t10

    def percent_overshoot(self):
        ymax = max(self.y)
        if ymax <= self.y_final * 1.001:
            return 0.0
        return (ymax - self.y_final) / self.y_final * 100

    def peak_time(self):
        mp = self.percent_overshoot()
        if mp > 0.1:
            peak_index = np.argmax(self.y)
            return self.t[peak_index]
        return None

    def settling_time(self):
        upper = self.y_final * 1.02
        lower = self.y_final * 0.98
        last_bad = None
        for i in range(len(self.y)):
            if self.y[i] > upper or self.y[i] < lower:
                last_bad = i
        if last_bad is None:
            return self.t[0]
        if last_bad + 1 >= len(self.t):
            return None
        return self.t[last_bad + 1]

    def steady_state_error(self):
        return abs(self.y_final - self.y[-1])

    def get_all_specs(self):
        return {
            "rise_time": self.rise_time(),
            "peak_time": self.peak_time(),
            "overshoot": self.percent_overshoot(),
            "settling_time": self.settling_time(),
            "steady_state_error": self.steady_state_error()
        }


class Plotter:
    def __init__(self, ax, figure):
        self.ax = ax
        self.figure = figure

    def plot(self, t, y, specs, tf):
        self.ax.clear()
        K = tf.K

        self.ax.plot(t, y, 'b-', linewidth=2, label='y(t)')
        self.ax.axhline(y=K, color='gray', linestyle='--', label=f'Final = {K}')
        self.ax.axhline(y=K * 1.02, color='green', linestyle=':', alpha=0.5)
        self.ax.axhline(y=K * 0.98, color='green', linestyle=':', alpha=0.5)
        self.ax.fill_between(t, K * 0.98, K * 1.02, alpha=0.1, color='green', label='±2% band')

        tr = specs["rise_time"]
        if tr is not None:
            self.ax.axvline(x=tr, color='orange', linestyle='--', label=f'Rise Time = {tr:.3f}s')

        tp = specs["peak_time"]
        mp = specs["overshoot"]
        if tp is not None and mp > 0.1:
            self.ax.axvline(x=tp, color='red', linestyle='--', label=f'Peak Time = {tp:.3f}s')
            self.ax.plot(tp, max(y), 'r*', markersize=12)

        ts = specs["settling_time"]
        if ts is not None:
            self.ax.axvline(x=ts, color='purple', linestyle='-.', label=f'Settling = {ts:.3f}s')

        self.ax.set_xlabel('Time (s)')
        self.ax.set_ylabel('Output y(t)')
        self.ax.set_title('Step Response\n' + tf.get_description())
        self.ax.legend(fontsize=9)
        self.ax.grid(True, alpha=0.3)
        self.ax.set_xlim([0, t[-1]])

        y_min = min(0, min(y)) - 0.05 * abs(K)
        y_max = max(max(y), K) + 0.1 * abs(K)
        self.ax.set_ylim([y_min, y_max])

        self.figure.tight_layout()


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Step Response Analyzer")
        self.root.geometry("1000x650")

        self.order_var = tk.IntVar(value=2)

        left = tk.Frame(root, padx=10, pady=10)
        left.pack(side="left", fill="y")

        tk.Label(left, text="System Order:", font=("Arial", 10, "bold")).pack(anchor="w")

        row = tk.Frame(left)
        row.pack(anchor="w")
        tk.Radiobutton(row, text="1st Order", variable=self.order_var, value=1,
                       command=self.on_order_change).pack(side="left")
        tk.Radiobutton(row, text="2nd Order", variable=self.order_var, value=2,
                       command=self.on_order_change).pack(side="left")

        ttk.Separator(left, orient="horizontal").pack(fill="x", pady=6)

        tk.Label(left, text="K (Gain):").pack(anchor="w")
        self.entry_K = tk.Entry(left, width=15, justify="center")
        self.entry_K.insert(0, "1.0")
        self.entry_K.pack(pady=4)

        self.label_zeta = tk.Label(left, text="zeta (Damping Ratio):")
        self.entry_zeta = tk.Entry(left, width=15, justify="center")
        self.entry_zeta.insert(0, "0.5")

        self.label_wn = tk.Label(left, text="wn (Natural Frequency rad/s):")
        self.entry_wn = tk.Entry(left, width=15, justify="center")
        self.entry_wn.insert(0, "5.0")

        self.label_tau = tk.Label(left, text="tau (Time Constant s):")
        self.entry_tau = tk.Entry(left, width=15, justify="center")
        self.entry_tau.insert(0, "1.0")

        self.on_order_change()

        ttk.Separator(left, orient="horizontal").pack(fill="x", pady=6)

        tk.Button(left, text="Analyze", command=self.run_analysis,
                  bg="#2196F3", fg="white", width=14).pack(pady=4)
        tk.Button(left, text="Clear", command=self.clear_plot,
                  bg="#f44336", fg="white", width=14).pack(pady=4)

        ttk.Separator(left, orient="horizontal").pack(fill="x", pady=6)

        tk.Label(left, text="Results:", font=("Arial", 10, "bold")).pack(anchor="w")

        tk.Label(left, text="Rise Time (s):").pack(anchor="w")
        self.label_tr = tk.Label(left, text="-", font=("Arial", 10, "bold"), fg="#333")
        self.label_tr.pack(anchor="w", pady=2)

        tk.Label(left, text="Peak Time (s):").pack(anchor="w")
        self.label_tp = tk.Label(left, text="-", font=("Arial", 10, "bold"), fg="#333")
        self.label_tp.pack(anchor="w", pady=2)

        tk.Label(left, text="Overshoot (%):").pack(anchor="w")
        self.label_mp = tk.Label(left, text="-", font=("Arial", 10, "bold"), fg="#333")
        self.label_mp.pack(anchor="w", pady=2)

        tk.Label(left, text="Settling Time (s):").pack(anchor="w")
        self.label_ts = tk.Label(left, text="-", font=("Arial", 10, "bold"), fg="#333")
        self.label_ts.pack(anchor="w", pady=2)

        tk.Label(left, text="Steady-State Error:").pack(anchor="w")
        self.label_ess = tk.Label(left, text="-", font=("Arial", 10, "bold"), fg="#333")
        self.label_ess.pack(anchor="w", pady=2)

        tk.Label(left, text="System Type:").pack(anchor="w")
        self.label_type = tk.Label(left, text="-", font=("Arial", 10, "bold"), fg="#555")
        self.label_type.pack(anchor="w", pady=2)

        right = tk.Frame(root)
        right.pack(side="left", fill="both", expand=True)

        self.figure, self.ax = plt.subplots(figsize=(7, 5))
        self.ax.set_title("Step Response\n(Enter parameters and click Analyze)")
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Output")
        self.ax.grid(True, alpha=0.3)

        self.canvas = FigureCanvasTkAgg(self.figure, master=right)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def on_order_change(self):
        if self.order_var.get() == 1:
            self.label_zeta.pack_forget()
            self.entry_zeta.pack_forget()
            self.label_wn.pack_forget()
            self.entry_wn.pack_forget()
            self.label_tau.pack(anchor="w")
            self.entry_tau.pack(pady=4)
        else:
            self.label_tau.pack_forget()
            self.entry_tau.pack_forget()
            self.label_zeta.pack(anchor="w")
            self.entry_zeta.pack(pady=4)
            self.label_wn.pack(anchor="w")
            self.entry_wn.pack(pady=4)

    def run_analysis(self):
        try:
            K = float(self.entry_K.get())
        except:
            messagebox.showerror("Error", "K is not valid!")
            return

        order = self.order_var.get()

        if order == 1:
            try:
                tau = float(self.entry_tau.get())
                if tau <= 0:
                    raise ValueError
                tf = TransferFunction(K, order=1, tau=tau)
            except:
                messagebox.showerror("Error", "tau must be a positive number!")
                return
        else:
            try:
                zeta = float(self.entry_zeta.get())
                if zeta < 0:
                    raise ValueError
            except:
                messagebox.showerror("Error", "zeta must be >= 0!")
                return
            try:
                wn = float(self.entry_wn.get())
                if wn <= 0:
                    raise ValueError
            except:
                messagebox.showerror("Error", "wn must be positive!")
                return
            tf = TransferFunction(K, order=2, zeta=zeta, wn=wn)

        step = StepResponse(tf)
        t, y = step.compute()

        analyzer = Analyzer(t, y, tf)
        specs = analyzer.get_all_specs()

        plotter = Plotter(self.ax, self.figure)
        plotter.plot(t, y, specs, tf)
        self.canvas.draw()

        def fmt(val):
            if val is None:
                return "N/A"
            return f"{val:.4f}"

        self.label_tr.config(text=fmt(specs["rise_time"]))
        self.label_tp.config(text=fmt(specs["peak_time"]) if specs["peak_time"] else "N/A (no peak)")
        self.label_mp.config(text=f"{specs['overshoot']:.2f}%")
        self.label_ts.config(text=fmt(specs["settling_time"]))
        self.label_ess.config(text=fmt(specs["steady_state_error"]))
        self.label_type.config(text=tf.get_system_type())

    def clear_plot(self):
        self.ax.clear()
        self.ax.set_title("Step Response\n(Enter parameters and click Analyze)")
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Output")
        self.ax.grid(True, alpha=0.3)
        self.canvas.draw()
        for lbl in [self.label_tr, self.label_tp, self.label_mp,
                    self.label_ts, self.label_ess, self.label_type]:
            lbl.config(text="-")


root = tk.Tk()
app = App(root)
root.mainloop()