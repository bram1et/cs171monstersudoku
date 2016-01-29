class InputInformation:
    def __init__(self, input_arguments):
        self.input_file = input_arguments[1]
        self.output_file = input_arguments[2]
        self.timeout_limit = input_arguments[3]
