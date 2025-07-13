import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
df = pd.read_excel('Uber Request Data.xlsx')

# Display basic info
print(df.info())
print(df.head())

# Convert timestamps to datetime
df['Request timestamp'] = pd.to_datetime(df['Request timestamp'], dayfirst=True, errors='coerce')
df['Drop timestamp'] = pd.to_datetime(df['Drop timestamp'], dayfirst=True, errors='coerce')

# Extract time features
df['Request hour'] = df['Request timestamp'].dt.hour
df['Request day'] = df['Request timestamp'].dt.date
df['Time slot'] = pd.cut(df['Request hour'],
                         bins=[-1, 4, 10, 16, 21, 24],
                         labels=['Late Night', 'Morning', 'Afternoon', 'Evening', 'Night'])

# Check for missing values
print(df.isnull().sum())

# Plot: Request status frequency
plt.figure(figsize=(8, 4))
sns.countplot(data=df, x='Status', palette='Set2')
plt.title('Request Status Frequency')
plt.show()

# Plot: Requests by hour and status
plt.figure(figsize=(14, 6))
sns.countplot(data=df, x='Request hour', hue='Status', palette='viridis')
plt.title('Hourly Request Distribution by Status')
plt.show()

# Plot: Requests by pickup point and status
plt.figure(figsize=(10, 5))
sns.countplot(data=df, x='Pickup point', hue='Status', palette='coolwarm')
plt.title('Pickup Point vs Request Status')
plt.show()

# Supply-demand gap: Count requests by status per hour
gap_data = df.groupby(['Request hour', 'Status']).size().unstack(fill_value=0)
gap_data.plot(kind='bar', stacked=True, figsize=(15, 6), colormap='tab20c')
plt.title('Supply-Demand Gap by Hour')
plt.ylabel('Number of Requests')
plt.xlabel('Hour of Day')
plt.xticks(rotation=0)
plt.legend(title='Status')
plt.tight_layout()
plt.show()

# Optional: Save cleaned data
df.to_csv("Cleaned_Uber_Data.csv", index=False)
