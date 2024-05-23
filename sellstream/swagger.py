from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions



schema_view = get_schema_view(
      openapi.Info(
            title="SellStream API",
            default_version='v1',
            description="""
            <img src="https://sell-stream.netlify.app/assets/logo-BKDu74En.png" alt="Your API Logo" width="200" height="200"/>

            ### Our POS System aims to provide a comprehensive solution that empowers retailers to enhance operational efficiency, improve customer satisfaction, and drive business growth. Whether you run a small boutique or a large retail chain, our system is designed to meet your needs and help you stay ahead in the competitive market.

            ### Key Features:

            #### Intuitive User Interface:
            - Easy-to-navigate interface for quick and efficient transaction processing.
            - Touchscreen compatibility for fast and convenient use.

            #### Sales Reporting and Analytics:
            - Detailed sales reports to monitor performance and make data-driven decisions.
            - Insights into best-selling products, peak sales periods, and customer behavior.
            - Exportable reports for accounting and financial analysis.
            
            #### Multi-Store Support:

            - Centralized management of multiple store locations.
            - Consolidated reporting and inventory management across all stores.
            - User roles and permissions to control access levels.

            #### Technology Stack:

            - Backend: Django Rest Framework (DRF) for scalable and secure API development.
            - Frontend: React.js for a dynamic and responsive user interface.
            - Database: PostgreSQL for reliable and efficient data management.
                  

            """,
            contact=openapi.Contact(email="admin@sellstream.com"),
            license=openapi.License(name="Team Hexabit"),
      ),
      public=True,
      permission_classes=[permissions.AllowAny],
)