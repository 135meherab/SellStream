from rest_framework import serializers
from product.models import Product, Order, Refund, Category, Customer
from shop.models import Shop, Branch
from employee.models import EmployeeModel
from django.db.models import Sum, Count, F


class AnalysisReportSerializer(serializers.Serializer):
      total_products = serializers.IntegerField()
      total_categories = serializers.IntegerField()
      total_orders = serializers.IntegerField()
      # total_refunds = serializers.IntegerField()
      total_customers = serializers.IntegerField()
      total_sales = serializers.DecimalField(max_digits=10, decimal_places=2)
      # total_profit = serializers.DecimalField(max_digits=10, decimal_places=2)
      total_employees = serializers.IntegerField()
      
      
      @classmethod
      def get_shop_report(cls, shop):
            branches = shop.branches.all()
            total_products = Product.objects.filter(branch__in = branches).count()
            total_categories = Category.objects.filter(shop = shop).count()
            total_orders = Order.objects.filter(branch__in = branches).count()
            total_sales_result = Order.objects.filter(branch__in=branches) \
                                  .aggregate(total_sales=Sum('total_price'))
            total_sales = total_sales_result['total_sales'] if total_sales_result['total_sales'] is not None else 0
            total_customers = Customer.objects.filter(shop = shop).count()
            total_employees = EmployeeModel.objects.filter(branch__in = branches).count()
            
      
            return cls({
                  'total_products': total_products,
                  'total_categories': total_categories,
                  'total_orders': total_orders,
                  'total_sales': total_sales,
                  'total_customers': total_customers,
                  'total_employees': total_employees,
            })
            
      
      @classmethod
      def get_branch_report(cls, branch):
            total_products = Product.objects.filter(branch = branch).count()
            total_categories = Category.objects.filter(shop = branch.shop).count()
            total_orders = Order.objects.filter(branch = branch).count()
            # total_sales = Order.objects.filter(branch = branch)\
            #       .aggregate(total_sales = Sum('total_price'))['total_price'] or 0
            total_sales_result = Order.objects.filter(branch = branch) \
                                  .aggregate(total_sales=Sum('total_price'))
            total_sales = total_sales_result['total_sales'] if total_sales_result['total_sales'] is not None else 0
            total_customers = Customer.objects.filter(id__in = Order.objects.filter(branch = branch)\
                  .values('customer_id')).distinct().count()
            total_employee = EmployeeModel.objects.filter(branch = branch).count()
            
            
      
            return cls({
                  'total_products': total_products,
                  'total_categories': total_categories,
                  'total_orders': total_orders,
                  'total_sales': total_sales,
                  'total_customers': total_customers,
                  'total_employees': total_employee,
            })
            
            
