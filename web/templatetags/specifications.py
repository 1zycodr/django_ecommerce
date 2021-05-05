from django import template
from django.utils.safestring import mark_safe
from web.models import Smartphone

register = template.Library()

TABLE_HEAD = """<table class="table">
    <tbody>"""

TABLE_ITEM = """        <tr>
            <td>{name}</td>
            <td>{value}</td>
        </tr>"""

TABLE_TAIL = """    </tbody>
</table>"""

PRODUCT_SPEC = {
    'notebook': {
        'Диагональ': 'diagonal',
        'Тип дисплея': 'display_type',
        'Оперативная память': 'ram',
        'Частота процессора': 'processor_freq',
        'Видеокарта': 'video',
        'Время работы аккумулятора': 'time_without_charge',
        'Операционная система': 'os'
    },
    'smartphone': {
        'Диагональ': 'diagonal',
        'Тип дисплея': 'display_type',
        'Разрешение экрана': 'resolution',
        'Оперативная память': 'ram',
        'Объем батареи': 'accum_volume',
        'Максимальный объем SD карты': 'sd_volume',
        'Задняя камера': 'main_cam',
        'Передняя камера': 'frontal_cam' 
    }
}

@register.filter
def product_specifications(product):
    model_name = product.__class__._meta.model_name

    if isinstance(product, Smartphone):
        if not product.sd:
            PRODUCT_SPEC[model_name].pop('Максимальный объем SD карты', None)
        else:
            PRODUCT_SPEC[model_name]['Максимальный объем SD карты'] = 'sd_volume'

    table_content = ''

    for name, value in PRODUCT_SPEC[model_name].items():
        table_content += TABLE_ITEM.format(name=name, value=getattr(product, value))

    return mark_safe(TABLE_HEAD + table_content + TABLE_TAIL)