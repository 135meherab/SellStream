from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=80)
    slug = models.SlugField()

<<<<<<< HEAD
class Uom(models.Model):
    name = models.CharField(max_length=80)

=======
    def __str__(self):
        return self.name

class Uom(models.Model):
    name = models.CharField(max_length=80)

    def __str__(self):
        return self.name

>>>>>>> c1d3c7f76dd2f2a4d6b3589fccf6c8b88f483f9a
class Customer(models.Model):
    name = models.CharField(max_length=30)
    phone_no = models.IntegerField(max_length=12)

<<<<<<< HEAD
=======
    def __str__(self):
        return self.name

>>>>>>> c1d3c7f76dd2f2a4d6b3589fccf6c8b88f483f9a
class Product(models.Model):
    name = models.CharField(max_length=80)
    description = models.TextField()
    product_code = models.CharField(max_length=30)
    quantity = models.DecimalField(max_digits=4, decimal_places=2)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    uom_name = models.ForeignKey(Uom,on_delete=models.CASCADE)
<<<<<<< HEAD
=======
    
    def __str__(self):
        return self.name
>>>>>>> c1d3c7f76dd2f2a4d6b3589fccf6c8b88f483f9a

class Order(models.Model):
    product_order = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
<<<<<<< HEAD
    date = models.DateTimeField(auto_now=True)
    quantity = models.DecimalField(max_digits=6, decimal_places=2)
    Total = models.DecimalField(max_digits=6, decimal_places=2)

=======
    datetime = models.DateTimeField(auto_now=True)
    quantity = models.DecimalField(max_digits=6, decimal_places=2)
    Total = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.product_order.name

>>>>>>> c1d3c7f76dd2f2a4d6b3589fccf6c8b88f483f9a
# class Order_Details(models.Model):
#     customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)


# class Booking(models.Model):
#     train = models.ForeignKey(Schedule, on_delete=models.CASCADE)
#     user = models.ForeignKey(Passenger, on_delete=models.CASCADE)
#     booked_seat = models.IntegerField()
#     def __str__(self):
#         return f'{self.user.user.first_name} {self.user.user.last_name} {self.train.train} on {self.train.date_of_journey} at {self.train.departure_time} seat no: {self.booked_seat} '

#     def cancel_booking(self):
#         self.delete()


