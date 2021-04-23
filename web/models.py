from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils import timezone

User = get_user_model()

class Category(models.Model):
    
    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    name = models.CharField(max_length=200, verbose_name='Название')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):

    class Meta:
        abstract = True

    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE)
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=250, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Цена')
    image = models.ImageField(verbose_name='Изображение')

    def __str__(self):
        return self.title


class Notebook(Product):

    class Meta:
        verbose_name = 'ноутбук' 
        verbose_name_plural = 'Ноутбуки'

    diagonal = models.CharField(max_length=250, verbose_name='Диагональ')
    display_type = models.CharField(max_length=250, verbose_name='Тип дисплея')
    ram = models.CharField(max_length=250, verbose_name='Оперативная память')
    processor_freq = models.CharField(max_length=250, verbose_name='Частота процессора')
    video = models.CharField(max_length=250, verbose_name='Видеокарта')
    time_without_charge = models.CharField(max_length=250, verbose_name='Время работы аккумулятора')
    os = models.CharField(max_length=250, verbose_name='Операционная система')


class Smartphone(Product):
    
    class Meta:
        verbose_name = 'смартфон' 
        verbose_name_plural = 'Смартфоны'
    
    diagonal = models.CharField(max_length=250, verbose_name='Диагональ')
    display_type = models.CharField(max_length=250, verbose_name='Тип дисплея')
    resolution = models.CharField(max_length=250, verbose_name='Разрешение экрана')
    
    ram = models.CharField(max_length=250, verbose_name='Оперативная память')
    accum_volume = models.CharField(max_length=250, verbose_name='Объем батареи')

    sd = models.BooleanField(default=False, verbose_name='SD карта')
    sd_volume = models.CharField(max_length=250, verbose_name='Максимальный объём sd карты', null=True, blank=True)

    main_cam = models.CharField(max_length=250, verbose_name='Задняя камера')
    frontal_cam = models.CharField(max_length=250, verbose_name='Фронтальная камера')


class Cart(models.Model):

    class Meta:
        verbose_name = 'корзина'
        verbose_name_plural = 'Корзины'

    owner = models.ForeignKey('Customer', verbose_name='Владелец', on_delete=models.CASCADE, null=True, blank=True)
    products = models.ManyToManyField('CartProduct', blank=True, related_name='products')
    total_products = models.PositiveIntegerField(default=0)
    
    in_order = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False)
    
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Общая цена', default=0)

    
    def __str__(self):
        return 'Корзина №' + str(self.id)


class CartProduct(models.Model):

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'Продукты корзин'

    user = models.ForeignKey('Customer', verbose_name='Покупатель', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name='Корзина', on_delete=models.CASCADE)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    quantity = models.PositiveIntegerField(default=1)

    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Общая цена', default=0)

    def __str__(self):
        return 'Продукт %s из корзины %d' % (self.content_object.title, self.cart.id)


class Customer(models.Model):
    
    class Meta:
        verbose_name = 'покупатель'
        verbose_name_plural = 'Покупатели'

    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, verbose_name='Номер телефона', null=True, blank=True)
    address = models.CharField(max_length=250, verbose_name='Адрес', null=True, blank=True)
    orders = models.ManyToManyField('Order', verbose_name='Заказы пользователя', related_name='orders', null=True, blank=True)

    def __str__(self):
        return 'Покупатель %s %s' % (self.user.first_name, self.user.last_name)


class Order(models.Model):

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'Заказы'

    STATUS_DEFAULT = 'new'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_READY = 'ready'
    STATUS_COMPLETED = 'completed'

    STATUS_CHOICES = (
        (STATUS_DEFAULT, 'Новый'),
        (STATUS_IN_PROGRESS, 'В обработке'), 
        (STATUS_READY, 'Готов'),
        (STATUS_COMPLETED, 'Выполнен'),
    )

    DELIVERY_TYPE_DEFAULT = 'self'
    DELIVERY_TYPE_DELIVERY = 'delivery'

    DELIVERY_TYPE_CHOICES = (
        (DELIVERY_TYPE_DEFAULT, 'Самовывоз'), 
        (DELIVERY_TYPE_DELIVERY, 'Доставка'), 
    )

    customer = models.ForeignKey('Customer', verbose_name='Покупатель', on_delete=models.CASCADE)
    
    first_name = models.CharField(max_length=30, verbose_name='Имя покупателя')
    last_name = models.CharField(max_length=30, verbose_name='Фамилия покупателя')
    phone = models.CharField(max_length=20, verbose_name='Номер телефона', null=True, blank=True)
    address = models.CharField(max_length=255, verbose_name='Адрес', null=True, blank=True)

    cart = models.ForeignKey('Cart', verbose_name='Корзина', on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=100, verbose_name='Статус заказа', choices=STATUS_CHOICES, default=STATUS_DEFAULT)
    delivery_type = models.CharField(max_length=100, verbose_name='Тип доставки', choices=DELIVERY_TYPE_CHOICES, default=DELIVERY_TYPE_DEFAULT)

    created_at = models.DateTimeField(auto_now=True, verbose_name='Дата создания')
    order_date = models.DateField(default=timezone.now, verbose_name='Дата получения заказа')

    def __str__(self):
        return 'Заказ №%d' % (self.id)