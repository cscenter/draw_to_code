import argparse

from model import Model
from pic_generator import generate_random_pic, save_pil_image, load_image, image_to_square
from latex_pic_generator import convert_to_latex


def arg_parse():
    parser = argparse.ArgumentParser(description='Convert draw to code.')
    parser.add_argument('--image', '-im', '-i',
                        type=str, help='Image', required=True)
    parser.add_argument('--image_size', '-s',
                        type=int, help='Image size', default=100)

    args = parser.parse_args()
    return args


def main():
    args = arg_parse()
    image_size = args.image_size
    image = args.image
    im = image_to_square(load_image(image), image_size)
    model = Model(image_size)

    print('solve')
    circles, segments, images = model.solve(im)

    for i, im in enumerate(images):
        save_pil_image(im, "pics/test_{}".format(i))

    latex = convert_to_latex([*circles, *segments])
    print(latex)


if __name__ == '__main__':
    main()
