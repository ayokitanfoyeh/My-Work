


import pandas as pd
import numpy as np
from pandas import DataFrame
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.formula.api import ols
import plotly.express as px
import plotly.graph_objects as go

# Load the data
sold = pd.read_csv('/Users/kitanolowofoyeku/Cafe+-+Sell+Meta+Data.csv')
transactions = pd.read_csv('/Users/kitanolowofoyeku/Cafe+-+Transaction+-+Store.csv')
date_info = pd.read_csv('/Users/kitanolowofoyeku/Cafe+-+DateInfo.csv')
# Fill in null values in holiday column
date_info['HOLIDAY'] = date_info['HOLIDAY'].fillna("Nonholiday")
# Merge dataframes and drop unwanted columns
data1 = pd.merge(sold.drop(['ITEM_ID'],axis=1), transactions.drop(['SELL_CATEGORY'], axis= 1), on =  'SELL_ID')
#Group by all columns/Sum Quantity
b = data1.groupby(['SELL_ID', 'SELL_CATEGORY', 'ITEM_NAME', 'CALENDAR_DATE','PRICE']).QUANTITY.sum()
#Reset index
intermediate_data = b.reset_index()
#Merge dataframes
combined_data = pd.merge(intermediate_data, date_info, on = 'CALENDAR_DATE')
#Replace different holiday names with 'Holiday'
combined_data['HOLIDAY'] = combined_data['HOLIDAY'].replace(['Luner New Year','Labor Day','Dragon Boat Festivel','Mid-Autumn Day'],'Holiday')
#Remove data that's on schoolbreaks and during the weekend
bau_data = combined_data[(combined_data['IS_SCHOOLBREAK']==0) & (combined_data['IS_WEEKEND']==0)]


def fun_optimize(var_opt, var_range, var_cost, bau_data, product, holiday):
    """[summary]
    Args:
        var_opt ([string]): [The value will be either price or quantity based on the selection made from UI]
        var_range ([int]): [The value will be maximum & minimum price based on selection made from range slider from UI]
        var_cost ([type]): [This is the fixed cost entered from UI]
        df ([type]): [The data set for our usecase]
        product: Product ID of product
        holiday: Holiday or Nonholiday
    Returns:
        [list]: [Returns a dataframe for table, 
                chart for Price Vs Quantity, 
                chart for optimized price set for maximum revenue, 
                Optimized value of revenue]
    """

    df2 = bau_data[(bau_data['HOLIDAY']== holiday) & (bau_data['SELL_ID']==product)]
    
    fig_PriceVsQuantity = px.scatter(
        df2, x="PRICE", y="QUANTITY", trendline="ols")

    # fit OLS model
    model = ols("QUANTITY ~ PRICE", data=df2).fit()

    #Math to get profit at each price
    Price = list(range(var_range[0], var_range[1], 1))
    cost = int(var_cost)
    quantity = []
    Revenue = []
    for i in Price:
        demand = model.params[0] + (model.params[1] * i)
        quantity.append(demand)
        Revenue.append((i-cost) * demand)

    profit = pd.DataFrame(
        {"Price": Price, "Revenue": Revenue, "Quantity": quantity})

    #Get maximizing profit
    max_val = profit.loc[(profit['Revenue'] == profit['Revenue'].max())]
        
    #Plot and design line graph
    fig_PriceVsRevenue = go.Figure()
    fig_PriceVsRevenue.update_xaxes(rangemode='nonnegative')
    fig_PriceVsRevenue.update_yaxes(rangemode='nonnegative')
    fig_PriceVsRevenue.add_trace(go.Scatter(
        x=profit['Price'], y=profit['Revenue']))
    fig_PriceVsRevenue.add_annotation(x=int(max_val['Price']), y=int(max_val['Revenue']),
                                      text="Maximum Profit",
                                      showarrow=True,
                                      arrowhead=1)

    fig_PriceVsRevenue.update_layout(
        showlegend=False,
        xaxis_title="Price",
        yaxis_title="Profit")

    fig_PriceVsRevenue.add_vline(x=int(max_val['Price']), line_width=2, line_dash="dash",
                                 line_color="red", opacity=0.25)

    # Identify the optimal price at which the revenue is maximum
    # profit[profit['Revenue'] == profit['Revenue'].max()]
    # pd.set_option('display.max_rows', profit.shape[0]+1)
    # profit.style.highlight_max(color = 'blue', axis = None)

    return [profit, fig_PriceVsRevenue, fig_PriceVsQuantity, round(max_val['Price'].values[0],2),round(max_val['Revenue'].values[0],3)]






