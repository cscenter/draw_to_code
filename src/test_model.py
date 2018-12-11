from model import Model
from pic_generator import generate_random_pic, save_pil_image, load_image


IMAGE_SIZE = 100
model = Model(IMAGE_SIZE)
im, figures = generate_random_pic(IMAGE_SIZE, 1, 1)
im = load_image("test.png")

print('solve')
circles, segments, images = model.solve(im)

print(circles)
print(segments)
print(images)

for i, im in enumerate(images):
    save_pil_image(im, "pics/test_{}".format(i))
