import os
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from typing import Optional

from PIL import Image, ImageTk
from mutagen.flac import FLAC
from mutagen.id3 import ID3
from mutagen.mp3 import MP3

from cli import extract_metadata, Metadata, MusicFileExplorer


def get_cover_art_path(file_path: str) -> Optional[str]:
    """
    Fonction pour obtenir l'image de couverture de l'album à partir d'un fichier MP3 ou FLAC.

    :param file_path: Le chemin du fichier.
    :return: L'image de couverture de l'album.
    """
    file_ext = os.path.splitext(file_path)[1].lower()

    if file_ext == ".mp3":
        audio = MP3(file_path, ID3=ID3)
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


class MusicExplorerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Explorateur de fichiers musicaux")
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        self.create_widgets()

    def create_widgets(self):
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.tree_frame = ttk.LabelFrame(self.main_frame, text="Fichiers musicaux", padding="10")
        self.tree_frame.grid(column=0, row=0, rowspan=2, padx=(0, 10), sticky=(tk.W, tk.E, tk.N, tk.S))

        self.tree = ttk.Treeview(self.tree_frame, selectmode="browse")
        self.tree.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.tree_scroll = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        self.tree_scroll.grid(column=1, row=0, sticky=(tk.N, tk.S))
        self.tree["yscrollcommand"] = self.tree_scroll.set

        self.tree["columns"] = ("path",)
        self.tree.column("#0", width=200)
        self.tree.column("path", width=0, stretch=tk.NO)
        self.tree.heading("#0", text="Nom")
        self.tree.heading("path", text="Chemin")

        self.tree.bind("<<TreeviewSelect>>", self.display_metadata)

        self.select_directory_button = ttk.Button(self.tree_frame, text="Sélectionner un dossier",
                                                  command=self.select_directory)
        self.select_directory_button.grid(column=0, row=1, pady=(10, 0), sticky=(tk.W, tk.E))

        self.metadata_frame = ttk.LabelFrame(self.main_frame, text="Métadonnées", padding="10")
        self.metadata_frame.grid(column=1, row=0, padx=(0, 10), sticky=(tk.W, tk.E, tk.N, tk.S))

        self.cover_art_label = ttk.Label(self.metadata_frame)
        self.cover_art_label.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.metadata_text = tk.Text(self.metadata_frame, wrap=tk.WORD, height=15, width=50)
        self.metadata_text.grid(column=0, row=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.metadata_text.config(state=tk.DISABLED)

        self.playlist_frame = ttk.LabelFrame(self.main_frame, text="Playlist", padding="10")
        self.playlist_frame.grid(column=2, row=0, padx=(0, 10), sticky=(tk.W, tk.E, tk.N, tk.S))

    def select_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.tree.delete(*self.tree.get_children())

            music_explorer = MusicFileExplorer(directory)
            music_explorer.explore_directory()
            music_files = music_explorer.get_music_files()

            for music_file in music_files:
                filename = os.path.basename(music_file)
                self.tree.insert("", "end", text=filename, values=(music_file,))

    def display_metadata(self, event):
        selected_item = self.tree.selection()[0]
        file_path = self.tree.item(selected_item)["values"][0]

        metadata = extract_metadata(file_path)
        if metadata:
            self.show_cover_art(metadata, file_path)
            self.show_metadata_text(metadata)

    def show_cover_art(self, metadata: Metadata, file_path: str):
        cover_art_path = get_cover_art_path(file_path)
        if cover_art_path:
            image = Image.open(cover_art_path)
            image.thumbnail((200, 200))
            photo = ImageTk.PhotoImage(image)
            self.cover_art_label.config(image=photo)
            self.cover_art_label.image = photo
        else:
            self.cover_art_label.config(image=None)

    def show_metadata_text(self, metadata: Metadata):
        self.metadata_text.config(state=tk.NORMAL)
        self.metadata_text.delete(1.0, tk.END)
        self.metadata_text.insert(tk.END, str(metadata))
        self.metadata_text.config(state=tk.DISABLED)


def main():
    root = tk.Tk()
    MusicExplorerGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
