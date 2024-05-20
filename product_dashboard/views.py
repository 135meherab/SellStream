from django.shortcuts import render

# Import for DB analysis
from django.db.models import Sum, Count, Avg, Max, Min, lookups, manager, options
import pandas as pd
import matplotlib.pyplot as plt

# importing tables
from product.models import Customer, Product, Order, Category

# Create your views here.
