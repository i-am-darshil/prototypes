import cv2
import numpy as np
import matplotlib.pyplot as plt

image = cv2.imread("logo.png", cv2.IMREAD_GRAYSCALE)

image = cv2.resize(image, (100, 100))

brightened = np.clip(image * 1.5, 0, 255).astype(np.uint8)
darkened = np.clip(image * 0.5, 0, 255).astype(np.uint8)
added = np.clip(image.astype(np.int16) + 50, 0, 255).astype(np.uint8)
subtracted = np.clip(image.astype(np.int16) - 50, 0, 255).astype(np.uint8)
transposed = np.transpose(image)

fig, axs = plt.subplots(2, 3, figsize=(12, 8))

images = [
    (image, "Original"),
    (brightened, "Brightened (×1.5)"),
    (darkened, "Darkened (×0.5)"),
    (added, "Added (+50)"),
    (subtracted, "Subtracted (–50)"),
    (transposed, "Transposed"),
]

for ax, (img, title) in zip(axs.ravel(), images):
    ax.imshow(img, cmap='gray', vmin=0, vmax=255)
    ax.set_title(title)
    ax.axis('off')

plt.tight_layout()
plt.show()
