import io
import typing

import unicodedata
import string

from transliterate import translit
from xlsxwriter import Workbook

valid_filename_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
char_limit = 255


def clean_filename(filename: str, whitelist: str = valid_filename_chars, replace=' ') -> str:
    # translit
    filename = translit(filename, "ru", reversed=True)
    # replace spaces
    for r in replace:
        filename = filename.replace(r, '_')

    # keep only valid ascii chars
    cleaned_filename = unicodedata.normalize('NFKD', filename).encode('ASCII', 'ignore').decode()

    # keep only whitelisted chars
    cleaned_filename = ''.join(c for c in cleaned_filename if c in whitelist)
    if len(cleaned_filename) > char_limit:
        print(
            "Warning, filename truncated because it was over {}. Filenames may no longer be unique".format(char_limit))
    return cleaned_filename[:char_limit]


def generate_xlsx(
        *,
        name: typing.Union[str, None] = None,
        header: typing.Union[list, None] = None,
        values: typing.Union[list, None] = None
) -> bytes:
    extra_row = 0
    column = 0
    output: io.BytesIO = io.BytesIO()
    book = Workbook(output)
    sheet = book.add_worksheet(name=name)
    cell_format_header = book.add_format(
        {
            'bold': False,
            'align': 'center',
            'valign': 'vcenter',
            'border': 1,
            'text_wrap': True,
            'font_name': 'Tahoma',
            'font_size': 13,
        }
    )
    cell_format = book.add_format(
        {
            'bold': False,
            'align': 'left',
            'valign': 'vcenter',
            'border': 1,
            'text_wrap': True,
            'font_name': 'Tahoma',
            'font_size': 12,
        }
    )
    if header:
        for index, value in enumerate(header):
            sheet.write(extra_row, index, value, cell_format_header)
        extra_row += 1
    for row, line in enumerate(start=extra_row, iterable=values):
        for column, value in enumerate(line):
            sheet.write(row, column, value, cell_format)
    for index, column in enumerate(zip(*values, header)):
        column_width = max(len(str(cell_value)) for cell_value in column)
        sheet.set_column(index, index, column_width)
    book.close()
    output.seek(0)
    return output.read()
