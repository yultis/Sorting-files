from pathlib import Path
import shutil
import sys
import file_parser
from normalize import normalize

# Функція, яка обробляє папки та переміщає файли, замінючи ("нормалізуючи") ім'я:
def handle_media(file_name: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents=True)
    file_name.replace(target_folder / normalize(file_name.name))

# Функція, яка розпаковує архіви, після чого видаляє самі архіви:
def handle_archive(file_name: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents=True)
    folder_for_file = target_folder / normalize(file_name.name.replace(file_name.suffix, ''))
    folder_for_file.mkdir(exist_ok=True, parents=True)
    
    try:
        shutil.unpack_archive(str(file_name.absolute()), str(folder_for_file.absolute()))
    except shutil.ReadError:
        folder_for_file.rmdir()
        return
    file_name.unlink()

    # Рекурсивно обробляємо розпакований вміст
    for item in folder_for_file.iterdir():
        if item.is_file() and item.suffix == '.zip':
            handle_archive(item, folder_for_file)


def main(folder: Path):
    file_parser.scan(folder) # викликаємо функцію scan з файлу file_parser
    # Ітераємося по кожному із списків всіх розширень JPEG, JPG, PNG, SVG, AVI і т.д. та визначаємо шлях, 
    # куди кладемо файли з відповідними розширеннями, викликаючи функцію handle_media:
    for file in file_parser.JPEG:
        handle_media(file, folder / 'images' / 'JPEG')
    for file in file_parser.JPG:
        handle_media(file, folder / 'images' / 'JPG')
    for file in file_parser.PNG:
        handle_media(file, folder / 'images' / 'PNG')
    for file in file_parser.SVG:
        handle_media(file, folder / 'images' / 'SVG')
    for file in file_parser.AVI:
        handle_media(file, folder / 'video' / 'AVI')
    for file in file_parser.MP4:
        handle_media(file, folder / 'video' / 'MP4')
    for file in file_parser.MOV:
        handle_media(file, folder / 'video' / 'MOV')
    for file in file_parser.MKV:
        handle_media(file, folder / 'video' / 'MKV')
    for file in file_parser.DOC:
        handle_media(file, folder / 'documents' / 'DOC')
    for file in file_parser.DOCX:
        handle_media(file, folder / 'documents' / 'DOCX')
    for file in file_parser.TXT:
        handle_media(file, folder / 'documents' / 'TXT')
    for file in file_parser.PDF:
        handle_media(file, folder / 'documents' / 'PDF')
    for file in file_parser.XLSX:
        handle_media(file, folder / 'documents' / 'XLSX')
    for file in file_parser.PPTX:
        handle_media(file, folder / 'documents' / 'PPTX')
    for file in file_parser.MP3:
        handle_media(file, folder / 'audio' / 'MP3')
    for file in file_parser.OGG:
        handle_media(file, folder / 'audio' / 'OGG')
    for file in file_parser.WAV:
        handle_media(file, folder / 'audio' / 'WAV')
    for file in file_parser.AMR:
        handle_media(file, folder / 'audio' / 'AMR')

    for file in file_parser.my_other:
        handle_media(file, folder / 'my_other')

    for file in file_parser.archives:
        handle_archive(file, folder / 'archives')

    for folder in file_parser.FOLDERS[::-1]:
        # Видаляємо пусті папки після сортування
        try:
            folder.rmdir()
        except OSError:
            print(f'Error during remove folder {folder}')


# Добавляємо точку входження:
if __name__ == "__main__":
    folder_process = Path(sys.argv[1])
    main(folder_process.resolve())