from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime, timedelta

# Import for DB analysis
from django.db.models import Sum, Count, Avg, Max, Min, lookups, manager, options
import pandas as pd
import matplotlib.pyplot as plt

# importing tables
from product.models import Customer, Product, Order, Category

# Create your views here.
def get_start_date(time_range):
      now = datetime.now()
      
      if time_range == 'today':
            start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
      elif time_range == 'yesterday':
            start_date = now - timedelta(days=1)
      elif time_range == 'last_week':
            start_date = now - timedelta(days=7)
      elif time_range == 'last_year':
            start_date = now - timedelta(days=365)
      else:
            start_date = now - timedelta(days=30)
      
      return start_date


# Monthly inventory report
def inventory_report(request):
      time_range = request.GET.get('time_range', 'last_month')
      start_date = get_start_date(time_range)
      
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
            
      return JsonResponse({'summary': summary_data}, safe=False)


