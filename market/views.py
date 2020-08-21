from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from .models import Item, Order, OrderItem, Address, Coupon, Refund, Payment
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.utils import timezone
from .forms import CheckoutForm, PaymentForm
from users.models import UserProfile
from django.contrib.auth.models import User


"""def Home(request):
    context={
        "item":Item.objects.all()
    }
    return render(request, "market/home.html", context)"""


"""class Home(ListView):
    model = Item
    paginate_by = 6
    template_name = "market/home.html"
    context_object_name = "item"

"""


class MarketListView(ListView):
    model = Item
    context_object_name = "item"
    template_name = "market/home.html"


class ProductListView(ListView):
    model = Item
    context_object_name = "item"
    template_name = "market/product.html"


class MarketDetailView(DetailView):
    model = Item
    context_object_name = "item"
    template_name = "market/detail1.html"


class MarketCreateView(LoginRequiredMixin, CreateView):
    model = Item
    fields = ["title", "description", "price",
              "discount_price", "label", "image", "sizes"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class MarketUpdateView(LoginRequiredMixin, UpdateView):
    model = Item
    fields = ["title", "description", "price",
              "discount_price", "label", "image", "sizes"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class MarketDeleteView(DeleteView):
    model = Item
    success_url = "/"


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                "object": order
            }
            messages.info(self.request, "Your order is being processed")
            return render(self.request, "market/order_summary.html", context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You have no active order")
            return redirect("/")


def add_to_cart(request, pk):
    item = get_object_or_404(Item, pk=pk)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item_id=item.pk).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, f"Your order has been updated")
            return redirect("order-summary")
        else:
            order.items.add(order_item)
            messages.info(request, f"An item was added to your order")
            return redirect("order-summary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, f"An item was added to your order")
        return redirect("order-summary")


def remove_single_item_cart(request, pk):
    item = get_object_or_404(Item, pk=pk)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item_id=item.pk).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
                messages.info(request, f"Your order has been updated")
                return redirect("order-summary")
            else:
                order.items.remove(order_item)
                messages.info(request, f"Your order has been updated")
                return redirect("order-summary")
        else:
            messages.info(request, f"You do not have a valid order")
            return redirect("order-summary")
    else:
        messages.info(request, f"You do not have a valid order")
        return redirect("order-summary")


def remove_from_cart(request, pk):
    item = get_object_or_404(Item, pk=pk)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item_id=item.pk).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, f"Your order has been updated")
            return redirect("/order-summary/")
        else:
            messages.info(request, f"Your order has been updated")
            return redirect("/order-summary/")
    else:
        messages.info(request, f"You do not have a valid order")
        return redirect("/order-summary/")


class CheckoutView(View):
    def get(self, *args, **kwargs):
        try:
            form = CheckoutForm()
            order = Order.objects.get(
                user=self.request.user,
                ordered=False
            )
            context = {
                "order": order,
                "form": form
            }
            shipping_address_qs = Address.objects.filter(
                user=self.request.user,
                address_type="S",
                default=True
            )
            if shipping_address_qs.exists():
                context.update({
                    "default_shipping_address": shipping_address_qs[0]
                })
            billing_address_qs = Address.objects.filter(
                user=self.request.user,
                address_type="B",
                default=True
            )
            if billing_address_qs.exists():
                context.update({
                    "default_billing_address": billing_address_qs[0]
                })
            return render(self.request, "market/checkout.html", context)
        except ObjectDoesNotExist:
            messages.success(self.request, f"carkes")
            return redirect("/checkout/")

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(
                user=self.request.user,
                ordered=False
            )
            if form.is_valid():
                use_default_shipping = form.cleaned_data.get(
                    "use_default_shipping")
                if use_default_shipping:
                    address_qs = Address.objects.filter(
                        user=self.request.user,
                        address_type="S",
                        default=True
                    )
                    if address_qs.exists():
                        shipping_address = address_qs[0]
                        order.shipping_address = shipping_address
                        order.save()
                    else:
                        messages.info(
                            self.request, f"No valid shipping_address exist")
                        return redirect("checkoutView")
                else:
                    shipping_address1 = form.cleaned_data.get(
                        "shipping_address1")
                    shipping_address2 = form.cleaned_data.get(
                        "shipping_address2")
                    shipping_country = form.cleaned_data.get(
                        "shipping_country")
                    shipping_zip = form.cleaned_data.get("shipping_zip")
                    if is_valid_form(
                            [shipping_address1, shipping_address2, shipping_country, shipping_zip]):
                        shipping_address = Address(
                            user=self.request.user,
                            home_address=shipping_address1,
                            street_address=shipping_address2,
                            country=shipping_country,
                            zip=shipping_zip,
                            address_type="S"
                        )
                        shipping_address.save()
                        order.shipping_address = shipping_address
                        order.save()

                        set_default_shipping = form.cleaned_data.get(
                            "set_default_shipping")
                        if set_default_shipping:
                            shipping_address.default = True
                            shipping_address.save()

                    else:
                        messages.info(
                            self.request, f"Kindly fill in the forms")

                same_billing_address = form.cleaned_data.get(
                    "same_billing_address")
                use_default_billing = form.cleaned_data.get(
                    "use_default_billing")

                if same_billing_address:
                    shipping_address1 = form.cleaned_data.get(
                        "shipping_address1")
                    shipping_address2 = form.cleaned_data.get(
                        "shipping_address2")
                    shipping_country = form.cleaned_data.get(
                        "shipping_country")
                    shipping_zip = form.cleaned_data.get("shipping_zip")
                    shipping_address = Address(
                        user=self.request.user,
                        home_address=shipping_address1,
                        street_address=shipping_address2,
                        country=shipping_country,
                        zip=shipping_zip,
                        address_type="S"
                    )

                    billing_address = shipping_address
                    billing_address.pk = None
                    billing_address.save()
                    billing_address.address_type = "B"
                    billing_address.save()
                    order.billing_address = billing_address
                    order.save()

                elif use_default_billing:
                    address_qs = Address.objects.filter(
                        user=self.request.user,
                        address_type="S",
                        default=True
                    )
                    if address_qs.exists():
                        billing_address = address_qs[0]
                        order.billing_address = billing_address
                        order.save()
                    else:
                        messages.info(
                            self.request, f"No valid billing_address exist")
                        return redirect("checkoutView")
                else:
                    billing_address1 = form.cleaned_data.get(
                        "billing_address1")
                    billing_address2 = form.cleaned_data.get(
                        "billing_address2")
                    billing_country = form.cleaned_data.get("billing_country")
                    billing_zip = form.cleaned_data.get("billing_zip")
                    if is_valid_form(
                            [billing_address1, billing_address2, billing_country, billing_zip]):
                        billing_address = Address(
                            user=self.request.user,
                            home_address=billing_address1,
                            street_address=billing_address2,
                            country=billing_country,
                            zip=billing_zip,
                            address_type="B"
                        )
                        billing_address.save()
                        order.billing_address = billing_address
                        order.save()

                        set_default_billing = form.cleaned_data.get(
                            "set_default_billing")
                        if set_default_billing:
                            billing_address.default = True
                            billing_address.save()

                    else:
                        messages.info(
                            self.request, f"Kindly fill in the forms")

                payment_type = form.cleaned_data.get(
                    "payment_type")
                if payment_type == "S":
                    return redirect("payment", payment_type="stripe")
                elif payment_type == "P":
                    return redirect("payment", payment_type="paypal")
                else:
                    messages.warning(
                        self.request, f"You did not select a valid payment option")
                    return redirect("checkoutView")
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
        return redirect("order-summary")


class Payment(View):
    def get(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        if order.billing_address:
            context = {
                "order": order
            }
            userprofile = self.request.user.userprofile
            if userprofile.one_click_purchasing:
                cards = stripe.Customer.list_sources(
                    userprofile.stripe_customer_id,
                    object="card",
                    limit=3,
                )
                card_list = cards["data"]
                if len(card_list) > 0:
                    context.update({
                        "card": card_list[0]
                    })
            return render(self.request, "market/payment.html", context)
        else:
            messages.success(self.request, f"tttyyyy")
            return redirect("checkoutView")

    def post(self, *args, **kwargs):
        order = Order.objects.get(uses=self.request.user)
        payment = PaymentForm(self.request.POST)
        userprofile = UserProfile.objects.get(user=self.request.user)
        if form.is_valid():
            use_default = form.cleaned_data.get("use_default")
            save = form.cleaned_data.get("save")
            token = form.cleaned_data.get("stripeToken")
            if save:
                if userprofile.stripe_customer_id != "" and userprofile.stripe_customer_id is not None:
                    customer = stripe.Customer.retrieve(
                        userprofile.stripe_customer_id)
                    customer.sources.create(source=token)
                else:
                    customer = stripe.Customer.create(
                        email=user.request.user.email)
                    customer.sources.create(source=token)
                    userprofile.one_click_purchasing = True
                    userprofile.stripe_customer_id = customer["id"]
                    userprofile.save()
            amount = int(order.individual_discount_total()*100)

            try:
                if use_default or save:
                    charge = stripe.Charge.create(
                        amount=amount,
                        currency="usd",
                        customer=userprofile.stripe_customer_id
                    )
                else:
                    charge = stripe.Charge.create(
                        amount=amount,
                        currency="usd",
                        source=token
                    )
                payment = Payment()
                payment.user = self.request.user
                payment.stripe_charge_id = charge["id"]
                payment.amount = order.individual_discount_total()
                payment.save()

                order.ordered = True
                """order.ref_code = get_ref_code()"""
                order.payment = payment
                order.save()

                order_items = order.items.all()
                order_items.update(ordered=True)
                for item in order_items:
                    item.save()

                messages.warning(self.request, f"tttyyyy")
                return redirect("payment")

            except stripe.error.CardError as e:
                messages.warning(self.request, f"many requests made")
                return redirect("/")

            except stripe.error.InvalidRequestError as e:
                messages.warning(self.request, f"Invalid parameters")
                return redirect("/")

            except stripe.error.AuthenticationError as e:
                messages.warning(self.request, f"AuthenticationError")
                return redirect("/")

            except stripe.error.APIConnectionError as e:
                messages.warning(self.request, f"Connection error")
                return redirect("/")

            except stripe.error.StripeError as e:
                messages.warning(
                    self.request, f"StripeError: Issue is being resolved")
                return redirect("/")

            except Exception as e:
                messages.warning(
                    self.request, f"StripeError: Issue is being resolved")
                return redirect("/")
