import unittest
# import code; code.interact(local=dict(globals(), **locals()))

def find_rectangular_overlap(rect1, rect2):

    # Calculate the overlap between the two rectangles
    if rect1['left_x'] < rect2['left_x']:
        x1, y1, w1, h1 = [rect1['left_x'], rect1['bottom_y'], rect1['width'], rect1['height']]
        x2, y2, w2, h2 = [rect2['left_x'], rect2['bottom_y'], rect2['width'], rect2['height']]
    else:
        x1, y1, w1, h1 = [rect2['left_x'], rect2['bottom_y'], rect2['width'], rect2['height']]
        x2, y2, w2, h2 = [rect1['left_x'], rect1['bottom_y'], rect1['width'], rect1['height']]

    x3, y3, w3, h3 = [None] * 4

    if (x2 < (x1 + w1)) and (y2 < (y1 + h1)):
        # find_x_overlap
        x3 = x2
        if (x1 + w1) > (x2 + w2):
            w3 = x1 + w1 - (x2 + w2)
        else:
            w3 = x1 + w1 - x2


        # find_y_overlap
        y3 = y2
        if (y1 + h1) > (y2 + h2):
            h3 = y1 + h1 - (y2 + h2)
        else:
            h3 = y1 + h1 - (y2)

    return {
        'left_x'   : x3,
        'bottom_y' : y3,
        'width'    : w3,
        'height'   : h3,
    }

# Tests

class Test(unittest.TestCase):

    def test_overlap_along_both_axes(self):
        rect1 = {
            'left_x': 1,
            'bottom_y': 1,
            'width': 6,
            'height': 3,
        }
        rect2 = {
            'left_x': 5,
            'bottom_y': 2,
            'width': 3,
            'height': 6,
        }
        expected = {
            'left_x': 5,
            'bottom_y': 2,
            'width': 2,
            'height': 2,
        }
        actual = find_rectangular_overlap(rect1, rect2)
        self.assertEqual(actual, expected)


    def test_one_rectangle_inside_another(self):
        rect1 = {
            'left_x': 1,
            'bottom_y': 1,
            'width': 6,
            'height': 6,
        }
        rect2 = {
            'left_x': 3,
            'bottom_y': 3,
            'width': 2,
            'height': 2,
        }
        expected = {
            'left_x': 3,
            'bottom_y': 3,
            'width': 2,
            'height': 2,
        }
        actual = find_rectangular_overlap(rect1, rect2)
        self.assertEqual(actual, expected)

    def test_both_rectangles_the_same(self):
        rect1 = {
            'left_x': 2,
            'bottom_y': 2,
            'width': 4,
            'height': 4,
        }
        rect2 = {
            'left_x': 2,
            'bottom_y': 2,
            'width': 4,
            'height': 4,
        }
        expected = {
            'left_x': 2,
            'bottom_y': 2,
            'width': 4,
            'height': 4,
        }
        actual = find_rectangular_overlap(rect1, rect2)
        self.assertEqual(actual, expected)

    def test_touch_on_horizontal_edge(self):
        rect1 = {
            'left_x': 1,
            'bottom_y': 2,
            'width': 3,
            'height': 4,
        }
        rect2 = {
            'left_x': 2,
            'bottom_y': 6,
            'width': 2,
            'height': 2,
        }
        expected = {
            'left_x': None,
            'bottom_y': None,
            'width': None,
            'height': None,
        }
        actual = find_rectangular_overlap(rect1, rect2)
        self.assertEqual(actual, expected)

    def test_touch_on_vertical_edge(self):
        rect1 = {
            'left_x': 1,
            'bottom_y': 2,
            'width': 3,
            'height': 4,
        }
        rect2 = {
            'left_x': 4,
            'bottom_y': 3,
            'width': 2,
            'height': 2,
        }
        expected = {
            'left_x': None,
            'bottom_y': None,
            'width': None,
            'height': None,
        }
        actual = find_rectangular_overlap(rect1, rect2)
        self.assertEqual(actual, expected)

    def test_touch_at_a_corner(self):
        rect1 = {
            'left_x': 1,
            'bottom_y': 1,
            'width': 2,
            'height': 2,
        }
        rect2 = {
            'left_x': 3,
            'bottom_y': 3,
            'width': 2,
            'height': 2,
        }
        expected = {
            'left_x': None,
            'bottom_y': None,
            'width': None,
            'height': None,
        }
        actual = find_rectangular_overlap(rect1, rect2)
        self.assertEqual(actual, expected)

    def test_no_overlap(self):
        rect1 = {
            'left_x': 1,
            'bottom_y': 1,
            'width': 2,
            'height': 2,
        }
        rect2 = {
            'left_x': 4,
            'bottom_y': 6,
            'width': 3,
            'height': 6,
        }
        expected = {
            'left_x': None,
            'bottom_y': None,
            'width': None,
            'height': None,
        }
        actual = find_rectangular_overlap(rect1, rect2)
        self.assertEqual(actual, expected)


unittest.main(verbosity=2)



'''
Solution:

  def find_range_overlap(point1, length1, point2, length2):
    # Find the highest start point and lowest end point.
    # The highest ("rightmost" or "upmost") start point is
    # the start point of the overlap.
    # The lowest end point is the end point of the overlap.
    highest_start_point = max(point1, point2)
    lowest_end_point = min(point1 + length1, point2 + length2)

    # Return null overlap if there is no overlap
    if highest_start_point >= lowest_end_point:
        return (None, None)

    # Compute the overlap length
    overlap_length = lowest_end_point - highest_start_point

    return (highest_start_point, overlap_length)


def find_rectangular_overlap(rect1, rect2):
    # Get the x and y overlap points and lengths
    x_overlap_point, overlap_width  = find_range_overlap(rect1['left_x'],
                                                         rect1['width'],
                                                         rect2['left_x'],
                                                         rect2['width'])
    y_overlap_point, overlap_height = find_range_overlap(rect1['bottom_y'],
                                                         rect1['height'],
                                                         rect2['bottom_y'],
                                                         rect2['height'])

    # Return null rectangle if there is no overlap
    if not overlap_width or not overlap_height:
        return {
            'left_x'   : None,
            'bottom_y' : None,
            'width'    : None,
            'height'   : None,
        }

    return {
        'left_x'   : x_overlap_point,
        'bottom_y' : y_overlap_point,
        'width'    : overlap_width,
        'height'   : overlap_height,
    }

Bonus
What if we had a list of rectangles and wanted to
find all the rectangular overlaps between all possible pairs
of two rectangles within the list? Note that we'd be returning a list of rectangles.
What if we had a list of rectangles and wanted to find the overlap
between all of them, if there was one? Note that we'd be returning a single rectangle.
'''
