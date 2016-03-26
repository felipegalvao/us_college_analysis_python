# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 10:51:34 2016

@author: e79q
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Import the Dataset from 2005 to a Pandas DataFrame
us_college_data = pd.read_csv("college-scorecard-raw-data-030216/merged_2005_PP.csv")

# Turn off chained assignment warnings on Pandas
pd.options.mode.chained_assignment = None  # default='warn'

# Remove duplicates on the dataframe based on the opeid6 column, since
# earnings and debt informations is the same
us_college_data = us_college_data.drop_duplicates(['opeid6'])

# Change NULL and PrivacySuppresed values on column to R NA, then convert
# everything to numeric
us_college_data.GRAD_DEBT_MDN[us_college_data.GRAD_DEBT_MDN == "PrivacySuppressed"] = np.nan
us_college_data.GRAD_DEBT_MDN[us_college_data.GRAD_DEBT_MDN == "NULL"] = np.nan
us_college_data.GRAD_DEBT_MDN = pd.to_numeric(us_college_data.GRAD_DEBT_MDN)

# Do the same cleaning for the earnings in 6 years column
us_college_data.md_earn_wne_p6[us_college_data.md_earn_wne_p6 == "PrivacySuppressed"] = np.nan
us_college_data.md_earn_wne_p6[us_college_data.md_earn_wne_p6 == "NULL"] = np.nan
us_college_data.md_earn_wne_p6 = pd.to_numeric(us_college_data.md_earn_wne_p6)

# Create a column on the DF for Earnings to Debt ratio (earnings / debt)
us_college_data['earnings_debt_ratio'] = pd.Series(us_college_data.md_earn_wne_p6 / us_college_data.GRAD_DEBT_MDN, index=us_college_data.index)

# Create column that calculates the number of months necessary to pay the
# average debt with the median earnings, considering that one person
# uses 10% of that earnings to pay the debt
us_college_data['months_to_pay'] = pd.Series(us_college_data.GRAD_DEBT_MDN / (us_college_data.md_earn_wne_p6 / 10 / 12), index=us_college_data.index)

# Set constant variables about the US average per capita income
# and average student loan debt (debt for 2005, income for 2011 (6 years after entry))
us_per_capita_income = 49781.4
us_avg_stdnt_loan_debt = 17233

# Filter the colleges where the earnings average is above 
# and the average debt is lesser than the US average
selected_colleges = us_college_data[(us_college_data.md_earn_wne_p6 > us_per_capita_income) & (us_college_data.GRAD_DEBT_MDN < us_avg_stdnt_loan_debt)]

# Sort the data frame by the ratio column and select the top 10
top_10_selected_by_ratio = selected_colleges.sort_values(by='earnings_debt_ratio', ascending=False)
top_10_selected_by_ratio = top_10_selected_by_ratio.iloc[:10]

# Here we'll trim the college names so that they don't mess up the plot
top_10_selected_by_ratio['Institution'] = pd.Series(top_10_selected_by_ratio.INSTNM.str[0:29], index=top_10_selected_by_ratio.index)

# Plot bar chart with the top 10 colleges by Earnings to Debt Ratio
y_axis = top_10_selected_by_ratio.earnings_debt_ratio
x_pos = np.arange(len(top_10_selected_by_ratio.Institution))
x_labels = top_10_selected_by_ratio.Institution

plt.bar(x_pos, y_axis)
plt.xticks(x_pos-0.6, tuple(x_labels), rotation=45)
plt.show()

print(top_10_selected_by_ratio[["Institution","md_earn_wne_p6","GRAD_DEBT_MDN","earnings_debt_ratio", "months_to_pay"]])

top_10_selected_by_earnings = selected_colleges.sort_values(by='md_earn_wne_p6', ascending=False)
top_10_selected_by_earnings = top_10_selected_by_earnings.iloc[:10]
top_10_selected_by_earnings['Institution'] = pd.Series(top_10_selected_by_earnings.INSTNM.str[0:29], index=top_10_selected_by_earnings.index)

y_axis = top_10_selected_by_earnings.md_earn_wne_p6
x_pos = np.arange(len(top_10_selected_by_earnings.Institution))
x_labels = top_10_selected_by_earnings.Institution

plt.bar(x_pos, y_axis)
plt.xticks(x_pos-0.6, tuple(x_labels), rotation=45)
plt.show()

print(top_10_selected_by_earnings[["Institution","md_earn_wne_p6","GRAD_DEBT_MDN","earnings_debt_ratio", "months_to_pay"]])

print(us_college_data['TUITIONFEE_IN'].corr(us_college_data['md_earn_wne_p6']))

scatter_plot = plt.scatter(us_college_data['TUITIONFEE_IN'], us_college_data['md_earn_wne_p6'],
                           alpha=0.5)