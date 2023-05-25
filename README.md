# internshipET4
macquarie university internship : signal processing and image processing project 

1 Introduction

This research project aims to explore the permeability of the blood-brain barrier (BBB) using fluorescent nanoparticles and the zebrafish model. The goal of the project is to understand how nanocarriers
of drugs can cross the BBB and reach the brain under various conditions. By tracking single Green
Fluorescent Protein (GFP) in live zebrafish, the project seeks to visualize and analyze the behavior
of these nanocarriers, shedding light on the mechanisms and challenges associated with drug delivery
to the brain. This project will help to improve our understanding of BBB permeability and explore
strategies to improve the administration of drugs to the brain for the diagnosis and treatment of brain
disorders.

2 Imaging techniques used in the project

For this research project two types of imaging are used.

2.1 Confocal Microscopy

Confocal microscopy is an advanced optical imaging technique that provides high resolution images
using lasers and fluorescence detectors. This technique is particularly useful for real-time imaging of
living tissues, such as the bloodstream of zebrafish. The advantage of confocal microscopy is that it
allows high-resolution, three-dimensional imaging with a large depth of field, which allows internal
structures to be visualized with great precision. In addition, this technique provides sharp images with
low brightness, minimizing damage to living tissue. However, the imaging process is slow and can’t
focalise on specific spot.

2.2 Widefield Microscopy

Fluorescence widefield microscopy is a simpler optical imaging technique that uses a laser at the right
wavelength to excite fluorescent molecules and detect their light emission. This technique allow realtime imaging with a frame rate around 15fps according to the CCD camera. Thus we can study the
bloodstream of zebrafish and GFP crossing the BBB. However, widefield fluorescence microscopy has
a shallow depth of field, which limits its ability to visualize deep structures. In addition, fluorescence
signals from structures outside the focal plane can interfere with the images, which can reduce the
overall image quality. This noise should be reduce to improve the quality of the modeling and the
visualisation of BBB permeability.

3 Description of the project

The main idea of this side project is to design a numerical method to link two imaging methods which
are widefield and confocal microscopy. Several requirements are related to it such as the repeatability
of the method for different data packages as well as the analysis and improvement of the data quality.
The project can be divided into several parts for a better understanding.

3.1 Confocal data modeling

As explained above, microscopy allows us to obtain cross-sections from a single plane, the focal plane
of our objective. We obtain parrallel sections of tissues that can be superimposed to obtain a 3d model.
To achieve this modeling several solutions are possible and are studied. Indeed the advantage of these
sections is the fact that we get closer to the methods used in tomogrophy in medical imaging. We can
thus base ourselves on the pre-existing reconstruction models allowing us a first approach. Modeling
large volumes of data such as those from the confocal microscope takes time and it is therefore necessary
to optimize the computing time of our algorithm

3.2 Widefield data modeling


We now turn to the reconstruction of the widefield data. As shown above, in a widefield microscope,
the entire focal volume is illuminated, but this creates blurring in the blurred areas above and below
the image plane. In order to be able to exploit the data we must first limit the noise surrounding the
study area. To do this we can perform a first processing of the images by delimiting the useful area
and applying filters. The microscope currently in use does not provide a 3-dimensional image. we need
to find a way to model the missing sections of the widefield using confocal data and theoretical blood
flow models.

3.3 Linking the two models

This part is one of the key elements of the project. Indeed, if the modelling of the two datasets is to be
successful, it must be possible to visualise them on a single model. The two microscopes do not have the
same resolution and therefore not the same size scale. We will not be able to see the whole blood flow
but only the area studied with the widefield. We need to find a way to determine the position (x,y,z)
of the data obtained with the widefield to be able to project them in the 3d confocal modelisation at
the right scale. To determine the position in space we can rely on the descriptors of points of interest.
These are techniques used in image processing to extract distinctive and reproducible features from an
image. These features help to identify specific points in the image, such as corners, edges or regions
with significant variations.

3.4 User interface

This last part focuses on improving the user interface to make it easier to use the algorithm without
having to modify the code between each data set.


References
- Nasse M. J., Woehl J. C., Huant S., ≪ High-resolution mapping of the three-dimensional point spread
function in the near-focus region of a confocal microscope ≫, Appl. Phys. Lett. 2007
- Haeberl´e O., Colicchio B., ≪ Techniques d’am´elioration de la r´esolution en microscopie de fluorescence : de la production des photons au traitement des images ≫, 2005
-Alexey Brodoline. Holographie num´erique appliqu´ee `a l’imagerie 3D rapide de la circulation sanguine chez le poisson-z`ebre. Autre [cond-mat.other]. Universit´e Montpellier, 2018. Fran¸cais. ffNNT :
2018MONTS058ff. fftel-02138965
-High-resolution restoration of 3D structures from widefield images with extreme low signal-to-noiseratio, Muthuvel Arigovindan, Jennifer C. Fung, Daniel Elnatan,and David A. Agard October 8, 2013
-Zhou, Q., Chen, Z., Liu, YH. et al. Three-dimensional wide-field fluorescence microscopy for transcranial mapping of cortical microcirculation. Nat Commun 13, 7969 (2022). https://doi.org/10.1038/s41467-
022-35733-0
