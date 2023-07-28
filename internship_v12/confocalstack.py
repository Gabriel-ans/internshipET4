import sys #Library
import numpy as np
import tifffile
from pyvistaqt import BackgroundPlotter
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QVBoxLayout, QWidget, QPushButton, QComboBox, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow): #UI
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ZStack Viewer")
        self.setWindowIcon(QIcon("icon.png"))
        
        # Create the main widget and layout
        self.central_widget = QWidget(self)
        self.layout = QVBoxLayout(self.central_widget)
        
        # Create the buttons
        self.load_button = QPushButton('Load Image', self)
        self.load_button.clicked.connect(self.load_image)
        self.plot_button = QPushButton('Plot Volume', self)
        self.plot_button.setEnabled(False)
        self.plot_button.clicked.connect(self.plot_volume)
        self.screenshot_button = QPushButton('Take Screenshot', self)
        self.screenshot_button.clicked.connect(self.take_screenshot)
        self.camera_info_button = QPushButton('Show Camera Info', self)
        self.camera_info_button.clicked.connect(self.show_camera_info)
        
        # Create the colormap selection combobox
        self.colormap_combobox = QComboBox(self)
        self.colormap_combobox.addItem('jet')
        self.colormap_combobox.addItem('hot')
        self.colormap_combobox.addItem('cool')
        self.colormap_combobox.addItem('viridis')
        self.colormap_combobox.addItem('magma')
        self.colormap_combobox.addItem('inferno')
        self.colormap_combobox.addItem('plasma')
        self.colormap_combobox.addItem('bone')
        self.colormap_combobox.addItem('copper')
        self.colormap_combobox.addItem('gray')
        
        # Create the depth peeling checkbox
        self.depth_peeling_checkbox = QComboBox(self)
        self.depth_peeling_checkbox.addItem('Enable Depth Peeling')
        
        # Create the opacity selection combobox
        self.opacity_combobox = QComboBox(self)
        opacity_options = [
            'linear', 'linear_r', 'geom', 'geom_r', 'sigmoid', 'sigmoid_1',
            'sigmoid_2', 'sigmoid_3', 'sigmoid_4', 'sigmoid_5', 'sigmoid_6',
            'sigmoid_7', 'sigmoid_8', 'sigmoid_9', 'sigmoid_10'
        ]
        self.opacity_combobox.addItems(opacity_options)
        self.opacity_combobox.setCurrentIndex(opacity_options.index('sigmoid_4'))  # Default to sigmoid_4
        self.opacity_combobox.currentIndexChanged.connect(self.update_opacity)
        
        # Add the buttons, combobox, and checkbox to the layout
        self.layout.addWidget(self.load_button)
        self.layout.addWidget(self.plot_button)
        self.layout.addWidget(self.screenshot_button)
        self.layout.addWidget(self.camera_info_button)
        self.layout.addWidget(self.colormap_combobox)
        self.layout.addWidget(self.depth_peeling_checkbox)
        self.layout.addWidget(self.opacity_combobox)
        
        # Create the pyvista plotter
        self.plotter = BackgroundPlotter()
        self.plotter.background_color = [255, 255, 255]
        
        # Set the layout and show the main window
        self.setCentralWidget(self.central_widget)
        self.show()
    
    def load_image(self): #Load the OME Tiff confocal stack into a numpy 3D array matrix
        filepath, _ = QFileDialog.getOpenFileName(self, 'Open OME TIFF Stack', '', 'OME TIFF Stack (*.ome.tif *.ome.tiff)')
        if filepath:
            try:
                stack = tifffile.imread(filepath)
                if stack.ndim != 3:
                    raise ValueError('The selected file is not a 3D OME TIFF stack.')
                self.volume_data = np.asarray(stack)
                self.plot_button.setEnabled(True)
            except Exception as e:
                QMessageBox.critical(self, 'Error', f'Error loading the OME TIFF stack:\n{e}')
    
    def plot_volume(self): #Display the Matrix with pyvista
        if hasattr(self, 'volume_data'):

            self.plotter.clear()
            
            # Add the volume to the plot
            cmap = self.colormap_combobox.currentText()
            opacity = self.opacity_combobox.currentText()
            volume_actor = self.plotter.add_volume(self.volume_data, cmap=cmap, opacity=opacity, show_scalar_bar=False)
            
            # Enable depth peeling if selected
            if self.depth_peeling_checkbox.currentText() == 'Enable Depth Peeling':
                self.plotter.enable_depth_peeling(number_of_peels=4, occlusion_ratio=0)
            
            # Render the plot
            self.plotter.show()
    
    def update_opacity(self): # Select the opacity of the rendering and update the view, sigmoid_
        if hasattr(self, 'volume_data') and self.plotter:
            # Get the selected opacity option from the combobox
            selected_opacity = self.opacity_combobox.currentText()

            # Check if a volume actor exists in the scene
            volume_actors = self.plotter.renderer.GetActors()
            if volume_actors and volume_actors.GetNumberOfItems() > 0:
                volume_actor = volume_actors.GetItemAsObject(0)
                if volume_actor.GetClassName() == 'vtkVolume':
                    volume_actor.property.set_scalar_opacity_unit_distance(1.0)
                    volume_actor.scalar_opacity_unit_distance = 0.01
                    volume_actor.property.set_use_bounds(True)
                    volume_actor.property.set_scalar_opacity(selected_opacity)
                    self.plotter.render()

    def take_screenshot(self): #Save the current image displayed
        screenshot_filename, _ = QFileDialog.getSaveFileName(self, 'Save Screenshot', '', 'Images (*.png *.jpg)')
        if screenshot_filename:
            self.plotter.screenshot(screenshot_filename, transparent_background=True)
            QMessageBox.information(self, 'Screenshot Saved', 'Screenshot saved successfully!')

    def show_camera_info(self): # give the position of the camera 
        camera_position = str(self.plotter.camera_position)
        QMessageBox.information(self, 'Camera Info', f'Camera Position:\n{camera_position}')

if __name__ == "__main__": #Start the main windows
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
