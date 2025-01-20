import cv2
import cvzone
from cvzone.FaceMeshModule import FaceMeshDetector
import tkinter as tk
from tkinter import Label, Button
from PIL import Image, ImageTk

class DistanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Distance Measurement App")
        self.root.geometry("800x600")
        self.running = False

        # Initialize video capture and face mesh detector
        self.cap = cv2.VideoCapture(0)
        self.detector = FaceMeshDetector(maxFaces=1)

        # Real-world width and focal length
        self.W = 6.3  # Real-world width in cm
        self.f = 310  # Focal length (adjust as per calibration)

        # GUI Components
        self.video_label = Label(root)
        self.video_label.pack(pady=10)

        self.distance_label = Label(root, text="Distance: -- cm", font=("Helvetica", 16))
        self.distance_label.pack(pady=10)

        self.start_button = Button(root, text="Start", command=self.start_video, width=10)
        self.start_button.pack(side=tk.LEFT, padx=10)

        self.stop_button = Button(root, text="Stop", command=self.stop_video, width=10)
        self.stop_button.pack(side=tk.LEFT, padx=10)

        self.exit_button = Button(root, text="Exit", command=self.close_app, width=10)
        self.exit_button.pack(side=tk.LEFT, padx=10)

    def start_video(self):
        """Start the video feed."""
        self.running = True
        self.process_video()

    def stop_video(self):
        """Stop the video feed."""
        self.running = False

    def process_video(self):
        """Process the video feed and update the GUI."""
        if not self.running:
            return

        success, img = self.cap.read()

        if success:
            img, faces = self.detector.findFaceMesh(img, draw=False)
            if faces:
                face = faces[0]
                pointLeft = face[145]
                pointRight = face[374]

                w, _ = self.detector.findDistance(pointLeft, pointRight)
                if w > 0:  # Avoid division by zero
                    d = (self.W * self.f) / w
                    self.distance_label.config(text=f"Distance: {int(d)} cm")

                    # Display distance on the image
                    cvzone.putTextRect(img, f'Distance: {int(d)} cm',
                                       (face[10][0] - 75, face[10][1] - 50), scale=2)

            # Convert image to a format Tkinter can use
            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            imgPIL = Image.fromarray(imgRGB)
            imgTk = ImageTk.PhotoImage(image=imgPIL)

            # Update the video label with the new frame
            self.video_label.imgTk = imgTk
            self.video_label.configure(image=imgTk)

        # Call this method again after 10ms
        self.root.after(10, self.process_video)

    def close_app(self):
        """Close the application and release resources."""
        self.running = False
        self.cap.release()
        cv2.destroyAllWindows()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = DistanceApp(root)
    root.protocol("WM_DELETE_WINDOW", app.close_app)
    root.mainloop()
