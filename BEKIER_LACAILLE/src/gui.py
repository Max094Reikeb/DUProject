import os
import mimetypes

class MusicFileExplorer:
    def __init__(self, root_directory):
        self.root_directory = root_directory
        self.music_files = []

    def explore_directory(self, directory=None):
        """
        Méthode pour explorer un répertoire et collecter les chemins des fichiers de musique (MP3 ou FLAC) qu'il contient.
        Cette méthode est récursive, c'est-à-dire qu'elle parcourt également tous les sous-répertoires du répertoire donné.
        :param directory: Le répertoire à explorer. Si None, utilise le répertoire racine de l'objet.
        """

        # Si le répertoire n'est pas spécifié, utilise le répertoire racine de l'objet.
        if directory is None:
            directory = self.root_directory

        # Parcourir les entrées du répertoire (fichiers et sous-répertoires).
        for entry in os.scandir(directory):
            # Si l'entrée est un fichier et qu'il s'agit d'un fichier de musique, ajoute son chemin à la liste des fichiers de musique.
            if entry.is_file() and self.is_music_file(entry.path):
                self.music_files.append(entry.path)
            # Si l'entrée est un répertoire, explore ce répertoire récursivement.
            elif entry.is_dir():
                self.explore_directory(entry.path)

    def is_music_file(self, file_path):
        """
        Cette fonction vérifie si un fichier est de type musical en se basant sur son extension et son type MIME.

        Args:
            file_path (str): Le chemin du fichier à vérifier.

        Returns:
            bool: True si le fichier est un fichier musical (.mp3 ou .flac), False sinon.
        """
        # Récupère l'extension du fichier et la convertit en minuscules
        file_ext = os.path.splitext(file_path)[1].lower()

        # Utilise la bibliothèque 'mimetypes' pour deviner le type MIME du fichier
        mime_type = mimetypes.guess_type(file_path)[0]

        # Vérifie si l'extension du fichier est .mp3 ou .flac et si le type MIME commence par 'audio/'
        if file_ext in ['.mp3', '.flac'] and mime_type is not None and mime_type.startswith('audio/'):
            return True

        # Retourne False si les conditions ci-dessus ne sont pas remplies
        return False

    # Définition de la méthode get_music_files
    def get_music_files(self):
        """
        Cette méthode retourne la liste des fichiers musicaux trouvés par l'instance de MusicFileExplorer.

        Returns:
            list: La liste des fichiers musicaux trouvés.
        """
        return self.music_files


# Chemin du répertoire racine contenant les fichiers musicaux
path = '\\Users\gucio\Documents\Orelsan'

# Création d'une instance de MusicFileExplorer avec le chemin du répertoire racine
music_explorer = MusicFileExplorer(path)

# Exploration du répertoire racine pour trouver les fichiers musicaux
music_explorer.explore_directory()

# Récupération de la liste des fichiers musicaux filtrés
filtered_music_files = music_explorer.get_music_files()

# Affichage des fichiers musicaux filtrés en fonction de leur extension
for music_file in filtered_music_files:
    print(music_file)
