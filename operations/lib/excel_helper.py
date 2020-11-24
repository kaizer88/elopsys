# -*- coding: utf-8 -*-

import xlrd, xlwt
import cStringIO
import datetime
import time

import logging
logger = logging.getLogger(__name__)

TICK='R'
NOTICK='£'

class ExcelHelper(object):
    def __init__(self, f=None, content=None, sheet_number=0, sheet_name=None, write=False):
        """ different arguments are required depending on the value of 'write' """
        super(ExcelHelper, self).__init__()
        if write:
            self._open_for_write(sheet_name)
        else:
            if sheet_name:
                self._open_for_read(f, content, sheet_name)
            else:
                self._open_for_read(f, content, sheet_number)

    def add_sheet(self, name, sheet_number):
        self.sheet = self.wb.add_sheet(name)
        self.sheet_number  = sheet_number
        self.x = 0
        self.y = 0

    def _open_for_read(self, f, content, sheet):

        if content:
            self.wb = xlrd.open_workbook(file_contents=content)
        else:
            self.wb = xlrd.open_workbook(f)
        if isinstance(sheet, basestring):
            self._goto_sheet(sheet_name=sheet)
        else:
            self._goto_sheet(int(sheet))

    def _open_for_write(self, sheet_name):
        self.wb = xlwt.Workbook(encoding='utf-8')
        self.sheet = self.wb.add_sheet(sheet_name) 
        self.sheet_number = 0
        self.x = 1
        self.y = 0
        self.tick_style = xlwt.easyxf('font: name Wingdings 2')
        self.date_style = xlwt.XFStyle()
        self.date_style.num_format_str = 'M/D/YY h:mm'
        self.bold_style = xlwt.easyxf('font: bold on')

    def _goto_sheet(self, index=0, sheet_name=None):
        try:
            if sheet_name is None:
                self.sheet_number = index-1
                self.sheet = self.wb.sheets()[self.sheet_number]
            else:
                self.sheet = self.wb.sheet_by_name(sheet_name)
                self.sheet_number = self.wb.sheet_names().index(sheet_name)
        except IndexError:
            raise Exception("No sheet at position %d" % index)

    @classmethod
    def _excel_unicode(self, val):
        if type(val) == float:
            if int(val) == val:
                return unicode(int(val))
        return unicode(val)

    def write_row(self, row, style=None):
        for y,d in enumerate(row):
            if type(d) == bool:
                d=TICK if d else NOTICK
                self.sheet.write(self.x, self.y+y, d, self.tick_style)
            elif type(d) == datetime.datetime:
                self.sheet.write(self.x, self.y+y, d, self.date_style)
            elif style:
                self.sheet.write(self.x, self.y+y, d, style)
            else:
                self.sheet.write(self.x, self.y+y, d)
        self.x += 1

    def write_merge(self, merge_row_from, merge_row_to, value):
        style = xlwt.XFStyle()
        font = xlwt.Font()
        font.bold = True
        style.font = font
        style.alignment.horz = style.alignment.HORZ_CENTER
        self.write(value=value, merge=[merge_row_from, merge_row_to], style=style)
        

    def write(self, value, x_offset=0, y_offset=0, style=None, merge=None):
        x = self.x + x_offset
        y = self.y + y_offset
        
        if merge:
            self.sheet.write_merge(0,0,merge[0],merge[1],value, style) 
        elif style:
            self.sheet.write(x, y, value, style)
        elif type(value) == bool:
            value=TICK if d else NOTICK
            self.sheet.write(x, y, value, self.tick_style)
        elif type(value) == datetime.datetime:
            self.sheet.write(x, y, value, self.date_style)
        elif type(value) == datetime.date:
            self.sheet.write(x, y, time.strftime('%Y-%m-%d', value.timetuple()))
        else:
            self.sheet.write(x, y, value)

    def read(self, row=None, column=None, as_date=False):
        row = self.x if row is None else row - 1
        column = self.y if column is None else column - 1
        if as_date:
            value = int(self._excel_unicode(self.sheet.cell_value(row, column)).strip())
            struct = xlrd.xldate_as_tuple(value, self.wb.datemode)
            return datetime.datetime(*struct)
        else:
            return self._excel_unicode(self.sheet.cell_value(row, column)).strip()

    def save(self):
        f = cStringIO.StringIO()
        self.wb.save(f)
        f.seek(0)
        return f

    def read_row(self, row, date_cols=[]):
        row  = row - 1
        values = []
        for col in range(self.sheet.ncols):
            cell_value = self.sheet.cell_value(row,col)
            try:
                
                if col in date_cols and cell_value:
                    values.append(xlrd.xldate_as_tuple(self.sheet.cell_value(row,col), self.wb.datemode))
                else:
                    values.append(self._excel_unicode(cell_value).strip())
            except IndexError:
                break
        return values

    def read_header(self, hearder_row=0):
        return [ v.lower() for v in self.read_row(hearder_row) ]

    def read_double_line_header(self, main_header_row=0, sub_header_row=1):
        headings_0_raw = self.read_row(main_header_row)
        prev = ''
        headings_0 = []
        headings_1 = self.read_row(sub_header_row)

        headings = [ "%s%s" % (x.lower(),y.lower()) for x,y in zip(headings_0_raw, headings_1) ]
        return headings

    def map_header_to_original(self):
        double_line_header = self.read_header()
        original = self.read_row(0)
        return dict( zip(double_line_header, original) )
        
    def set_cols_width(self, widths):
        for i,w in enumerate(widths):
            self.sheet.col(i).width = w

    @property
    def stats(self):
        return { 'sheet_name': [self.sheet.name, 'Sheet name'] }

    @property
    def nrows(self):
        return self.sheet.nrows

    @property
    def ncols(self):
        return self.sheet.ncols

    @classmethod
    def as_bool(self, value):
        return value==TICK or value=='R' or value.upper()=='X' # 'R' is the checkbox wingding, X is just the letter X
    
    
