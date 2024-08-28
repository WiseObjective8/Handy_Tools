# pylint: disable = missing-function-docstring
# pylint: disable = missing-class-docstring
# pylint: disable = missing-module-docstring
# pylint: disable = broad-exception-caught
import os
import sys
import argparse
from Youtube.yt_vid_logic import YT
from Youtube.yt_playlist_logic import PL
from Youtube.logic_helpers import APP_PATH


def show_files(path):
    try:
        if sys.platform == "win32":
            os.startfile(path)
        elif sys.platform == "darwin":
            os.system(f"open {path}")
        else:
            os.system(f"xdg-open {path}")
    except Exception as e:
        print(f"Failed to open folder: {str(e)}")


def download(url, is_playlist, file_type, resolution):
    try:
        if is_playlist:
            downloader = PL(url)
            downloader.download_playlist(file_type, resolution)
        else:
            downloader = YT(url)
            downloader.download_video(file_type, resolution)
        print(f"{downloader.title} is downloaded")
    except Exception as e:
        print(f"Error: {str(e)}")


def main():
    parser = argparse.ArgumentParser(description="YouTube Downloader CLI")
    parser.add_argument("-u", "--url", type=str, help="URL of the video or playlist")
    parser.add_argument(
        "-p", "--playlist", action="store_true", help="Download as a playlist"
    )
    parser.add_argument(
        "-f",
        "--file-type",
        type=int,
        default=3,
        choices=[1, 2, 3],
        help="File type to download: 1 for audio, 2 for video, 3 for both",
    )
    parser.add_argument(
        "-r",
        "--resolution",
        type=int,
        default=3,
        choices=[1, 2, 3],
        help="Resolution: 1 for 1080p, 2 for 720p, 3 for 480p",
    )
    parser.add_argument(
        "-s", "--show", action="store_true", help="Show the download folder"
    )

    args = parser.parse_args()

    if args.show:
        show_files(APP_PATH)
        return

    if not args.url:
        print("URL is required unless using the -s/--show option.")
        return

    download(args.url, args.playlist, args.file_type, args.resolution)


def interactive_shell():
    print("YouTube Downloader CLI")
    while True:
        try:
            # Custom prompt
            command = input("YT-CLI> ").strip()
            if command.lower() in ["exit", "quit"]:
                break

            # Parse command and arguments
            args = command.split()
            if not args:
                continue

            if args[0] == "show":
                show_files(APP_PATH)
            elif args[0] == "download":
                parser = argparse.ArgumentParser()
                parser.add_argument("-u", "--url", type=str, required=True)
                parser.add_argument("-p", "--playlist", action="store_true")
                parser.add_argument("-f", "--file-type", type=int, default=3)
                parser.add_argument("-r", "--resolution", type=int, default=3)
                cmd_args = parser.parse_args(args[1:])

                download(
                    cmd_args.url,
                    cmd_args.playlist,
                    cmd_args.file_type,
                    cmd_args.resolution,
                )
            else:
                print(f"Unknown command: {args[0]}")

        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {str(e)}")

    print("Exiting YT-CLI.")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main()
    else:
        interactive_shell()
