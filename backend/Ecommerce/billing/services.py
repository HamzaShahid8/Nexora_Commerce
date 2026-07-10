from .models import *


class InvoiceService:

    @staticmethod
    def create_invoice(validated_data):

        items = validated_data.pop("invoice_items")

        order = validated_data["order"]
        coupon = validated_data.get('coupon')

        invoice = Invoice.objects.create(
            user=order.user,
            coupon=coupon,
            **validated_data
        )

        for item in items:
            InvoiceItem.objects.create(
                invoice=invoice,
                product=item["product"],
                quantity=item["quantity"],
                price=item["product"].price,
            )

        invoice.calculate_totals()

        return invoice

    @staticmethod
    def update_invoice(instance, validated_data):

        items = validated_data.pop("invoice_items", None)

        order = validated_data.get("order", instance.order)

        instance.user = order.user
        instance.order = order
        instance.payment = validated_data.get(
            "payment",
            instance.payment,
        )
        instance.coupon = validated_data.get(
            "coupon",
            instance.coupon,
        )
        instance.invoice_number = validated_data.get(
            "invoice_number",
            instance.invoice_number,
        )

        instance.save()

        if items is not None:

            instance.invoice_items.all().delete()

            for item in items:
                InvoiceItem.objects.create(
                    invoice=instance,
                    product=item["product"],
                    quantity=item["quantity"],
                    price=item["product"].price,
                )

        instance.calculate_totals()

        return instance

    @staticmethod
    def delete_invoice(instance):

        instance.delete()

        return True