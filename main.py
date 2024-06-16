import os
import shutil
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class DownloadOrganizerHandler(FileSystemEventHandler):
    def __init__(self, folder_to_track, folders_by_extension):
        self.folder_to_track = folder_to_track
        self.folders_by_extension = folders_by_extension
        self.create_folders()
        self.organize_existing_files()

    def create_folders(self):
        for folder in set(self.folders_by_extension.values()):
            if not os.path.exists(folder):
                os.makedirs(folder)
                print(f"Created folder: {folder}")

    def organize_existing_files(self):
        for filename in os.listdir(self.folder_to_track):
            source = os.path.join(self.folder_to_track, filename)
            if os.path.isfile(source):
                self.process_file(source, filename)

    def on_modified(self, event):
        print("Modification detected.")
        for filename in os.listdir(self.folder_to_track):
            source = os.path.join(self.folder_to_track, filename)
            if os.path.isfile(source):
                self.process_file(source, filename)

    def process_file(self, source, filename):
        print(f"Processing file: {filename}")
        extension = os.path.splitext(filename)[1].lower()
        if extension in self.folders_by_extension:
            destination_folder = self.folders_by_extension[extension]
            destination = os.path.join(destination_folder, filename)
            destination = self.handle_duplicates(destination)
            print(f"Moving {source} to {destination}")
            shutil.move(source, destination)
        else:
            print(f"No folder defined for extension: {extension}")

    def handle_duplicates(self, path):
        base, extension = os.path.splitext(path)
        counter = 1
        new_path = path
        while os.path.exists(new_path):
            new_path = f"{base}_{counter}{extension}"
            counter += 1
        return new_path

def main():
    downloads_folder = os.path.expanduser("~/Downloads")
    folders_by_extension = {
        # Images
        '.jpg': os.path.join(downloads_folder, 'Images'),
        '.jpeg': os.path.join(downloads_folder, 'Images'),
        '.png': os.path.join(downloads_folder, 'Images'),
        '.gif': os.path.join(downloads_folder, 'Images'),
        '.bmp': os.path.join(downloads_folder, 'Images'),
        '.svg': os.path.join(downloads_folder, 'Images'),

        # Documents
        '.pdf': os.path.join(downloads_folder, 'Documents'),
        '.doc': os.path.join(downloads_folder, 'Documents'),
        '.docx': os.path.join(downloads_folder, 'Documents'),
        '.xls': os.path.join(downloads_folder, 'Documents'),
        '.xlsx': os.path.join(downloads_folder, 'Documents'),
        '.ppt': os.path.join(downloads_folder, 'Documents'),
        '.pptx': os.path.join(downloads_folder, 'Documents'),
        '.txt': os.path.join(downloads_folder, 'Documents'),
        '.odt': os.path.join(downloads_folder, 'Documents'),

        # Music
        '.mp3': os.path.join(downloads_folder, 'Music'),
        '.wav': os.path.join(downloads_folder, 'Music'),
        '.aac': os.path.join(downloads_folder, 'Music'),
        '.flac': os.path.join(downloads_folder, 'Music'),

        # Videos
        '.mp4': os.path.join(downloads_folder, 'Videos'),
        '.mov': os.path.join(downloads_folder, 'Videos'),
        '.avi': os.path.join(downloads_folder, 'Videos'),
        '.mkv': os.path.join(downloads_folder, 'Videos'),
        '.wmv': os.path.join(downloads_folder, 'Videos'),

        # Archives
        '.zip': os.path.join(downloads_folder, 'Archives'),
        '.rar': os.path.join(downloads_folder, 'Archives'),
        '.tar': os.path.join(downloads_folder, 'Archives'),
        '.gz': os.path.join(downloads_folder, 'Archives'),

        # Code
        '.py': os.path.join(downloads_folder, 'Code'),
        '.java': os.path.join(downloads_folder, 'Code'),
        '.cpp': os.path.join(downloads_folder, 'Code'),
        '.js': os.path.join(downloads_folder, 'Code'),
        '.html': os.path.join(downloads_folder, 'Code'),
        '.css': os.path.join(downloads_folder, 'Code'),
        '.json': os.path.join(downloads_folder, 'Code'),
        '.xml': os.path.join(downloads_folder, 'Code'),
        '.sh': os.path.join(downloads_folder, 'Code'),

        # Others
        '.iso': os.path.join(downloads_folder, 'DiscImages'),
        '.exe': os.path.join(downloads_folder, 'Executables'),
        '.msi': os.path.join(downloads_folder, 'Executables'),
    }

    event_handler = DownloadOrganizerHandler(downloads_folder, folders_by_extension)
    observer = Observer()
    observer.schedule(event_handler, downloads_folder, recursive=False)
    observer.start()

    print("Starting observer. Monitoring folder:", downloads_folder)
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    print("Observer stopped.")

if __name__ == "__main__":
    main()
