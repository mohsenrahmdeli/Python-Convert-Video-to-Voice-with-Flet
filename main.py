from turtle import color
from fastapi import background
import flet as ft
import moviepy.editor as mp
import os
import threading
import time
import subprocess
import platform

def main(page: ft.Page):
    # Page settings
    page.title = "Video to Audio Converter"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window_width= 450
    page.window_height = 450

    # Create widgets
    video_file_picker = ft.FilePicker(on_result=lambda e: setattr(video_path, 'value', e.files[0].path if e.files else ""))
    save_folder_picker = ft.FilePicker(on_result=lambda e: setattr(output_folder, 'value', e.path if e.path else ""))
    page.overlay.extend([video_file_picker, save_folder_picker])

    video_path = ft.TextField(label="Video file address", width=400, read_only=True)
    output_folder = ft.TextField(label="The address of the storage folder", width=400, read_only=True)

    video_picker_button = ft.ElevatedButton("Select the video file", icon=ft.icons.VIDEO_FILE, on_click=lambda _: video_file_picker.pick_files(allow_multiple=False))
    folder_picker_button = ft.ElevatedButton("Select the storage folder", icon=ft.icons.FOLDER, on_click=lambda _: save_folder_picker.get_directory_path())
    convert_button = ft.ElevatedButton("Convert", icon=ft.icons.AUDIO_FILE, on_click=lambda _: start_conversion_thread(video_path.value, output_folder.value, page))

    # Create loading animation and message and hide them
    loading_indicator = ft.ProgressRing(visible=False)
    loading_text = ft.Text(
        "The video is being converted to sound and after completion, the folder where the audio file is saved will be opened.",
        visible=False,
        weight=ft.FontWeight.BOLD,
        rtl= True
        )

    # Add widgets to the page
    page.add(
        ft.Column(
            [
                video_path,
                video_picker_button,
                output_folder,
                folder_picker_button,
                convert_button,
                loading_indicator,
                loading_text,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

    # Function to start conversion in a separate thread
    def start_conversion_thread(video_path, output_folder, page):
        threading.Thread(target=convert_video_to_audio, args=(video_path, output_folder, page)).start()

    def convert_video_to_audio(video_path, output_folder, page):
        if video_path and output_folder:
            try:
                # Show loading animation and message
                loading_indicator.visible = True
                loading_text.visible = True
                page.update()

                # Extract the name of the video file
                video_filename = os.path.basename(video_path)
                audio_filename = os.path.splitext(video_filename)[0] + ".mp3"
                audio_path = os.path.join(output_folder, audio_filename)

                # Convert video to audio
                my_clip = mp.VideoFileClip(video_path)
                my_clip.audio.write_audiofile(audio_path)

                # Hide loading animation and message
                loading_indicator.visible = False
                loading_text.visible = False
                page.update()

                # Display success message
                success_dialog = ft.AlertDialog(
                    bgcolor="GREEN",
                    title=ft.Text("Successful conversion"),
                    content=ft.Text(
                        f"Convert video to audio successfully! File saved : {audio_path}",
                        weight=ft.FontWeight.BOLD,
                        rtl= True),
                    on_dismiss=lambda e: open_folder(output_folder)
                )
                page.dialog = success_dialog
                success_dialog.open = True
                page.update()

            except Exception as e:
                error_dialog = ft.AlertDialog(
                    bgcolor="RED",
                    title=ft.Text("Error"),
                    content=ft.Text(f"Error converting video : {e}"),
                )
                page.dialog = error_dialog
                error_dialog.open = True
                page.update()

        else:
            incomplete_input_dialog = ft.AlertDialog(
                bgcolor="RED",
                title=ft.Text("Incomplete input",
                    weight=ft.FontWeight.BOLD,
                    rtl= True),
                content=ft.Text("Please enter video file addresses and save folder!",
                                weight=ft.FontWeight.BOLD,
                                rtl= True
                                ),
            )
            page.dialog = incomplete_input_dialog
            incomplete_input_dialog.open = True
            page.update()

    # Function to open the save folder
    def open_folder(folder_path):
        if platform.system() == "Windows":
            os.startfile(folder_path)
        elif platform.system() == "Darwin":  # macOS
            subprocess.Popen(["open", folder_path])
        else:  # Linux
            subprocess.Popen(["xdg-open", folder_path])

ft.app(target=main)
