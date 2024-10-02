# Histogram Equalization and Matching

This project implements **Histogram Equalization** and **Histogram Matching** for both grayscale and color images using Python.

## Table of Contents
- [Introduction](#introduction)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
  - [Histogram Equalization](#histogram-equalization)
  - [Histogram Matching](#histogram-matching)
- [File Structure](#file-structure)

## Introduction

1. **Histogram Equalization**: Enhances image contrast by redistributing pixel intensities to make the histogram more uniform. Applied to grayscale and color images (using the V channel in HSV).
  
2. **Histogram Matching**: Adjusts the histogram of a source image to match a target image. For color images, only the V channel in the HSV color space is matched.

## Requirements

- Python 3.x
- OpenCV (`cv2`)
- NumPy
- Matplotlib

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/histogram-equalization-matching.git
   ```

2. Install dependencies:

   ```bash
   pip install opencv-python numpy matplotlib
   ```

## Usage

### 1. Histogram Equalization

Perform histogram equalization on grayscale and color images (in the HSV space for color).

```python
# Grayscale Equalization
equalized_gray = histogram_equalization_gray(lena_gray_dark)

# Color Equalization (HSV - V channel)
equalized_color_hsv = histogram_equalization_color_hsv(livingroom_dark)
```

#### Inputs:
- `lena_gray_dark.jpg` (grayscale), `livingroom_dark.jpg` (color)

#### Outputs:
- Equalized grayscale and color images.

### 2. Histogram Matching

Perform histogram matching on grayscale and color images (using the V channel for color).

```python
# Grayscale Matching
matched_gray = histogram_matching_gray(mandril_gray, lena_gray)

# Color Matching (HSV - V channel)
matched_color_hsv = histogram_matching_color_hsv(mandril_color, lena_color)
```

#### Inputs:
- `mandril_gray.jpg` (source grayscale), `lena_gray_512.jpg` (target grayscale)
- `mandril_color.jpg` (source color), `lena_color_512.jpg` (target color)

#### Outputs:
- Matched grayscale and color images.


