import sys
from pathlib import Path

JPEG = []
JPG = []
PNG = []
SVG = []
AVI = []
MP4 = []
MOV = []
MKV = []
DOC = []
DOCX = []
TXT = []
PDF = []
XLSX = []
PPTX = []
MP3 = []
OGG = []
WAV = []
AMR = []
my_other = []
archives = []

# Регістр відомих розширень:
REGISTER_EXTENSION = {
    'JPEG': JPEG,
    'JPG': JPG,
    'PNG': PNG,
    'SVG': SVG,
    'AVI': AVI,
    'MP4': MP4,
    'MOV': MOV,
    'MKV': MKV,
    'DOC': DOC,
    'DOCX': DOCX,
    'TXT': TXT,
    'PDF': PDF,
    'XLSX': XLSX,
    'PPTX': PPTX,
    'MP3': MP3,
    'OGG': OGG,
    'WAV': WAV,
    'AMR': AMR,
    'ZIP': archives,
    'GZ': archives,
    'TAR': archives,
}

# Добавляємо змінну, де будуть зберігатися всі папки:
FOLDERS = []
# Добавляємо змінну, де будуть зберігатися всі відомі розширення:
EXTENSIONS = set()
# Добавляємо змінну, де будуть зберігатися всі розширення, які не змогли ідентифікувати:
UNKNOWN = set()


# Функція, яка повертає позширення з файла:
def get_extension(name: str) -> str:
    return Path(name).suffix[1:].upper()  # suffix[1:] -> .jpg -> JPG

# Функція, яка отримує на вхід якийсь шлях, і перевіряє по цьому шляху чи це є папка, чи файл:
def scan(folder: Path):
    for item in folder.iterdir():
        # Робота з папкою
        if item.is_dir():  # перевіряємо чи об'єкт папка
            if item.name not in ('archives', 'video', 'audio', 'documents', 'images', 'my_other'):
                FOLDERS.append(item)
                scan(item)
            continue

        # Робота з файлом
        extension = get_extension(item.name)  # беремо розширення файлу
        full_name = folder / item.name  # беремо повний шлях до файлу
        if not extension:
            my_other.append(full_name)
        else:
            try:
                ext_reg = REGISTER_EXTENSION[extension]
                ext_reg.append(full_name)
                EXTENSIONS.add(extension)
            except KeyError:
                UNKNOWN.add(extension)  # .py, .psd, .cr2
                my_other.append(full_name)

if __name__ == '__main__':  # добавляємо точку входження
    folder_process = sys.argv[1]
    scan(Path(folder_process))
    print(f'Images jpeg: {JPEG}')
    print(f'Images jpg: {JPG}')
    print(f'Images png: {PNG}')
    print(f'Images svg: {SVG}')
    print(f'Video avi: {AVI}')
    print(f'Video avi: {MP4}')
    print(f'Video avi: {MOV}')
    print(f'Video avi: {MKV}')
    print(f'Documents doc: {DOC}')
    print(f'Documents docx: {DOCX}')
    print(f'Documents txt: {TXT}')
    print(f'Documents pdf: {PDF}')
    print(f'Documents xlsx: {XLSX}')
    print(f'Documents pptx: {PPTX}')
    print(f'Audio mp3: {MP3}')
    print(f'Audio mp3: {OGG}')
    print(f'Audio mp3: {WAV}')
    print(f'Audio mp3: {AMR}')
    print(f'Archives zip, gz, ztar: {archives}')

    print(f'EXTENSIONS: {EXTENSIONS}')
    print(f'UNKNOWN: {UNKNOWN}')
    print(f'EXTENSIONS: {EXTENSIONS}')
    print(f'FOLDERS: {FOLDERS}')