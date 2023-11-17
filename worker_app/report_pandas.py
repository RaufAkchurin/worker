from django.http import HttpResponse
from django.views import View
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import NamedStyle
from django.db.models import F, Sum
from .models import Shift, WorkType


class GenerateReportView(View):
    def get(self, request, *args, **kwargs):
        # Извлекаем данные из базы
        work_types = WorkType.objects.annotate(
            сумма=F('total_scope') * F('price_for_worker'),
        ).values(
            'name',
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
            'measurement_type__name': 'ед.изм.',
            'total_scope': 'кол-во',
            'price_for_worker': 'цена',
            'quantity_shift': 'кол-во выполненное',
        })

        # Вычисляем сумму для заказчика на оплату
        merged_df['сумма_заказчика'] = merged_df['кол-во выполненное'] * merged_df['price_for_customer']

        # Группируем данные по названию типа работ и агрегируем значения
        grouped_df = merged_df.groupby('Наименование работ').agg({
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
            grouped_df.to_excel(writer, sheet_name='WorkTypes', index=False)

            # Устанавливаем ширину столбцов
            for column in writer.sheets['WorkTypes'].columns:
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
                writer.sheets['WorkTypes'].column_dimensions[column[0].column_letter].width = adjusted_width

        # Отправляем файл пользователю
        with open(excel_file_path, 'rb') as excel:
            response = HttpResponse(excel.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=report.xlsx'

        return response
