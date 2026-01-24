# Horizontal image flip.....
from PIL import Image
image = Image.open('original.jpg')
flipped_horizontally = image.transpose(Image.FLIP_LEFT_RIGHT)
flipped_horizontally.save('flipped_horizontaly.jpg')
image.show()
