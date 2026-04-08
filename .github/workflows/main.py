from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image as KivyImage
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView
from kivy.core.window import Window
from kivy.utils import platform
from PIL import Image as PILImage
import os

Window.clearcolor = (0.97, 0.97, 0.97, 1)
FRAMES = [
    {"name": "Stand with Iran",      "file": "frame_iran.png"},
    {"name": "Stand with Palestine", "file": "frame_palestine.png"},
    {"name": "Stand with Kashmir",   "file": "frame_kashmir.png"},
    {"name": "I Love Pakistan",      "file": "frame_pakistan.png"},
    {"name": "Peace For All",        "file": "frame_peace.png"},
]
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")

def apply_frame(photo_path, frame_file, output_path):
    photo = PILImage.open(photo_path).convert("RGBA")
    frame = PILImage.open(os.path.join(ASSETS_DIR, frame_file)).convert("RGBA")
    w, h = photo.size
    m = min(w, h)
    photo = photo.crop(((w-m)//2, (h-m)//2, (w-m)//2+m, (h-m)//2+m))
    photo = photo.resize((1080,1080), PILImage.LANCZOS)
    frame = frame.resize((1080,1080), PILImage.LANCZOS)
    result = PILImage.alpha_composite(photo, frame).convert("RGB")
    result.save(output_path, "JPEG", quality=95)
    return output_path

class HomeScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.photo = None
        self.frame = None
        self.frame_btns = []
        root = BoxLayout(orientation="vertical", padding=14, spacing=10)
        root.add_widget(Label(text="Profile Frame Maker", font_size="22sp", bold=True, color=(0.1,0.1,0.1,1), size_hint_y=None, height=55))
        self.preview = KivyImage(size_hint=(1,None), height=250, allow_stretch=True, keep_ratio=True)
        root.add_widget(self.preview)
        b1 = Button(text="Select Photo from Gallery", size_hint_y=None, height=52, background_color=(0.2,0.6,1,1), color=(1,1,1,1))
        b1.bind(on_press=self.open_gallery)
        root.add_widget(b1)
        root.add_widget(Label(text="Choose Frame:", font_size="15sp", color=(0.2,0.2,0.2,1), size_hint_y=None, height=32))
        sv = ScrollView(size_hint=(1,None), height=110)
        gl = GridLayout(cols=len(FRAMES), size_hint_x=None, spacing=6)
        gl.bind(minimum_width=gl.setter("width"))
        for f in FRAMES:
            b = Button(text=f["name"], size_hint=(None,1), width=120, background_color=(0.85,0.85,0.85,1), color=(0.1,0.1,0.1,1), font_size="11sp")
            b.fdata = f
            b.bind(on_press=self.sel_frame)
            gl.add_widget(b)
            self.frame_btns.append(b)
        sv.add_widget(gl)
        root.add_widget(sv)
        b2 = Button(text="Apply Frame & Save", size_hint_y=None, height=52, background_color=(0.1,0.7,0.3,1), color=(1,1,1,1))
        b2.bind(on_press=self.save)
        root.add_widget(b2)
        root.add_widget(Label(text="Saves as 1080x1080 - Perfect for FB/Instagram DP", font_size="11sp", color=(0.5,0.5,0.5,1), size_hint_y=None, height=30))
        self.add_widget(root)

    def open_gallery(self, *a):
        c = BoxLayout(orientation="vertical", spacing=6, padding=6)
        path = "/sdcard/DCIM" if platform=="android" else os.path.expanduser("~")
        fc = FileChooserListView(filters=["*.jpg","*.jpeg","*.png"], path=path)
        c.add_widget(fc)
        btn = Button(text="Select", size_hint_y=None, height=44)
        c.add_widget(btn)
        p = Popup(title="Select Photo", content=c, size_hint=(0.95,0.9))
        def pick(*a):
            if fc.selection:
                self.photo = fc.selection[0]
                self.preview.source = self.photo
                self.preview.reload()
                p.dismiss()
        btn.bind(on_press=pick)
        p.open()

    def sel_frame(self, btn):
        for b in self.frame_btns:
            b.background_color = (0.85,0.85,0.85,1)
            b.color = (0.1,0.1,0.1,1)
        btn.background_color = (0.2,0.6,1,1)
        btn.color = (1,1,1,1)
        self.frame = btn.fdata

    def save(self, *a):
        if not self.photo:
            self.msg("Error", "Pehle photo select karein!")
            return
        if not self.frame:
            self.msg("Error", "Koi frame select karein!")
            return
        out = "/sdcard/Pictures/ProfileFrames" if platform=="android" else os.path.expanduser("~/Pictures/ProfileFrames")
        os.makedirs(out, exist_ok=True)
        path = os.path.join(out, self.frame["name"].replace(" ","_")+".jpg")
        try:
            apply_frame(self.photo, self.frame["file"], path)
            self.preview.source = path
            self.preview.reload()
            self.msg("Saved!", "Image save ho gayi!\nGaller
