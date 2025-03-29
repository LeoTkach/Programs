from mutagen.id3 import ID3, TIT2, TPE1, APIC, TRCK, TALB
from mutagen.mp3 import MP3

# Пути к файлам
mp3_file = r"D:\CV\Music\Me and My Broken Heart.mp3"
image_file = r"D:\CV\Music\rixton.jpg"

# Открываем MP3-файл и создаем ID3-теги, если их нет
audio = MP3(mp3_file, ID3=ID3)

if not audio.tags:
    audio.add_tags()

# Удаляем все старые обложки (исправленный способ)
apic_keys = [tag for tag in audio.tags.keys() if tag.startswith("APIC")]
for tag in apic_keys:
    del audio.tags[tag]

# Читаем картинку
with open(image_file, "rb") as img:
    cover_data = img.read()

# Добавляем теги
audio.tags["TIT2"] = TIT2(encoding=3, text="Me and My Broken Heart")  # Название песни
audio.tags["TPE1"] = TPE1(encoding=3, text="Rixton")  # Исполнитель
audio.tags["TRCK"] = TRCK(encoding=3, text="3")  # Номер трека
audio.tags["TALB"] = TALB(encoding=3, text="")  # Альбом (можно изменить)

# Добавляем обложку
audio.tags.add(
    APIC(
        encoding=3,  # UTF-8
        mime="image/jpeg",  # Формат изображения
        type=3,  # 3 = обложка (Front Cover)
        desc="Cover",
        data=cover_data,
    )
)

# Сохраняем изменения
audio.save(v2_version=3)  # Принудительно сохраняем как ID3v2.3 для совместимости
