import csv


class Save():
    def __init__(self, filename: str, fieldnames: list, translator: dict, path: str):
        self.new_entry = []
        self.path = path
        self.filename = filename
        self.fieldnames = fieldnames
        self.translator = translator
        self.file = self.generate_save_file()
        if self.file == False:
            self.file = self.generate_save_file()
        
    
    def generate_save_file(self):
        try:
            with open(f"{self.path}{self.filename}.csv", "r", newline="") as save_file:
                reader = csv.DictReader(save_file, fieldnames=self.fieldnames)
                save_dict = []
                for line in reader:
                    save_dict.append(line)
                return save_dict
        except FileNotFoundError:
            with open(f"{self.path}{self.filename}.csv", "w+", newline="") as save_file:
                writer = csv.DictWriter(save_file, fieldnames=self.fieldnames)
                return False
        finally:
            pass

    def csv_writer(self):
        with open(f"{self.path}{self.filename}.csv", "a", newline="") as save_file:
            writer = csv.DictWriter(save_file, fieldnames=self.fieldnames)
            for entry in self.new_entry:
                writer.writerow(entry)

    def update_list(self, data):
        data = data
        new_line = {}
        for i, field in enumerate(self.fieldnames):
            new_line[field] = data[i]
        self.file.append(new_line)
        self.new_entry.append(new_line)

    def update_dict(self, entry: dict): #dict keys should be fieldnames
        new_line = entry
        self.file.append(new_line)
        self.new_entry.append(new_line)
    
    def translate(self, column_name):
        if column_name in self.translator:
            return self.translator[column_name]


