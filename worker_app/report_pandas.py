from django.http import HttpResponse
from django.views import View
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import NamedStyle, Alignment, PatternFill
from django.db.models import F, Sum
from .models import Shift, WorkType


class GenerateReportView(View):
    def get(self, request, *args, **kwargs):
        # Извлекаем данные из базы
        work_types = WorkType.objects.annotate(
            сумма=F('total_scope') * F('price_for_worker'),
        ).values(
            'name',
            'category__name',  # Include the category name for grouping
            'measurement_type__name',
            'total_scope',
            'price_for_worker',
            'сумма',
        )

        # Преобразуем queryset в DataFrame
        df = pd.DataFrame(list(work_types))

        # Получаем данные из модели Shift и объединяем их с DataFrame
        shift_df = Shift.objects.values(
            work_type_name=F('work_type__name'),
            category_name=F('work_type__category__name'),  # Include the category name for grouping
            quantity_shift=F('value'),
            price_for_customer=F('work_type__price_for_customer'),
        )

        # Преобразуем queryset в DataFrame
        shift_df = pd.DataFrame(list(shift_df))

        # Объединяем DataFrames
        merged_df = pd.merge(df, shift_df, how='left', left_on='name', right_on='work_type_name')

        # Rename columns after the merge
        merged_df = merged_df.rename(columns={
            'name': 'Наименование работ',
            'category__name': 'Категория',  # Rename the category column
            'measurement_type__name': 'ед.изм.',
            'total_scope': 'кол-во',
            'price_for_worker': 'цена',
            'quantity_shift': 'кол-во выполненное',
        })

        # Вычисляем сумму для заказчика на оплату
        merged_df['сумма_заказчика'] = merged_df['кол-во выполненное'] * merged_df['price_for_customer']

        # Группируем данные по категории и типу работ, агрегируем значения
        grouped_df = merged_df.groupby(['Категория', 'Наименование работ']).agg({
            'ед.изм.': 'first',
            'кол-во': 'sum',
            'цена': 'first',
            'сумма': 'sum',
            'кол-во выполненное': 'sum',
            'сумма_заказчика': 'sum',
        }).reset_index()

        # Создаем Excel-файл
        excel_file_path = 'report.xlsx'
        with pd.ExcelWriter(excel_file_path, engine='openpyxl') as writer:
            # Create an empty 'WorkTypes' sheet
            writer.book.create_sheet('WorkTypes')

            for category, category_df in grouped_df.groupby('Категория'):
                # Write category name row for each category
                category_row = pd.DataFrame({'Наименование работ': [f'Категория: {category}'], 'Категория': ['']})
                writer.sheets['WorkTypes'].append(list(category_row.iloc[0]), )

                # Merge cells, make text bold, center alignment, and yellow background for the category name
                for cell in list(writer.sheets['WorkTypes'].rows)[-1]:
                    cell.alignment = Alignment(horizontal='center', vertical='center')
                    cell.font = NamedStyle(name='Bold').font.__class__(bold=True)
                    cell.fill = PatternFill(start_color='FFFF00', end_color='FFFF00', fill_type='solid')

                # Write data for each category
                category_df.to_excel(writer, sheet_name='WorkTypes', index=False,
                                     startrow=writer.sheets['WorkTypes'].max_row)

            # Устанавливаем ширину столбцов для каждого листа
            for sheet_name in writer.sheets.keys():
                for column in writer.sheets[sheet_name].columns:
                    max_length = 0
                    column = [column[0]] + [str(i) for i in column[1:]]
                    for cell in column:
                        try:
                            if len(str(cell)) > max_length:
                                max_length = len(cell)
                        except:
                            pass
                    adjusted_width = (max_length + 2)

                    # Применяем ширину столбца к листу Excel
                    writer.sheets[sheet_name].column_dimensions[column[0].column_letter].width = adjusted_width

        # Отправляем файл пользователю
        with open(excel_file_path, 'rb') as excel:
            response = HttpResponse(excel.read(),
                                    content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=report.xlsx'

        return response
