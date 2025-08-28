#!python3

from pathlib import Path
from send2trash import send2trash
import sys

def list_directory(path: Path) -> list[Path]:
    """
    Retourne la liste des fichiers contenus dans un répertoire.
    """
    if not path.is_dir():
        print(f"{path} n'est pas un répertoire valide")
        sys.exit(1)

    return [f for f in path.iterdir()]

def list_files_recursive(path: Path) -> list[Path]:
    """
    Retourne tous les fichiers contenus dans le chemin donné (récursif si dossier).
    """
    files: list[Path] = []

    if path.is_dir():
        for root, _, filenames in os.walk(path):
            root_path = Path(root)
            for file in filenames:
                files.append(root_path / file)
    else:
        files.append(path)

    return files

def is_oversized(file_path: Path, limit_mb: int = 100) -> bool:
    """
    Vérifie si un fichier dépasse la taille limite (par défaut 100 MB)
    """
    size = file_path.stat().st_size
    limit_bytes = limit_mb * (2 ** 20)
    return size > limit_bytes

def move_to_trash(file_path: Path) -> None:
    """
    Envoie un fichier à la corbeille.
    """
    try:
        send2trash(file_path)
    except Exception as e:
        print(f"Erreur lors de la suppression de {file_path}: {e}")

def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python unneeded_files.py [path]")
        sys.exit(1)

    base_path = Path(sys.argv[1])
    entries = list_directory(base_path)

    try:
        for entry in entries:
            for file_path in list_files_recursive(entry):
                if is_oversized(file_path):
                    move_to_trash(file_path)
    except Exception as e:
        print(f"Erreur générale: {e}")

if __name__ == "__main__":
    import os
    main()
