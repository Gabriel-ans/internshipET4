import sys
import multipagetiff as mtif
import matplotlib.pyplot as plt
import tifffile as tiff
import numpy as np
import cv2
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QFileDialog, QGraphicsScene, QGraphicsView, QSlider, QLabel
)
from PyQt5.QtGui import QPixmap, QImage, QPainter, QColor
from PyQt5.QtCore import Qt, QRectF, QByteArray, QBuffer, QIODevice
from PyQt5.QtWidgets import QGraphicsPixmapItem


class PNGItem(QGraphicsView): #UI and variable

    def __init__(self, image, parent=None):

        super().__init__(parent)
        self.image = image
        self.setFlag(QGraphicsView.ItemIsMovable)
        self.setFlag(QGraphicsView.ItemSendsGeometryChanges)
        self.setCacheMode(QGraphicsView.CacheBackground)
        self.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)
        self.png_item = None


    def boundingRect(self):
        return QRectF(self.image.rect())

    def paint(self, painter, option, widget):
        painter.drawPixmap(self.image.rect(), self.image)

    def mousePressEvent(self, event):
        self.prev_pos = event.pos()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        dx = event.pos().x() - self.prev_pos.x()
        dy = event.pos().y() - self.prev_pos.y()
        self.moveBy(dx, dy)
        self.prev_pos = event.pos()
        super().mouseMoveEvent(event)


class ImageViewer(QMainWindow): #UI and variable
    def __init__(self):
        super().__init__()

        self.current_item = None
        self.image_stack = None
        self.png_item = None

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Image Viewer")
        self.setGeometry(100, 100, 1000, 800)

        self.scene = QGraphicsScene(self)
        self.view = QGraphicsView(self.scene)
        self.view.setStyleSheet("background-color: black;")
        self.view.setSceneRect(0, 0, 800, 600)

        self.load_tiff_button = QPushButton("Load TIFF Stack")
        self.load_tiff_button.clicked.connect(self.load_tiff_stack)

        self.load_png_button = QPushButton("Load PNG")
        self.load_png_button.clicked.connect(self.load_png)

        self.png_opacity_slider = QSlider(Qt.Horizontal)
        self.png_opacity_slider.setMaximum(100)
        self.png_opacity_slider.setValue(100)
        self.png_opacity_slider.valueChanged.connect(self.update_opacity)

        self.png_zoom_slider = QSlider(Qt.Horizontal)
        self.png_zoom_slider.setMinimum(50)
        self.png_zoom_slider.setMaximum(200)
        self.png_zoom_slider.setValue(100)
        self.png_zoom_slider.valueChanged.connect(self.update_zoom)

        self.tiff_slider = QSlider(Qt.Horizontal)
        self.tiff_slider.setMaximum(0)
        self.tiff_slider.valueChanged.connect(self.update_tiff_image)

        self.png_opacity_label = QLabel("PNG Opacity")
        self.png_zoom_label = QLabel("PNG Zoom")
        self.tiff_label = QLabel("TIFF Image")

        self.screenshot_button = QPushButton("Save new tiff")
        self.screenshot_button.clicked.connect(self.take_screenshot)

        layout = QVBoxLayout()
        layout.addWidget(self.view)
        layout.addWidget(self.load_tiff_button)
        layout.addWidget(self.load_png_button)
        layout.addWidget(self.png_opacity_label)
        layout.addWidget(self.png_opacity_slider)
        layout.addWidget(self.png_zoom_label)
        layout.addWidget(self.png_zoom_slider)
        layout.addWidget(self.tiff_label)
        layout.addWidget(self.tiff_slider)
        layout.addWidget(self.screenshot_button)  
        layout.addWidget(self.crop_button)

        main_widget = QWidget()
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

    def load_tiff_stack(self): #Tifffile library, charge the tiff into a matrix, define slider
        file_path, _ = QFileDialog.getOpenFileName(self, "Choose TIFF Stack", "", "TIFF Files (*.tif)")
        if file_path:
            self.image_stack = mtif.read_stack(file_path, units='um')
            self.tiff_slider.setMaximum(len(self.image_stack) - 1)
            self.current_index = 0
            self.update_tiff_image()

    def update_tiff_image(self): # update the interface
        if self.image_stack is not None and 0 <= self.tiff_slider.value() < len(self.image_stack):
            self.current_index = self.tiff_slider.value()
            self.show_image()

    def show_image(self):
        if self.image_stack is not None and 0 <= self.current_index < len(self.image_stack):
            image = self.image_stack[self.current_index]

            # Create a Matplotlib figure and canvas for the widefield data
            plt.style.use('dark_background')
            fig, ax = plt.subplots(figsize=(5.12, 5.12), dpi=100)
            ax.imshow(image, cmap='gray')
            ax.axis('off')
            ax.set_frame_on(False)

            # Draw the figure on the canvas
            fig.canvas.draw()

            # Get the buffer and dimensions for alignement
            buf = fig.canvas.tostring_rgb()
            width, height = fig.canvas.get_width_height()

            # Convert the buffer to a QImage and create a QPixmap from it, UI
            qimage = QImage(buf, width, height, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qimage)
            if self.current_item:
                self.scene.removeItem(self.current_item)
            self.current_item = QGraphicsPixmapItem(pixmap)
            self.scene.addItem(self.current_item)

            # Center the image within the view
            x = (self.view.viewport().width() - width) // 2
            y = (self.view.viewport().height() - height) // 2
            self.current_item.setPos(x, y)

    def load_png(self): # Load the PNG to display it over the widefield
        file_path, _ = QFileDialog.getOpenFileName(self, "Choose PNG Image", "", "PNG Files (*.png)")
        if file_path:
            self.png_item = QGraphicsPixmapItem(QPixmap(file_path))
            self.scene.addItem(self.png_item)
            self.png_item.setFlag(QGraphicsPixmapItem.ItemIsMovable)
            self.png_item.setZValue(1)  # Set the Z value to ensure it's displayed above the TIFF image

    def crop_image(self):
        # Take a screenshot of the full view
        pixmap = self.view.grab()

        # Convert the screenshot to a numpy array for cropping
        qimage = pixmap.toImage()
        screenshot_array = QImageToNumpyArray(qimage)

        # Define the cropping region
        top, bottom, left, right = 45, 440, 365, 760


        # Check if the cropping region is within bounds
        if 0 <= top < bottom <= screenshot_array.shape[0] and 0 <= left < right <= screenshot_array.shape[1]:
            # Crop the image using cv2
            cropped_image = screenshot_array[top:bottom, left:right, :3]

            # Check if the cropped image is not empty
            if not cropped_image.size == 0:
                # Save the cropped image using tiff (or any other format)
                save_file, _ = QFileDialog.getSaveFileName(self, "Save Cropped Image", "", "TIFF Files (*.tif);;PNG Files (*.png)")
                if save_file:
                    cv2.imwrite(save_file, cv2.cvtColor(cropped_image, cv2.COLOR_RGB2BGR))
                    print("Image cropped and saved successfully.")
            else:
                print("Cropped image is empty. Please check the cropping region.")
        else:
            print("Invalid cropping region. Please check the bounds.")

    def update_opacity(self): # adjust opacity of the confocal PNG
        if self.png_item:
            opacity_percent = self.png_opacity_slider.value()
            opacity = opacity_percent / 100.0
            self.png_item.setOpacity(opacity)

    def update_zoom(self): #adjust the size onf the png
        if self.png_item:
            zoom_factor = self.png_zoom_slider.value() / 100.0
            self.png_item.setScale(zoom_factor)

    def take_screenshot(self):  # Loop to get all the widefield with the confocal overlay
        if self.image_stack is not None:
            save_file, _ = QFileDialog.getSaveFileName(self, "Save TIFF Stack with Overlays", "", "TIFF Files (*.tif)")
            if save_file:
                with tiff.TiffWriter(save_file) as tif:
                    for idx, image in enumerate(self.image_stack):
                        self.current_index = idx
                        self.show_image()
                        pixmap = self.view.grab()
                        if pixmap:
                            qimage = pixmap.toImage()
                            screenshot_array = QImageToNumpyArray(qimage)

                            # Define the cropping region
                            top, bottom, left, right = 45, 440, 365, 760


                            # Check if the cropping region is within bounds
                            if 0 <= top < bottom <= screenshot_array.shape[0] and 0 <= left < right <= screenshot_array.shape[1]:
                                # Crop the image using cv2
                                cropped_image = screenshot_array[top:bottom, left:right, :3]

                                # Check if the cropped image is not empty
                                if not cropped_image.size == 0:
                                    tif.write(cv2.cvtColor(cropped_image, cv2.COLOR_RGB2BGR))
                                else:
                                    print(f"Cropped image {idx} is empty. Please check the cropping region.")
                            else:
                                print(f"Invalid cropping region for image {idx}. Please check the bounds.")
                        plt.close('all')



def QImageToNumpyArray(qimage): #Transform the screenshot into numpy array for the convertion into a tiff file later
    width = qimage.width()
    height = qimage.height()
    ptr = qimage.bits()
    ptr.setsize(qimage.byteCount())
    arr = np.array(ptr).reshape(height, width, 4)  # 4 channels: RGBA
    return arr


if __name__ == "__main__": #Start the main window 
    app = QApplication(sys.argv)
    window = ImageViewer()
    window.show()
    sys.exit(app.exec_())


