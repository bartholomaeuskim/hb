import xlrd
import os.path
import sqlite3, sys, datetime

class InputExcel:
    def __init__(self, filename):
        self.filename = filename
        self.header = []

    def data_input(self):
        conn = sqlite3.connect('hb.db')
        c = conn.cursor()
        wb = xlrd.open_workbook(self.filename)
        ws = wb.sheet_by_index(0)
        self.header = ws.row_values(0)
        query = self.make_query()
        value = []
        for i in range(1, ws.nrows):
            pointer = 0
            temp_list = []
            for data in ws.row_values(i):
                if self.header[pointer].find("date") is -1:
                    if type(data) is float:
                        temp_list.append(str(int(data)))
                    else:
                        temp_list.append(str(data))
                else:
                    temp_list.append(datetime.datetime(*xlrd.xldate_as_tuple(data, wb.datemode)).isoformat())
                pointer += 1
            value.append(tuple(temp_list))
        c.executemany(query, value)
        conn.commit()
        conn.close()

    def make_query(self):
        query = '''INSERT INTO vehicle('''
        for a in self.header:
            query = query+a+''', '''
        query = query[:len(query)-2]+''') values('''
        for i in range(len(self.header)):
            query += '''?, '''
        query = query[:len(query)-2]+''')'''
        return query


if __name__ == "__main__":
    if len(sys.argv) is 1:
        print("Please input an excel filename (Usage: python input_from_excel.py test.xlsx)")
    elif not os.path.isfile(sys.argv[1]):
        print(sys.argv[1],"does not exist.")
    else:
        exe = InputExcel(sys.argv[1])
        exe.data_input()
