import argparse
import mimetypes
import os
from typing import Union, List
from xml.dom import minidom
from xml.etree.ElementTree import Element, SubElement, tostring

from tinytag import TinyTag


class Metadata:
    def __init__(self, title: str, artist: str, album: str, duration: float, genre: str, track_number: int,
                 year: int, ):
        self.title = title
        self.artist = artist
        self.album = album
        self.duration = duration
        self.genre = genre
        self.track_number = track_number
        self.year = year

    def __str__(self):
        return (
            f"title: {self.title}\n"
            f"artist: {self.artist}\n"
            f"album: {self.album}\n"
            f"duration: {self.duration}\n"
            f"genre: {self.genre}\n"
            f"track_number: {self.track_number}\n"
            f"year: {self.year}"
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
            duration=tag.duration,
            genre=tag.genre,
            track_number=tag.track,
            year=tag.year,
        )

        return metadata

    except Exception as e:
        print(f"Erreur lors de l'extraction des métadonnées: {e}")
        return None


def create_xspf_playlist(music_files: List[str], output_path: str):
    """
    Fonction pour créer une playlist XSPF à partir d'une liste de fichiers musicaux, et enregistrer la playlist
    dans un fichier spécifié.

    :param music_files: Liste de chemins de fichiers musicaux à inclure dans la playlist.
    :param output_path: Chemin d'accès du fichier où la playlist XSPF sera enregistrée.
    """
    playlist = Element("playlist", version="1", xmlns="http://xspf.org/ns/0/")
    track_list = SubElement(playlist, "trackList")

    for music_file in music_files:
        metadata = extract_metadata(music_file)
        if metadata:
            track = SubElement(track_list, "track")
            SubElement(track, "location").text = music_file
            SubElement(track, "title").text = metadata["title"]
            SubElement(track, "creator").text = metadata["artist"]
            SubElement(track, "album").text = metadata["album"]
            SubElement(track, "duration").text = str(int(metadata["duration"] * 1000))
            SubElement(track, "trackNum").text = str(metadata["track_number"])
            SubElement(track, "meta", rel="year").text = metadata["year"]
            SubElement(track, "meta", rel="genre").text = metadata["genre"]

    pretty_playlist = minidom.parseString(tostring(playlist, "utf-8")).toprettyxml(indent="  ")

    with open(output_path, "w", encoding="utf-8") as output_file:
        output_file.write(pretty_playlist)


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
        print('Veuillez spécifier un répertoire avec l\'option -d ou un fichier avec l\'option -f')
    else:
        if args.directory is not None:
            music_explorer = MusicFileExplorer(args.directory)
            music_explorer.explore_directory()
            filtered_music_files = music_explorer.get_music_files()

            if args.output is not None:
                create_xspf_playlist(filtered_music_files, args.output)

            for music_file in filtered_music_files:
                print(f"Fichier: {music_file}")
                metadata = extract_metadata(music_file)
                if metadata:
                    print("Métadonnées extraites :")
                    for key, value in metadata.items():
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
