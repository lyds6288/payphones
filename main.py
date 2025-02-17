from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy_garden.mapview import MapView, MapMarker
from kivy.uix.label import Label
from kivy.uix.popup import Popup

# Menu Screen
class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        btn_map = Button(text="Open Map", size_hint=(1, 0.2))
        btn_map.bind(on_press=lambda x: setattr(self.manager, "current", "map"))

        # Button to open the phone list screen
        btn_phonelist = Button(text="List of Payphones", size_hint=(1, 0.2))
        btn_phonelist.bind(on_press=lambda x: setattr(self.manager, "current", "phonelist"))
        
        # Button to open the add location screen
        btn_addloc = Button(text="Add a Location", size_hint=(1, 0.2))
        btn_addloc.bind(on_press=lambda x: setattr(self.manager, "current", "addloc"))


        layout.add_widget(btn_map)
        layout.add_widget(btn_phonelist)
        layout.add_widget(btn_addloc)

        self.add_widget(layout)

# Interactive Map Screen
class MapScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout()

        # Create a MapView
        # 49.88126500050453, -97.13988187732663 : Quickie Mart phone
        self.mapview = MapView(zoom=10, lat=49.88126500050453, lon=-97.13988187732663)  # starting location: Quickie Mart phone
        marker = MapMarker(lat=49.88126500050453, lon=-97.13988187732663)  # Quickie Mart marker
        
        self.layout.add_widget(self.mapview)
        self.add_widget(self.layout)

        self.mapview.bind(on_touch_down=self.add_marker)

        # Add a back button to navigate back to the menu
        self.btn_back = Button(text="Back to Menu", size_hint=(1, 0.1))
        self.btn_back.bind(on_press=lambda x: setattr(self.manager, "current", "menu"))
        self.layout.add_widget(self.btn_back)  # Add the back button to the layout


    #add a marker where user taps
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
        self.layout = BoxLayout(orientation='vertical')
        label = Label(text="Phone List\nHere is where you can view all the payphones in Winnipeg in a list format.")
        self.layout.add_widget(label)
        self.add_widget(self.layout)

        # Add a back button to navigate back to the menu
        self.btn_back = Button(text="Back to Menu", size_hint=(1, 0.1))
        self.btn_back.bind(on_press=lambda x: setattr(self.manager, "current", "menu"))
        self.layout.add_widget(self.btn_back)  # Add the back button to the layout


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
