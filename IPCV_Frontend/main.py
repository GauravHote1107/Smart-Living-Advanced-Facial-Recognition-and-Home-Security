import cv2
import face_recognition
import numpy as np
import time

from notifier import Notifier
from node_client import NodeClient

NOTIFICATION_DELAY = 45
OPEN_DELAY = 5

video_capture = cv2.VideoCapture(0)
node_client = NodeClient()

known_face_encodings = [
    face_recognition.api.face_encodings(
        face_recognition.load_image_file("faces/gaurav.jpg"), model="small"
    )[0]
]
known_face_names = ["Gaurav Hote"]
face_locations = []
face_names = []
process_this_frame = True

last_time_sent = 0


def shrink_frame(frame):
    global face_locations, face_encodings, face_names

    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = np.ascontiguousarray(small_frame[:, :, ::-1])
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    face_names = []
    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"

        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]

        face_names.append(name)

def draw_rectangle(frame):
    global face_locations, face_names
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)


if __name__ == "__main__":
    last_opened = 0
    while True:
        if cv2.waitKey(1) & 0xFF == ord("q"):
            for setting in node_client.values_cache:
                node_client.reset_pin(setting)
            break

        ret, frame = video_capture.read()

        shrink_frame(frame)
        draw_rectangle(frame)

        cv2.imshow("Video", frame)
        current_time = int(time.time())

        if not face_names and current_time - last_opened > OPEN_DELAY:
            node_client.reset_pin("D4")
            node_client.rotate_servo("D1", 180)
            continue

        intruder = False
        for face_name in face_names:
            if face_name not in known_face_names:
                intruder = True
                break

        node_client.update_pin("D4", 1023)
        if intruder and current_time - last_time_sent > NOTIFICATION_DELAY:
            Notifier.send_notification()
            last_time_sent = current_time
        elif not intruder and current_time - last_opened > OPEN_DELAY:
            node_client.rotate_servo("D1", 0)
            last_opened = current_time

    video_capture.release()
    cv2.destroyAllWindows()
