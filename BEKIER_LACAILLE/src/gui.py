import os
from typing import Optional, List

from kivy.app import App
from kivy.properties import StringProperty, BooleanProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.textinput import TextInput
from mutagen.flac import FLAC
from mutagen.mp3 import MP3

from cli import extract_metadata, Playlist, PLAYLISTS_DIR, get_playlists


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


def resize_label(instance, value):
    instance.text_size = (value[0], None)


class SelectableLabel(RecycleDataViewBehavior, Label):
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def apply_selection(self, rv, index, is_selected):
        self.selected = is_selected
        if is_selected:
            rv.parent.parent.parent.display_tracks(rv.data[index]['text'])
            rv.selected_item = rv.data[index]['text']
        else:
            rv.selected_item = None


class PlaylistsView(RecycleView):
    selected_item = StringProperty(None, allownone=True)

    def __init__(self, playlists, **kwargs):
        super(PlaylistsView, self).__init__(**kwargs)
        self.viewclass = 'SelectableLabel'
        self.data = [{'text': playlist} for playlist in playlists]


class SelectableTrackLabel(SelectableLabel):
    def apply_selection(self, rv, index, is_selected):
        self.selected = is_selected
        if is_selected:
            rv.parent.parent.parent.display_metadata(None, [rv.data[index]['text']], None)
            rv.selected_item = rv.data[index]['text']
        else:
            rv.selected_item = None


class TracksView(RecycleView):
    selected_item = StringProperty(None, allownone=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.viewclass = 'SelectableTrackLabel'


class NewPlaylistPopup(Popup):
    def __init__(self, create_callback, **kwargs):
        super().__init__(**kwargs)
        self.title = 'Nouvelle Playlist'
        self.size_hint = (0.7, 0.4)
        self.size = (400, 200)  # test
        self.auto_dismiss = False

        content_layout = BoxLayout(orientation='vertical', padding=[10, 10, 10, 10], spacing=10)

        self.text_input = TextInput(hint_text="Entrez le nom de la playlist", multiline=False, size_hint_y=None,
                                    height=70)
        content_layout.add_widget(self.text_input)

        button_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)

        cancel_button = Button(text='Annuler', size_hint_x=None, width=150)
        cancel_button.bind(on_release=self.dismiss)
        button_layout.add_widget(cancel_button)

        confirm_button = Button(text='Confirmer', size_hint_x=None, width=150)
        confirm_button.bind(on_release=self.confirm)
        button_layout.add_widget(confirm_button)

        content_layout.add_widget(button_layout)

        self.create_callback = create_callback
        self.content = content_layout

    def confirm(self, instance):
        self.create_callback(self.text_input.text)
        self.dismiss()


class MusicExplorer(BoxLayout):
    metadata_text = StringProperty("Sélectionnez un fichier...")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.current_playlist = None

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
        self.playlist_filechooser = FileChooserListView(filters=['*.xspf'], path=PLAYLISTS_DIR, size_hint_y=0.8)
        self.playlist_filechooser.bind(on_submit=self.load_playlist)
        right_layout.add_widget(self.playlist_filechooser)

        new_playlist_button = Button(text="Nouvelle playlist", size_hint_y=0.1)
        new_playlist_button.bind(on_press=self.create_new_playlist)
        right_layout.add_widget(new_playlist_button)

        add_to_playlist_button = Button(text="Ajouter à la playlist", size_hint_y=0.1)
        add_to_playlist_button.bind(on_press=self.add_to_playlist)
        right_layout.add_widget(add_to_playlist_button)

        remove_from_playlist_button = Button(text="Supprimer de la playlist", size_hint_y=0.1)
        remove_from_playlist_button.bind(on_press=self.remove_from_playlist)
        right_layout.add_widget(remove_from_playlist_button)

        delete_playlist_button = Button(text="Supprimer la playlist", size_hint_y=0.1)
        delete_playlist_button.bind(on_press=self.delete_playlist)
        right_layout.add_widget(delete_playlist_button)

        self.add_widget(right_layout)

        self.playlist_layout = BoxLayout(orientation='vertical', size_hint_x=0.75)

        self.playlist_list = PlaylistsView(playlists=self.get_playlist_names(), size_hint_y=0.5)
        self.playlist_layout.add_widget(self.playlist_list)

        self.playlist_tracks = TracksView(size_hint_y=0.5)
        self.playlist_layout.add_widget(self.playlist_tracks)

        self.add_widget(self.playlist_layout)

    @staticmethod
    def get_playlist_names() -> List[str]:
        playlist_files = get_playlists(PLAYLISTS_DIR)
        return [os.path.splitext(os.path.basename(f))[0] for f in playlist_files]

    def refresh_playlist_file_chooser(self):
        """
        Permet de rafraichir l'explorateur de playlists.
        """
        original_path = self.playlist_filechooser.path
        self.playlist_filechooser.path = os.path.dirname(original_path)
        self.playlist_filechooser.path = original_path

    def display_metadata(self, instance, selection, touch):
        """
        Permet d'afficher les métadonnées du morceau sélectionné.

        :param instance: Instance du GUI.
        :param selection: Morceau sélectionné dans le FileChooser.
        :param touch: Réaction à la sélection. (clic de la souris)
        """
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
        """
        Permet de charger la playlist sélectionnée.

        :param instance: Instance du GUI.
        :param selection: Playlist sélectionnée dans le FileChooser.
        :param touch: Réaction à la sélection. (clic de la souris)
        """
        print("load_playlist called with selection:", selection)
        if selection:
            playlist_path = selection[0]
            self.current_playlist = Playlist(playlist_path)

            tracks = self.current_playlist.music_files
            self.playlist_tracks.data = [{'text': track} for track in tracks]
            self.ids['playlist_tracks'].data = [{'text': track.title} for track in tracks]
            self.playlist_tracks.refresh_from_data()
        else:
            self.playlist_tracks.data = [{'text': "Aucune playlist sélectionnée..."}]
            self.playlist_tracks.refresh_from_data()

    def display_track_metadata(self, index):
        track = self.ids['playlist_tracks'].data[index]
        metadata = extract_metadata(track)
        if metadata:
            self.metadata_text = metadata.__str__()

    def create_new_playlist(self, instance):
        """
        Permet de créer une nouvelle playlist.

        :param instance: Instance du GUI.
        """
        popup = NewPlaylistPopup(self.create_playlist_callback)
        popup.open()

    def create_playlist_callback(self, playlist_name):
        """
        Fonction recevant le nom de la nouvelle playlist.

        :param playlist_name: Nom de la nouvelle playlist.
        """
        if playlist_name:
            new_playlist_path = os.path.join(PLAYLISTS_DIR, f"{playlist_name}.xspf")

            Playlist(new_playlist_path)

            self.playlist_list.data.append({'text': playlist_name})
            self.playlist_list.refresh_from_data()
            self.refresh_playlist_file_chooser()
        else:
            print("Le nom de la playlist est vide !")

    def delete_playlist(self, instance):
        """
        Permet de supprimer une playlist.

        :param instance: Instance de GUI.
        """
        playlist_path = self.playlist_filechooser.selection[0]
        if playlist_path:
            Playlist(playlist_path).delete()
            self.refresh_playlist_file_chooser()
        else:
            print("Aucune playlist sélectionnée.")

    def add_to_playlist(self, instance):
        """
        Permet d'ajouter le morceau sélectionné à la playlist sélectionnée.

        :param instance: Instance du GUI.
        """
        file_path = self.filechooser.selection[0]
        playlist_path = self.playlist_filechooser.selection[0]

        if playlist_path:
            Playlist(playlist_path).add_tracks([file_path])
        else:
            print("Aucune playlist sélectionnée.")

    def remove_from_playlist(self, instance):
        """
        Permet de retirer le morceau sélectionné de la playlist sélectionnaée.

        :param instance: Instance du GUI.
        """
        if self.playlist_tracks.selected_item:
            self.current_playlist.remove_track([self.playlist_tracks.selected_item])
            self.load_playlist(None, self.playlist_filechooser.selection, None)


class MusicExplorerApp(App):
    def build(self):
        return MusicExplorer()


if __name__ == '__main__':
    MusicExplorerApp().run()
