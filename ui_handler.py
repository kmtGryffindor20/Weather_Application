# Import Statements

import customtkinter as ctk

from PIL import Image

import api_handler

# Constants and Global Fields

GRAY = "#BDC3CB"
FONT = 'Century Gothic'
temp_unit = 'Celsius'
wind_unit = 'm/s'
press_unit = 'mbar'


class SettingsTopLevelWindow(ctk.CTkToplevel):
    """Creates a TopLevel Window for the Settings Menu"""

    def __init__(self, *args):
        """Initializes the CTk Window and opens the Settings Menu"""
        super().__init__(*args)
        self.title("Configure Settings")
        self.geometry("320x180")
        self.resizable(False, False)
        self.configure(pady=15)
        self.iconbitmap('./Icons/settings.ico')

        # Labels of the Units

        temperature_choice_label = ctk.CTkLabel(master=self, text="     Temperature Unit:   ", font=(FONT, 14, 'bold'))
        wind_speed_choice_label = ctk.CTkLabel(master=self, text="  Wind Speed Unit:  ", font=(FONT, 14, 'bold'))
        pressure_choice_label = ctk.CTkLabel(master=self, text="  Pressure Unit:  ", font=(FONT, 14, 'bold'))

        # String Variables for the choice of the units
        self.temperature_var = ctk.StringVar(value=temp_unit)
        self.wind_var = ctk.StringVar(value=wind_unit)
        self.pressure_var = ctk.StringVar(value=press_unit)

        # Options Menus for the different units
        temperature_menu = ctk.CTkOptionMenu(self, values=["Celsius", "Fahrenheit"],
                                             variable=self.temperature_var)
        wind_menu = ctk.CTkOptionMenu(self, values=['m/s', 'km/hr'], variable=self.wind_var)
        pressure_menu = ctk.CTkOptionMenu(self, values=['mbar', 'atm'], variable=self.pressure_var)

        # Button for Applying Changes
        submit_button = ctk.CTkButton(master=self, text="Apply", font=(FONT, 14, 'normal'), command=self.submit)

        # Griding Each Element
        temperature_choice_label.grid(column=0, row=0)
        temperature_menu.grid(column=1, row=0, pady=15, padx=10)
        wind_speed_choice_label.grid(column=0, row=1)
        wind_menu.grid(column=1, row=1)
        pressure_choice_label.grid(column=0, row=2, pady=15)
        pressure_menu.grid(column=1, row=2)
        submit_button.grid(column=0, row=3, columnspan=2, sticky='ew')

    def submit(self):
        """Function for the Apply Changes Button which sets the global units to the settings window's current units
        and destroys the window"""
        global temp_unit
        temp_unit = self.temperature_var.get()
        global wind_unit
        wind_unit = self.wind_var.get()
        global press_unit
        press_unit = self.pressure_var.get()
        self.destroy()


class App(ctk.CTk):
    """Creates the main application window"""

    def __init__(self):
        """Initializes all the elements of the main window"""
        super().__init__()

        ctk.set_appearance_mode('dark')
        self.title("Weather")
        self.geometry("950x700")
        self.config(padx=200, pady=50)
        self.resizable(False, False)
        self.iconbitmap('./Icons/icon.ico')

        # All the images to be put

        weather_image = ctk.CTkImage(light_image=Image.open("./Icons/01n.png"),
                                     size=(100, 60))
        thermometer_image = ctk.CTkImage(light_image=Image.open("Icons/thermometer.png"),
                                         size=(13, 13))
        wind_image = ctk.CTkImage(light_image=Image.open("Icons/wind_speed.png"),
                                  size=(13, 13))
        pressure_image = ctk.CTkImage(light_image=Image.open("Icons/pressure.png"),
                                      size=(13, 13))
        humidity_image = ctk.CTkImage(light_image=Image.open("Icons/humidity.png"),
                                      size=(13, 13))
        settings_image = ctk.CTkImage(light_image=Image.open('Icons/settings.png'), size=(15, 15))

        # All Labels

        self.current_city = ctk.CTkLabel(master=self, text="Varanasi", font=(FONT, 30, "bold"))
        self.skies_current = ctk.CTkLabel(master=self, image=weather_image, compound='right', text="Clear Sky",
                                          font=(FONT, 14, "normal"))
        self.temperature = ctk.CTkLabel(master=self, text="31°C", pady=5, font=(FONT, 28, "bold"))

        # Text Field

        self.search_field = ctk.CTkEntry(master=self, width=400)
        self.search_field.insert(ctk.END, "Varanasi")

        # Buttons

        search_button = ctk.CTkButton(master=self, text="Search", font=(FONT, 14, 'normal'),
                                      command=self.search_city_data)
        settings_button = ctk.CTkButton(master=self, image=settings_image, text="", font=(FONT, 14, 'normal'),
                                        width=15, command=self.open_settings)

        # Things in Forecast Frame

        forecast_frame = ctk.CTkFrame(master=self, width=400, height=200, border_width=2, border_color=GRAY)
        upcoming_forecast_label = ctk.CTkLabel(master=forecast_frame, text="Upcoming Forecast",
                                               font=(FONT, 14, 'normal'),
                                               text_color=GRAY)
        self.all_forecasts_times = []
        self.all_forecasts = []
        self.all_forecast_images = []
        for index in range(3):
            self.all_forecasts_times.append(ctk.CTkLabel(master=forecast_frame, text=f"{(index * 3)}:00",
                                                         font=(FONT, 12, 'normal'),
                                                         text_color=GRAY))
            self.all_forecasts.append(ctk.CTkLabel(master=forecast_frame, text=f"25°C",
                                                   font=(FONT, 20, 'bold'),
                                                   text_color=GRAY))
            self.hour_img = ctk.CTkImage(light_image=Image.open(f"./Icons/0{index + 1}n.png"),
                                         size=(100, 60))
            self.all_forecast_images.append(ctk.CTkLabel(master=forecast_frame, image=self.hour_img, text=""))
            self.all_forecast_images[index].grid(column=index, row=2)
            self.all_forecasts_times[index].grid(column=index, row=1, padx=80, sticky='ew')
            self.all_forecasts[index].grid(column=index, row=3, pady=5)

        # Griding in Forecast Frame

        forecast_frame.grid(column=0, row=4, columnspan=2, sticky='ew')
        upcoming_forecast_label.grid(column=0, row=0, columnspan=3, pady=5)

        # Things in Weather Details Frame

        weather_details_frame = ctk.CTkFrame(master=self, width=400, height=500, border_color=GRAY, border_width=2)
        feels_like = ctk.CTkLabel(master=weather_details_frame, image=thermometer_image,
                                  compound='left', text=' Feels Like    ',
                                  font=(FONT, 14, 'normal'))
        self.feels_like_value = ctk.CTkLabel(master=weather_details_frame, text=' 20°C    ',
                                             font=(FONT, 24, 'normal'), pady=20)
        wind_speed = ctk.CTkLabel(master=weather_details_frame, image=wind_image, compound='left',
                                  text=' Wind Speed   ',
                                  font=(FONT, 14, 'normal'))
        self.wind_speed_value = ctk.CTkLabel(master=weather_details_frame, text=' 10km/hr    ',
                                             font=(FONT, 24, 'normal'))
        pressure = ctk.CTkLabel(master=weather_details_frame, image=pressure_image, compound='left',
                                text=' Pressure     ',
                                font=(FONT, 14, 'normal'))
        self.pressure_value = ctk.CTkLabel(master=weather_details_frame, text=' 0mbar    ',
                                           font=(FONT, 24, 'normal'))
        humidity = ctk.CTkLabel(master=weather_details_frame, image=humidity_image, compound='left',
                                text=' Humidity    ',
                                font=(FONT, 14, 'normal'))
        self.humidity_value = ctk.CTkLabel(master=weather_details_frame, text=' 2%    ',
                                           font=(FONT, 24, 'normal'), pady=20)

        # Griding in Weather Details Frame

        weather_details_frame.grid(column=0, row=5, columnspan=2, pady=20, sticky='ew')
        feels_like.grid(column=0, row=0, padx=50, pady=5)
        self.feels_like_value.grid(column=0, row=1, padx=100)
        wind_speed.grid(column=1, row=0)
        self.wind_speed_value.grid(column=1, row=1, padx=100)
        pressure.grid(column=0, row=2)
        self.pressure_value.grid(column=0, row=3)
        humidity.grid(column=1, row=2)
        self.humidity_value.grid(column=1, row=3, pady=5)

        # Griding in the Main Window

        self.current_city.grid(column=0, row=1, sticky='ew', columnspan=2, pady=(30, 0))
        self.skies_current.grid(column=0, row=2, columnspan=2, sticky='ew', pady=(20, 10))
        self.temperature.grid(column=0, row=3, pady=(0, 35), columnspan=2)
        self.search_field.grid(column=0, row=0, padx=10)
        search_button.grid(column=1, row=0)
        settings_button.grid(column=2, row=0)

        self.search_city_data()  # Call for the initial data showing

        self.settings_window = None  # Initializing the settings window currently to be None

        self.mainloop()  # Starting the main loop of the application

    def search_city_data(self):
        """Updates the window data fields with the data of the city in the ``search_field``"""

        city = self.search_field.get()  # Gets the city filled in the search field
        if city != "":  # Search takes place only when something has been entered in the search field
            try:
                lat, lon = map(float, api_handler.get_current_city_code(city))

            except TypeError:  # If the Geocoding returns None we need to show an Error Screen
                error = ctk.CTkToplevel()
                error.title("No Result Found")
                error.config(padx=50, pady=0)
                error.resizable(False, False)
                error_image = ctk.CTkImage(light_image=Image.open('./Icons/404_error.png'), size=(300, 350))
                error_label = ctk.CTkLabel(
                    master=error, image=error_image,
                    text='Try Entering a valid city name, or give country codes to search accurately.',
                    compound='left',
                    font=(FONT, 15, 'bold'), wraplength=300
                )
                error_label.pack()
                error.grab_set()

            else:  # If no error occurs we show the data of the city weather
                next_six_hours_city_data = api_handler.get_3hour_weather_data(lat, lon)
                current_weather_data = api_handler.get_current_weather_data(lat, lon)

                # Block for specifying hemispheres of the place

                if lat < 0 <= lon:
                    self.current_city.configure(
                        text=f"{current_weather_data['name']} : ({-round(lat, 4)}°S,{round(lon, 4)}°E)"
                    )
                elif lon < 0 <= lat:
                    self.current_city.configure(
                        text=f"{current_weather_data['name']} : ({round(lat, 4)}°N,{-round(lon, 4)}°W)"
                    )
                elif lon < 0 and lat < 0:
                    self.current_city.configure(
                        text=f"{current_weather_data['name']} : ({-round(lat, 4)}°S,{-round(lon, 4)}°W)"
                    )
                else:
                    self.current_city.configure(
                        text=f"{current_weather_data['name']} : ({round(lat, 4)}°N,{round(lon, 4)}°E)")

                # Configure the current sky condition label
                self.skies_current.configure(text=f"{current_weather_data['weather'][0]['description'].title()}")

                # Configure the Temperature Label as per the unit decided by the user
                if temp_unit == 'Celsius':
                    self.temperature.configure(text=f'{int(float(current_weather_data["main"]["temp"]))}°C')
                else:
                    self.temperature.configure(
                        text=f'{int(float(current_weather_data["main"]["temp"])) * 9 / 5 + 32}°F')

                # Change the image of the current sky
                this_image = ctk.CTkImage(
                    dark_image=Image.open(f"./Icons/{current_weather_data['weather'][0]['icon']}.png"),
                    size=(100, 60)
                )
                self.skies_current.configure(image=this_image)

                # Changes in the 3-hour forecast
                for index in range(3):
                    hour = (int(next_six_hours_city_data['list'][index]['dt_txt'].split()[1].split(':')[0]) + 5) % 24

                    self.all_forecasts_times[index].configure(
                        text=f"{hour}:30"
                    )
                    if temp_unit == 'Celsius':
                        self.all_forecasts[index].configure(
                            text=f"{int(float(next_six_hours_city_data['list'][index]['main']['temp']))}°C"
                        )
                    else:
                        self.all_forecasts[index].configure(
                            text=f"{int(float(next_six_hours_city_data['list'][index]['main']['temp'])) * 9 / 5 + 32}°F"
                        )
                    this_image = ctk.CTkImage(
                        light_image=Image.open(
                            f"./Icons/{next_six_hours_city_data['list'][index]['weather'][0]['icon']}.png"),
                        size=(100, 60)
                    )
                    self.all_forecast_images[index].configure(image=this_image)

                # Changes in the Weather Details Frame as per the user decide units
                if temp_unit == 'Celsius':
                    self.feels_like_value.configure(
                        text=f"{int(float(current_weather_data['main']['feels_like']))}°C"
                    )
                else:
                    self.feels_like_value.configure(
                        text=f"{int(float(current_weather_data['main']['feels_like'])) * 9 / 5 + 32}°F"
                    )
                if wind_unit == 'm/s':
                    self.wind_speed_value.configure(
                        text=f"{current_weather_data['wind']['speed']}m/s"
                    )
                else:
                    self.wind_speed_value.configure(
                        text=f"{round(current_weather_data['wind']['speed'] * 3.6, 2)} km/hr"
                    )

                self.humidity_value.configure(
                    text=f"{current_weather_data['main']['humidity']}%"
                )

                if press_unit == 'mbar':
                    self.pressure_value.configure(
                        text=f"{current_weather_data['main']['pressure']} mbar"
                    )
                else:
                    self.pressure_value.configure(
                        text=f"{round(current_weather_data['main']['pressure'] / 1013, 2)} atm"
                    )

    def open_settings(self):
        """Function to open a Top Level Settings Menu to configure the units of data to be shown"""
        if self.settings_window is None or not self.settings_window.winfo_exists():
            self.settings_window = SettingsTopLevelWindow(self)
        self.settings_window.grab_set()
