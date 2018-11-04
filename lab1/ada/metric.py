class Metric:

    def __init__(self, img_name, img_dimensions, processing_time, matches_count):
        self.img_name = img_name
        # will be either + or -
        self.object_present = img_name[3]
        self.img_dimensions = img_dimensions
        self.processing_time = processing_time
        self.matches_count = matches_count
