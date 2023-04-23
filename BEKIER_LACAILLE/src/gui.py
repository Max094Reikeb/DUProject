import os
from typing import Optional

from kivy.app import App
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.image import Image
from kivy.uix.label import Label
from mutagen.flac import FLAC
from mutagen.mp3 import MP3

from cli import extract_metadata


def get_cover_art_path(file_path: str) -> Optional[str]:
    """
    Fonction pour obtenir l'image de couverture de l'album à partir d'un fichier MP3 ou FLAC.

    :param file_path: Le chemin du fichier.
    :return: L'image de couverture de l'album.
    """
    file_ext = os.path.splitext(file_path)[1].lower()

    if file_ext == ".mp3":
        audio = MP3(file_path)
        if "APIC:" in audio:
            artwork = audio["APIC:"].data

            cover_art_path = os.path.splitext(file_path)[0] + ".jpg"
            with open(cover_art_path, "wb") as img:
                img.write(artwork)

            return cover_art_path
        else:
            return None
    elif file_ext == ".flac":
        audio = FLAC(file_path)
        if audio.pictures:
            artwork = audio.pictures[0].data

            cover_art_path = os.path.splitext(file_path)[0] + ".jpg"
            with open(cover_art_path, "wb") as img:
                img.write(artwork)

            return cover_art_path
        else:
            return None
    else:
        return None


class MusicExplorer(BoxLayout):
    metadata_text = StringProperty("Sélectionnez un fichier...")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'

        left_layout = BoxLayout(orientation='vertical', size_hint_x=0.3)
        self.filechooser = FileChooserListView(filters=['*.mp3', '*.flac'], path='/', size_hint_y=0.9)
        self.filechooser.bind(on_submit=self.display_metadata)
        left_layout.add_widget(self.filechooser)

        # select_button = Button(text="Sélectionner un dossier", size_hint_y=0.1)
        # select_button.bind(on_press=self.select_directory)
        # left_layout.add_widget(select_button)

        self.add_widget(left_layout)

        center_layout = BoxLayout(orientation='vertical', size_hint_x=0.7)

        self.cover_art_image = Image(size_hint_y=0.5)
        center_layout.add_widget(self.cover_art_image)

        self.metadata_label = Label(text=self.metadata_text, halign='center', valign='top', size_hint_y=0.5)
        self.metadata_label.bind(size=self.resize_label)
        center_layout.add_widget(self.metadata_label)

        self.add_widget(center_layout)

    def select_directory(self, instance):
        directory = self.filechooser.path
        # Ajouter des fonctionnalités supplémentaires pour gérer la sélection du répertoire

    def display_metadata(self, instance, selection, touch):
        if selection:
            file_path = selection[0]
            metadata = extract_metadata(file_path)
            if metadata:
                self.metadata_label.text = str(metadata)
                cover_art_path = get_cover_art_path(file_path)
                if cover_art_path:
                    self.cover_art_image.source = cover_art_path
                else:
                    self.cover_art_image.source = ''
            else:
                self.metadata_label.text = "Métadonnées non disponibles pour ce fichier."
                self.cover_art_image.source = ''
        else:
            self.metadata_label.text = "Sélectionnez un fichier..."
            self.cover_art_image.source = ''

    def resize_label(self, instance, value):
        instance.text_size = (value[0], None)


class MusicExplorerApp(App):
    def build(self):
        return MusicExplorer()


if __name__ == '__main__':
    MusicExplorerApp().run()
