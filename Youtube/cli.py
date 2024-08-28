# code_cli.py

import argparse
import subprocess
import os
import downloader

DOWNLOAD_PATH = downloader.DOWNLOAD_PATH
YT = downloader.Download()


def main():
    parser = argparse.ArgumentParser(description="YouTube Video Downloader CLI")
    subparsers = parser.add_subparsers(dest="command")

    # Command for downloading a single video
    video_parser = subparsers.add_parser("video", help="Download a YouTube video")
    video_parser.add_argument("url", type=str, help="URL of the YouTube video")

    # Command for downloading a playlist
    playlist_parser = subparsers.add_parser(
        "playlist", help="Download a YouTube playlist"
    )
    playlist_parser.add_argument("url", type=str, help="URL of the YouTube playlist")

    # Command for showing contents of the download directory
    show_parser = subparsers.add_parser("show", help="Show downloaded files")

    # Command for opening the download directory
    open_parser = subparsers.add_parser("open", help="Open download directory")

    args = parser.parse_args()

    if args.command == "video":
        t = (
            int(input("Download type:\n1. audio\n2. video\n3. both\ndefault [3] --> "))
            or 3
        )
        u = int(input("Resolution:\n1. 1080p\n2. 720p\n3. 480p\ndefault [1] --> ")) or 1
        confirm = (
            input(
                f"Proceed with type: {YT.dty[t]} and resolution: {YT.res[u]}/ [yes/no]"
            )
            .strip()
            .lower()
            == "yes"
        )
        if confirm:
            download_path = YT.download_video(args.url, download_type=t, resolution=u)
            print(f"Download complete: {download_path}")
        else:
            print("Download cancelled")
    elif args.command == "playlist":
        downloader.download_playlist(args.url)
        print(f"Playlist downloaded to: {DOWNLOAD_PATH}")

    elif args.command == "show":
        for root, dirs, files in os.walk(DOWNLOAD_PATH):
            for file in files:
                print(file)

    elif args.command == "open":
        subprocess.run(["explorer", DOWNLOAD_PATH])


if __name__ == "__main__":
    main()
