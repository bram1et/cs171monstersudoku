class FileWriter:
    def __init__(self, output_file):
        self.output_file = output_file

    def write_to_output(self, run_info):
        self.output_file.write("TOTAL_START=" + str(run_info.total_start) + "\n")
        self.output_file.write("PREPROCESSING_START=" + str(run_info.preprocessing_start) + "\n")
        self.output_file.write("PREPROCESSING_DONE=" + str(run_info.preprocessing_done) + "\n")
        self.output_file.write("SEARCH_START=" + str(run_info.search_start) + "\n")
        self.output_file.write("SEARCH_DONE=" + str(run_info.search_done) + "\n")
        self.output_file.write("SOLUTION_TIME=" + str(run_info.preprocessing_done - run_info.preprocessing_start +
                                                      run_info.search_done - run_info.search_start) + "\n")
        self.output_file.write("STATUS=" + str(run_info.status) + "\n")
        self.output_file.write("SOLUTION=" + str(run_info.solution) + "\n")
        if run_info.status == "timeout":
            self.output_file.write("COUNT_NODES=" + str(run_info.count_nodes) + "\n")
            self.output_file.write("COUNT_DEADENDS=" + str(run_info.count_deadends) + "\n")

