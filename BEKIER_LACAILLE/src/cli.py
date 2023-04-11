import argparse
from typing import Union

from tinytag import TinyTag


def extract_metadata(file_path: str) -> Union[None, dict]:
    """
    Fonction pour extraire les métadonnées d'un fichier MP3 ou FLAC.

    :param file_path: Chemin d'accès au fichier MP3 ou FLAC.
    :return: Un dictionnaire contenant les métadonnées si le fichier est valide, sinon None.
    """
    try:
        tag = TinyTag.get(file_path)

        metadata = {
            'title': tag.title,
            'artist': tag.artist,
            'album': tag.album,
            'duration': tag.duration,
            'genre': tag.genre,
            'track_number': tag.track,
            'year': tag.year,
        }

        return metadata

    except Exception as e:
        print(f"Erreur lors de l'extraction des métadonnées: {e}")
        return None


def main():
    parser = argparse.ArgumentParser(description="Extraction des métadonnées d'un fichier MP3 ou FLAC.")
    parser.add_argument('-f', '--file', type=str, required=True, help='Chemin d\'accès au fichier MP3 ou FLAC')
    args = parser.parse_args()

    if args.file is None:
        print('Veuillez spécifier un fichier avec l\'option -f.')
    else:
        metadata = extract_metadata(args.file)
        if metadata:
            print("Métadonnées extraites :")
            for key, value in metadata.items():
                print(f"{key}: {value}")


if __name__ == '__main__':
    main()
