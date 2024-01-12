import tkinter as tk
from functools import partial

import cv2
import cv2 as cv
import PIL.Image, PIL.ImageTk
from src.Twilio import SS_Senders as SS_S
import datetime
import os
from JSON import jsonHandlers as jh
import threading
import face_recognition
from subprocess import call


class SystemWindow:
    def __init__(self, master):
        self.master = master
        self.entered_code = False
        self.initial_time = 45
        self.found_person = False
        self.image_path = "../face2.png"
        self.vid = VideoCapture(self)
        self.tries_left = 3
        self.used_all_tries = False
        self.next_run = False
        self.unauth_called = False;

        self.delay = 0.001

        window_width = self.master.winfo_screenwidth() - 250
        window_height = self.master.winfo_screenheight() - 250

        self.rel_x = window_width / 4
        self.rel_y = window_height / 2
        self.setup_window()

    def start_count_down(self, seconds=45):
        self.count_down_timer['text'] = "Time Left : " + str(seconds) + " S"

        if (seconds > 0 and not self.entered_code and not self.used_all_tries and not self.next_run):
            self.master.after(1000, self.start_count_down, seconds - 1)
        elif (seconds > 0 and self.entered_code and not self.used_all_tries and not self.next_run):
            self.alert_welcome()
            self.reset_timer()
        elif seconds <= 0 or (seconds > 0 and self.used_all_tries and not self.next_run):
            self.reset_timer()
            self.perform_unauth_sequence()
        else:
            self.reset_timer()
            self.next_run = False

    def reset_timer(self):
        self.count_down_timer['text'] = "Time Left : " + str(self.initial_time) + " S"

    def perform_unauth_sequence(self):
        SS_S.send_img_email("gamers2333@gmail.com", "gamers2333@gmail.com", self.image_path)
        unauth_alert_thread = threading.Thread(target=self.alert_unauthorized)
        unauth_alert_thread.start()
        self.tries_left = 3
        self.used_all_tries = False
        self.next_run = True

    def setup_window(self):
        self.configure_window()
        self.add_window_components()
        self.master.mainloop()

    def configure_window(self):
        width = self.master.winfo_screenwidth()
        height = self.master.winfo_screenheight()

        self.set_window_size(width, height)
        self.master.title("Lab Security System")

    def take_snapshot(self):
        image_path = "cv2 capture.png"
        ret, frame = self.vid.get_stream_frame()

        cv.imwrite(image_path, frame)

    def add_window_components(self):

        label = self.create_window_label("Professor Wilfido Moreno Lab Security System", self.rel_x, self.rel_y)

        text_field = self.create_window_textfield(self.rel_x, self.rel_y + 60)
        self.create_button("Submit code", self.rel_x, self.rel_y + 120,
                           partial(self.checkIfEnteredCodeCorrectly, text_field))

        self.count_down_timer = self.create_window_label("45 S", self.rel_x * 3.5, self.rel_y / 2)

        self.openCv_canvas = self.create_openCV_canvas(self.rel_x * 3.5 - (self.vid.width / 2), self.rel_y / 2 + 75)
        update_canvas = threading.Thread(target=self.update_openCvCanvas)
        update_canvas.start()

    def create_openCV_canvas(self, x=0, y=0):
        openCv_canvas = tk.Canvas(self.master, width=self.vid.width, height=self.vid.height)
        openCv_canvas.place(x=x, y=y)
        return openCv_canvas

    def update_openCvCanvas(self):
        while self.vid.isOpened():
            ret, frame = self.vid.get_stream_frame()

            if ret:
                self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
                self.openCv_canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

    def create_window_label(self, text_, x=0, y=0):
        label = tk.Label(self.master, text=text_)
        label.place(x=x, y=y)
        return label

    def create_window_textfield(self, x=0, y=0):
        text_field = tk.Entry(self.master)
        text_field.place(x=x, y=y)
        return text_field

    def create_button(self, text, x, y, func):
        button = tk.Button(self.master, text=text, command=func)
        button.place(x=x, y=y)
        return button

    def set_window_size(self, width=0, height=0):
        self.master.geometry("%dx%d" % (width, height))

    def checkIfEnteredCodeCorrectly(self, code_entered):
        if (code_entered.get() == jh.get_secret_code()):
            self.entered_code = True
            self.found_person = False
            self.tries_left = 3
        else:
            self.tries_left -= 1

            if self.tries_left == 0:
                self.found_person = False
                self.used_all_tries = True
                self.perform_unauth_sequence()

        code_entered.delete(0, 'end')

    def alert_wrong_code(self):
        alert_speech = "You have entered the wrong code."
        call(['espeak', '-v', 'EN-US', '-s 160', alert_speech])

    def alert_unauthorized(self):
        alert_speech = ("Unauthorized to enter the lab, please exit.")
        call(['espeak', '-v', 'EN-US', '-s 160', alert_speech])

    def alert_welcome(self):
        alert_speech = ("Welcome to the lab!")
        call(['espeak', '-v', 'EN-US', '-s 160', alert_speech])


class VideoCapture:
    def __init__(self, master, video_source_port=1):
        open_cam = threading.Thread(target=self.wait_to_open, args=[video_source_port])
        open_cam.start()
        open_cam.join()
        self.master = master
        #self.face_cascade = cv.CascadeClassifier('./haarcascade_frontalface_alt2.xml')
        self.res = "480p"
        self.STD_DIMENSIONS = {
            "480p": (640, 480),
            "720p": (1280, 720),
            "1080p": (1920, 1080),
            "4k": (3840, 2160)
        }

        self.VIDEO_TYPE = {
            'avi': cv.VideoWriter_fourcc(*'XVID'),
            'mp4': cv.VideoWriter_fourcc(*'XVID')
        }

        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

        self.width = self.vid.get(cv.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv.CAP_PROP_FRAME_HEIGHT)

    def wait_to_open(self, video_source_port):
        self.vid = cv.VideoCapture(video_source_port)
        while not self.vid.isOpened():
            print("waiting for cam to open")
        return True

    def isOpened(self):
        return self.vid.isOpened()

    def get_stream_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()

            if ret:
                face_img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                face_locations = face_recognition.face_locations(face_img)


                for (top, right, bottom, left) in face_locations:
                    color = (255, 0, 0)
                    stroke = 2

                    start_coord = (left, top)
                    end_coord = (right, bottom)

                    cv2.rectangle(frame, start_coord, end_coord, color, stroke)

                    if not self.master.found_person:
                        self.master.master.after(1500, self.take_snapshot)

                if len(face_locations) > 0 and not self.master.found_person:
                    print("faces > 1")

                    self.master.start_count_down(self.master.initial_time)
                    self.master.found_person = True
                    print(self.master.found_person)

                return ret, frame
            else:
                return ret, None
        else:
            return None, None

    #     ret, frame = self.vid.read()
    #
    #     gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    #     faces = self.face_cascade.detectMultiScale(gray_frame , scaleFactor=1.05, minNeighbors=3)
    #
    #     for (x,y,w,h) in faces:
    #         color = (255 , 0 , 0)
    #         stroke = 2
    #
    #         end_coordy = y + h
    #         end_coordx = x+w
    #
    #         cv.rectangle(frame , (x,y) , (end_coordx , end_coordy) , color , stroke)
    #
    #         if not self.master.found_person:
    #             self.master.master.after(2000 , self.take_snapshot)
    #
    #
    #     if len(faces) > 0 and not self.master.found_person:
    #         print("faces > 1")
    #
    #         self.master.start_count_down(self.master.initial_time)
    #         self.master.found_person = True
    #         print(self.master.found_person)
    #
    #     if ret :
    #         return(ret , cv.cvtColor(frame, cv.COLOR_BGR2RGB))
    #     else :
    #         return(ret , None)

    def take_snapshot(self):
        ret, frame = self.get_stream_frame()
        image2 = self.master.image_path
        cv.imwrite(image2, frame)

    def get_video_name(self):
        e = datetime.datetime.now()

        date_as_string = "%s/%s/%s" % (e.month, e.day, e.year)
        timing_as_string = "%s:%s:%s" % (e.hour, e.minute, e.second)

        file_suffix = ".avi"
        file_indentifier = "video_" + date_as_string + "_" + timing_as_string

        return file_indentifier + file_suffix

    def get_video_type(self, filename):
        filename, ext = os.path.splitext(filename)
        if ext in self.VIDEO_TYPE:
            return self.VIDEO_TYPE[ext]

        return self.VIDEO_TYPE['avi']

    def change_res(self, width, height):
        self.vid.set(3, width)
        self.vid.set(4, height)

    def start_recording(self):
        file_name = "video.avi"

        video_writer = cv.VideoWriter(file_name, self.get_video_type(file_name), 25, self.get_dims(self.vid, self.res))

        video_writer.release()

    def get_dims(self, cap, res='1080p'):
        width, height = self.STD_DIMENSIONS["480p"]
        if res in self.STD_DIMENSIONS:
            width, height = self.STD_DIMENSIONS[res]

        self.change_res(width, height)
        return width, height

    def release_cam(self):
        if self.vid.isOpened():
            self.vid.release()
