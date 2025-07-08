import cv2
import numpy as np
import matplotlib.pyplot as plt

image = cv2.imread("logo.png", cv2.IMREAD_GRAYSCALE)

resized = cv2.resize(image, (24, 24), interpolation=cv2.INTER_AREA)

fig, axs = plt.subplots(1, 2, figsize=(14, 7))

axs[0].imshow(resized, cmap='gray', vmin=0, vmax=255)
axs[0].set_title("Image")
axs[0].axis('off')

axs[1].imshow(resized, cmap='gray', vmin=0, vmax=255)
for i in range(resized.shape[0]):
    for j in range(resized.shape[1]):
        axs[1].text(j, i, f"{resized[i, j]}", ha='center', va='center', color='red', fontsize=8)
axs[1].set_title("Matrix Values")
axs[1].axis('off')

plt.tight_layout()
plt.show()
