import flet as ft
import moviepy.editor as mp
import os
import threading
import time

def main(page: ft.Page):
    page.title = "Video to Audio Converter"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    video_file_picker = ft.FilePicker(on_result=lambda e: setattr(video_path, 'value', e.files[0].path if e.files else ""))
    save_folder_picker = ft.FilePicker(on_result=lambda e: setattr(output_folder, 'value', e.path if e.path else ""))
    page.overlay.extend([video_file_picker, save_folder_picker])

    video_path = ft.TextField(label="Video file address", width=400, read_only=True)
    output_folder = ft.TextField(label="The address of the storage folder", width=400, read_only=True)

    video_picker_button = ft.ElevatedButton("Select the video file", icon=ft.icons.VIDEO_FILE, on_click=lambda _: video_file_picker.pick_files(allow_multiple=False))
    folder_picker_button = ft.ElevatedButton("Select the storage folder", icon=ft.icons.FOLDER, on_click=lambda _: save_folder_picker.get_directory_path())
    convert_button = ft.ElevatedButton("Convert", icon=ft.icons.AUDIO_FILE, on_click=lambda _: start_conversion_thread(video_path.value, output_folder.value, page))

    progress_bar = ft.ProgressBar(width=400, visible=False)

    page.add(
        ft.Column(
            [
                video_path,
                video_picker_button,
                output_folder,
                folder_picker_button,
                convert_button,
                progress_bar
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

    def start_conversion_thread(video_path, output_folder, page):
        threading.Thread(target=convert_video_to_audio, args=(video_path, output_folder, page)).start()

    def convert_video_to_audio(video_path, output_folder, page):
        if video_path and output_folder:
            try:
                progress_bar.visible = True
                progress_bar.value = 0
                page.update()

                video_filename = os.path.basename(video_path)
                audio_filename = os.path.splitext(video_filename)[0] + ".mp3"
                audio_path = os.path.join(output_folder, audio_filename)

                my_clip = mp.VideoFileClip(video_path)

                duration = my_clip.duration
                step = duration / 10

                for i in range(10):
                    time.sleep(step / 2)
                    progress_bar.value = (i + 1) / 10
                    page.update()

                my_clip.audio.write_audiofile(audio_path)

                progress_bar.value = 1.0
                page.update()

                success_dialog = ft.AlertDialog(
                    title=ft.Text("Successful conversion"),
                    content=ft.Text(f"Convert video to audio successfully! File saved: {audio_path}"),
                )
                page.dialog = success_dialog
                success_dialog.open = True
                page.update()

            except Exception as e:
                error_dialog = ft.AlertDialog(
                    title=ft.Text("Error"),
                    content=ft.Text(f"Error converting video: {e}"),
                )
                page.dialog = error_dialog
                error_dialog.open = True
                page.update()

            finally:
                progress_bar.visible = False
                page.update()
        else:
            incomplete_input_dialog = ft.AlertDialog(
                title=ft.Text("Incomplete input"),
                content=ft.Text("Please enter video file addresses and save folder!!"),
            )
            page.dialog = incomplete_input_dialog
            incomplete_input_dialog.open = True
            page.update()

ft.app(target=main)
