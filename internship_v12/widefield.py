import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QSlider, QVBoxLayout, QWidget, QPushButton, QFileDialog, QComboBox, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import multipagetiff as mtif
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.cm as cm
import moviepy.editor as mpy
import numpy as np
from PyQt5.QtGui import QImage
import multipagetiff as mtif
import tifffile as tiff
import cv2

class ImageViewer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.image_stack = None
        self.current_index = 0
        self.colormap = 'gray'

        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)

        layout = QVBoxLayout()
        layout.addWidget(self.canvas)

        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.valueChanged.connect(self.on_slider_changed)
        layout.addWidget(self.slider)

        self.button = QPushButton("Choose TIFF Stack", self)
        self.button.clicked.connect(self.choose_tiff_stack)
        layout.addWidget(self.button)

        self.colormap_combo = QComboBox(self)
        self.colormap_combo.currentIndexChanged.connect(self.on_colormap_changed)
        layout.addWidget(self.colormap_combo)

        self.save_button = QPushButton("Save Image", self)
        self.save_button.clicked.connect(self.save_image)
        layout.addWidget(self.save_button)

        self.save_video_button = QPushButton("Save Video", self)
        self.save_video_button.clicked.connect(self.save_video)
        layout.addWidget(self.save_video_button)

        self.screenshot_button = QPushButton("Save modified Tiff", self)
        self.screenshot_button.clicked.connect(self.take_screenshot)
        layout.addWidget(self.screenshot_button)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.setWindowTitle("TIFF Stack Viewer")
        self.setGeometry(100, 100, 800, 800)

        self.populate_colormap_combo()

    def populate_colormap_combo(self):
        colormaps = ['gray', 'hot', 'cool', 'viridis', 'plasma', 'inferno']
        for cmap in colormaps:
            self.colormap_combo.addItem(cmap)

    def choose_tiff_stack(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Choose TIFF Stack")
        if file_path:
            self.image_stack = mtif.read_stack(file_path, units='um')
            self.current_index = 0
            self.slider.setRange(0, len(self.image_stack) - 1)
            self.show_image()

    def show_image(self):
        if self.image_stack is not None:
            image = self.image_stack[self.current_index]

            self.ax.imshow(image, cmap=self.colormap)
            self.canvas.draw()

    def on_slider_changed(self, value):
        self.current_index = value
        self.show_image()

    def on_colormap_changed(self, index):
        self.colormap = self.colormap_combo.currentText()
        self.show_image()

    def save_image(self):
        if self.image_stack is not None:
            image = self.image_stack[self.current_index]

            file_path, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "PNG files (*.png)")
            if file_path:
                plt.imsave(file_path, image, cmap=self.colormap)
                QMessageBox.information(self, "Save Image", "Image saved successfully.")

    def save_video(self):
        if self.image_stack is not None:
            file_path, _ = QFileDialog.getSaveFileName(self, "Save Video", "", "MP4 files (*.mp4)")
            if file_path:
                video_frames = []
                for image in self.image_stack:
                    # Normalize the 16-bit image to the range [0, 1]
                    normalized_image = image.astype(np.float32) / np.max(image)

                    # Apply the colormap to the normalized image
                    colored_image = cm.get_cmap(self.colormap)(normalized_image)
                    # Convert the image to RGB format
                    rgb_image = np.uint8(colored_image * 255)

                    # Add the RGB image to the video frames list
                    video_frames.append(rgb_image)

                # Create a video clip from the frames
                video_clip = mpy.ImageSequenceClip(video_frames, fps=10)
                # Write the video clip to the file path
                video_clip.write_videofile(file_path, codec='libx264')

                QMessageBox.information(self, "Save Video", "Video saved successfully.")


    def QImageToNumpyArray(self, qimage):
        width = qimage.width()
        height = qimage.height()
        ptr = qimage.bits()
        ptr.setsize(qimage.byteCount())
        arr = np.array(ptr).reshape(height, width, 4)  # 4 channels: RGBA
        return arr

    def take_screenshot(self):
        if self.image_stack is not None:
            save_file, _ = QFileDialog.getSaveFileName(self, "Save TIFF Stack with Overlays", "", "TIFF Files (*.tif)")
            if save_file:
                with tiff.TiffWriter(save_file) as tif:
                    for idx, image in enumerate(self.image_stack):
                        self.current_index = idx
                        self.show_image()
                        pixmap = self.canvas.grab()
                        if pixmap:
                            qimage = pixmap.toImage()
                            screenshot_array = self.QImageToNumpyArray(qimage)

                            # Calculate the center of the frame
                            center_y, center_x = screenshot_array.shape[0] // 2, screenshot_array.shape[1] // 2

                            # Calculate the top-left corner of the cropping region
                            top = center_y - 220
                            left = center_x - 215

                            # Calculate the bottom-right corner of the cropping region
                            bottom = center_y + 225
                            right = center_x + 230

                            # Crop the image using cv2
                            cropped_image = screenshot_array[top:bottom, left:right, :3]

                            # Check if the cropped image is not empty
                            if not cropped_image.size == 0:
                                tif.write(cv2.cvtColor(cropped_image, cv2.COLOR_RGB2BGR))
                            else:
                                print(f"Cropped image {idx} is empty. Please check the cropping region.")
                        plt.close('all')
if __name__ == '__main__':
    app = QApplication(sys.argv)
    viewer = ImageViewer()
    viewer.show()
    sys.exit(app.exec())
