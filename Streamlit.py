import pandas as pd
import streamlit as st
import plotly.express as px

# Page Titles
st.set_page_config(page_title='Data Visualisation',
                   page_icon=':chart_with_upwards_trend:',
                   layout='wide')
st.title(':blue[Data Visualisation] :chart_with_upwards_trend: ')
st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)
st.subheader('Send me your EXCEL file')

# Uploading data
uploaded_file = st.file_uploader(' :open_file_folder: Choose a file', type=['csv','xlsx'])
if uploaded_file:
    st.markdown('---')
    df = pd.read_csv(uploaded_file, encoding='windows-1252')

    
    df["Order Date"] = pd.to_datetime(df["Order Date"])

    # fliter min date & max date
    startDate = pd.to_datetime(df["Order Date"]).min()
    endDate = pd.to_datetime(df["Order Date"]).max()
    col1, col2 = st.columns((2))
    with col1:
        date1 = pd.to_datetime(st.date_input("Start Date", startDate))
    with col2:
        date2 = pd.to_datetime(st.date_input("End Date", endDate))

    df = df[(df["Order Date"] >= date1) & (df["Order Date"] <= date2)].copy()

    with st.sidebar:
        st.sidebar.header("Choose your filter: 	:star2: ")
        region_filter = st.multiselect(label= 'Select The Region',
                                    options=df['Region'].unique(),
                                    default=df['Region'].unique())

        city_filter = st.multiselect(label='Select The City',
                                options=df['City'].unique(),
                                default=df['City'].unique())

        state_filter = st.multiselect(label='Select The State',
                                options=df['State'].unique(),
                                default=df['State'].unique())
    filtered_df = df.query('Region == @region_filter & City == @city_filter & State == @state_filter')

    # Sumary
    total_customer = len(pd.unique(df['Customer ID']))
    total_city = len(pd.unique(df['City']))
    total_sub_category = len(pd.unique(df['Sub-Category']))
    total_sales= float(df['Sales'].sum()) 
    total_profit = float(df['Profit'].sum())

    total1,total2,total3,total4,total5 = st.columns(5,gap='large')
    with total1:
        st.image('image/focus-group.png',use_column_width='always')
        st.metric(label = 'Total Customer', value=(total_customer))    
    
    with total2:
        st.image('image/international.png',use_column_width='always')
        st.metric(label='Total City', value=(total_city))
   
    with total3:
        st.image('image/blinder.png',use_column_width='always')
        st.metric(label= 'Total Sub Category',value=(total_sub_category))
   
    with total4:
        st.image('image/money-bag.png',use_column_width='always')
        st.metric(label='Total Sales',value=round(total_sales,1))
   
    with total5:
        st.image('image/capitalize.png',use_column_width='always')
        st.metric(label='Total Profit',value=round(total_profit,2))

    # Bar & Pie chart
    category_df = filtered_df.groupby(by = ["Category"], as_index = False)["Sales"].sum()
    col1, col2 = st.columns((2))
    with col1:
        st.subheader("Category wise Sales")
        fig = px.bar(category_df, x = "Category", y = "Sales", text = ['${:,.2f}'.format(x) for x in category_df["Sales"]],
                    template = "seaborn")
        st.plotly_chart(fig, theme="streamlit", use_container_width=True, height = 200)
    with col2:
        st.subheader("Region wise Sales")
        fig = px.pie(filtered_df, values = "Sales", names = "Region", hole = 0.5)
        fig.update_traces(text = filtered_df["Region"], textposition = "outside")
        st.plotly_chart(fig,use_container_width=True)

    # Text table
    col3, col4 = st.columns((2))
    with col3:
        with st.expander("Category_ViewData"):
            st.write(category_df.style.background_gradient(cmap="Blues"))
            csv = category_df.to_csv(index = False).encode('utf-8')
    with col4:
        with st.expander("Region_ViewData"):
            region = filtered_df.groupby(by = "Region", as_index = False)["Sales"].sum()
            st.write(region.style.background_gradient(cmap="Oranges"))
            csv = region.to_csv(index = False).encode('utf-8')

    # Time Series   
    filtered_df["month_year"] = filtered_df["Order Date"].dt.to_period("M")
    st.subheader('Time Series Analysis')

    linechart = pd.DataFrame(filtered_df.groupby(filtered_df["month_year"].dt.strftime("%Y : %b"))["Sales"].sum()).reset_index()
    fig1 = px.line(linechart, x = "month_year", y="Sales", labels = {"Sales": "Amount"},height=500, width = 1000,template="gridon")
    st.plotly_chart(fig1,use_container_width=True)

    # TreeMap(Region, category, Sub-category of Sales)
    st.subheader("Region, Category, Sub-Category of Sales using TreeMap")
    fig2 = px.treemap(filtered_df, path = ["Region","Category","Sub-Category"], values = "Sales",hover_data = ["Sales"],
                    color = "Sub-Category")
    fig2.update_layout(width = 800, height = 650)
    st.plotly_chart(fig2, use_container_width=True)

    # Pie chart with profit
    chart1, chart2 = st.columns((2))
    with chart1:
        st.subheader('Category wise Profit')
        fig = px.pie(filtered_df, values = "Profit", names = "Category", template = "gridon")
        fig.update_traces(text = filtered_df["Category"], textposition = "inside")
        st.plotly_chart(fig,use_container_width=True)
    with chart2:
        st.subheader('Segment wise Profit')
        fig = px.pie(filtered_df, values = "Profit", names = "Segment", template = "plotly_dark")
        fig.update_traces(text = filtered_df["Segment"], textposition = "inside")
        st.plotly_chart(fig,use_container_width=True)
    
    # Create a scatter plot
    data = px.scatter(filtered_df, x = "Sales", y = "Profit", size = "Quantity")
    data['layout'].update(title="Scatter Plot of the relationship between Sales and Profit",
                        titlefont = dict(size=20),xaxis = dict(title="Sales",titlefont=dict(size=19)),
                        yaxis = dict(title = "Profit", titlefont = dict(size=19)))
    st.plotly_chart(data,use_container_width=True)

