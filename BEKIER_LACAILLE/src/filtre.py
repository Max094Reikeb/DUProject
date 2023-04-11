import os
import mimetypes

"""

Création de la classe MusicFileExplorer 

"""

class MusicFileExplorer:
    def __init__(self, root_directory):
        self.root_directory = root_directory
        self.music_files = []

"""

Définition de  la méthode explore_directory pour parcourir récursivement un répertoire et ses sous-dossiers

"""

    def explore_directory(self, directory=None):
        if directory is None:
            directory = self.root_directory

        for entry in os.scandir(directory):
            if entry.is_file() and self.is_music_file(entry.path):
                self.music_files.append(entry.path)
            elif entry.is_dir():
                self.explore_directory(entry.path)

"""

Définition de la méthode is_music_file pour vérifier si un fichier est un fichier audio MP3 ou FLAC en vérifiant son extension et son type MIME

"""

    def is_music_file(self, file_path):
        file_ext = os.path.splitext(file_path)[1].lower()
        mime_type = mimetypes.guess_type(file_path)[0]

        if file_ext in ['.mp3', '.flac'] and mime_type is not None and mime_type.startswith('audio/'):
            return True
        return False

"""

Définition de la méthode get_music_files pour renvoyer la liste des fichiers musicaux filtrés

"""

    def get_music_files(self):
        return self.music_files


path = #'\\Chemin\\Vers_Album_1'


music_explorer = MusicFileExplorer(path) # Création d'une instance de MusicFileExplorer avec le chemin du répertoire racine
music_explorer.explore_directory()
filtered_music_files = music_explorer.get_music_files()

# Affichage des fichiers musicaux filtrés en fonction de leur extension
for music_file in filtered_music_files:
    print(music_file)

