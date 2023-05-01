import copy
import ex5_helper
import math
import sys
from typing import List, Tuple

##############################################################################
# FILE: cartoonify.py
# EXERCISE: Intro2cs ex5 2021-2022
# WRITER: Tal Sharon, 315813980, talsharon
# DESCRIPTION: a program which conducts image processing, making a cartoon out of an image.
##############################################################################


def separate_channels(image: List[list[list]]) -> List[list[list]]:
    """
    separates the channels of an image
    :param image: an image which needs it's channel separated
    :return: a third dimensional matrix - lists of every channel of the original image separated to a different list
    """
    separated_channel = []
    for channel in range(len((image[0][0]))):
        separated_channel.append([])
        for row in range(len(image)):
            separated_channel[channel].append([])
    for row in range(len(image)):
        for column in range(len(image[row])):
            for channel in range(len(image[row][column])):
                separated_channel[channel][row].append(image[row][column][channel])
    return separated_channel


def combine_channels(channels: List[list[list]]) -> List[list[list]]:
    """
    combines channels to a single image
    :param channels: a third dimensional matrix of the separated channels of an image
    :return: a third dimensional matrix (an image) of all the channels combined together
    """
    combined_channel = []
    for row in range(len(channels[0])):
        combined_channel.append([])
        for column in range(len(channels[0][0])):
            combined_channel[row].append([])
    for channel in range(len(channels)):
        for row in range(len(channels[channel])):
            for column in range(len(channels[channel][row])):
                combined_channel[row][column].append(channels[channel][row][column])
    return combined_channel


def RGB2grayscale(colored_image: List[list[list]]) -> List[list]:
    """
    turn and RGB image to a greyscale image
    :param colored_image: a colored RedGreenBlue image - a third dimensional matrix
    :return: the greyscale image - a two dimensional matrix
    """
    greyscale_image = copy.deepcopy(colored_image)
    for row in range(len(greyscale_image)):
        for column in range(len(greyscale_image[row])):
            red = greyscale_image[row][column][0]
            green = greyscale_image[row][column][1]
            blue = greyscale_image[row][column][2]
            grayscale_value = red * 0.299 + green * 0.587 + blue * 0.114
            greyscale_image[row][column] = round(grayscale_value)
    return greyscale_image


def blur_kernel(size: int) -> List[list]:
    """
    creates a kernel to be used for blurring an image
    :param size: the block size of the kernel
    :return: a kernel
    """
    if size < 0:
        size = -1 * size
    kernel = []
    for i in range(size):
        kernel.append([])
        for j in range(size):
            kernel[i].append(1/size**2)
    return kernel


def apply_kernel(image: List[list], kernel: List[list]):
    """
    blurs an a greyscale image - applies a blur kernel on the image
    :param image: the image to be blurred
    :param kernel: the kernel blurring the image
    :return: the blurred greyscale image
    """
    blurred_image = copy.deepcopy(image)
    s = len(kernel) // 2
    for row in range(len(blurred_image)):
        for column in range(len(blurred_image[row])):
            neighbours = find_blur_neighbours(image, column, row, s)
            blurred_image[row][column] = blur_pixel(kernel, neighbours)
    return blurred_image


def blur_pixel(kernel: List[list[list]], neighbours: List):
    """
    generates the bluring action on a certain pixel
    :param kernel: the kernel of the blurring method
    :param neighbours: the neighbour pixels which are used in the kernel to create the blur
    :return: a new "blurred" value for the pixel
    """
    blurred_pixel = 0
    for i in range(len(kernel)):
        for j in range(len(kernel)):
            blurred_pixel += kernel[i][j] * neighbours[i][j]
    blurred_pixel = round(blurred_pixel)
    return blurred_pixel


def find_blur_neighbours(image: List[list[list]], column: int, row: int, s: int) -> List[list]:
    """
    gets the neighbours of a pixel by a given size
    :param image: the original image
    :param column: the column index of the pixel
    :param row: the row index of the pixel
    :param s: the distance between the pixel and the further neighbour
    :return: a list of all neighbours
    """
    neighbours = []
    for block_row in range(row - s, (row + s + 1)):
        neighbours_row = []
        if block_row > (len(image) - 1) or block_row < 0:
            for out_of_border_column in range(2 * s + 1):
                neighbours_row.append(image[row][column])
        else:
            for block_column in range(column - s, (column + s + 1)):
                if block_column > (len((image[row])) - 1) or block_column < 0:
                    neighbours_row.append(image[row][column])
                else:
                    neighbours_row.append(image[block_row][block_column])
        neighbours.append(neighbours_row)
    return neighbours


def interpolate(image: List[list], y: int, x: int, real_y: int, real_x: int) -> int:
    """
    calculates the value for a pixel in the resized image relative of it's location
    :param image: the original image
    :param y: the height of the resized image
    :param x: the width of the resized image
    :param real_y: the height distance relative to a certain pixel
    :param real_x: the width distance relative to a certain pixel
    :return: value of a pixel in the resized image
    """
    if y % 1 == 0 and x % 1 == 0:
        d = image[y][x]
        pixel_sum = d
    elif y % 1 == 0:
        b = image[y][int(x // 1)]
        d = image[y][int((x // 1) + 1)]
        pixel_sum = b * 1 * (1 - real_x) + \
                    d * real_x * 1
    elif x % 1 == 0:
        a = image[int(y // 1)][x]
        c = image[int((y // 1) + 1)][x]
        pixel_sum = a * 1 * (1 - real_y) + \
                    c * 1 * (1 - real_y)
    else:
        a = image[int(y // 1)][int(x // 1)]
        b = image[int((y // 1) + 1)][int(x // 1)]
        c = image[int(y // 1)][int((x // 1) + 1)]
        d = image[int((y // 1) + 1)][int((x // 1) + 1)]
        pixel_sum = a * (1 - real_x) * (1 - real_y) + \
                    b * real_y * (1 - real_x) + \
                    c * real_x * (1 - real_y) + \
                    d * real_x * real_y
    return pixel_sum


def bilinear_interpolation(image: List[list[list]], y: int, x: int) -> int:
    """
    gets the value of a pixel in a resized image
    :param image: the original image
    :param y: the height of the resized image
    :param x: the width of the resized image
    :return: the value of a pixel in the resized image
    """
    real_x = x % 1
    real_y = y % 1
    pixel_sum = round(interpolate(image, y, x, real_y, real_x))
    return pixel_sum


def resize(image: List[list], new_height: int, new_width: int) -> List[list[list]]:
    """
    resizes a one channel image
    :param image: the original one channel image
    :param new_height: the new height in pixels
    :param new_width: the new width in pixels
    :return: the resized image
    """
    height_ratio = len(image) / new_height
    width_ratio = len(image[0]) / new_width
    resized_image = get_resized_pixels(image, new_height, height_ratio, new_width, width_ratio)
    resized_image = resize_corners(image, new_height, new_width, resized_image)
    return resized_image


def resize_corners(image: List[list], new_height: int, new_width: int, resized_image: List[list]) -> List[list]:
    """
    correcting the corner pixels of the resized image
    :param image: the original one channel image
    :param new_height: the new height in pixels
    :param new_width: the new width in pixels
    :param resized_image: the resized image
    :return:
    """
    resized_image[0][0] = image[0][0]
    resized_image[new_height - 1][0] = image[len(image) - 1][0]
    resized_image[0][new_width - 1] = image[0][len(image[0]) - 1]
    resized_image[new_height - 1][new_width - 1] = image[len(image) - 1][len(image[0]) - 1]
    return resized_image


def get_resized_pixels(image: List[list], new_height: int, height_ratio: float, new_width: int, width_ratio: float) \
        -> List[list]:
    """
    gets the new values of all the needed pixels for the resized image
    :param image: the original one channel image
    :param new_height: the new height in pixels
    :param height_ratio: the ratio between the original height to the new height of the resized image
    :param new_width: the new width in pixels
    :param width_ratio: the ratio between the original width to the new width of the resized image
    :return: a list of all the new pixels of the resized image
    """
    resized_image = []
    for row in range(new_height):
        new_row = []
        for column in range(new_width):
            new_pixel = bilinear_interpolation(image, round(row * height_ratio), round(column * width_ratio))
            new_row.append(new_pixel)
        resized_image.append(new_row)
    return resized_image


def resize_color(image: List[list], new_height: int, new_width: int) -> List[list[list]]:
    """
    resizing a colored image
    :param image: the original one channel image
    :param new_height: the new height in pixels
    :param new_width: the new width in pixels
    :return: the resized image
    """
    resized_img = copy.deepcopy(image)
    resized_img = separate_channels(resized_img)
    resized_channels = resize_channels(new_height, new_width, resized_img)
    combined_img = combine_channels(resized_channels)
    resized_img = combined_img
    return resized_img


def resize_channels(new_height: int, new_width: int, img: List[list]) -> List[list]:
    """
    resizing all the channels of a colored image
    :param new_height: the new height in pixels
    :param new_width: the new width in pixels
    :param img: the image which needs to be resized
    :return: the resized channels of the image
    """
    resized_channels = []
    for channel in img:
        resized_channel = []
        for i in range(len(channel)):
            resized_channel = resize(channel, new_height, new_width)
        resized_channels.append(resized_channel)
    return resized_channels


def rotate_90(image: List[list], direction: str) -> List[list]:
    """
    rotates an image 90 degrees right or left
    :param image: the image needs to be rotated
    :param direction: the direction of rotation
    :return: the rotated image
    """
    rotated_image = []
    for column in range(len(image[0])):
        rotated_image.append([])
    if direction == "R":
        rotate_right(image, rotated_image)
    else:
        rotated_image = rotate_left(image, rotated_image)
    return rotated_image


def rotate_left(image: List[list], rotated_image: List[list]) -> List[list]:
    """
    rotates an image to the left
    :param image: the original image
    :param rotated_image: the image to be rotated
    :return: the left rotated image
    """
    for row in range(len(image)):
        for column in range((len(image[0]))):
            rotated_image[column].append(image[row][column])
    rotated_image = rotated_image[::-1]
    return rotated_image


def rotate_right(image: List[list], rotated_image: List[list]) -> List[list]:
    """
    rotates an image to the right
    :param image: the original image
    :param rotated_image: the image to be rotated
    :return: the right rotated image
    """
    for row in range((len(image) - 1), -1, -1):
        for column in range(len(image[0])):
            rotated_image[column].append(image[row][column])
    return rotated_image


def get_edges(image: List[list], blur_size: int, block_size: int, c: int) -> List[list]:
    """
    gets the edges of an image
    :param image: the original image
    :param blur_size: the size of the blur
    :param block_size: the size of the block for a pixel to compare
    :param c: the difference between the threshold to the pixels value
    :return: an image of the original image's edges
    """
    blurred_image, edged_image, r = initiate_get_edges(block_size, blur_size, image)
    for row in range(len(blurred_image)):
        for column in range(len(blurred_image[0])):
            edged_image[row][column] = edge_pixel(blurred_image, row, column, c, r)
    return edged_image


def edge_pixel(blurred_image: List[list], row: int, column: int, c: int, r: int) -> int:
    """
    finding if a pixel is an edge and if so, edging the pixel
    :param blurred_image: the image after a blurring process
    :param row: the index of the pixel's row
    :param column: the index of the pixel's row
    :param c: the difference between the threshold to the pixels value
    :param r: the distance between the pixel and the border of the block
    :return: a new value for the pixel according if it's an edge or not
    """
    threshold = get_threshold(blurred_image, row, column, r)
    edged_pixel = 255
    if blurred_image[row][column] < threshold - c:
        edged_pixel = 0
    return edged_pixel


def get_threshold(blurred_image: List[list], row: int, column: int, r: int) -> int:
    """
    creates the threshold for the edge process
    :param blurred_image: the image after the blurring process
    :param column: the index of the pixel's row
    :param r: the distance between the pixel and the border of the block
    :param row: the index of the pixel's row
    :return: the threshold of a pixel
    """
    block = []
    for i in range(row - r, row + r + 1):
        if i >= len(blurred_image) or i < 0:
            for k in range(column - r, column + r + 1):
                block.append(blurred_image[row][column])
        else:
            for j in range(column - r, column + r + 1) or j < 0:
                if j >= (len(blurred_image[0])):
                    block.append(blurred_image[row][column])
                else:
                    block.append(blurred_image[i][j])
    threshold = sum(block) / len(block)
    return threshold


def initiate_get_edges(block_size: int, blur_size: int, image: List[list]) -> Tuple[List[list], List[list], int]:
    """
    initiates all the needed objects for getting the edges
    :param block_size: the size of the block for a pixel to compare
    :param blur_size: the size of the blur
    :param image: the original image
    :return: the blurred image, a copy of the original image to get edges and the max "radius" of the block
    """
    kernel = blur_kernel(blur_size)
    blurred_image = apply_kernel(image, kernel)
    edged_image = copy.deepcopy(blurred_image)
    r = block_size // 2
    return blurred_image, edged_image, r


def quantize(image: List[list], N: int) -> List[list]:
    """
    quantize the shades of a one channel image
    :param image: the original image
    :param N: the parameter for the levels of shades to quantize
    :return: the image after the quantize process
    """
    quant_image = copy.deepcopy(image)
    for row in range(len(quant_image)):
        for column in range(len(quant_image[0])):
            floor_value = math.floor(int(quant_image[row][column]) * N / 255)
            quant_value = round(floor_value * 255 / N)
            quant_image[row][column] = quant_value
    return quant_image


def quantize_colored_image(image: List[list[list]], N: int) -> List[list[list]]:
    """
    quantize the colors and shades of a multi-color image
    :param image: the original image
    :param N: the parameter for the levels of shades to quantize
    :return: the image after the quantize process
    """
    color_quant_image = copy.deepcopy(image)
    separated_img = separate_channels(color_quant_image)
    quant_channels = quantize_channels(N, separated_img)
    combined_img = combine_channels(quant_channels)
    color_quant_image = combined_img
    return color_quant_image


def quantize_channels(N: int, separated_img: List[list[list]]) -> List[list[list]]:
    """
    quantize the channels of a colored image
    :param N: the parameter for the levels of shades to quantize
    :param separated_img: the image separated to different color channels
    :return: the image's channels after the quantize process
    """
    quant_channels = []
    for channel in separated_img:
        channel = quantize(channel, N)
        quant_channels.append(channel)
    return quant_channels


def create_black(img: List[list]) -> List[list]:
    """
    creates a black image in the same size of an image
    :param img: an image
    :return: a black image
    """
    blacked = copy.deepcopy(img)
    for i in range(len(img)):
        for j in range(len(img[0])):
            for k in range(len(img[0][0])):
                blacked[i][j][k] = 0
    return blacked


def add_mask(image1: List[list], image2: List[list], mask: List[list]) -> List[list[list]]:
    """
    adds a mask on two images
    :param image1: the first image
    :param image2: the second image
    :param mask: the mask - two dimensional matrix - one channel image
    :return: the new image containing the masked two images
    """
    masked_img1 = copy.deepcopy(image1)
    if type(image1[0][0]) is int:
        # image1 and image2 are greyscale or one channel
        sep_img1 = apply_mask(image1, image2, mask)
        return sep_img1
    else:
        # image1 and image2 are colored
        sep_img1 = separate_channels(masked_img1)
        sep_img2 = separate_channels(image2)
        masked_img1 = mask_channels(sep_img1, sep_img2, mask)
        return masked_img1


def mask_channels(sep_img1: List[list[list]], sep_img2: List[list[list]], mask: List[list]) -> List[list[list]]:
    """
    masking the different channels of a colored image
    :param sep_img1: the first image after it's channels were separated
    :param sep_img2: the first image after it's channels were separated
    :param mask: the mask
    :return: the masked channels
    """
    masked_channels = []
    for count, channel in enumerate(sep_img1):
        new_channel_img = apply_mask(channel, sep_img2[count], mask)
        masked_channels.append(new_channel_img)
    combined_img = combine_channels(masked_channels)
    return combined_img


def apply_mask(image1: List[list], image2: List[list], mask: List[list]) -> List[list]:
    """
    applying the mask on a single channel
    :param image1: a channel of the first image
    :param image2: a channel the second image
    :param mask: the mask - two dimensional matrix - one channel image
    :return: the new channel containing the masked two channels
    """
    new_channel = []
    for row in range(len(image1)):
        new_channel.append([])
        for column in range(len(image1[0])):
            new_column = round(image1[row][column] * mask[row][column] + image2[row][column] * (1 - mask[row][column]))
            new_channel[row].append(new_column)
    return new_channel


def make_mask(image: List[list]) -> List[list]:
    """
    makes mask out of an image
    :param image: the image to convert
    :return: the mask
    """
    for i in range(len(image)):
        for j in range(len(image[0])):
            image[i][j] = image[i][j] / 255
    return image


def cartoonify(image: List[list], blur_size: int, th_block_size: int, th_c: int, quant_num_shades: int) -> List[list]:
    """
    the general function that makes a cartoon out of an image
    :param image: the original image
    :param blur_size: the size of the blur
    :param th_block_size: the size of the threshold block (for get edge process)
    :param th_c: the difference between the threshold to the pixels value (for get edge process)
    :param quant_num_shades: the parameter for the levels of shades to quantize
    :return: the cartoonified image
    """
    cartoonified_img, edged_img, mask_edges = initiate_cartoonify(blur_size, image, th_block_size, th_c)
    masked_img = make_cartoon(cartoonified_img, edged_img, image, mask_edges, quant_num_shades)
    cartoonified_img = masked_img
    return cartoonified_img


def make_cartoon(cartoonified_img, edged_img, image, mask_edges, quant_num_shades):
    """
    the actual last step of making the cartoon
    :param cartoonified_img: the cartooned image
    :param edged_img: and image of the original image's edges
    :param image: the original image
    :param mask_edges: the mask for the masking process
    :param quant_num_shades: the parameter for the levels of shades to quantize
    :return: the cartoon
    """
    if type(image[0][0]) is int:
        # if image is greyscale
        quanted_img = quantize(cartoonified_img, quant_num_shades)
        masked_img = add_mask(quanted_img, edged_img, mask_edges)
    else:
        quanted_img = quantize_colored_image(cartoonified_img, quant_num_shades)
        black_img = create_black(quanted_img)
        masked_img = add_mask(quanted_img, black_img, mask_edges)
    return masked_img


def initiate_cartoonify(blur_size: int, image: List[list], th_block_size: int, th_c: int) -> \
        Tuple[List[list], List[list], List[list]]:
    """
    initiates all the needed objects for cartoonifying
    :param blur_size: the size of the blur
    :param image: the original image
    :param th_block_size: the size of the threshold block (for get edge process)
    :param th_c: the difference between the threshold to the pixels value (for get edge process)
    :return: a copy of the original image, the image of edges, the mask for the masking process
    """
    cartoonified_img = copy.deepcopy(image)
    greyscale_img = RGB2grayscale(cartoonified_img)
    edged_img = get_edges(greyscale_img, blur_size, th_block_size, th_c)
    mask_edges = make_mask(edged_img)
    return cartoonified_img, edged_img, mask_edges


def main():
    """
    the main function, ables to make cartoons through the commandline
    :return: saves the cartoonified image
    """
    if len(sys.argv) != 8:
        if len(sys.argv) > 8:
            print("too many arguments entered")
        else:
            print("not enough arguments entered")
    else:
        blur_size, cartoon_dest, image_source, max_im_size, quant_num_shades, th_block_size, th_c = set_argv()
        image = ex5_helper.load_image(image_source)
        image = check_max_size(image, max_im_size)
        cartoon = cartoonify(image, blur_size, th_block_size, th_c, quant_num_shades)
        ex5_helper.save_image(cartoon, cartoon_dest)


def check_max_size(image: List[list], max_im_size: int) -> List[list]:
    """
    checks if the image is too big, if so, resizes the image according to the max size.
    :param image: the original image
    :param max_im_size: the max size
    :return: the image in a compatible size
    """
    if max_im_size < len(image):
        size_ratio = len(image) / max_im_size
        new_height = max_im_size
        new_width = round(len(image[0]) / size_ratio)
        image = resize(image, new_height, new_width)
    return image


def set_argv() -> Tuple[int, str, str, int, int, int, int]:
    """
    sets parameters from command line
    :return: renamed parameters
    """
    image_source = sys.argv[1]
    cartoon_dest = sys.argv[2]
    max_im_size = int(sys.argv[3])
    blur_size = int(sys.argv[4])
    th_block_size = int(sys.argv[5])
    th_c = int(sys.argv[6])
    quant_num_shades = int(sys.argv[7])
    return blur_size, cartoon_dest, image_source, max_im_size, quant_num_shades, th_block_size, th_c


if __name__ == '__main__':
    main()
