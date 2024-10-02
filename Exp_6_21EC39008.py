# -*- coding: utf-8 -*-
"""Exp_6_21EC39008.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1LYgpA0kQ5eQC1R0fBwKSmWZiKur7HAak
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt

# Function to compute the histogram of an image
def compute_histogram(image):
    hist, bins = np.histogram(image.flatten(), 256, [0, 256])
    return hist

# Function to compute cumulative distribution function (CDF)
def compute_cdf(hist):
    cdf = hist.cumsum()  # Cumulative sum of the histogram
    cdf_normalized = cdf * hist.max() / cdf.max()  # Normalize the cdf
    return cdf, cdf_normalized

# Histogram equalization function for grayscale images
def histogram_equalization_gray(image):
    hist = compute_histogram(image)
    cdf, _ = compute_cdf(hist)

    # Mask all the zero values in CDF
    cdf_m = np.ma.masked_equal(cdf, 0)
    # Perform histogram equalization
    cdf_m = (cdf_m - cdf_m.min()) * 255 / (cdf_m.max() - cdf_m.min())
    cdf_final = np.ma.filled(cdf_m, 0).astype('uint8')

    # Map the original image pixels to the equalized pixels
    equalized_image = cdf_final[image]

    return equalized_image

# Histogram equalization function for color images (using HSV color space)
def histogram_equalization_color_hsv(image):
    # Convert the image from BGR to HSV color space
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Equalize the histogram of the Value (V) channel
    hsv_image[:, :, 2] = cv2.equalizeHist(hsv_image[:, :, 2])

    # Convert the HSV image back to BGR format
    equalized_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)

    return equalized_image

# Function to plot histograms
def plot_histograms(image, title):
    plt.figure(figsize=(10,5))
    if len(image.shape) == 2:  # Grayscale image
        plt.hist(image.ravel(), 256, [0, 256], color='gray')
        plt.title(f'Histogram of {title}')
        plt.xlabel('Pixel Intensity')
        plt.ylabel('Frequency')
        plt.show()
    else:  # Color image
        color = ('b', 'g', 'r')
        for i, col in enumerate(color):
            hist = cv2.calcHist([image], [i], None, [256], [0, 256])
            plt.plot(hist, color=col, label=f'{col.upper()} Channel')
        plt.xlim([0, 256])
        plt.title(f'Histogram of {title}')
        plt.xlabel('Pixel Intensity')
        plt.ylabel('Frequency')
        plt.legend(loc='upper right')  # Add legend for color channels
        plt.show()

# Loading images
lena_gray_dark_original = cv2.imread('lena_gray_dark.jpg')  # Grayscale image
lena_gray_dark = cv2.imread('lena_gray_dark.jpg', 0)  # Grayscale image
livingroom_dark = cv2.imread('livingroom_dark.tiff')  # Color image

# Apply histogram equalization
equalized_gray = histogram_equalization_gray(lena_gray_dark)
equalized_color_hsv = histogram_equalization_color_hsv(livingroom_dark)

# Plot histograms
plot_histograms(lena_gray_dark, 'Original Grayscale Image')
plot_histograms(equalized_gray, 'Equalized Grayscale Image')
plot_histograms(livingroom_dark, 'Original Color Image')
plot_histograms(equalized_color_hsv, 'Equalized Color Image (HSV)')

# Displaying images using matplotlib
plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.imshow(lena_gray_dark_original, cmap='gray')
plt.title('Original Grayscale Image')

plt.subplot(1, 2, 2)
plt.imshow(equalized_gray, cmap='gray')
plt.title('Equalized Grayscale Image')

plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.imshow(cv2.cvtColor(livingroom_dark, cv2.COLOR_BGR2RGB))
plt.title('Original Color Image')

plt.subplot(1, 2, 2)
plt.imshow(cv2.cvtColor(equalized_color_hsv, cv2.COLOR_BGR2RGB))
plt.title('Equalized Color Image (HSV)')

plt.show()

import cv2
import numpy as np
import matplotlib.pyplot as plt

# Function to compute the histogram and CDF of an image
def compute_histogram_and_cdf(image):
    hist, bins = np.histogram(image.flatten(), 256, [0, 256])
    cdf = hist.cumsum()  # Cumulative sum
    cdf_normalized = cdf / cdf.max()  # Normalize the cdf
    return hist, cdf_normalized

# Function for histogram matching (grayscale or single channel)
def histogram_matching_gray(source, target):
    # Compute histograms and CDFs for source and target
    source_hist, source_cdf = compute_histogram_and_cdf(source)
    target_hist, target_cdf = compute_histogram_and_cdf(target)

    # Create a mapping from source pixel values to target pixel values
    mapping = np.zeros(256)
    for src_pixel in range(256):
        # Find the closest pixel value in the target image's CDF
        closest_pixel = np.argmin(np.abs(source_cdf[src_pixel] - target_cdf))
        mapping[src_pixel] = closest_pixel

    # Apply the mapping to the source image to get the matched image
    matched_image = mapping[source]

    return matched_image.astype(np.uint8)

# Function for histogram matching on the V channel in HSV color space
def histogram_matching_color_hsv(source, target):
    # Convert the images from BGR to HSV color space
    source_hsv = cv2.cvtColor(source, cv2.COLOR_BGR2HSV)
    target_hsv = cv2.cvtColor(target, cv2.COLOR_BGR2HSV)

    # Perform histogram matching only on the V (Value) channel
    source_v = source_hsv[:, :, 2]
    target_v = target_hsv[:, :, 2]

    matched_v = histogram_matching_gray(source_v, target_v)

    # Replace the V channel in the source image with the matched V channel
    source_hsv[:, :, 2] = matched_v

    # Convert the image back to BGR color space
    matched_image = cv2.cvtColor(source_hsv, cv2.COLOR_HSV2BGR)

    return matched_image

# Function to plot histograms
def plot_histograms(image, title):
    plt.figure(figsize=(10, 5))
    if len(image.shape) == 2:  # Grayscale image
        plt.hist(image.ravel(), 256, [0, 256], color='gray')
        plt.title(f'Histogram of {title}')
        plt.xlabel('Pixel Intensity')
        plt.ylabel('Frequency')
        plt.show()
    else:  # Color image
        color = ('b', 'g', 'r')
        for i, col in enumerate(color):
            hist = cv2.calcHist([image], [i], None, [256], [0, 256])
            plt.plot(hist, color=col, label=f'{col.upper()} Channel')
        plt.xlim([0, 256])
        plt.title(f'Histogram of {title}')
        plt.xlabel('Pixel Intensity')
        plt.ylabel('Frequency')
        plt.legend(loc='upper right')
        plt.show()

# Loading images
mandril_color = cv2.imread('mandril_color.jpg')
lena_color = cv2.imread('lena_color_512.jpg')

mandril_gray = cv2.imread('mandril_gray.jpg', 0)  # Grayscale image
lena_gray = cv2.imread('lena_gray_512.jpg', 0)  # Grayscale image

# Apply histogram matching for grayscale images
matched_gray = histogram_matching_gray(mandril_gray, lena_gray)

# Apply histogram matching for color images using HSV (V channel only)
matched_color_hsv = histogram_matching_color_hsv(mandril_color, lena_color)

# Plot histograms for grayscale
plot_histograms(mandril_gray, 'Source Grayscale Image (Mandril)')
plot_histograms(lena_gray, 'Target Grayscale Image (Lena)')
plot_histograms(matched_gray, 'Histogram Matched Grayscale Image')

# Plot histograms for color images
plot_histograms(mandril_color, 'Source Color Image (Mandril)')
plot_histograms(lena_color, 'Target Color Image (Lena)')
plot_histograms(matched_color_hsv, 'Histogram Matched Color Image (HSV - V Channel)')

# Displaying images using matplotlib
plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.imshow(mandril_gray, cmap='gray')
plt.title('Source Grayscale Image (Mandril)')

plt.subplot(1, 2, 2)
plt.imshow(matched_gray, cmap='gray')
plt.title('Histogram Matched Grayscale Image')

plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.imshow(cv2.cvtColor(mandril_color, cv2.COLOR_BGR2RGB))
plt.title('Source Color Image (Mandril)')

plt.subplot(1, 2, 2)
plt.imshow(cv2.cvtColor(matched_color_hsv, cv2.COLOR_BGR2RGB))
plt.title('Histogram Matched Color Image (HSV - V Channel)')

plt.show()