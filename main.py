from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy_garden.mapview import MapView, MapMarker
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout

# Menu Screen
class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        root = FloatLayout()
        layout = BoxLayout(
            orientation='vertical',
            size_hint=(.7, None),
            height=300,  # 3 buttons * 80 + spacing
            spacing=20,
            pos_hint={'center_x': .5, 'center_y': .5}
        )

        btn_map = Button(
            text="Open Map - suuuuuper bad",
            size_hint=(1, None),
            height=80,
            background_color=(1, 0, 0, 1)  # red
        )
        btn_map.bind(on_press=lambda x: setattr(self.manager, "current", "map"))

        btn_phonelist = Button(
            text="List of Payphones - this is the only thing that really works rn lulls",
            size_hint=(1, None),
            height=80,
            background_color=(0.3, 0.8, 0.3, 1)  # green
        )
        btn_phonelist.bind(on_press=lambda x: setattr(self.manager, "current", "phonelist"))

        btn_addloc = Button(
            text="Add a Location - not implemented",
            size_hint=(1, None),
            height=80,
            background_color=(1, 0, 0, 1)  # red
        )
        btn_addloc.bind(on_press=lambda x: setattr(self.manager, "current", "addloc"))

        layout.add_widget(btn_map)
        layout.add_widget(btn_phonelist)
        layout.add_widget(btn_addloc)

        root.add_widget(layout)
        self.add_widget(root)

# Interactive Map Screen
class MapScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout()

        # Create a MapView
        # 49.88126500050453, -97.13988187732663 : Quickie Mart phone
        self.mapview = MapView(zoom=10, lat=49.88126500050453, lon=-97.13988187732663)  # starting location: Quickie Mart phone
        marker = MapMarker(lat=49.88126500050453, lon=-97.13988187732663)  # Quickie Mart marker
        
        self.mapview.add_widget(marker)  # Add the marker to the mapview
        self.layout.add_widget(self.mapview)
        self.add_widget(self.layout)

        self.mapview.bind(on_touch_down=self.add_marker)

        # Add a back button to navigate back to the menu
        self.btn_back = Button(text="Back to Menu", size_hint=(1, 0.1))
        self.btn_back.bind(on_press=lambda x: setattr(self.manager, "current", "menu"))
        self.layout.add_widget(self.btn_back)  # Add the back button to the layout


    # add a marker where user taps
    def add_marker(self, instance, touch):
        if self.mapview.collide_point(*touch.pos):
            lat, lon = self.mapview.get_latlon_at(*touch.pos)
            marker = MapMarker(lat=lat, lon=lon)
            marker.bind(on_release=lambda m: self.show_marker_info(lat, lon))
            self.mapview.add_widget(marker)

    def show_marker_info(self, lat, lon):
        """Show info when clicking on a marker"""
        popup = Popup(title="Marker Info",
                      content=Label(text=f"Location: {lat:.4f}, {lon:.4f}"),
                      size_hint=(0.5, 0.3))
        popup.open()


# phone list screen
class PhoneList(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.locations = [
            {
                "name": "Quickie Mart",
                "lat": 49.881265,
                "lon": -97.139882,
                "image": "assets/images/quickie_mart.jpg",
                "full_coor": "Location: 49.881265, -97.139882"
            },
            {
                "name": "Old Spaghetti Factory",
                "lat": 49.8951,
                "lon": -97.1384,
                "image": "assets/images/old_spaghetti_factory_1.jpg",
                "full_coor": "Location: 49.8951, -97.1384"
            }
            # Add more locations as needed
        ]

        root = FloatLayout()
        self.layout = BoxLayout(orientation='vertical', size_hint=(.7, .7), pos_hint={'center_x': .5, 'center_y': .5}, spacing=20)
        label = Label(
            text="Payphones in\nWinnipeg Locations.",
            font_size=42,
            size_hint_y=None,
            height=135,
            halign='center',
            valign='middle'
        )
        label.bind(width=lambda instance, value: setattr(instance, 'text_size', (value, instance.height)))
        self.layout.add_widget(label)

        # Add a phone booth location with image
        for loc in self.locations:
            phonebooth_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=300)
            phonebooth_image = Image(
                source=loc["image"],
                size_hint=(None, None),
                size=(300, 300),
                allow_stretch=True,
                keep_ratio=True
            )
            phonebooth_info = Label(text=f"{loc['name']}\nLat: {loc['lat']}, Lon: {loc['lon']}",)
            phonebooth_layout.add_widget(phonebooth_image)
            phonebooth_layout.add_widget(phonebooth_info)
            self.layout.add_widget(phonebooth_layout)

        # Add a back button to navigate back to the menu
        self.btn_back = Button(text="Back to Menu", size_hint_y=None, height=100)
        self.btn_back.bind(on_press=lambda x: setattr(self.manager, "current", "menu"))
        self.layout.add_widget(self.btn_back)

        root.add_widget(self.layout)
        self.add_widget(root)


# add a location screen
class AddLocation(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        label = Label(text="Add a Location\nHere you can find instructions to add a phonebooth to the list.")
        self.layout.add_widget(label)
        self.add_widget(self.layout)

        # Add a back button to navigate back to the menu
        self.btn_back = Button(text="Back to Menu", size_hint=(1, 0.1))
        self.btn_back.bind(on_press=lambda x: setattr(self.manager, "current", "menu"))
        self.layout.add_widget(self.btn_back)  # Add the back button to the layout


# Screen Manager
class MyApp(App):
    def build(self):
        sm = ScreenManager()

        # add screens
        sm.add_widget(MenuScreen(name="menu"))
        sm.add_widget(MapScreen(name="map"))
        sm.add_widget(PhoneList(name="phonelist"))
        sm.add_widget(AddLocation(name="addloc"))

        return sm

if __name__ == "__main__":
    MyApp().run()
