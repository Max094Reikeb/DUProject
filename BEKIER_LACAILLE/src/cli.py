import argparse
from mutagen.easyid3 import EasyID3
from mutagen.flac import FLAC


def get_metadata(filename: str):
    """
    Extrait les métadonnées d'un fichier MP3 ou FLAC et le retourne en un dictionnaire.

    Args:
        filepath (str): Chemin du fichier d'entrée.

    Returns:
        dict: Un dictionnaire contenant les métadonnées extraites du fichier.
    """

    if filename.endswith('.mp3'):
        audio = EasyID3(filename)
    elif filename.endswith('.flac'):
        audio = FLAC(filename)
    else:
        raise ValueError('Format de fichier non supporté.')

    return {'title': audio['title'][0] if 'title' in audio else None,
            'artist': audio['artist'][0] if 'artist' in audio else None,
            'album': audio['album'][0] if 'album' in audio else None,
            'year': audio['date'][0] if 'date' in audio else None}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extraire les métadonnées d\'un fichier MP3 ou FLAC.')
    parser.add_argument('-f', '--file', type=str, help='Le fichier dont on veut extraire les métadonnées.',
                        required=True)
    args = parser.parse_args()

    if args.file is None:
        print('Veuillez spécifier un fichier avec l\'option -f.')
    else:
        metadata = get_metadata(args.file)
        for key, value in metadata:
            print(f'{key}: {value}')
