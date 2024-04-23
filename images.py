from png import *

def get_png(file: str) -> list[list[tuple]]:
    """
    Given a file path, returns the image formatted like:
    [
        [(R, G, B), (R, G, B)],
        [(R, G, B), (R G, B)]
    ]
    where R, G, B are all between 0 and 1
    """
    image = Reader(filename=file).asDirect()
    pixels = [list(row) for row in image[2]]
    image_arr = []
    step = 3
    if len(pixels[0]) % 4 == 0:
        step = 4
    for row in pixels:
        curr_row = []
        for pixel_num in range(0, len(row), step):
            curr_row.append((row[pixel_num] / 255, row[pixel_num + 1] / 255, row[pixel_num + 2] / 255))
        image_arr.append(curr_row)
    return image_arr

def image_to_grayscale(image: list[list[tuple]]) -> list[list[float]]:
    """
    Given an image (as defined by the get_png function), returns the same array, but with (R, G, B) replaced with a value of 0 to 1, where 0 is dark and 1 is light
    """
    img_arr = []
    for row in image:
        curr_row = []
        for color in row:
            value = 0.299 * color[0] + 0.587 * color[1] + 0.114 * color[2]
            if value > 1:
                value = 1
            curr_row.append(value)
        img_arr.append(curr_row)
    return img_arr

def image_to_pypng(image: list[list[tuple]]) -> list[list[float]]:
    """
    Given an image formatted as described in get_png, returns an array that pypng likes: [(R, G, B), (R, G, B)] to [R, G, B, R, G, B]
    """
    img_arr = []
    for row in image:
        new_row = []
        for color in row:
            new_row.append(int(color[0] * 255))
            new_row.append(int(color[1] * 255))
            new_row.append(int(color[2] * 255))
        img_arr.append(new_row)
    return from_array(img_arr, "RGB")

def gray_image_to_pypng(image: list[list[float]]) -> list[list[float]]:
    """
    Given an image formatted as described in image_to_grayscale, returns an array that pypng likes: [f, f] to [R, G, B, R, G, B] where R1 = G1 = B1 = f * 255 (f is from 0 to 1)
    """
    img_arr = []
    for row in image:
        new_row = []
        for dark in row:
            new_row.append(int(dark * 255))
            new_row.append(int(dark * 255))
            new_row.append(int(dark * 255))
        img_arr.append(new_row)
    return from_array(img_arr, "RGB")

def threshold_gray(image: list[list[float]], n: int = 7) -> list[list[int]]:
    """
    Given a gray image:
    [
        [f, f],
        [f, f]
    ]
    where f is a pixel's lightness value between 0 and 1, replaces f with an integer from 0 to n-1, where 0 becomes 0 and 1 becomes n-1
    """
    img_arr = []
    for row in image:
        new_row = []
        for value in row:
            for i in range(1, n+1):
                if value <= i / n or i == n:
                    new_row.append(i - 1)
                    break
        img_arr.append(new_row)
    return img_arr

def threshold_to_1bit(image: list[list[int]]) -> list[list[tuple]]:
    """
    Given an image where each pixel is an integer from 0 to n (haven't decided), replaces each pixel with either (0, 0, 0) or (1, 1, 1) depending on the pixel value (darkness) and the logic applied to a specific darkness to create a stippling effect
    """
    img_arr = []
    for row_num in range(len(image)):
        new_row = []
        for col in range(len(image[row_num])):
            match image[row_num][col]:

                case 6: # White
                    new_row.append((1, 1, 1))

                case 5:
                    """
                    W___W___W___
                    __W___W___W___
                    ____________
                    W___W___W___
                    __W___W___W___
                    """
                    if row_num % 3 == 0:
                        if col % 4 == 0:
                            new_row.append((0, 0, 0))
                        else:
                            new_row.append((1, 1, 1))
                    elif row_num % 3 == 1:
                        if col % 4 == 2:
                            new_row.append((0, 0, 0))
                        else:
                            new_row.append((1, 1, 1))
                    else:
                        new_row.append((1, 1, 1))

                case 4:
                    """
                    W___W___W___
                    __W___W___W___
                    """
                    if row_num % 2 == 0:
                        if col % 4 == 0:
                            new_row.append((0, 0, 0))
                        else:
                            new_row.append((1, 1, 1))
                    else:
                        if col % 4 == 2:
                            new_row.append((0, 0, 0))
                        else:
                            new_row.append((1, 1, 1))

                case 3:
                    if row_num % 2 == col % 2:
                        new_row.append((0, 0, 0))
                    else:
                        new_row.append((1, 1, 1))

                case 2:
                    """
                    W___W___W___
                    __W___W___W___
                    """
                    if row_num % 2 == 0:
                        if col % 4 == 0:
                            new_row.append((1, 1, 1))
                        else:
                            new_row.append((0, 0, 0))
                    else:
                        if col % 4 == 2:
                            new_row.append((1, 1, 1))
                        else:
                            new_row.append((0, 0, 0))

                case 1:
                    """
                    W___W___W___
                    __W___W___W___
                    ____________
                    W___W___W___
                    __W___W___W___
                    """
                    if row_num % 3 == 0:
                        if col % 4 == 0:
                            new_row.append((1, 1, 1))
                        else:
                            new_row.append((0, 0, 0))
                    elif row_num % 3 == 1:
                        if col % 4 == 2:
                            new_row.append((1, 1, 1))
                        else:
                            new_row.append((0, 0, 0))
                    else:
                        new_row.append((0, 0, 0))

                case 0:
                    new_row.append((0, 0, 0))
                    # Alternative black
                    # match row_num % 4:
                    #     case 0:
                    #         if col % 4 == 0:
                    #             new_row.append((1, 1, 1))
                    #         else:
                    #             new_row.append((0, 0, 0))
                    #     case 1:
                    #         new_row.append((0, 0, 0))
                    #     case 2:
                    #         if col % 4 == 2:
                    #             new_row.append((1, 1, 1))
                    #         else:
                    #             new_row.append((0, 0, 0))
                    #     case 3:
                    #         new_row.append((0, 0, 0))

        img_arr.append(new_row)
    return img_arr

city_image = get_png(r"C:\Users\jord0451.SCDSB.000\Desktop\cat.png")
print("got png")
gray_city_image = image_to_grayscale(city_image)
print("got grayscale")
thresholded_image = threshold_gray(gray_city_image)
print("thresholded")
final = threshold_to_1bit(thresholded_image)
print("shaded")
pypngfinal: Image = image_to_pypng(final)
print("converted")
pypngfinal.save(r"C:\Users\jord0451.SCDSB.000\Desktop\catoldblack.png")
print("saved: done!")