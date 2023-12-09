# Import necessary modules and classes
import customtkinter as ctk
from settings import *
from PIL import Image

# Define the SidePanel class
class SidePanel(ctk.CTkFrame):
    def __init__(self, parent, set_style, update_map):
        super().__init__(master=parent, fg_color=SIDE_PANEL_BG)
        self.grid(row=0, column=0, sticky='nsew')

        # Create widgets within the side panel
        ViewButtons(self, set_style)
        self.history_frame = HistoryFrame(self, update_map)

# Define the HistoryFrame class
class HistoryFrame(ctk.CTkScrollableFrame):
    def __init__(self, parent, update_map):
        super().__init__(master=parent)
        self.pack(expand=True, fill='both', padx=5, pady=5)
        self.font = ctk.CTkFont(family=TEXT_FONT, size=TEXT_SIZE)
        self.update_map = update_map

    def add_location_entry(self, location):
        # Add a location entry to the history frame
        HistoryItem(self, location, self.font, self.update_map)

# Define the HistoryItem class
class HistoryItem(ctk.CTkFrame):
    def __init__(self, parent, location, font, update_map):
        super().__init__(master=parent)
        self.pack(fill='x')

        # Extract relevant data from the location
        self.address = location.address
        town = self.address.split(',')[0]
        country = self.address.split(',')[-1]
        if town == country:
            address_string = town
        else:
            address_string = f'{town}, {country}'

        # Create buttons for the history entry
        ctk.CTkButton(
            self,
            command=lambda: update_map(self.address),
            text=address_string,
            font=font,
            anchor='w',
            fg_color='transparent',
            hover_color=HISTORY_HOVER_COLOR,
            text_color=TEXT_COLOR).pack(side='left')
        ctk.CTkButton(
            self,
            command=lambda: self.pack_forget(),
            text='x',
            font=font,
            anchor='e',
            fg_color='transparent',
            hover_color=HISTORY_HOVER_COLOR,
            width=10,
            text_color=TEXT_COLOR).pack(side='right')

# Define the ViewButtons class
class ViewButtons(ctk.CTkFrame):
    def __init__(self, parent, set_style):
        super().__init__(master=parent, fg_color='transparent')
        self.pack(side='bottom', fill='both', padx=5, pady=5)

        # Configure layout
        self.rowconfigure(0, weight=1)
        self.columnconfigure((0, 1, 2), weight=1, uniform='a')

        # Load images for view buttons
        map_image = ctk.CTkImage(dark_image=Image.open(map_image_path), light_image=Image.open(map_image_path))
        paint_image = ctk.CTkImage(dark_image=Image.open(paint_image_path), light_image=Image.open(paint_image_path))
        terrain_image = ctk.CTkImage(dark_image=Image.open(terrain_image_path), light_image=Image.open(terrain_image_path))

        # Create view buttons
        ctk.CTkButton(self, text='', command=lambda: set_style('map'), width=60, image=map_image,
                      fg_color=BUTTON_COLOR, hover_color=BUTTON_HOVER_COLOR).grid(row=0, column=0, sticky='w')
        ctk.CTkButton(self, text='', command=lambda: set_style('terrain'), width=60, image=terrain_image,
                      fg_color=BUTTON_COLOR, hover_color=BUTTON_HOVER_COLOR).grid(row=0, column=1)
        ctk.CTkButton(self, text='', command=lambda: set_style('paint'), width=60, image=paint_image,
                      fg_color=BUTTON_COLOR, hover_color=BUTTON_HOVER_COLOR).grid(row=0, column=2, sticky='e')
