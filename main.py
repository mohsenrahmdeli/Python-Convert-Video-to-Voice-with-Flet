import flet as ft
import moviepy.editor as mp
import os

def main(page: ft.Page):
    page.title = "Video to Audio Converter"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # ایجاد ویجت‌ها
    video_file_picker = ft.FilePicker(on_result=lambda e: setattr(video_path, 'value', e.files[0].path if e.files else ""))
    save_folder_picker = ft.FilePicker(on_result=lambda e: setattr(output_folder, 'value', e.path if e.path else ""))
    page.overlay.extend([video_file_picker, save_folder_picker])

    video_path = ft.TextField(label="Video file address", width=400, read_only=True)
    output_folder = ft.TextField(label="The address of the storage folder", width=400, read_only=True)

    video_picker_button = ft.ElevatedButton("Select the video file", icon=ft.icons.VIDEO_FILE, on_click=lambda _: video_file_picker.pick_files(allow_multiple=False))
    folder_picker_button = ft.ElevatedButton("Select the storage folder", icon=ft.icons.FOLDER, on_click=lambda _: save_folder_picker.get_directory_path())
    convert_button = ft.ElevatedButton("Convert", icon=ft.icons.AUDIO_FILE, on_click=lambda _: convert_video_to_audio(video_path.value, output_folder.value, page))

    page.add(
        ft.Column(
            [
                video_path,
                video_picker_button,
                output_folder,
                folder_picker_button,
                convert_button,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

def convert_video_to_audio(video_path, output_folder, page):
    if video_path and output_folder:
        try:
            video_filename = os.path.basename(video_path)
            audio_filename = os.path.splitext(video_filename)[0] + ".mp3"
            audio_path = os.path.join(output_folder, audio_filename)

            my_clip = mp.VideoFileClip(video_path)
            my_clip.audio.write_audiofile(audio_path)

            page.dialog.open(
                ft.AlertDialog(
                    title=ft.Text("Successful conversion"),
                    content=ft.Text(f"Convert video to audio successfully! File saved: {audio_path}"),
                    on_dismiss=lambda e: page.dialog.close(),
                )
            )
        except Exception as e:
            page.dialog.open(
                ft.AlertDialog(
                    title=ft.Text("Error"),
                    content=ft.Text(f"Error converting video: {e}"),
                    on_dismiss=lambda e: page.dialog.close(),
                )
            )
    else:
        page.dialog.open(
            ft.AlertDialog(
                title=ft.Text("Incomplete input"),
                content=ft.Text("Please enter video file addresses and save folder!"),
                on_dismiss=lambda e: page.dialog.close(),
            )
        )

ft.app(target=main)
