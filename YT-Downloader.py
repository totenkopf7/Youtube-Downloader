import subprocess
import threading
from tkinter import *
import tkinter
from tkinter import ttk
from tkinter import filedialog
from pytube import YouTube
from tkinter import messagebox
from pytube import Playlist
import requests
import os
import time
subprocess.run("python -m pip install --upgrade pytube", shell=True)

def prog_bar():
    progressbar = Tk()
    progressbar.geometry("555x33+600+100")
    progressbar.title("Downloading ffmpeg, please wait...")
    pb = ttk.Progressbar(progressbar, orient='horizontal', mode='determinate')
    pb.pack(expand=True, fill=tkinter.BOTH, side=tkinter.TOP)
    pb.start(11)
    progressbar.after(60000, message2)
    progressbar.after(90000, progressbar.destroy)
    progressbar.mainloop()



def message1():
    global msg
    msg = messagebox.showinfo(title="Downloading.......", message="Please wait a few seconds until ffmpeg is downloaded.")

def message2():
    messagebox.showinfo(title="Download Completed", message="Download completed. Please restart the app.")

def download_ffmpeg():
    r = requests.get("https://www.dropbox.com/s/ur8miwz54us8ruc/ffmpeg.exe?dl=1", allow_redirects=True)
    open('C:/ffmpeg.exe', 'wb').write(r.content)
if os.path.exists("C:/ffmpeg.exe"):
    os.environ["IMAGEIO_FFMPEG_EXE"] = r"C:\ffmpeg.exe"

else:
    # threading.Thread(target=message1).start()
    threading.Thread(target=prog_bar).start()
    threading.Thread(target=download_ffmpeg).start()
    start_time = threading.Timer(33, message2)
    # start_time.start()
    # os.environ["IMAGEIO_FFMPEG_EXE"] = rf"{directory}\ffmpeg"
    os.environ["IMAGEIO_FFMPEG_EXE"] = r"C:\ffmpeg.exe"
    # root.update()
# directory = os.getcwd()



# # os.environ["IMAGEIO_FFMPEG_EXE"] = r"D:\Python Projects\Windows\youtube_downloader\ffmpeg"
# # print(f"{directory}\\ffmpeg")
from moviepy.video.io.VideoFileClip import VideoFileClip


def space():
    space = Label(text="", bg="black")
    space.pack()


Folder_Name = ""


def open_location():
    global Folder_Name
    Folder_Name = filedialog.askdirectory()
    os.chdir(Folder_Name)
    if len(Folder_Name) > 1:
        path_url.config(text=Folder_Name, fg="green")

    else:
        messagebox.showwarning(title="oops", message="No path given!")
        path_url.config(text="Please specify a folder!", fg="red")
    return


def download_playlist():
    progress_bar.config(text="0 / 0", fg="white")
    root.update()
    playlist_url = url_box.get()
    if len(playlist_url) > 1 and "youtube.com" in playlist_url and "list" in playlist_url:
        url_error.config(text="")
        root.update()
        if len(Folder_Name) > 1:
            playlist_url = url_box.get()
            playlist = Playlist(playlist_url)
            number = 0
            for video in playlist.videos:
                time.sleep(1)
                video.streams.get_highest_resolution().download(Folder_Name)
                playlist_id = playlist.playlist_id
                API_key = "AIzaSyAMWYbTQqtGHobV5zP1fh1DFEYKKRokalk"
                playlist_size = f"https://www.googleapis.com/youtube/v3/playlistItems?part=id&maxResults=0&playlistId={playlist_id}&key={API_key}"
                response = requests.get(playlist_size)
                results = response.json()["pageInfo"]["totalResults"]
                number += 1
                progression = str(number) + " / " + str(results)
                progress_bar.config(text=progression, bg="black", fg="white")
                root.update()
            progress_bar.config(text="Downloaded successfully", fg="green")

        else:
            messagebox.showwarning(title="oops", message="No path given!")
            path_url.config(text="Please specify a folder!", fg="red")
    else:
        messagebox.showwarning(title="oops", message="Wrong URL!")
        url_error.config(text="Try again!", fg="red")

    return


def download_mp3_playlist():
    progress_bar.config(text="0 / 0", fg="white")
    root.update()
    url = url_box.get()
    if len(url) > 1 and "youtube.com" in url and "list" in url:
        url_error.config(text="")
        root.update()
        if len(Folder_Name) > 1:
            progress_bar.config(text="0 / 0", fg="white")
            url_error.config(text="")
            root.update()
            url = Playlist(url_box.get())
            list = url.video_urls
            number = 0
            for link in list:
                yt = YouTube(link)
                yt.streams.get_highest_resolution().download(Folder_Name)
                time.sleep(1)
                music = yt.streams.first()
                default_filename = music.default_filename
                new_filename = default_filename.split(".")[0]
                mp4 = Folder_Name + fr'/{new_filename}.mp4'
                mp3 = Folder_Name + fr'/{new_filename}.mp3'
                videoclip = VideoFileClip(mp4)
                audioclip = videoclip.audio
                audioclip.write_audiofile(mp3)
                audioclip.close()
                videoclip.close()
                os.system(f' del "{new_filename}.mp4"')
                playlist_id = url.playlist_id
                API_key = "AIzaSyAMWYbTQqtGHobV5zP1fh1DFEYKKRokalk"
                playlist_size = f"https://www.googleapis.com/youtube/v3/playlistItems?part=id&maxResults=0&playlistId={playlist_id}&key={API_key}"
                response = requests.get(playlist_size)
                results = response.json()["pageInfo"]["totalResults"]
                number += 1
                progression = str(number) + " / " + str(results)
                progress_bar.config(text=progression, bg="black", fg="white")
                root.update()
                progress_bar.config(text="Downloaded successfully", fg="green")

        else:
            messagebox.showwarning(title="oops", message="No path given!")
            path_url.config(text="Please specify a folder!", fg="red")

    else:
        messagebox.showwarning(title="oops", message="Wrong URL!")
        url_error.config(text="Try again!", fg="red")


def download_youtube():
    url = url_box.get()
    if len(url) > 1 and "youtube.com" in url and "playlist" not in url:
        url_error.config(text="")
        root.update()
        if len(Folder_Name) > 1:
            yt = YouTube(url)
            global video_id
            video_id = yt.video_id
            time.sleep(5)
            yt.streams.get_highest_resolution().download(Folder_Name)
            progress_bar.config(text="Downloaded successfully", fg="green")
            path_url.config(text="")

        else:
            messagebox.showwarning(title="oops", message="No path given!")
            path_url.config(text="Please specify a folder!", fg="red")

    else:
        messagebox.showwarning(title="oops", message="Wrong URL!")
        url_error.config(text="Try again!", fg="red")


def convert_to_mp3():
    if len(url_box.get()) > 1 and "youtube.com" in url_box.get() and "playlist" not in url_box.get():
        url_error.config(text="")
        root.update()
        if len(Folder_Name) > 1:
            yt = YouTube(url_box.get())
            yt.streams.get_highest_resolution().download(Folder_Name)
            time.sleep(5)
            music = yt.streams.first()
            default_filename = music.default_filename
            new_filename = default_filename.split(".")[0]
            mp4 = Folder_Name + fr'/{new_filename}.mp4'
            mp3 = Folder_Name + fr'/{new_filename}.mp3'
            videoclip = VideoFileClip(mp4)
            audioclip = videoclip.audio
            audioclip.write_audiofile(mp3)
            audioclip.close()
            videoclip.close()
            os.system(f' del "{new_filename}.mp4"')
            progress_bar.config(text="Downloaded successfully", fg="green")
        else:
            messagebox.showwarning(title="oops", message="No path given!")
            path_url.config(text="Please specify a folder!", fg="red")

    else:
        messagebox.showwarning(title="oops", message="Wrong URL!")
        url_error.config(text="Try again!", fg="red")

def close_program():
    root.quit()




root = Tk()



# root.iconbitmap("yt.ico")
root.title("Youtube Downloader")
root.geometry("450x610")
root.columnconfigure(0, weight=1)
root.config(bg="black")

space()
# img = PhotoImage(file="YT-pic.png")
# pic = Label(root, image=img, bg="black")
# pic.pack()

space()

url_label = Label(root, text="Enter video / playlist URL", bg="black", fg="white", font=("jost", 9, "bold"))
url_label.pack()

EntryVar = StringVar()
url_box = Entry(root, width=50, textvariable=EntryVar)
url_box.pack()

url_error = Label(root, text="", fg="red", bg="black", font=("jost", 9, "bold"))
url_error.pack()

space()

path_label = Label(root, text="Save the video file", bg="black", fg="white", font=("jost", 9, "bold"))
path_label.pack()

path_btn = Button(root, width=11, height=2, bg="#CC1B25", fg="white", text="Choose Path", command=open_location)
path_btn.pack()

path_url = Label(root, text="", fg="red", bg="black", font=("jost", 9, "bold"))
path_url.pack()

space()

download_btn = Button(width=23, height=1, bg="black", fg="white", text="Download Video", font=("jost", 11, "bold"),
                      command=download_youtube)
download_btn.pack()

space()

mp3_btn = Button(width=23, height=1, bg="black", fg="white", text=" Download MP3",
                 font=("jost", 11, "bold"), command=convert_to_mp3)
mp3_btn.pack()

space()

playlist_btn = Button(width=23, height=1, bg="black", fg="white", text=" Download Video Playlist",
                      font=("jost", 11, "bold"),
                      command=download_playlist)
playlist_btn.pack()

space()

mp3_playlist_btn = Button(width=23, height=1, bg="black", fg="white", text=" Download MP3 Playlist",
                          font=("jost", 11, "bold"), command=download_mp3_playlist)
mp3_playlist_btn.pack()

space()

progress_bar = Label(root, text="", bg="black", fg="white", font=("jost", 11, "bold"))
progress_bar.pack()

space()

cancel_btn = Button(root, text="Stop and close", bg="black", fg="white", font=("jost", 11, "bold"), command=close_program)
# cancel_btn.pack()

space()
dev_label = Label(root, text="Developed by Totenkopf 💀", bg="black", fg="#CC1B25", font=("jost", 11))
dev_label.pack()

root.mainloop()

if __name__ == '__main__':
    def refresh():
        progress_bar.destroy()
        message1()