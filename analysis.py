# Online Shopper Purchase Behavior Analysis
# Data: UCI Online Shoppers Purchasing Intention Dataset (Sakar & Kastro, 2018), CC BY 4.0
# Question: Which browsing behaviors are linked to whether a session ends in a purchase?

# ===== 0. Setup =====
# Import pandas (pd), matplotlib.pyplot (plt), and stats from scipy
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

# Show all columns when printing
pd.set_option("display.max_columns", None)
print()

# ===== 1. Load and check the data =====
# Read online_shoppers_intention.csv into df
df = pd.read_csv("online_shoppers_intention.csv")

# Print the shape of df
print("=== Shape of the data ===")
print(df.shape)
print()

# Print the overall purchase rate (%), rounded to 1 decimal place
print("=== Overall purchase rate (%) ===")
print((df["Revenue"].mean() * 100).round(1))
print()

# ===== 2. Q1: Do purchasers view more pages and stay longer? =====
# 2a. Print the median pages viewed and median time on product pages, by Revenue
print("=== Median pages viewed and time spent on product pages ===")
print(df.groupby("Revenue")["ProductRelated"].median())
print(df.groupby("Revenue")["ProductRelated_Duration"].median())
print()

# 2b. Box plot of pages viewed by Revenue (hide outliers), save as figures/q1_pages_boxplot.png

df.boxplot(column="ProductRelated", by="Revenue", showfliers=False)

# Add a clear title and axis labels
plt.title("Product pages viewed: non-purchasers vs. purchasers")
plt.xlabel("Purchased")
plt.ylabel("Number of product pages viewed")
plt.suptitle("")

# Show the chart
plt.tight_layout()
plt.savefig("figures/q1_pages_boxplot.png", dpi=150, bbox_inches="tight")
plt.show()

# 2c. Box plot of time on product pages by Revenue (hide outliers), save as figures/q1_time_boxplot.png
df.boxplot(column="ProductRelated_Duration", by="Revenue", showfliers=False)
plt.title("Time on product pages: non-purchasers vs. purchasers")
plt.xlabel("Purchased")
plt.ylabel("Time spent on product pages (seconds)")
plt.suptitle("")

# Show the chart
plt.tight_layout()
plt.savefig("figures/q1_time_boxplot.png", dpi=150, bbox_inches="tight")
plt.show()


# 2d. Split df into bought and not_bought
bought = df[df["Revenue"] == True]
not_bought = df[df["Revenue"] == False]

# 2e. Mann-Whitney U tests for pages and time, print both p-values
mw_pages = stats.mannwhitneyu(bought["ProductRelated"], not_bought["ProductRelated"])
print("=== p-value (Mann-Whitney U, pages viewed) ===")
print(mw_pages.pvalue)
print()

mw_time = stats.mannwhitneyu(bought["ProductRelated_Duration"], not_bought["ProductRelated_Duration"])
print("=== p-value (Mann-Whitney U, time on product pages) ===")
print(mw_time.pvalue)
print()


# ===== 3. Q2: Do new and returning visitors buy at different rates? =====
# 3a. Remove "Other" visitors and save as df_nr
df_nr = df[df["VisitorType"] != "Other"]

# 3b. Calculate purchase rate (%) by VisitorType and save as purchase_rate
purchase_rate = (df_nr.groupby("VisitorType")["Revenue"].mean()* 100).round(1)
print("=== Purchase rate by visitor type (%) ===")
print(purchase_rate)
print()

# 3c. Bar chart with a 15.5% baseline, save as figures/q2_visitor_type_bar.png
purchase_rate.plot(kind="bar")
plt.title("Purchase rate: new vs. returning visitors")
plt.xlabel("Visitor type")
plt.ylabel("Purchase rate (%)")
plt.axhline(15.5, color="gray", linestyle="--")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("figures/q2_visitor_type_bar.png", dpi=150, bbox_inches="tight")
plt.show()


# 3d. Crosstab and chi-square test, print the p-value
table_nr = pd.crosstab(df_nr["VisitorType"], df_nr["Revenue"])
print("=== Crosstab: visitor type x purchase ===")
print(table_nr)
print()
# Run a chi-square test on table_nr and save the result as chi_nr
chi_nr = stats.chi2_contingency(table_nr)

# Print the expected counts (what the table would look like if there were no difference)
print("=== Expected counts if there were no difference ===")
print(chi_nr.expected_freq)
print()

# Print the p-value
print("=== p-value (chi-square test, new vs. returning) ===")
print(chi_nr.pvalue)
print()

# ===== 4. Q3: Does purchase rate change with total time on site? =====
# 4a. Create Total_Duration = sum of the three duration columns
df["Total_Duration"] = df["Administrative_Duration"]+df["Informational_Duration"]+df["ProductRelated_Duration"]

# 4b. Cut Total_Duration into four groups and save as Duration_Group
df["Duration_Group"] = pd.cut(df["Total_Duration"],
                              bins=[0, 60, 300, 900, float("inf")],
                              labels=["<1 min", "1-5 min", "5-15 min", "15+ min"],
                              right=False)
# 4c. Calculate purchase rate (%) by Duration_Group and save as rate_by_duration
rate_by_duration = (df.groupby("Duration_Group")["Revenue"].mean()*100).round(1)
print("=== Purchase rate by total time on site (%) ===")
print(rate_by_duration)
print()

# 4d. Bar chart with a 15.5% baseline, save as figures/q3_duration_bar.png
rate_by_duration.plot(kind="bar")
plt.title("Purchase rate by total time on site")
plt.xlabel("Total time on site")
plt.ylabel("Purchase rate (%)")
plt.axhline(15.5, color="gray", linestyle="--")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("figures/q3_duration_bar.png", dpi=150, bbox_inches="tight")
plt.show()

# 4e. Crosstab and chi-square test, print the p-value
table_duration = pd.crosstab(df["Duration_Group"], df["Revenue"])
print("=== Crosstab: Total time on site x purchase ===")
print(table_duration)
print()
# Run a chi-square test on table_duration and save the result as chi_duration
chi_duration = stats.chi2_contingency(table_duration)
print("=== Expected counts if there were no difference ===")
print(chi_duration.expected_freq)
print()

# Print the p-value with a title
print("=== p-value (chi-square test, <1m, 1-5m, 5-15m, 15m+) ===")
print(chi_duration.pvalue)
print()