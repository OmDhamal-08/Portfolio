from django.core.management.base import BaseCommand
from portfolio_app.models import Project
from datetime import datetime

class Command(BaseCommand):
    help = 'Populate projects with complete information including descriptions'

    def handle(self, *args, **options):
        # Clear existing projects
        Project.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Cleared existing projects'))
        
        complete_projects = [
            {
                'title': 'Portfolio Website',
                'short_description': 'A responsive portfolio website showcasing projects and skills with Django backend.',
                'description': """A fully responsive personal portfolio website built with Django and Tailwind CSS. This project showcases my skills, projects, and achievements with a modern, interactive design.

## Key Features
- **Fully Responsive Design**: Works perfectly on all devices from mobile to desktop
- **Dynamic Content Management**: Easy to update projects, skills, and certifications through admin panel
- **Contact Form Integration**: Visitors can send messages directly via email
- **Project Filtering**: Filter projects by type and status for better navigation
- **SEO Optimized**: Built with search engine optimization in mind
- **Fast Performance**: Optimized images and assets for quick loading

## Technical Implementation
The website uses Django's MVT (Model-View-Template) architecture with PostgreSQL as the database. The frontend is built with Tailwind CSS for rapid styling and Alpine.js for client-side interactivity.

## What I Learned
- Advanced Django template inheritance and context processors
- Tailwind CSS utility-first workflow
- Alpine.js for lightweight interactivity
- PostgreSQL database optimization techniques
- Deployment strategies for Django applications""",
                'project_type': 'web',
                'status': 'completed',
                'tech_stack': 'Django, Python, PostgreSQL, Tailwind CSS, Alpine.js, JavaScript',
                'github_link': 'https://github.com/OmDhamal-08/Portfolio',
                'documentation_link': 'https://portfolio-five-nu-11.vercel.app/',
                'start_date': datetime(2024, 1, 10),
                'end_date': datetime(2024, 2, 20),
                'featured': True,
                'display_order': 1,
                'is_active': True,
            },

            {
                'title': 'Heat Attack Prediction',
                'short_description': 'ML-based system predicting heat attack risks using environmental and health data.',
                'description': """A machine learning system that predicts the risk of heat-related health attacks using environmental and personal health data.

## Key Features
- **Real-time Risk Prediction**: Uses current weather data and health metrics
- **Multiple ML Models**: Ensemble learning with Random Forest, XGBoost, and Logistic Regression
- **Alert System**: Sends SMS notifications for high-risk predictions
- **Interactive Dashboard**: Real-time visualization of risk factors
- **Historical Analysis**: Tracks and analyzes past predictions and outcomes

## Technical Implementation
- **ML Models**: Scikit-learn, TensorFlow for deep learning components
- **Backend**: Django REST Framework for API endpoints
- **Frontend**: React.js with Chart.js for visualizations
- **Database**: PostgreSQL with time-series data optimization
- **External APIs**: Weather data integration, SMS gateway

## Model Performance
- **Accuracy**: 92% on test dataset
- **Precision**: 89% for positive cases
- **Recall**: 94% for at-risk individuals
- **F1-Score**: 0.915 overall

## Impact
This system can help healthcare providers and individuals prepare for heat-related health risks, potentially reducing emergency incidents during heat waves.""",
                'project_type': 'ml',
                'status': 'completed',
                'tech_stack': 'Python, Scikit-learn, TensorFlow, Django REST Framework, React.js',
                'github_link': 'https://github.com/OmDhamal-08/heart-disease-app',
                'documentation_link': 'https://heart-disease-app-00sv.onrender.com/',
                'start_date': datetime(2023, 11, 5),
                'end_date': datetime(2024, 1, 15),
                'featured': True,
                'display_order': 2,
                'is_active': True,
            },

            {
                'title': 'House Price Prediction',
                'short_description': 'ML model predicting house prices based on location, size, and amenities.',
                'description': """A comprehensive machine learning application that predicts house prices based on location, amenities, and market trends.

## Key Features
- **Multiple Regression Models**: Linear Regression, Decision Trees, Random Forest comparison
- **Feature Importance Analysis**: Identifies key factors affecting house prices
- **Interactive Visualization**: Plotly dashboards for data exploration
- **Neighborhood Comparison**: Compares prices across different areas
- **Prediction Confidence**: Shows confidence intervals for predictions

## Technical Implementation
- **Data Processing**: Pandas for data cleaning and feature engineering
- **ML Pipeline**: Scikit-learn Pipeline for reproducible workflows
- **Web Interface**: Flask with Bootstrap frontend
- **Visualization**: Matplotlib, Seaborn, and Plotly for charts

## Model Details
- **Best Model**: Random Forest Regressor
- **R² Score**: 0.87 on validation set
- **MAE**: $12,500
- **Key Features**: Location, square footage, number of bedrooms, year built

## Applications
- Real estate investors for market analysis
- Homeowners for property valuation
- Construction companies for project planning""",
                'project_type': 'ml',
                'status': 'completed',
                'tech_stack': 'Python, Pandas, NumPy, Scikit-learn, Matplotlib, Flask',
                'github_link': 'https://github.com/OmDhamal-08/House_Price_predicition',
                'start_date': datetime(2023, 9, 1),
                'end_date': datetime(2023, 10, 20),
                'featured': False,
                'display_order': 3,
                'is_active': True,
            },

            {
                'title': 'Expense Tracker',
                'short_description': 'Web application for tracking expenses and managing personal finances.',
                'description': """A web-based expense tracking application with budget management and financial insights.

## Key Features
- **Multi-Category Tracking**: Categorize expenses with custom tags and categories
- **Budget Management**: Set monthly budgets and receive alerts
- **Report Generation**: Export to PDF, Excel, or CSV formats
- **Visual Dashboard**: Interactive charts for expense analysis
- **Multi-Currency Support**: Handle expenses in different currencies
- **Recurring Expenses**: Automatic tracking of regular payments

## Technical Implementation
- **Backend**: Django with Django REST Framework
- **Frontend**: React.js with Material-UI components
- **Charts**: Chart.js and Recharts for visualization
- **PDF Generation**: ReportLab for report creation
- **Authentication**: JWT with refresh tokens

## Security Features
- End-to-end encryption for sensitive data
- Two-factor authentication option
- Session management with device tracking
- Audit logs for all financial transactions""",
                'project_type': 'web',
                'status': 'completed',
                'tech_stack': 'Django, Django REST Framework, React.js, Chart.js, PostgreSQL',
                'github_link': 'https://github.com/OmDhamal-08/expense-tracker',
                'documentation_link': 'https://github.com/OmDhamal-08/expense-tracker/wiki',
                'start_date': datetime(2023, 8, 10),
                'end_date': datetime(2023, 10, 5),
                'featured': True,
                'display_order': 4,
                'is_active': True,
            },

            {
                'title': 'Food Analyzer AI',
                'short_description': 'AI system analyzing food images for nutritional content and health patterns.',
                'description': """An AI-powered food analysis system that evaluates nutritional values and detects unhealthy patterns from food images.

## Current Status: In Development

## Planned Features
- **Food Recognition**: CNN-based image classification for 100+ food items
- **Nutritional Analysis**: Estimate calories, macros, and micronutrients
- **Diet Tracking**: Log meals and track nutritional intake
- **Meal Planning**: AI-generated meal plans based on goals
- **Health Insights**: Detect unhealthy eating patterns
- **Integration**: Connect with fitness apps and wearables

## Technical Stack
- **Computer Vision**: TensorFlow, OpenCV for image processing
- **Backend**: FastAPI for high-performance API endpoints
- **Mobile App**: React Native for cross-platform mobile
- **Database**: MongoDB for flexible document storage
- **Cloud**: Firebase for authentication and real-time database

## Progress So Far
✅ Basic food recognition model (50 classes) - 85% accuracy
✅ REST API development with FastAPI
🔄 Mobile app development (in progress)
📅 Nutritional database integration (planned)""",
                'project_type': 'ml',
                'status': 'in_progress',
                'tech_stack': 'Python, TensorFlow, OpenCV, FastAPI, MongoDB, React Native',
                'github_link': 'https://github.com/OmDhamal-08/Food_analyzer_app',
                'start_date': datetime(2024, 2, 1),
                'end_date': None,
                'featured': False,
                'display_order': 5,
                'is_active': True,
            },
        ]

        for project_data in complete_projects:
            try:
                project = Project.objects.create(**project_data)
                self.stdout.write(
                    self.style.SUCCESS(f'Created project: {project.title}')
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Error creating {project_data["title"]}: {str(e)}')
                )
        

        self.stdout.write(self.style.SUCCESS(f'Successfully created {len(complete_projects)} projects with complete information'))

