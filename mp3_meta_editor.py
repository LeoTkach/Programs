from mutagen.id3 import ID3, TIT2, TPE1, APIC, TRCK, TALB
from mutagen.mp3 import MP3


mp3_file = r"D:\CV\Music\Me and My Broken Heart.mp3"
image_file = r"D:\CV\Music\rixton.jpg"

audio = MP3(mp3_file, ID3=ID3)

if not audio.tags:
    audio.add_tags()


apic_keys = [tag for tag in audio.tags.keys() if tag.startswith("APIC")]
for tag in apic_keys:
    del audio.tags[tag]


with open(image_file, "rb") as img:
    cover_data = img.read()

audio.tags["TIT2"] = TIT2(encoding=3, text="Me and My Broken Heart")  
audio.tags["TPE1"] = TPE1(encoding=3, text="Rixton")  
audio.tags["TRCK"] = TRCK(encoding=3, text="3")  
audio.tags["TALB"] = TALB(encoding=3, text="")  


audio.tags.add(
    APIC(
        encoding=3,  # UTF-8
        mime="image/jpeg",  
        type=3,  
        desc="Cover",
        data=cover_data,
    )
)


audio.save(v2_version=3)  
