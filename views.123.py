# data_analysis_app/views.py
from django.shortcuts import render, HttpResponse
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from io import BytesIO
import base64
from io import StringIO

def data_tab(request):
    # Read Titanic dataset from CSV
    df = pd.read_csv(r'C:\Users\User\Downloads\food_6000.csv', encoding='latin-1')
 # Get the first ten rows of the dataset
    df_first_ten = df.head(10)

    # Get information about the columns (data types, non-null counts, null counts)
    columns_info = pd.DataFrame({
        'Column Name': df.columns,
        'Data Type': df.dtypes,
        'Non-Null Count': df.notnull().sum(),
        'Null Count': df.isnull().sum()
    })

    # Convert DataFrame to HTML for rendering in template
    table_html = df_first_ten.to_html(classes='table table-hover table-striped-columns table-secondary')

    # Include the columns information in the HTML template
    columns_info_html = f"{columns_info.to_html(classes='table table-hover table-striped-columns table-info', index=False)}"

    return render(request, 'data_tab.html', {'table_html': table_html, 'columns_info_html': columns_info_html})


  
def descriptive_statistics_tab(request):
    # Read Titanic dataset from CSV
    df = pd.read_csv(r'C:\Users\User\Downloads\food_6000.csv', encoding='latin-1')
    
    # Perform descriptive statistics using pandas
    descriptive_stats = df.describe().to_html(classes='table table-hover table-striped-columns table-info')

    return render(request, 'descriptive_statistics_tab.html', {'descriptive_stats': descriptive_stats})




def box_plot(request):
    # Read Titanic dataset from CSV
    df = pd.read_csv(r'C:\Users\User\Downloads\food_6000.csv', encoding='latin-1')

    # Default settings for the plot
    default_category = 'Pclass'
    default_value = 'Fare'

    # Get user-selected options (if any)
    selected_category = request.GET.get('category', default_category)
    selected_value = request.GET.get('value', default_value)

    # Validate selected features
    if selected_category not in df.columns or selected_value not in df.columns:
        error_message = "Invalid features selected for box plot."
        return render(request, 'error_page.html', {'error_message': error_message})

    # Create an interactive box plot using Plotly
    fig = px.box(df, x=selected_category, y=selected_value, title=f'Box Plot: {selected_value} by {selected_category}')

    # Convert the plot to HTML for rendering in the template
    plot_html = fig.to_html(full_html=False)

    # Pass parameters to the template for customization options
    box_cus_options = {
        'categories': df.columns.tolist(),
        'default_category': default_category,
        'default_value': default_value,
        'selected_category': selected_category,
        'selected_value': selected_value,
    }
    return {'plot_html': plot_html, 'box_cus_options': box_cus_options}
    #return render(request, 'box_plot.html', {'plot_html': plot_html, 'customization_options': customization_options})








def exploratory_data_analysis_tab(request):
    # Read Titanic dataset from CSV
    df = pd.read_csv(r'C:\Users\User\Downloads\food_6000.csv', encoding='latin-1')
    # Default settings for the plot
    default_feature = 'state'
    default_bins = 20

    # Get user-selected options (if any)
    selected_feature = request.GET.get('Total Time(Mins)', default_feature)
    selected_bins = int(request.GET.get('bins', default_bins))

    # Create an interactive histogram using Plotly
    fig = px.histogram(df, x='Total Time(Mins)', nbins=selected_bins, title=f'{selected_feature} Distribution')

    # Convert the plot to HTML for rendering in the template
    plot_html = fig.to_html(full_html=False)

    # Pass parameters to template for customization options
    customization_options = {
        'features': df.columns.tolist(),
        'default_feature': default_feature,
        'default_bins': default_bins,
        'selected_feature': selected_feature,
        'selected_bins': selected_bins,
    }

    ##########################   Box Plot ##############################
    # Default settings for the plot
    default_category = 'Pclass'
    default_value = 'Fare'

    # Get user-selected options (if any)
    selected_category = request.GET.get('category', default_category)
    selected_value = request.GET.get('value', default_value)

    # Validate selected features
    if selected_category not in df.columns or selected_value not in df.columns:
        # If invalid features selected, render the page with the default content
        return render(request, 'exploratory_data_analysis_tab.html', {
            'plot_html': plot_html,
            'customization_options': customization_options,
            'box_plot_html': None,  # Set box_plot_html to None
            'box_cus_options': None,  # Set box_cus_options to None
            'plot_html_scatter': None,
            'customization_options_scatter': None,
            'plot_html_pie': None,
            'customization_options_pie': None,
        })

    # Create an interactive box plot using Plotly
    fig_box = px.box(df, x=selected_category, y=selected_value,
                     title=f'Box Plot: {selected_value} by {selected_category}')

    # Convert the plot to HTML for rendering in the template
    box_plot_html = fig_box.to_html(full_html=False)

    # Pass parameters to the template for customization options
    box_cus_options = {
        'categories': df.columns.tolist(),
        'default_category': default_category,
        'default_value': default_value,
        'selected_category': selected_category,
        'selected_value': selected_value,
    }

    ####################### Scatter Plot ###############################

    # Default settings for the scatter plot
    default_x_feature = 'cook_time'
    default_y_feature = 'prep_time'

    # Get user-selected options (if any)
    selected_x_feature = request.GET.get('x_feature', default_x_feature)
    selected_y_feature = request.GET.get('y_feature', default_y_feature)

    # Create an interactive scatter plot using Plotly
    fig_scatter = px.scatter(df, x=selected_x_feature, y=selected_y_feature, color='Pclass',
                             title=f'Scatter Plot: {selected_x_feature} vs. {selected_y_feature}')

    # Convert the scatter plot to HTML for rendering in the template
    plot_html_scatter = fig_scatter.to_html(full_html=False)

    # Pass parameters to template for customization options
    customization_options_scatter = {
        'features': df.columns.tolist(),
        'default_x_feature': default_x_feature,
        'default_y_feature': default_y_feature,
        'selected_x_feature': selected_x_feature,
        'selected_y_feature': selected_y_feature,
    }

    ################################ Pie Chart #################################
    # Default settings for the pie chart
    default_feature_pie = 'Survived'

    # Get user-selected options (if any)
    selected_feature_pie = request.GET.get('feature_pie', default_feature_pie)

    # Create an interactive pie chart using Plotly
    fig_pie = px.pie(df, names=selected_feature_pie, title=f'Pie Chart: {selected_feature_pie}')

    # Convert the pie chart to HTML for rendering in the template
    plot_html_pie = fig_pie.to_html(full_html=False)

    # Pass parameters to the template for customization options
    customization_options_pie = {
        'features_pie': df.columns.tolist(),
        'default_feature_pie': default_feature_pie,
        'selected_feature_pie': selected_feature_pie,
    }

    return render(request, 'exploratory_data_analysis_tab.html', {
        'plot_html': plot_html,
        'customization_options': customization_options,
        'box_plot_html': box_plot_html,
        'box_cus_options': box_cus_options,
        'plot_html_scatter': plot_html_scatter,
        'customization_options_scatter': customization_options_scatter,
        'plot_html_pie': plot_html_pie,
        'customization_options_pie': customization_options_pie,
    })
















def export_to_csv(request):
    # Read Titanic dataset from CSV
    df = pd.read_csv(r'C:\Users\User\Downloads\food_6000.csv', encoding='latin-1')

    # Generate CSV file
    csv_file = df.to_csv(index=False)

    # Create HTTP response with CSV file
    response = HttpResponse(csv_file, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="indian_food.csv"'
    
    return response


def export_to_excel(request):
    # Read Titanic dataset from CSV
    df = pd.read_csv(r'C:\Users\User\Downloads\food_6000.csv', encoding='latin-1')

    # Generate Excel file
    excel_file = BytesIO()
    with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    excel_file.seek(0)

    # Create HTTP response with Excel file
    response = HttpResponse(excel_file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="data_analysis_project.csv"'

    return response
