import csv
from django import forms

class UploadFileForm(forms.Form):
    title = forms.CharField()
    file = forms.FileField()


class Transformer():
    def __init__(self, file, translator: dict):
        self.new_entry = []
        self.fieldnames = list(translator.keys())
        self.translator = translator
        self.file = file
        self.record = self.generate_record()
        
    
    def generate_record(self):
        record = self.file
        reader = csv.DictReader(record.splitlines())
        record_list = []
        for line in reader:
            
            entry = dict([(fieldname, line[self.translator[fieldname]]) for fieldname in self.fieldnames])
            record_list.append(entry)
        return record_list



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


