from PIL import Image
from collections import Counter

class PixelCounter:
    def __init__(self, image_path, threshold=30):
        self.image_path = image_path


    def count_pixels(self):
        img = Image.open(self.image_path)

        #Creates an empty list to store all pixel colours
        pixel_colours = []

        #Goes through every pixel in the image, adding the colour of each to a list
        for y in range(img.height):
            for x in range(img.width):
                pixel_colour = img.getpixel((x, y))
                pixel_colours.append(pixel_colour)

        #Counts the number of ocurrences of colours and saves them as (rgb_code):num_ocurrences
        colour_counts = Counter(pixel_colours)

        #Saves the most frequent colours into the top_colours variable as a tuple
        top_colours = colour_counts.most_common()

        #Converts top colours(RGB plus count) into just RGB code list
        rgb_codes = [str(colour[0])[1:-1] for colour in top_colours]

        return rgb_codes

    def remove_similar_colours(self, rgb_codes):
        #Creates an empty dictionary to store the RGB codes and their sums
        rgb_to_sum = {}

        #Iterates over the RGB codes and calculate their sums
        for code in rgb_codes:
            rgb_integers = [int(x.strip()) for x in code.split(",")]
            colour_sum = sum(rgb_integers)
            #Adds the RGB code and its sum to the dictionary, maintaining the order
            if colour_sum not in rgb_to_sum:
                rgb_to_sum[colour_sum] = code

        #Creates an empty set to store the filtered sums
        filtered_sums = set()
        similar_threshold = 25

        #Iterates over the sums in the dictionary and filter out similar ones
        for sum_val in rgb_to_sum:
            is_similar = False
            #Checks if the sum is similar to any existing sum in the filtered set
            for filtered_sum in filtered_sums:
                if abs(sum_val - filtered_sum) <= similar_threshold:
                    is_similar = True
                    break
            #If the sum is not similar, adds it to the filtered set
            if not is_similar:
                filtered_sums.add(sum_val)

        #Creates a list to store the filtered RGB codes, maintaining the order
        filtered_rgb_codes = []
        for sum_val in rgb_to_sum:
            #If the sum is in the filtered set, adds the corresponding RGB code to the list
            if sum_val in filtered_sums:
                filtered_rgb_codes.append(rgb_to_sum[sum_val])

        return filtered_rgb_codes













