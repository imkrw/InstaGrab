from flet import *
import instaloader
import os
import argparse
import shutil


parser = argparse.ArgumentParser()
parser.add_argument(
    "--username", type=str, help="Instagram username (Only Public Profile)"
)
args = parser.parse_args()


def event_handle(e):
    global image_folder
    if e.data == "close":
        try:
            if image_folder:
                shutil.rmtree(image_folder)
        except:
            pass
        e.page.window_destroy()


def main(page: Page):
    page.theme_mode = ThemeMode.DARK
    page.window_center()
    page.on_window_event = event_handle
    page.window_prevent_close = True
    page.window_width = 775
    page.window_height = 960
    page.window_maximizable = False
    page.window_resizable = False

    if args.username:
        ig = instaloader.Instaloader(
            quiet=True,
            compress_json=False,
            save_metadata=False,
            check_resume_bbd=False,
            download_videos=False,
            download_video_thumbnails=False,
        )
        page.title = "InstaGrab - Downloading"
        page.update()
        ig.download_profile(args.username)
        page.title = "InstaGrab - Finished"
        page.update()
    else:
        page.window_destroy()
        print("Please provide a username using the --username argument.")

    images = Column(expand=True, spacing=0, scroll="always")
    global image_folder
    image_folder = args.username
    image_file_names = [
        file
        for file in os.listdir(image_folder)
        if file.endswith(".jpg") and "profile" not in file
    ]

    page.add(
        Column(
            horizontal_alignment=CrossAxisAlignment.CENTER,
            expand=True,
            spacing=0,
            controls=[images, Row()],
        )
    )

    for file_name in image_file_names:
        image_path = os.path.join(image_folder, file_name)
        images.controls.append(
            Image(
                src=image_path,
            )
        )

    page.update()


app(target=main)
