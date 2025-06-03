from PIL import Image, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

import os, time
from dotenv import load_dotenv
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from supabase import create_client, Client

# ===== Load Environment ===== #
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("❌ SUPABASE_URL atau SUPABASE_KEY belum diatur di file .env")

BUCKET_NAME = 'testfield'
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ===== Direktori Gambar ===== #
input_dir = "images"
output_dir = os.path.join(input_dir, "output")
os.makedirs(output_dir, exist_ok=True)

image_extensions = [".jpg", ".jpeg", ".png", ".JPG", ".JPEG", ".PNG"]

# ===== Upload ke Supabase ===== #
def upload_to_supabase(filepath):
    try:
        filename = os.path.basename(filepath)
        name_only, _ = os.path.splitext(filename)

        parts = name_only.split("_")
        if len(parts) >= 3:
            name = parts[0]
            tanggal = parts[1]
            jam = parts[2].replace("-", ":")
        else:
            name = name_only
            tanggal = ""
            jam = ""

        with open(filepath, 'rb') as f:
            file_data = f.read()

        supabase.storage.from_(BUCKET_NAME).upload(
            path=filename,
            file=file_data
        )
        print(f"[Upload ✅] Berhasil upload: {filename}")

        public_url = supabase.storage.from_(BUCKET_NAME).get_public_url(filename)
        print(f"[URL] {public_url}")

        supabase.table("fotos").insert({
            "name": name,
            "tanggal": tanggal,
            "jam": jam,
            "url": public_url
        }).execute()

        print(f"[DB ✅] Disimpan ke tabel: {name}, {tanggal}, {jam}, {public_url}")

    except Exception as e:
        print(f"[Upload ❌] Gagal upload {filepath}: {e}")

# ===== Konversi Gambar ===== #
def convert_single_image_to_webp(filepath, quality=80, resize_ratio=0.5):
    ext = os.path.splitext(filepath)[1]
    if ext.lower() not in image_extensions:
        return

    filename = os.path.basename(filepath)
    name, _ = os.path.splitext(filename)
    output_path = os.path.join(output_dir, name + ".webp")

    try:
        print(f"[Convert] {filename} → {output_path}")
        im = Image.open(filepath).convert("RGB")

        if resize_ratio < 1.0:
            new_size = (int(im.width * resize_ratio), int(im.height * resize_ratio))
            im = im.resize(new_size, Image.LANCZOS)
            print(f"[Resize] Ukuran baru: {new_size}")

        im.save(output_path, "webp", quality=quality, method=6)

        if not os.path.commonpath([filepath, output_dir]) == output_dir:
            os.remove(filepath)
            print(f"[Delete] File asli dihapus: {filepath}")

        upload_to_supabase(output_path)

    except Exception as e:
        print(f"[Error] Gagal konversi {filename}: {e}")

# ===== Watchdog Handler ===== #
class WatchFolder(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            time.sleep(0.5)
            convert_single_image_to_webp(event.src_path)

# ===== Main ===== #
if __name__ == "__main__":
    print(f"📁 Memantau folder: {input_dir}")
    event_handler = WatchFolder()
    observer = Observer()
    observer.schedule(event_handler, path=input_dir, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
