import os
from typing import Optional, List

from kivy.app import App
from kivy.properties import StringProperty, BooleanProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from mutagen.flac import FLAC
from mutagen.mp3 import MP3

from cli import extract_metadata, Playlist, PLAYLISTS_DIR, get_playlists, create_playlist


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


class SelectableLabel(RecycleDataViewBehavior, Label):
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def apply_selection(self, rv, index, is_selected):
        self.selected = is_selected
        if is_selected:
            rv.parent.parent.parent.display_playlist_tracks(rv.data[index]['text'])
            rv.selected_item = rv.data[index]['text']
        else:
            rv.selected_item = None


class PlaylistsView(RecycleView):
    selected_item = StringProperty(None, allownone=True)

    def __init__(self, playlists, **kwargs):
        super(PlaylistsView, self).__init__(**kwargs)
        self.viewclass = 'SelectableLabel'
        self.data = [{'text': playlist} for playlist in playlists]


def resize_label(instance, value):
    instance.text_size = (value[0], None)


class MusicExplorer(BoxLayout):
    metadata_text = StringProperty("Sélectionnez un fichier...")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'

        left_layout = BoxLayout(orientation='vertical', size_hint_x=0.25)
        self.filechooser = FileChooserListView(filters=['*.mp3', '*.flac'], path='/', size_hint_y=0.9)
        self.filechooser.bind(on_submit=self.display_metadata)
        left_layout.add_widget(self.filechooser)

        self.add_widget(left_layout)

        self.center_layout = BoxLayout(orientation='vertical', size_hint_x=0.75)

        self.cover_art_image = Image(size_hint_y=0.5)
        self.center_layout.add_widget(self.cover_art_image)

        self.metadata_label = Label(text=self.metadata_text, halign='center', valign='top', size_hint_y=0.5)
        self.metadata_label.bind(size=resize_label)
        self.center_layout.add_widget(self.metadata_label)

        self.add_widget(self.center_layout)

        right_layout = BoxLayout(orientation='vertical', size_hint_x=0.25)
        filechooser = FileChooserListView(filters=['*.xspf'], path=PLAYLISTS_DIR, size_hint_y=0.9)
        filechooser.bind(on_submit=self.load_playlist)
        right_layout.add_widget(filechooser)

        new_playlist_button = Button(text="Nouvelle playlist", size_hint_y=0.1)
        new_playlist_button.bind(on_press=self.create_new_playlist)
        right_layout.add_widget(new_playlist_button)

        add_to_playlist_button = Button(text="Ajouter à la playlist", size_hint_y=0.1)
        add_to_playlist_button.bind(on_press=self.add_to_playlist)
        right_layout.add_widget(add_to_playlist_button)

        self.add_widget(right_layout)

        self.playlist_layout = BoxLayout(orientation='vertical', size_hint_x=0.75)

        self.playlist_list = PlaylistsView(playlists=self.get_playlist_names(), size_hint_y=0.9)
        self.playlist_layout.add_widget(self.playlist_list)

        self.add_widget(self.playlist_layout)

    def select_directory(self, instance):
        directory = self.filechooser.path

    @staticmethod
    def get_playlist_names() -> List[str]:
        playlist_files = get_playlists(PLAYLISTS_DIR)
        return [os.path.splitext(os.path.basename(f))[0] for f in playlist_files]

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

    def load_playlist(self, instance, selection, touch):
        if selection:
            playlist_path = selection[0]
            playlist = Playlist(playlist_path)
            if playlist:
                self.playlist_list = playlist.read_xspf_playlist()
            else:
                self.playlist_list = "Erreur lors du chargement de la playlist."
        else:
            self.playlist_list = "Aucune playlist sélectionnée..."

    def create_new_playlist(self, instance):
        new_playlist_name = "Nouvelle playlist"
        new_playlist_path = os.path.join(PLAYLISTS_DIR, f"{new_playlist_name}.xspf")
        create_playlist(Playlist, new_playlist_path)
        self.playlist_list.item_strings.append(new_playlist_name)
        self.playlist_list.adapter.data.extend([new_playlist_name])
        self.playlist_list.adapter.reload_view_attrs(self.playlist_list, 0)

    def add_to_playlist(self, instance):
        file_path = self.filechooser.selection[0]
        selected_playlist = self.playlist_list.selected_item

        if selected_playlist:
            playlist_path = os.path.join(PLAYLISTS_DIR, f"{selected_playlist}.xspf")
            Playlist(playlist_path).add_track_to_playlist(file_path)
        else:
            print("Aucune playlist sélectionnée.")


class MusicExplorerApp(App):
    def build(self):
        return MusicExplorer()


if __name__ == '__main__':
    MusicExplorerApp().run()
