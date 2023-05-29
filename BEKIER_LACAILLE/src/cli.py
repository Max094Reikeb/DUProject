import argparse
import mimetypes
import os
import xml.etree.ElementTree as ET
from typing import Union, List
from xml.dom import minidom
from xml.etree.ElementTree import Element, SubElement, tostring

from tinytag import TinyTag

PLAYLISTS_DIR = 'playlists'


class Metadata:
    def __init__(self, title: str, artist: str, album: str, year: int, duration: float, albumartist: str, genre: str,
                 track: int, track_total: int, composer: str):
        self.title = title
        self.artist = artist
        self.album = album
        self.year = year
        self.duration = duration
        self.albumartist = albumartist
        self.genre = genre
        self.track = track
        self.track_total = track_total
        self.composer = composer

    def __str__(self):
        return (
            f"Titre: {self.title}\n"
            f"Artiste: {self.artist}\n"
            f"Album: {self.album}\n"
            f"Année: {self.year}\n"
            f"Durée: {self.duration}\n"
            f"Artiste de l'album : {self.albumartist}\n"
            f"Genre: {self.genre}\n"
            f"Numéro de piste: {self.track}/${self.track_total}\n"
            f"Compositeur: {self.composer}\n"
        )


def extract_metadata(file_path: str) -> Union[None, Metadata]:
    """
    Fonction pour extraire les métadonnées d'un fichier MP3 ou FLAC.

    :param file_path: Chemin d'accès au fichier MP3 ou FLAC.
    :return: Une instance de la classe Metadata contenant les métadonnées si le fichier est valide, sinon None.
    """
    try:
        tag = TinyTag.get(file_path)

        metadata = Metadata(
            title=tag.title,
            artist=tag.artist,
            album=tag.album,
            year=tag.year,
            duration=tag.duration,
            albumartist=tag.albumartist,
            genre=tag.genre,
            track=tag.track,
            track_total=tag.track_total,
            composer=tag.composer
        )

        return metadata

    except Exception as e:
        print(f"Erreur lors de l'extraction des métadonnées: {e}")
        return None


def get_playlists(directory: str) -> List[str]:
    """
    Récupère la liste des playlists dans le répertoire donné.

    :param directory: Le chemin du répertoire contenant les playlists.
    :return: Une liste des chemins de fichiers des playlists.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)
    return [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.xspf')]


class Playlist:
    def __init__(self, path: str):
        self.path = path
        if not os.path.exists(path):
            self.create()
        self.tree = ET.parse(path)
        self.music_files = self.read()

    def create(self):
        """
        Fonction pour créer une playlist XSPF vide et l'enregistrer dans un fichier spécifié.
        """
        playlist = Element("playlist", version="1", xmlns="http://xspf.org/ns/0/")
        track_list = SubElement(playlist, "trackList")

        pretty_playlist = minidom.parseString(tostring(playlist, "utf-8")).toprettyxml(indent="  ")
        with open(self.path, "w", encoding="utf-8") as output_file:
            output_file.write(pretty_playlist)

    def delete(self):
        """
        Fonction pour supprimer la playlist.
        """
        if os.path.exists(self.path):
            os.remove(self.path)
        else:
            print(f"Erreur : Le fichier {self.path} n'existe pas.")

    def read(self) -> List[str]:
        """
        Fonction pour lire les données d'un fichier XSPF.

        :return: Une liste des éléments contenus dans le fichier playlist XSPF.
        """
        namespace = {'ns0': 'http://xspf.org/ns/0/'}
        music_files = []

        for track in self.tree.getroot().findall('ns0:trackList/track', namespace):
            location = track.find('location', namespace)
            if location is not None:
                music_files.append(location.text)

        return music_files

    def write(self):
        """
        Ré-écris la playlist avec les bons morceaux.
        """
        pretty_playlist = minidom.parseString(tostring(self.tree.getroot(), "utf-8")).toprettyxml(indent="  ")

        with open(self.path, "w", encoding="utf-8") as output_file:
            output_file.write(pretty_playlist)

    def display_tracks(self) -> None:
        """
        Affiche les morceaux contenus dans la playlist.
        """
        for track in self.music_files:
            print(track)

    def remove_track(self, tracks_to_remove: List[str]):
        """
        Supprime une liste de morceaux de la playlist.

        :param tracks_to_remove: Listes de morceaux à supprimer.
        """
        namespace = {'ns0': 'http://xspf.org/ns/0/'}

        track_list_element = self.tree.getroot().find('ns0:trackList', namespace)
        if track_list_element is None:
            print(f"Erreur : La playlist {self.path} ne contient pas de balise 'trackList'.")
            return

        for track in track_list_element.findall('track', namespace):
            location = track.find('location', namespace)
            for track_to_remove in tracks_to_remove:
                if location is not None and location.text == track_to_remove:
                    track_list_element.remove(track)
                    break

        self.write()

    def add_tracks(self, music_files: List[str]):
        """
        Ajoute une liste de morceaux à la playlist.

        :param music_files: Liste de chemins de fichiers musicaux à inclure dans la playlist.
        """
        if not all(is_music_file(music_file) for music_file in music_files):
            print(f"Certains fichiers de la liste ne sont pas des fichiers de musique valides.")
            return

        namespace = {'ns0': 'http://xspf.org/ns/0/'}

        track_list_element = self.tree.getroot().find('ns0:trackList', namespace)
        if track_list_element is None:
            print(f"Erreur : La playlist {self.path} ne contient pas de balise 'trackList'.")
            return

        for music_file in music_files:
            metadata = extract_metadata(music_file)
            if not metadata:
                print(f"Impossible d'extraire les métadonnées du fichier {music_file}.")
                continue

            track = SubElement(track_list_element, "track")
            SubElement(track, "location").text = music_file
            SubElement(track, "title").text = metadata.title
            SubElement(track, "artist").text = metadata.artist
            SubElement(track, "album").text = metadata.album
            SubElement(track, "year").text = str(metadata.year)
            SubElement(track, "duration").text = str(int(metadata.duration * 1000))
            SubElement(track, "albumartist").text = metadata.albumartist
            SubElement(track, "genre").text = metadata.genre
            SubElement(track, "track").text = str(metadata.track)
            SubElement(track, "track_total").text = str(metadata.track_total)
            SubElement(track, "composer").text = metadata.composer

        self.write()


def is_music_file(file_path):
    """
    Fonction pour vérifier si un fichier est de type musical en se basant sur son extension et son type MIME.

    :param file_path: Le chemin du fichier à vérifier.
    :return: True si le fichier est un fichier musical (.mp3 ou .flac), False sinon.
    """
    file_ext = os.path.splitext(file_path)[1].lower()

    mime_type = mimetypes.guess_type(file_path)[0]

    if file_ext in ['.mp3', '.flac'] and mime_type is not None and mime_type.startswith('audio/'):
        return True

    return False


class MusicFileExplorer:
    def __init__(self, root_directory):
        self.root_directory = root_directory
        self.music_files = []

    def explore_directory(self, directory=None):
        """
        Fonction pour explorer un répertoire et collecter les chemins des fichiers de musique (MP3 ou FLAC) qu'il contient.
        Cette fonction est récursive, c'est-à-dire qu'elle parcourt également tous les sous-répertoires du répertoire donné.

        :param directory: Le répertoire à explorer. Si None, utilise le répertoire racine de l'objet.
        """
        if directory is None:
            directory = self.root_directory

        for entry in os.scandir(directory):
            if entry.is_file() and is_music_file(entry.path):
                self.music_files.append(entry.path)
            elif entry.is_dir():
                self.explore_directory(entry.path)

    def get_music_files(self):
        """
        Fonction pour retourner la liste des fichiers musicaux trouvés par l'instance de MusicFileExplorer.

        :return: La liste des fichiers musicaux trouvés.
        """
        return self.music_files


def main():
    parser = argparse.ArgumentParser(description="Explorer et extraire les métadonnées des fichiers musicaux.")
    parser.add_argument('-d', '--directory', type=str, help='Chemin d\'accès au répertoire racine')
    parser.add_argument('-f', '--file', type=str, help='Chemin d\'accès au fichier MP3 ou FLAC')
    parser.add_argument('-o', '--output', type=str, help='Chemin d\'accès à la playlist XSPF à créer')
    args = parser.parse_args()

    if args.directory is None and args.file is None:
        print('Paramètres manquants. Veuillez rajouter -h ou --help pour obtenir de l\'aide.')
    else:
        if args.directory is not None:
            music_explorer = MusicFileExplorer(args.directory)
            music_explorer.explore_directory()
            filtered_music_files = music_explorer.get_music_files()

            if args.output is not None:
                playlist_manager = Playlist(args.output)
                playlist_manager.add_tracks(filtered_music_files)

            for music_file in filtered_music_files:
                print(f"Fichier: {music_file}")
                metadata = extract_metadata(music_file)
                if metadata:
                    print("Métadonnées extraites :")
                    for key, value in metadata.__dict__.items():
                        print(f"{key}: {value}")
                    print("\n")

        if args.file is not None:
            metadata = extract_metadata(args.file)
            if metadata:
                print(f"Fichier: {args.file}")
                print("Métadonnées extraites :")
                print(metadata)


if __name__ == '__main__':
    main()
