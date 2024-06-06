from rest_framework import decorators, response
from product.models import Product
from django.http import JsonResponse
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
# import matplotlib.pyplot as plt

# Import for DB analysis
from django.db.models import Sum

# importing tables
from product.models import Order, Category

# Create your views here.
def get_start_date(time_range):
      now = datetime.now()
      
      if time_range == 'today':
            return now.replace(hour=0, minute=0, second=0, microsecond=0)
      elif time_range == 'yesterday':
            return now - timedelta(days=1)
      elif time_range == 'last_week':
            return now - timedelta(days=now.weekday() + 7)
      elif time_range == 'last_year':
            return now.replace(year=now.year - 1, month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
      else:
            return now - timedelta(days=30)


# Category report
@decorators.api_view(['GET'])
def sales_by_category(request):
      # get the start date
      time_range = request.GET.get('time_range', 'last_month')
      start_date = get_start_date(time_range)
      
      # sales data from order based on category
      orders = Order.objects.filter(order_date__gte = start_date)\
            .values('products__category', 'total_price')
            
      # Convert for easier manipulation
      df = pd.DataFrame(list(orders))
      
      if df.empty:
            return JsonResponse({'message': 'No data available for the given time range'}, status = 404)
      
      # Group by
      category_sales = df.groupby('products__category')['total_price'].sum().reset_index()
      print(category_sales)
      
      # get category names
      category_sales['products__category'] = category_sales['products__category']\
            .apply(lambda x: Category.objects.get(id = x).name)
            
      # Prepare data for the front end
      data = {
            'categories': category_sales['products__category'].tolist(),
            'total_sales': category_sales['total_price'].tolist(),
      }
      
      return JsonResponse(data, status = 200)
      


# Inventory Turnover Rate
# @decorators.api_view(['GET'])
# def inventory_turnover_rate(request):
#       # get the start date



# inventory report
@decorators.api_view(['GET'])
def inventory_report(request):
      time_range = request.GET.get('time_range', 'last_month')
      start_date = get_start_date(time_range)
      
      try:
            # Calculate total quantity sold for each product
            products_sold = Order.objects.filter(
                  order_date__gte = start_date
            ).values('products').annotate(total_sold = Sum('products__quantity'))  #use annotate to use extra field
            
            # total sold for each product
            product_sales = {
                  product['products']: product['total_sold'] for product in products_sold
            }
            
            # get all products and annotate with sales data
            products = Product.objects.all()
            analysis_data = []
            
            out_of_stock_count = 0
            slow_turnover_count = 0
            high_turnover_count = 0
            category_sales = {}
            
            for product in products:
                  total_sold = product_sales.get(product.id, 0)
                  inventory_turnover_rate = total_sold / (product.quantity + total_sold) if product.quantity + total_sold > 0 else 0
                  
                  # getting data for the inventory analysis
                  is_out_of_stock = product.quantity == 0
                  is_slow_moving = inventory_turnover_rate < 0.1
                  is_high_turnover = inventory_turnover_rate > 0.7
                  
                  if is_out_of_stock:
                        out_of_stock_count += 1
                  if is_slow_moving:
                        slow_turnover_count += 1
                  if is_high_turnover:
                        high_turnover_count += 1
                        
                  # Accumulate sales data for each category
                  category_sales[product.category.id] = category_sales.get(product.category.id, 0) + total_sold
                  
                  
                  analysis_data.append({
                        'product_code': product.product_code,
                        'name': product.name,
                        'category': product.category.name,
                        'quantity': product.quantity,
                        'total_sold': total_sold,
                        'inventory_turnover_rate': inventory_turnover_rate,
                        'is_slow_moving': inventory_turnover_rate < 0.1,
                        'is_out_of_stock': product.quantity == 0,
                  })

                  
            # Sort products by turnover rate
            analysis_data.sort(key = lambda x: x['inventory_turnover_rate'], reverse=True)
            
            # Get top 5 high and slow turnover products
            top_5_high_turnover = analysis_data[:5]
            top_5_slow_turnover = analysis_data[-5:]
            
            # Find the category with the highest sales
            highest_sold_category = None
            if category_sales:
                  highest_sold_category = max(category_sales, key = category_sales.get)
                  highest_sold_category = Category.objects.get(id = highest_sold_category).name
            
            
            summary_data = {
                  'highest_sold_category': highest_sold_category if highest_sold_category else None,
                  'out_of_stock_count': out_of_stock_count,
                  'slow_turnover_count': slow_turnover_count,
                  'high_turnover_products': high_turnover_count,
                  'top_5_high_turnover': top_5_high_turnover,
                  'top_5_slow_turnover': top_5_slow_turnover,
            }
                  
            return response.Response({'summary': summary_data}, status=200)
      except Exception as e:
            return response.Response({'error': str(e)}, status=500)


# Function for product report
@decorators.api_view(['GET'])
def product_report(request):
      # Pass the query parameters
      time_range = request.GET.get('time_range', 'last_month')
      start_date = get_start_date(time_range)
      
      try:
            # Calculate the total revenue for each product
            products_revenue = Order.objects.filter(order_date__gte = start_date)\
                  .values('products__id', 'products__name', 'products__category__name')\
                  .annotate(total_revenue = Sum(F('products__selling_price') * F('products__order__products__quantity')))\
                        .order_by('-total_revenue')[:10] or []
                        
            # Calculate the total quantity sold for each product
            products_quantity = Order.objects.filter(order_date__gte = start_date)\
                  .values('products__id', 'products__name', 'products__category__name')\
                  .annotate(total_quantity = Sum('products__order__products__quantity'))\
                        .order_by('-total_quantity')[:10] or []
                        
            # Total revenue
            total_revenue = Order.objects.filter(order_date__gte = start_date)\
                  .aggregate(total_revenue = Sum(F('products__selling_price') * F('products__quantity')))['total_revenue'] or 0
            
            # Total quantity sold
            total_quantity = Order.objects.filter(order_date__gte = start_date)\
                  .aggregate(total_quantity = Sum('products__order__products__quantity'))['total_quantity'] or 0
                        
            # Create the revenue products list
            top_revenue_products = [{
                  'product_id': item['products__id'],
                  'product_name': item['products__name'],
                  'category': item['products__category__name'],
                  'total_revenue': item['total_revenue'] or 0,
            } for item in products_revenue]
            
            # create the quantity products list
            top_quantity_products = [{
                  'product_id': item['products__id'],
                  'product_name': item['products__name'],
                  'category': item['products__category__name'],
                  'total_quantity': item['total_quantity'] or 0,
            } for item in products_quantity]
            
            
            # Create the response data
            response_data = {
                  'total_revenue': total_revenue,
                  'total_quantity': total_quantity,
                  'top_revenue_products': top_revenue_products,
                  'top_quantity_products': top_quantity_products,
            }
            
            return response.Response(response_data, status=200)
      except Exception as e:
            return response.Response({'error': str(e)}, status=500)
      
      