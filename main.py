import flet as ft
import moviepy.editor as mp

def main(page: ft.Page):
    page.title = "Video to Audio Converter"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    video_file_picker = ft.FilePicker(on_result=lambda e: setattr(video_path, 'value', e.files[0].path if e.files else ""))
    page.overlay.append(video_file_picker)

    video_path = ft.TextField(label="Video file address", width=400, read_only=True)
    output_textbox = ft.TextField(label="Output audio file address", width=400)

    video_picker_button = ft.ElevatedButton("Select the video file", icon=ft.icons.VIDEO_FILE, on_click=lambda _: video_file_picker.pick_files(allow_multiple=False))
    convert_button = ft.ElevatedButton("convert", icon=ft.icons.AUDIO_FILE, on_click=lambda _: convert_video_to_audio(video_path.value, output_textbox.value, page))

    page.add(
        ft.Column(
            [
                video_path,
                video_picker_button,
                output_textbox,
                convert_button,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

def convert_video_to_audio(video_path, audio_path, page):
    if video_path and audio_path:
        try:
            my_clip = mp.VideoFileClip(video_path)
            my_clip.audio.write_audiofile(audio_path)
            page.dialog.open(
                ft.AlertDialog(
                    title=ft.Text("Successful conversion"),
                    content=ft.Text("Convert video to audio successfully!"),
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
                content=ft.Text("Please enter video and audio file addresses!"),
                on_dismiss=lambda e: page.dialog.close(),
            )
        )

ft.app(target=main)
