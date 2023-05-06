import zipfile
import chardet

def unarchive_book(path):
    title = path.rsplit("/", 1)[1].replace(".zip", "")
    archive = zipfile.ZipFile(path, 'r')

    for txt_file in archive.namelist():
        print(title)
        if txt_file.endswith(".txt"):
            raw_text = archive.read(txt_file)
            break

    detect = chardet.detect(raw_text)

    raw_text = raw_text.decode(detect["encoding"])

    return raw_text
