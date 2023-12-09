# Import necessary modules and classes
import customtkinter as ctk
from settings import *
import tkintermapview
from geopy.geocoders import Nominatim
from sidepanel import SidePanel

# Define the main application class
class MapApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Set appearance mode to 'dark'
        ctk.set_appearance_mode('dark')
        self.geometry('1200x800+100+50')
        self.minsize(800, 600)
        self.title('Map')
        self.iconbitmap('map.ico')

        # Initialize data
        self.input_string = ctk.StringVar()

        # Configure layout
        self.rowconfigure(0, weight=1, uniform='a')
        self.columnconfigure(0, weight=2, uniform='a')
        self.columnconfigure(1, weight=8, uniform='a')

        # Create and place widgets
        self.map_widget = MapWidget(self, self.input_string, self.submit_location)
        self.side_panel = SidePanel(self, self.map_widget.set_style, self.map_widget.submit_location)

        self.mainloop()

    def submit_location(self, event):
        # Get geolocation data using Nominatim
        geolocator = Nominatim(user_agent='my-user')
        location = geolocator.geocode(self.input_string.get())

        # Update map based on the location data
        if location:
            self.map_widget.set_address(location.address)
            self.side_panel.history_frame.add_location_entry(location)
            # Clear the input
            self.input_string.set('')
        else:
            self.map_widget.location_entry.error_animation()

# Define the MapWidget class
class MapWidget(tkintermapview.TkinterMapView):
    def __init__(self, parent, input_string, submit_location):
        super().__init__(master=parent)
        self.grid(row=0, column=1, sticky='nsew')

        # Create the location entry widget
        self.location_entry = LocationEntry(self, input_string, submit_location)

    def set_style(self, view_style):
        # Set tile server based on the view style
        if view_style == 'map':
            self.set_tile_server(MAIN_URL)
        if view_style == 'terrain':
            self.set_tile_server(TERRAIN_URL)
        if view_style == 'paint':
            self.set_tile_server(PAINT_URL)

    def submit_location(self, event):
        # Forward the location submission event to the location entry widget
        self.location_entry.submit_location(event)

# Define the LocationEntry class
class LocationEntry(ctk.CTkEntry):
    def __init__(self, parent, input_string, submit_location):
        # Initialize color-related variables
        self.color_index = 15
        color = COLOR_RANGE[self.color_index]
        self.error = False

        super().__init__(
            master=parent,
            textvariable=input_string,
            corner_radius=0,
            border_width=4,
            fg_color=ENTRY_BG,
            border_color=f'#F{color}{color}',
            text_color=TEXT_COLOR,
            font=ctk.CTkFont(family=TEXT_FONT, size=TEXT_SIZE))
        self.place(relx=0.5, rely=0.95, anchor='center')

        # Bind the return key to the location submission
        self.bind('<Return>', submit_location)

        # Trace changes in the input string to remove error status
        input_string.trace('w', self.remove_error)

    def error_animation(self):
        # Perform error animation by changing border and text colors
        self.error = True
        if self.color_index > 0:
            self.color_index -= 1
            border_color = f'#F{COLOR_RANGE[self.color_index]}{COLOR_RANGE[self.color_index]}'
            text_color = f'#{COLOR_RANGE[-self.color_index - 1]}00'
            self.configure(border_color=border_color, text_color=text_color)
            self.after(40, self.error_animation)

    def remove_error(self, *args):
        # Remove error status by resetting colors
        if self.error:
            self.configure(border_color=ENTRY_BG, text_color=TEXT_COLOR)
            self.color_index = 15

# Run the MapApp
MapApp()
