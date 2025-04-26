import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import pandas as pd
import seaborn as sns

from src.domain.facade.weather_facade import WeatherFacade
from src.domain.models.forecast_mode import ForecastMode
from src.domain.models.location import Location


class WeatherAppGUI:
    def __init__(self, master):
        self.master = master
        master.title("Weather Data Viewer")
        self.facade = WeatherFacade(api_name="open-meteo")

        # Configure style
        self.style = ttk.Style()
        self.style.configure('TFrame', padding=5)
        self.style.configure('TLabel', padding=5)
        self.style.configure('TButton', padding=5)

        # Create main container
        self.main_frame = ttk.Frame(master)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Input Section
        self.create_input_section()
        
        # Results Section
        self.create_results_section()

    def create_input_section(self):
        input_frame = ttk.LabelFrame(self.main_frame, text="Location Details")
        input_frame.pack(fill=tk.X, padx=10, pady=5)

        entries = [
            ("Country:", "country_entry"),
            ("City:", "city_entry"),
            ("Postal Code:", "postal_entry")
        ]

        for row, (label, name) in enumerate(entries):
            ttk.Label(input_frame, text=label).grid(row=row, column=0, sticky=tk.W)
            entry = ttk.Entry(input_frame)
            entry.grid(row=row, column=1, padx=5, pady=2, sticky=tk.EW)
            setattr(self, name, entry)

        # Set default values after creating entries
        self.country_entry.insert(0, "Germany")
        self.city_entry.insert(0, "Saarbrücken")
        self.postal_entry.insert(0, "66111")

        # Mode Selection
        ttk.Label(input_frame, text="Forecast Mode:").grid(row=3, column=0, sticky=tk.W)
        self.mode_var = tk.StringVar()
        self.mode_combobox = ttk.Combobox(
            input_frame,
            textvariable=self.mode_var,
            values=["Current", "Past", "Forecast"],
            state="readonly"
        )
        self.mode_combobox.grid(row=3, column=1, padx=5, pady=2, sticky=tk.W)
        self.mode_combobox.current(0)
        self.mode_combobox.bind("<<ComboboxSelected>>", self.update_parameters)

        # Time Parameters
        self.param_frame = ttk.Frame(input_frame)
        self.param_frame.grid(row=4, column=0, columnspan=2, sticky=tk.EW)
        
        ttk.Label(self.param_frame, text="Time Interval:").pack(side=tk.LEFT)
        self.interval_var = tk.StringVar()
        self.interval_combo = ttk.Combobox(
            self.param_frame,
            textvariable=self.interval_var,
            state="readonly",
            width=8
        )
        self.interval_combo.pack(side=tk.LEFT, padx=5)

        ttk.Label(self.param_frame, text="Duration:").pack(side=tk.LEFT)
        self.duration_entry = ttk.Entry(self.param_frame, width=6)
        self.duration_entry.pack(side=tk.LEFT)

        # Fetch Button
        self.fetch_btn = ttk.Button(
            input_frame,
            text="Fetch Weather Data",
            command=self.fetch_weather
        )
        self.fetch_btn.grid(row=5, column=0, columnspan=2, pady=10)

    def create_results_section(self):
        results_frame = ttk.LabelFrame(self.main_frame, text="Weather Data")
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Text Results
        self.results_text = tk.Text(results_frame, height=10, wrap=tk.WORD)
        self.results_text.pack(fill=tk.X, pady=5)

        # Visualization Frame
        self.plot_frame = ttk.Frame(results_frame)
        self.plot_frame.pack(fill=tk.BOTH, expand=True)

    def update_parameters(self, event=None):
        mode = self.mode_var.get()
        forecast_mode = ForecastMode[mode.upper()]
        self.interval_combo['values'] = forecast_mode.time_interval
        self.interval_combo.current(0)

    def validate_inputs(self):
        # Basic validation example
        if not self.postal_entry.get().isdigit():
            raise ValueError("Postal code must be numeric")
        return True

    def fetch_weather(self):
        try:
            self.validate_inputs()
            location = Location(
                country=self.country_entry.get(),
                city=self.city_entry.get(),
                postal_code=self.postal_entry.get()
            )

            mode = ForecastMode[self.mode_var.get().upper()]
            time_interval = self.interval_var.get()
            time = int(self.duration_entry.get())

            df = self.facade.get_weather(
                location=location,
                mode=mode,
                time_interval=time_interval,
                time=time
            )

            if df is not None and not df.empty:
                self.display_results(df)
                self.plot_data(df)
            else:
                self.results_text.delete(1.0, tk.END)
                self.results_text.insert(tk.END, "No weather data found for this location.")
                # Clear plot
                for widget in self.plot_frame.winfo_children():
                    widget.destroy()

        except Exception as e:
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, f"Error: {str(e)}")
            # Clear plot
            for widget in self.plot_frame.winfo_children():
                widget.destroy()

    def display_results(self, df: pd.DataFrame):
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, df.to_string())

    def plot_data(self, df: pd.DataFrame):
        # Clear previous plot
        for widget in self.plot_frame.winfo_children():
            widget.destroy()

        # Create new plot
        fig = Figure(figsize=(6, 4), dpi=100)
        ax = fig.add_subplot(111)
        
        if 'temperature_2m' in df.columns:
            sns.lineplot(data=df, x=df.index, y='temperature_2m', ax=ax)
        elif 'temperature_2m_max' in df.columns:
            df[['temperature_2m_max', 'temperature_2m_min']].plot(ax=ax)
            
        ax.set_title("Temperature Data")
        ax.set_xlabel("Date/Time")
        ax.set_ylabel("Temperature (°C)")

        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherAppGUI(root)
    root.mainloop()