from django.db import models
from db.base_model import BaseModel


class OrderInfo(BaseModel):
    PAY_METHODS = {
        '1': "货到付款",
        '2': "微信支付",
        '3': "支付宝",
        '4': "银联支付",
    }

    PAY_METHODS_ENUM = {
        "CASH": 1,
        "ALIPAY": 2,
    }

    ORDER_STATUS = {
        1: "待支付",
        2: "待发货",
        3: "待收货",
        4: "待评价",
        5: "已完成",
    }

    PAY_METHOD_CHOICES = (
        (1, '货到付款'),
        (2, '微信支付'),
        (3, '支付宝'),
        (4, '银联支付'),
    )

    ORDER_STATUS_CHOICES = (
        (1, '待支付'),
        (2, '待发货'),
        (3, '待收货'),
        (4, '待评价'),
        (5, '已完成'),
    )

    order_id = models.CharField(max_length=128, primary_key=True, verbose_name='订单ID')
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, verbose_name='用户')
    addr = models.ForeignKey('user.Address', on_delete=models.CASCADE, verbose_name='地址')
    pay_method = models.SmallIntegerField(choices=PAY_METHOD_CHOICES, default=3, verbose_name='支付方式')
    totle_count = models.IntegerField(default=1, verbose_name='商品数量')
    totle_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='总金额')
    transit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='运费')
    order_status = models.SmallIntegerField(choices=ORDER_STATUS_CHOICES, default=1, verbose_name='订单状态')
    trade_no = models.CharField(max_length=100, default='', verbose_name='支付编号')

    class Meta:
        db_table = 'df_order_info'
        verbose_name = '订单'
        verbose_name_plural = verbose_name


class OrderGoods(BaseModel):
    order = models.ForeignKey("OrderInfo", on_delete=models.CASCADE, verbose_name='订单')
    sku = models.ForeignKey('goods.GoodSKU', on_delete=models.CASCADE, verbose_name='商品SKU')
    count = models.IntegerField(default=1, verbose_name='商品数量')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='价格')
    comment = models.CharField(max_length=256, default='', verbose_name='评价')

    class Meta:
        db_table = 'df_order_goods'
        verbose_name = '订单商品'
        verbose_name_plural = verbose_name
