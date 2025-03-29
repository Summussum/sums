import csv, json
from datetime import datetime
from django import forms
from dateutil.parser import parse

class UploadFileForm(forms.Form):
    title = forms.CharField()
    file = forms.FileField()


class Transformer():
    def __init__(self, file, translator: dict, date_format: str):
        self.new_entry = []
        self.fieldnames = list(json.loads(translator).keys())
        self.translator = json.loads(translator)
        self.file = file
        self.record = self.generate_record()
        self.date_format = date_format
        self.format_dates()
        self.format_amounts()
        
    
    def generate_record(self):
        record = self.file
        reader = csv.DictReader(record.splitlines())
        record_list = []
        for line in reader:
            
            entry = dict([(fieldname, line[self.translator[fieldname]]) for fieldname in self.fieldnames])
            record_list.append(entry)
        return record_list
    
    def format_dates(self):
        if self.date_format == "automatic":
            for line in self.record:
                line["transaction_date"] = parse(line["transaction_date"]).isoformat()[:10]
        else:
            for line in self.record:
                line["transaction_date"] = datetime.strptime(line["transaction_date"], self.date_format).isoformat()[:10]

    def format_amounts(self):
        if "deposits" in self.fieldnames:
            for line in self.record:
                line["amount"] = -abs(float(line["amount"].replace(",", "")))
                line["amount"] += abs(float(line["deposits"].replace(",", "")))


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


