
## About Bellabeat

Bellabeat is a women-focused wellness technology company founded in 2014. Its products include:

- **Bellabeat App**: Tracks user wellness and syncs with other Bellabeat products.
- **Leaf**: Wearable wellness tracker.
- **Time**: Smart wellness watch.
- **Spring**: Smart water bottle.
- **Membership**: Personalized plans for lifestyle, sleep, mindfulness, etc.

**Stakeholders:**

- Urška Sršen – Co-founder & Chief Creative Officer  
- Sando Mur – Co-founder & Mathematician  
- Bellabeat Marketing Analytics Team

## 1. Ask

**Business Task:**

The Bellabeat marketing analytics team wants to analyze smart device usage trends to gain insight into how consumers are using their Fitbit smart devices. These insights will help guide Bellabeat’s marketing strategy, focusing on one of their wellness products, such as the “Time” smart watch.

**Key Stakeholder Goals:**

- Increase the company’s growth.
- Gather high-level recommendations to inform marketing strategies.
- Better understand user behavior through wearable fitness tracker data.

**SMART Questions:**

- What are some trends in smart device usage?
- How could these trends apply to Bellabeat customers?
- How could these trends influence Bellabeat’s marketing strategy?

---

## 2. Prepare

**Data Source:**
The dataset used in this project is the FitBit Fitness Tracker Data, available publicly on Kaggle. It was made available under a **CC0: Public Domain license**, which allows unrestricted use for analysis and educational purposes.

- The data was originally collected through voluntary submission via Amazon Mechanical Turk in **2016**, and includes **personal fitness tracker information from 30 individuals** over approximately one month.
    
- It covers a variety of metrics, including:
    - Daily and minute-level step counts
    - Activity intensities
    - Calories burned
    - Sleep patterns
    - Heart rate recordings
        

**Limitations and Considerations:**

- **Outdated Data**: The dataset is nearly a decade old and may not reflect current user behavior or device capabilities.
- **Small Sample Size**: Only 30 users are included, limiting the generalizability of insights.
- **Lack of Demographics**: No age, gender, or location data is available, which restricts segmentation.
- **Fragmented Structure**: Minute-level datasets have no time zones or calendar alignment and can only be joined using user ID and parsed timestamps.
- **Self-Reported Submission**: Data was submitted manually, which may introduce inconsistencies or gaps.
    
> Despite its limitations, the dataset offers valuable insight into general activity and health tracking behaviors, and serves as a strong foundation for demonstrating the data analysis process in this capstone project.

---

## 3. Process

### Tool Selection

Due to the size and fragmentation of datasets, Google BigQuery was chosen for data preparation and querying.

### Initial Exploration and Dataset Selection

I choosed the `dailyActivity` table as the base for our analysis because it includes key variables: participant ID, date, total steps, distances, calories burned, and time spent at various activity levels. While initially considering the `minutes` datasets, they had limited identifiers and were harder to join consistently.

### Data Cleaning Steps

 Started by exploring the data schema and converting relevant fields:

- Converted `ActivityDate` to a date format.
- Converted all numeric values (steps, distance, minutes, calories) into appropriate numeric types and rounded where necessary.
- Removed `TrackerDistance` (duplicate of `TotalDistance`).
- Removed empty fields like `LoggedActivitiesDistance`.


![[Pasted image 20250621114635.png]]
![[Pasted image 20250621114742.png]]

```sql
CREATE OR REPLACE TABLE `eng-district-463201-h7.FitBit.dailyActivity_Clean` AS
SELECT
  Id,
  PARSE_DATE('%m/%d/%Y', ActivityDate) AS ActivityDate,
  ROUND(CAST(TotalDistance AS NUMERIC), 3) AS TotalDistance,
  ROUND(CAST(VeryActiveDistance AS NUMERIC), 3) AS VeryActiveDistance,
  ROUND(CAST(ModeratelyActiveDistance AS NUMERIC), 3) AS ModeratelyActiveDistance,
  ROUND(CAST(LightActiveDistance AS NUMERIC), 3) AS LightActiveDistance,
  ROUND(CAST(SedentaryActiveDistance AS NUMERIC), 3) AS SedentaryActiveDistance,
  CAST(VeryActiveMinutes AS NUMERIC) AS VeryActiveMinutes,
  CAST(FairlyActiveMinutes AS NUMERIC) AS FairlyActiveMinutes,
  CAST(LightlyActiveMinutes AS NUMERIC) AS LightlyActiveMinutes,
  CAST(SedentaryMinutes AS NUMERIC) AS SedentaryMinutes,
  CAST(Calories AS NUMERIC) AS Calories,
  CAST(TotalSteps AS NUMERIC) AS TotalSteps
FROM
  `eng-district-463201-h7.FitBit.dailyActivity`
```

### Outlier Detection: Sedentary Time

To detect unusual usage behavior, I sorted the dataset by `SedentaryMinutes`. In there, observed users with extremely low values across all metrics (steps, distance, calories), possibly indicating a user who turned the device on and off without using it.

![[Pasted image 20250621122205.png]]

```sql
SELECT Id, ActivityDate, TotalSteps, TotalDistance,VeryActiveMinutes, FairlyActiveMinutes,LightlyActiveMinutes, SedentaryMinutes, Calories 
FROM `eng-district-463201-h7.FitBit.dailyActivity_Clean` 
ORDER BY SedentaryMinutes ASC
```



### Outlier Detection: Calories

Then, sorted by `Calories` in descending order to check for inconsistencies. Some users burned more calories despite recording fewer steps and activity minutes — an indicator of possible errors or edge cases.


![[Pasted image 20250621120211.png]]


```sql
SELECT Id, ActivityDate, TotalSteps, TotalDistance,VeryActiveMinutes, FairlyActiveMinutes,LightlyActiveMinutes, SedentaryMinutes, Calories 
FROM `eng-district-463201-h7.FitBit.dailyActivity_Clean` 
ORDER BY Calories DESC
```

### Data Integrity Check

We validated that step counts in `dailySteps` matched those in `dailyActivity` using a join on `Id` and `Date`. This ensures the datasets can be reliably merged and that step totals are consistent.

```sql
CREATE OR REPLACE TABLE `eng-district-463201-h7.FitBit.dailySteps_dailyActivity_JoinCheck` AS
SELECT
  ds.Id,
  PARSE_DATE('%m/%d/%Y', SPLIT(ds.ActivityDay, ' ')[OFFSET(0)]) AS ActivityDate,
  CAST(ds.StepTotal AS NUMERIC) AS StepTotal,
  da.TotalSteps,
  CAST(ds.StepTotal AS NUMERIC) = da.TotalSteps AS StepsMatch
FROM
  `eng-district-463201-h7.FitBit.dailySteps` AS ds
INNER JOIN
  `eng-district-463201-h7.FitBit.dailyActivity_Clean` AS da
ON
  ds.Id = da.Id AND 
  PARSE_DATE('%m/%d/%Y', SPLIT(ds.ActivityDay, ' ')[OFFSET(0)]) = da.ActivityDate
```

As shown in the charts comparing step data, the values are consistent across datasets. This consistency confirms the integrity and reliability of the information.

![[comparison_total_steps.png]]
---

## 4. Analyze

### General Profile

Calculated averages for key activity metrics and understanding of the users profile:

```sql
SELECT
  ROUND(AVG(VeryActiveMinutes) / 60, 2) AS avg_Very_active_hours,
  ROUND(AVG(FairlyActiveMinutes) / 60, 2) AS avg_Fairly_active_hours,
  ROUND(AVG(LightlyActiveMinutes) / 60, 2) AS avg_Lightly_active_hours,
  ROUND(AVG(SedentaryMinutes) / 60, 2) AS avg_Sedentary_hours,
  ROUND(AVG(Calories), 0) AS avg_Calories_burned,
  ROUND(AVG(TotalSteps), 0) AS avg_Steps
FROM
  `eng-district-463201-h7.FitBit.dailyActivity_Clean`
```

**Findings:**

| Very Active (hrs) | Fairly Active (hrs) | Lightly Active (hrs) | Sedentary (hrs) | Calories Burned | Steps |
|------------------:|---------------------:|----------------------:|----------------:|-----------------:|-------:|
| 0.36              | 0.23                 | 3.24                  | 16.42           | 2,330            | 7,736  |

Most users were sedentary for over 16 hours per day. Only 0.59 hours per day were spent in moderate-to-high activity, suggesting a need for more active habits.

### Correlation: Activity and Sleep

Joined sleep and activity data to assess relationships between active time and sleep quantity.

```sql
CREATE OR REPLACE TABLE `eng-district-463201-h7.FitBit.dailyActivity_Complete` AS
SELECT
  da.*,
  CAST(sd.TotalSleepRecords AS NUMERIC) AS TotalSleepRecords,
  ROUND(CAST(sd.TotalMinutesAsleep AS NUMERIC) / 60, 2) AS TotalTimeAsleep_Hours,
  ROUND(CAST(sd.TotalTimeInBed AS NUMERIC) / 60, 2) AS TotalTimeInBed_Hours
FROM
  `eng-district-463201-h7.FitBit.dailyActivity_Clean` AS da
LEFT JOIN
  `eng-district-463201-h7.FitBit.sleepDay` AS sd
ON
  TRIM(LOWER(da.Id)) = TRIM(LOWER(sd.Id))
  AND da.ActivityDate = PARSE_DATE('%m/%d/%Y', SPLIT(sd.SleepDay, ' ')[OFFSET(0)])
```

![[activity_vs_sleep_neon.png]]

> Observation: Users who recorded at least 0.4 hours of activity were more likely to get more than 6 hours of sleep.

### Hourly/Weekly Usage Heatmap

We analyzed intensity per 3-hour time block and day of the week.

```sql
CREATE OR REPLACE TABLE `eng-district-463201-h7.FitBit.intensity_By_Block` AS
SELECT
  FORMAT_TIMESTAMP('%A', PARSE_TIMESTAMP('%m/%d/%Y %I:%M:%S %p', TRIM(ActivityMinute))) AS DayOfWeek,
  CONCAT(
    LPAD(CAST(DIV(EXTRACT(HOUR FROM PARSE_TIMESTAMP('%m/%d/%Y %I:%M:%S %p', TRIM(ActivityMinute))), 3) * 3 AS STRING), 2, '0'),
    '-',
    LPAD(CAST(DIV(EXTRACT(HOUR FROM PARSE_TIMESTAMP('%m/%d/%Y %I:%M:%S %p', TRIM(ActivityMinute))), 3) * 3 + 3 AS STRING), 2, '0')
  ) AS HourBlock,
  AVG(CAST(Intensity AS FLOAT64)) AS AvgIntensity
FROM
  `eng-district-463201-h7.FitBit.minuteIntensities`
GROUP BY DayOfWeek, HourBlock
```

![[frequency_days_heatmap2 5.png]]

**Result:** Users are most active from **12 PM to 9 PM**, especially on **Saturdays from 12–3 PM**.

### Weekday vs Weekend Behavior

```sql
CREATE OR REPLACE VIEW `eng-district-463201-h7.FitBit.dailyActivity_SummaryByDayOfWeek` AS
SELECT
  FORMAT_TIMESTAMP('%A', CAST(ActivityDate AS TIMESTAMP)) AS DayOfWeek,
  CASE
    WHEN EXTRACT(DAYOFWEEK FROM CAST(ActivityDate AS DATE)) IN (1,7) THEN 'Weekend'
    ELSE 'Weekday'
  END AS DayType,
  AVG(TotalTimeInBed_Hours) AS AvgTimeInBed,
  AVG(TotalTimeAsleep_Hours) AS AvgTimeAsleep,
  AVG(SAFE_DIVIDE(TotalTimeAsleep_Hours, NULLIF(TotalTimeInBed_Hours, 0))) AS AvgSleepEfficiency,
  AVG(VeryActiveMinutes + FairlyActiveMinutes + LightlyActiveMinutes) AS AvgActiveMinutes
FROM
  `eng-district-463201-h7.FitBit.dailyActivity_Clean`
WHERE
  TotalTimeInBed_Hours IS NOT NULL
  AND TotalTimeAsleep_Hours IS NOT NULL
GROUP BY
  DayOfWeek, DayType
```

![[average_active_minutes_weekday_vs_weekend.png]]

> Sleep efficiency and activity levels tend to be slightly better on weekends.


### Heart Rate Analysis

In this section, we are going to explore the relationship between users’ **average heart rate** and their **physical activity levels**. The goal was to identify whether elevated heart rate readings are associated with sedentary lifestyles or low activity engagement.

Followed a multi-step approach:

1. **heart_rate_daily CTE**: Calculated the **daily average heart rate** per user from second-level granularity data.
2. **activity_daily CTE**: Pulled daily activity minutes by type from the cleaned `dailyActivity` table.
3. **combined CTE**: Joined both datasets on `Id` and `date` to align heart rate and activity data per user per day.
4. **filtered_users CTE**: Filtered out users with less than 3 days of data to ensure reliability.
5. **Final SELECT**:
    - Calculated per-user average metrics.
    - Classified users based on:
        - **Activity level**:
            - Less than 30 minutes/day → `Sedentary`
            - 30–99 minutes/day → `Low Active`
            - 100+ minutes/day → `Active`
        - **Heart rate status**:
            - > 85 bpm → `Elevated Heart Rate`
            - ≤85 bpm → `Normal Heart Rate`


```SQL
WITH heart_rate_daily AS ( 
  SELECT
    Id,
    DATE(PARSE_TIMESTAMP('%m/%d/%Y %I:%M:%S %p', Time)) AS date,
    AVG(CAST(Value AS FLOAT64)) AS avg_heart_rate
  FROM `eng-district-463201-h7.FitBit.heartrateSeconds`
  GROUP BY Id, date
),

activity_daily AS (
  SELECT
    Id,
    DATE(ActivityDate) AS date,
    VeryActiveMinutes,
    FairlyActiveMinutes,
    LightlyActiveMinutes,
    SedentaryMinutes
  FROM `eng-district-463201-h7.FitBit.dailyActivity_Clean`
),

combined AS (
  SELECT
    hr.Id,
    hr.date,
    hr.avg_heart_rate,
    COALESCE(ad.VeryActiveMinutes, 0) AS VeryActiveMinutes,
    COALESCE(ad.FairlyActiveMinutes, 0) AS FairlyActiveMinutes,
    COALESCE(ad.LightlyActiveMinutes, 0) AS LightlyActiveMinutes,
    COALESCE(ad.SedentaryMinutes, 0) AS SedentaryMinutes
  FROM heart_rate_daily hr
  LEFT JOIN activity_daily ad
    ON hr.Id = ad.Id AND hr.date = ad.date
),

filtered_users AS (
  SELECT
    Id,
    COUNT(*) AS total_days,
    AVG(avg_heart_rate) AS avg_heart_rate,
    AVG(VeryActiveMinutes) AS avg_very_active_minutes,
    AVG(FairlyActiveMinutes) AS avg_fairly_active_minutes,
    AVG(LightlyActiveMinutes) AS avg_lightly_active_minutes,
    AVG(SedentaryMinutes) AS avg_sedentary_minutes
  FROM combined
  GROUP BY Id
  HAVING total_days >= 3
)

SELECT
  Id,
  total_days,
  ROUND(avg_heart_rate, 1) AS avg_heart_rate,
  ROUND(avg_very_active_minutes, 1) AS avg_very_active_minutes,
  ROUND(avg_fairly_active_minutes, 1) AS avg_fairly_active_minutes,
  ROUND(avg_lightly_active_minutes, 1) AS avg_lightly_active_minutes,
  ROUND(avg_sedentary_minutes, 1) AS avg_sedentary_minutes,
  CASE
    WHEN (avg_very_active_minutes + avg_fairly_active_minutes) < 30 THEN 'Sedentary'
    WHEN (avg_very_active_minutes + avg_fairly_active_minutes) BETWEEN 30 AND 99 THEN 'Low Active'
    WHEN (avg_very_active_minutes + avg_fairly_active_minutes) >= 100 THEN 'Active'
    ELSE 'Unclassified'
  END AS activity_level,
  CASE
    WHEN avg_heart_rate > 85 THEN 'Elevated Heart Rate'
    ELSE 'Normal Heart Rate'
  END AS heart_rate_status
FROM filtered_users
ORDER BY (avg_very_active_minutes + avg_fairly_active_minutes) DESC;
```

### Reference for Heart Rate Threshold

> **Note:** A resting heart rate above **85 bpm** was used as the threshold for “Elevated Heart Rate” based on meta-analysis evidence.  
Individuals with a resting heart rate above **80 bpm** had a **45% higher risk of all-cause mortality** and **33% higher risk of cardiovascular mortality** compared to those with lower heart rates. The risk increases further above 90 bpm.
> *Source: Zhang D, Shen X, Qi X. Resting heart rate and all-cause and cardiovascular mortality in the general population: a meta-analysis. CMAJ. 2016 Feb 16;188(3):E53-E63. doi: [10.1503/cmaj.150535](https://doi.org/10.1503/cmaj.150535)*  


![[elevated_heart_rate_analysis.png]]

From the resulting visualization we can observe that:

- **40% of users with elevated heart rate** fell into the **sedentary** category.
- **25% were considered low active**.
- Only a minority of users with elevated heart rate maintained high activity levels.
    

This suggests that many users with high heart rates might not be engaging in enough physical activity, possibly leading to health risks. It emphasizes an opportunity for Bellabeat to identify and nudge users with elevated heart rates to be more active — a potential feature for **smart notifications** or **personalized wellness advice**.

---

## 5. Share

**Visuals Used:**

- Data integrity validation charts (steps comparison).
- Daily averages of key metrics (steps, calories, minutes).
- Activity vs. Sleep scatter plot.
- Heatmap of activity intensity by day and time.
- Heart rate vs. activity level classification bar plot.

**Key Findings:**

1. **Sedentary lifestyle**: Users are inactive for ~16.4 hours/day on average.
2. **Low intense activity**: Most users engage in <1 hour/day of moderate to vigorous activity.
3. **Activity–Sleep link**: ≥0.4 hours of activity is associated with longer sleep duration.
4. **Weekend peak engagement**: Users are most active on Saturdays, especially between 12–3 PM.
5. **Elevated heart rate concern**: 40% of users with high resting heart rate are sedentary; 25% are low active — suggesting health risk opportunities.
6. **Calorie inconsistencies**: Some users report high calorie burn with little activity — possible tracking or sync issues.
7. **Drop-off patterns**: A few users engage briefly and stop, possibly due to discomfort, poor battery, or lack of motivation.

---

## 6. Act

**Strategic Recommendations for Bellabeat:**

1. **Proactive Health Alerts**  
    Identify users with elevated resting heart rates and low activity levels. Trigger real-time notifications to encourage physical activity and reduce health risks.
2. **Behavior-Based Notifications**  
    Leverage peak engagement windows — particularly **afternoons and weekends** — to push motivational messages or launch wellness challenges.
3. **Market the Time Watch as a Wellness Ally**  
    Highlight how the Time watch tracks both activity and heart rate, helping users better understand and manage their overall health.
4. **Promote Sleep–Activity Balance**  
    Educate users on how even moderate daily activity (~0.4 hrs/day) is linked to longer sleep duration — an insight backed by real usage data.
5. **Weekend Wellness Campaigns**  
    Launch targeted campaigns on weekends, when users are naturally more active. These can include app-based competitions or reminders for hydration, movement, or mindfulness.
6. **Refine Data Ecosystem**  
    Address calorie estimation inconsistencies by improving synchronization between physical metrics and device feedback, ensuring more accurate user insights.
7. **Investigate Drop-Off Behavior**  
    Some users recorded minimal interaction with the device — turning it on briefly and ceasing usage. This could indicate issues such as:
    - Physical discomfort or unattractive design
    - Lack of perceived value from insights provided
    - Short battery life or absence of waterproofing
    
    Bellabeat should consider:
    - Short surveys for users who disengage early
    - Testing alternate onboarding or habit-building flows
    - Prioritizing **comfort, aesthetics, battery performance, and durability** (e.g., waterproof materials) in future product iterations
      
> Understanding not just _how_ users behave, but _why_ they disengage, is key to sustainable adoption and satisfaction.

---
