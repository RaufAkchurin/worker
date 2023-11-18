from django.http import HttpResponse
from django.views import View
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import NamedStyle, Alignment, PatternFill
from django.db.models import F, Sum
from openpyxl.utils import get_column_letter
from rest_framework import status
from rest_framework.response import Response

from .models import Shift, WorkType, Object


class GenerateReportView(View):
    def get(self, request, *args, **kwargs):
        # Извлекаем данные из базы
        object_id = kwargs.get("object_id", None)
        object = Object.objects.filter(id=object_id).first()
        work_types = WorkType.objects.filter(category__object=object)

        if not work_types.count():
            return HttpResponse({'WorkType for this object not found'}, status=status.HTTP_404_NOT_FOUND)

        work_types = work_types.annotate(
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
            # Создаем пустой лист 'WorkTypes'
            writer.book.create_sheet('WorkTypes')

            # Записываем название объекта в первую строку и объединяем первые шесть ячеек
            object_name_row = pd.DataFrame({'Наименование объекта': [object.name] + [''] * 5})
            writer.sheets['WorkTypes'].append(list(object_name_row.iloc[0]), )

            # Устанавливаем высоту строки
            start_row = writer.sheets['WorkTypes'].max_row
            writer.sheets['WorkTypes'].row_dimensions[
                start_row].height = 30  # Например, устанавливаем высоту в 30 пунктов

            # Объединяем первые шесть ячеек в первой строке
            start_col = 1
            end_col = 8
            end_row = start_row
            writer.sheets['WorkTypes'].merge_cells(start_row=start_row, start_column=start_col, end_row=end_row,
                                                   end_column=end_col)

            # Устанавливаем выравнивание для объединенных ячеек
            merged_cells = writer.sheets['WorkTypes'].cell(row=start_row, column=start_col)
            merged_cells.alignment = Alignment(horizontal='center', vertical='center')

            # Продолжаем существующий цикл для записи данных категорий
            for category, category_df in grouped_df.groupby('Категория'):

                # Записываем название категории в каждую строку
                category_row = pd.DataFrame({'Наименование работ': [f'Категория: {category}'], 'Категория': ['']})
                writer.sheets['WorkTypes'].append(list(category_row.iloc[0]), )

                # Объединяем ячейки, делаем текст жирным, центрируем, устанавливаем желтый фон для названия категории
                for cell in list(writer.sheets['WorkTypes'].rows)[-1]:
                    cell.alignment = Alignment(horizontal='center', vertical='center')
                    cell.font = NamedStyle(name='Bold').font.__class__(bold=True)
                    cell.fill = PatternFill(start_color='FFFF00', end_color='FFFF00', fill_type='solid')

                # Записываем данные для каждой категории
                category_df.to_excel(writer, sheet_name='WorkTypes', index=False,
                                     startrow=writer.sheets['WorkTypes'].max_row)

            # Устанавливаем ширину для объединенных ячеек
            for col in range(start_col, end_col + 1):
                col_letter = get_column_letter(col)
                writer.sheets['WorkTypes'].column_dimensions[col_letter].width = 15

        # Отправляем файл пользователю
        with open(excel_file_path, 'rb') as excel:
            response = HttpResponse(excel.read(),
                                    content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=report.xlsx'

        return response
