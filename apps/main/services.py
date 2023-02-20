import io

from xlsxwriter import Workbook

header = ("Выгрузка результатов онлайн голосования проекта 'Новая звезда' за",
          'Тур',
          )
subheader = ('№', 'Фамилия, имя участника', 'Регион', 'количество голосов', '%голосов')


# make header_sheet
def generate_file(*, header: tuple, subheader: tuple, header_value: tuple, subheader_values: list[dict]) -> bytes:
    output: io.BytesIO = io.BytesIO()
    book = Workbook(output)
    sheet = book.add_worksheet()
    sheet.set_column(0, 0, 10)
    sheet.set_column(1, 1, 40)
    sheet.set_column(2, 2, 40)
    sheet.set_column(3, 3, 10)
    sheet.set_column(4, 4, 10)
    sheet.set_row(2, height=30)
    cell_format = book.add_format(
        {
            'bold': True,
            'align': 'center',
            'valign': 'vcenter',
            'border': 5,
            'text_wrap': True,
            'font_name': 'Tahoma',
            'font_size': 10,
        }
    )

    for num, element in enumerate(header):
        sheet.merge_range(
            first_row=num,
            first_col=0,
            last_row=num,
            last_col=3,
            data=element,
            cell_format=cell_format
        )
        sheet.write(num, 4, header_value[num], cell_format)
        sheet.set_row(num, height=20)

    sheet.write_row(len(header), 0, subheader, cell_format)
    for num, element in enumerate(subheader_values, start=len(header) + 1):
        sheet.write_row(num, 0, (num-2, element['name'], element['region'], element['count_votes']), cell_format)
    book.close()
    output.seek(0)
    return output.read()
