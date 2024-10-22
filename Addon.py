#############################################
#     Storage Utilization by Object Type
#############################################
storage_by_object_sql = """
WITH size_metrics AS (
    SELECT 
        DATABASE_NAME,
        SCHEMA_NAME,
        TABLE_NAME,
        TABLE_TYPE,
        ROW_COUNT,
        CASE 
            WHEN ACTIVE_BYTES < 1024 THEN ACTIVE_BYTES || ' B'
            WHEN ACTIVE_BYTES < 1048576 THEN ROUND(ACTIVE_BYTES/1024, 2) || ' KB'
            WHEN ACTIVE_BYTES < 1073741824 THEN ROUND(ACTIVE_BYTES/1048576, 2) || ' MB'
            WHEN ACTIVE_BYTES < 1099511627776 THEN ROUND(ACTIVE_BYTES/1073741824, 2) || ' GB'
            ELSE ROUND(ACTIVE_BYTES/1099511627776, 2) || ' TB'
        END AS ACTIVE_SIZE,
        ROUND(ACTIVE_BYTES/NULLIF(ROW_COUNT, 0), 2) as BYTES_PER_ROW,
        ROUND(ACTIVE_BYTES/1073741824, 2) as ACTIVE_GB_RAW
    FROM snowflake.account_usage.table_storage_metrics
    WHERE ACTIVE_BYTES > 0
)
SELECT * FROM size_metrics
ORDER BY ACTIVE_GB_RAW DESC
LIMIT 20
"""
storage_objects_df = run_query(storage_by_object_sql)

fig_storage_objects = px.treemap(
    storage_objects_df,
    path=[px.Constant('All'), 'DATABASE_NAME', 'SCHEMA_NAME', 'TABLE_NAME'],
    values='ACTIVE_GB_RAW',
    color='BYTES_PER_ROW',
    title="Storage Hierarchy Analysis",
    hover_data=['ROW_COUNT', 'ACTIVE_SIZE', 'TABLE_TYPE']
)

#############################################
#     Query Performance Deep Dive
#############################################
query_perf_sql = f"""
WITH query_metrics AS (
    SELECT 
        QUERY_TYPE,
        WAREHOUSE_NAME,
        DATABASE_NAME,
        SCHEMA_NAME,
        USER_NAME,
        ROUND(TOTAL_ELAPSED_TIME/1000, 2) as EXECUTION_SECONDS,
        ROUND(BYTES_SCANNED/1048576, 2) as MB_SCANNED,
        ROUND(BYTES_WRITTEN/1048576, 2) as MB_WRITTEN,
        ROUND(BYTES_SPILLED_TO_LOCAL_STORAGE/1048576, 2) as MB_SPILLED_LOCAL,
        ROUND(BYTES_SPILLED_TO_REMOTE_STORAGE/1048576, 2) as MB_SPILLED_REMOTE,
        CREDITS_USED_COMPUTE + CREDITS_USED_CLOUD_SERVICES as TOTAL_CREDITS,
        PERCENTAGE_SCANNED_FROM_CACHE
    FROM snowflake.account_usage.query_history
    WHERE start_time between '{s}' and '{e}'
        AND EXECUTION_STATUS = 'SUCCESS'
)
SELECT * FROM query_metrics
WHERE TOTAL_CREDITS > 0
ORDER BY TOTAL_CREDITS DESC
LIMIT 100
"""
query_perf_df = run_query(query_perf_sql)

# Create multiple visualizations for query performance
fig_query_spill = px.scatter(
    query_perf_df,
    x='MB_SCANNED',
    y='TOTAL_CREDITS',
    size='MB_SPILLED_REMOTE',
    color='WAREHOUSE_NAME',
    title="Query Spilling Analysis",
    hover_data=['QUERY_TYPE', 'USER_NAME', 'EXECUTION_SECONDS']
)

fig_cache_impact = px.scatter(
    query_perf_df,
    x='EXECUTION_SECONDS',
    y='PERCENTAGE_SCANNED_FROM_CACHE',
    size='MB_SCANNED',
    color='WAREHOUSE_NAME',
    title="Cache Utilization Impact",
    hover_data=['QUERY_TYPE', 'USER_NAME', 'TOTAL_CREDITS']
)

#############################################
#     Database Growth Trends
#############################################
db_growth_sql = """
WITH daily_db_size AS (
    SELECT 
        DATABASE_NAME,
        DATE_TRUNC('day', USAGE_DATE) as USAGE_DATE,
        SUM(CASE 
            WHEN ACTIVE_BYTES < 1073741824 THEN ROUND(ACTIVE_BYTES/1048576, 2)
            WHEN ACTIVE_BYTES < 1099511627776 THEN ROUND(ACTIVE_BYTES/1073741824, 2)
            ELSE ROUND(ACTIVE_BYTES/1099511627776, 2)
        END) as SIZE_VALUE,
        CASE 
            WHEN MAX(ACTIVE_BYTES) < 1073741824 THEN 'MB'
            WHEN MAX(ACTIVE_BYTES) < 1099511627776 THEN 'GB'
            ELSE 'TB'
        END as SIZE_UNIT
    FROM snowflake.account_usage.database_storage_usage_history
    GROUP BY 1, 2
)
SELECT * FROM daily_db_size
ORDER BY USAGE_DATE DESC, SIZE_VALUE DESC
"""
db_growth_df = run_query(db_growth_sql)

fig_db_growth = px.line(
    db_growth_df,
    x='USAGE_DATE',
    y='SIZE_VALUE',
    color='DATABASE_NAME',
    title="Database Size Growth Trends",
    labels={'SIZE_VALUE': 'Size (Dynamic Unit)'},
    hover_data=['SIZE_UNIT']
)

#############################################
#     Warehouse Efficiency Analysis
#############################################
warehouse_efficiency_sql = f"""
WITH warehouse_metrics AS (
    SELECT 
        WAREHOUSE_NAME,
        WAREHOUSE_SIZE,
        COUNT(*) as QUERY_COUNT,
        AVG(TOTAL_ELAPSED_TIME/1000) as AVG_EXECUTION_SEC,
        SUM(TOTAL_ELAPSED_TIME/1000)/3600 as TOTAL_EXECUTION_HOURS,
        SUM(CREDITS_USED_COMPUTE) as COMPUTE_CREDITS,
        SUM(CREDITS_USED_CLOUD_SERVICES) as CLOUD_CREDITS,
        SUM(BYTES_SCANNED)/POWER(1024,3) as TB_SCANNED,
        AVG(PERCENTAGE_SCANNED_FROM_CACHE) as AVG_CACHE_HIT,
        SUM(CASE WHEN BYTES_SPILLED_TO_REMOTE_STORAGE > 0 THEN 1 ELSE 0 END) as SPILLING_QUERIES
    FROM snowflake.account_usage.query_history
    WHERE start_time between '{s}' and '{e}'
        AND WAREHOUSE_NAME IS NOT NULL
    GROUP BY 1, 2
)
SELECT 
    *,
    ROUND(SPILLING_QUERIES::FLOAT / NULLIF(QUERY_COUNT, 0) * 100, 2) as SPILL_PERCENTAGE,
    ROUND(COMPUTE_CREDITS / NULLIF(TOTAL_EXECUTION_HOURS, 0), 2) as CREDITS_PER_HOUR
FROM warehouse_metrics
ORDER BY COMPUTE_CREDITS DESC
"""
warehouse_efficiency_df = run_query(warehouse_efficiency_sql)

fig_warehouse_efficiency = px.scatter(
    warehouse_efficiency_df,
    x='CREDITS_PER_HOUR',
    y='AVG_CACHE_HIT',
    size='QUERY_COUNT',
    color='WAREHOUSE_SIZE',
    title="Warehouse Efficiency Matrix",
    hover_data=['WAREHOUSE_NAME', 'SPILL_PERCENTAGE', 'TB_SCANNED']
)

#############################################
#     Schema-Level Query Patterns
#############################################
schema_patterns_sql = f"""
WITH schema_metrics AS (
    SELECT 
        DATABASE_NAME,
        SCHEMA_NAME,
        COUNT(DISTINCT USER_NAME) as UNIQUE_USERS,
        COUNT(*) as QUERY_COUNT,
        AVG(TOTAL_ELAPSED_TIME/1000) as AVG_EXECUTION_SEC,
        SUM(CREDITS_USED_COMPUTE + CREDITS_USED_CLOUD_SERVICES) as TOTAL_CREDITS,
        SUM(CASE 
            WHEN BYTES_SCANNED < 1048576 THEN ROUND(BYTES_SCANNED/1024, 2)
            WHEN BYTES_SCANNED < 1073741824 THEN ROUND(BYTES_SCANNED/1048576, 2)
            ELSE ROUND(BYTES_SCANNED/1073741824, 2)
        END) as DATA_PROCESSED,
        CASE 
            WHEN MAX(BYTES_SCANNED) < 1048576 THEN 'KB'
            WHEN MAX(BYTES_SCANNED) < 1073741824 THEN 'MB'
            ELSE 'GB'
        END as DATA_UNIT
    FROM snowflake.account_usage.query_history
    WHERE start_time between '{s}' and '{e}'
    GROUP BY 1, 2
)
SELECT * FROM schema_metrics
ORDER BY TOTAL_CREDITS DESC
"""
schema_patterns_df = run_query(schema_patterns_sql)

fig_schema_patterns = px.sunburst(
    schema_patterns_df,
    path=['DATABASE_NAME', 'SCHEMA_NAME'],
    values='TOTAL_CREDITS',
    color='QUERY_COUNT',
    title="Schema Usage Patterns",
    hover_data=['UNIQUE_USERS', 'AVG_EXECUTION_SEC', 'DATA_PROCESSED', 'DATA_UNIT']
)

# Create containers for new visualizations
st.subheader("Storage Analysis")
container_storage = st.container()
with container_storage:
    st.plotly_chart(fig_storage_objects, use_container_width=True)
    st.plotly_chart(fig_db_growth, use_container_width=True)

st.subheader("Query Performance Analysis")
container_query_perf = st.container()
with container_query_perf:
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_query_spill, use_container_width=True)
    with col2:
        st.plotly_chart(fig_cache_impact, use_container_width=True)

st.subheader("Warehouse and Schema Analysis")
container_warehouse = st.container()
with container_warehouse:
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_warehouse_efficiency, use_container_width=True)
    with col2:
        st.plotly_chart(fig_schema_patterns, use_container_width=True)

# Add explanatory metrics boxes
st.subheader("Key Performance Indicators")
col1, col2, col3, col4 = st.columns(4)

# Calculate summary metrics
total_spill_queries = warehouse_efficiency_df['SPILLING_QUERIES'].sum()
avg_cache_hit = warehouse_efficiency_df['AVG_CACHE_HIT'].mean()
total_storage = storage_objects_df['ACTIVE_GB_RAW'].sum()
avg_credits_per_hour = warehouse_efficiency_df['CREDITS_PER_HOUR'].mean()

with col1:
    st.metric("Total Spilling Queries", f"{total_spill_queries:,.0f}")
with col2:
    st.metric("Avg Cache Hit Rate", f"{avg_cache_hit:.1f}%")
with col3:
    st.metric("Total Active Storage", f"{total_storage:.1f} GB")
with col4:
    st.metric("Avg Credits/Hour", f"{avg_credits_per_hour:.2f}")

# Add detailed findings and recommendations
st.subheader("Analysis Insights")
st.write("""
### Storage Insights
- Visualize storage distribution across databases, schemas, and tables
- Track storage growth trends with human-readable sizes
- Identify tables with inefficient storage usage (high bytes per row)

### Query Performance Insights
- Monitor query spilling patterns and their impact on credit consumption
- Analyze cache utilization effectiveness
- Track query performance across different warehouses

### Warehouse Efficiency Insights
- Compare warehouse sizes and their credit consumption rates
- Monitor spilling percentages and cache hit rates
- Analyze credit usage patterns per warehouse size
""")

#############################################
#     Table Cost Analysis by Warehouse
#############################################
table_warehouse_cost_sql = f"""
WITH table_metrics AS (
    -- Get table storage costs
    SELECT 
        t.DATABASE_NAME,
        t.SCHEMA_NAME,
        t.TABLE_NAME,
        ROUND(t.ACTIVE_BYTES/POWER(1024,3), 2) as STORAGE_GB,
        ROUND(t.ACTIVE_BYTES/POWER(1024,4), 2) as STORAGE_TB,
        t.ROW_COUNT,
        ROUND(t.ACTIVE_BYTES/NULLIF(t.ROW_COUNT, 0), 2) as BYTES_PER_ROW
    FROM snowflake.account_usage.table_storage_metrics t
    WHERE t.ACTIVE_BYTES > 0
),
query_costs AS (
    -- Get query costs per table
    SELECT 
        q.DATABASE_NAME,
        q.SCHEMA_NAME,
        q.TABLE_NAME,
        q.WAREHOUSE_NAME,
        COUNT(*) as QUERY_COUNT,
        SUM(CREDITS_USED_COMPUTE + CREDITS_USED_CLOUD_SERVICES) as TOTAL_CREDITS,
        AVG(TOTAL_ELAPSED_TIME/1000) as AVG_EXECUTION_SEC,
        SUM(BYTES_SCANNED)/POWER(1024,3) as GB_SCANNED
    FROM snowflake.account_usage.access_history q
    WHERE start_time between '{s}' and '{e}'
    GROUP BY 1, 2, 3, 4
)
SELECT 
    tm.*,
    qc.WAREHOUSE_NAME,
    qc.QUERY_COUNT,
    qc.TOTAL_CREDITS,
    qc.AVG_EXECUTION_SEC,
    qc.GB_SCANNED,
    ROUND(qc.GB_SCANNED/NULLIF(tm.STORAGE_GB, 0) * 100, 2) as SCAN_RATIO,
    ROUND(qc.TOTAL_CREDITS/NULLIF(qc.QUERY_COUNT, 0), 4) as CREDITS_PER_QUERY
FROM table_metrics tm
LEFT JOIN query_costs qc 
    ON tm.DATABASE_NAME = qc.DATABASE_NAME 
    AND tm.SCHEMA_NAME = qc.SCHEMA_NAME 
    AND tm.TABLE_NAME = qc.TABLE_NAME
ORDER BY qc.TOTAL_CREDITS DESC NULLS LAST
"""
table_warehouse_cost_df = run_query(table_warehouse_cost_sql)

# Create visualization for table costs
fig_table_costs = px.treemap(
    table_warehouse_cost_df,
    path=[px.Constant('All'), 'WAREHOUSE_NAME', 'DATABASE_NAME', 'SCHEMA_NAME', 'TABLE_NAME'],
    values='STORAGE_GB',
    color='CREDITS_PER_QUERY',
    title="Table Storage and Query Cost Analysis by Warehouse",
    custom_data=['QUERY_COUNT', 'TOTAL_CREDITS', 'ROW_COUNT', 'BYTES_PER_ROW', 'SCAN_RATIO']
)

#############################################
#     Expensive Query Analysis by User
#############################################
expensive_queries_sql = f"""
WITH user_query_costs AS (
    SELECT 
        USER_NAME,
        WAREHOUSE_NAME,
        QUERY_TYPE,
        QUERY_TEXT,
        DATABASE_NAME,
        SCHEMA_NAME,
        TOTAL_ELAPSED_TIME/1000 as EXECUTION_SEC,
        CREDITS_USED_COMPUTE + CREDITS_USED_CLOUD_SERVICES as QUERY_CREDITS,
        BYTES_SCANNED/POWER(1024,3) as GB_SCANNED,
        ROWS_PRODUCED,
        CASE 
            WHEN BYTES_SPILLED_TO_REMOTE_STORAGE > 0 THEN 'Yes'
            ELSE 'No'
        END as HAS_SPILLING,
        COMPILATION_TIME/1000 as COMPILE_SEC,
        EXECUTION_TIME/1000 as PURE_EXEC_SEC,
        QUEUED_PROVISIONING_TIME/1000 as QUEUE_SEC,
        TRANSACTION_BLOCKED_TIME/1000 as BLOCKED_SEC,
        PERCENTAGE_SCANNED_FROM_CACHE as CACHE_HIT_RATIO
    FROM snowflake.account_usage.query_history
    WHERE start_time between '{s}' and '{e}'
        AND EXECUTION_STATUS = 'SUCCESS'
        AND CREDITS_USED_COMPUTE > 0
)
SELECT 
    *,
    ROUND(GB_SCANNED/NULLIF(ROWS_PRODUCED, 0), 4) as GB_PER_ROW,
    ROUND(QUERY_CREDITS/NULLIF(ROWS_PRODUCED, 0), 6) as CREDITS_PER_ROW
FROM user_query_costs
ORDER BY QUERY_CREDITS DESC
LIMIT 100
"""
expensive_queries_df = run_query(expensive_queries_sql)

# Create visualization for expensive queries
fig_expensive_queries = px.scatter(
    expensive_queries_df,
    x='EXECUTION_SEC',
    y='QUERY_CREDITS',
    color='WAREHOUSE_NAME',
    size='GB_SCANNED',
    hover_data=['USER_NAME', 'QUERY_TYPE', 'GB_PER_ROW', 'CREDITS_PER_ROW', 'CACHE_HIT_RATIO'],
    title="Most Expensive Queries Analysis"
)

#############################################
#     Cost Optimization Opportunities
#############################################
optimization_opps_sql = f"""
WITH warehouse_metrics AS (
    SELECT 
        WAREHOUSE_NAME,
        COUNT(*) as QUERY_COUNT,
        SUM(CASE WHEN BYTES_SPILLED_TO_REMOTE_STORAGE > 0 THEN 1 ELSE 0 END) as SPILLING_QUERIES,
        AVG(CASE WHEN EXECUTION_TIME > 0 
            THEN QUEUED_PROVISIONING_TIME::FLOAT / EXECUTION_TIME 
            ELSE 0 END) * 100 as AVG_QUEUE_RATIO,
        AVG(PERCENTAGE_SCANNED_FROM_CACHE) as AVG_CACHE_HIT,
        SUM(CREDITS_USED_COMPUTE + CREDITS_USED_CLOUD_SERVICES) as TOTAL_CREDITS,
        COUNT(DISTINCT USER_NAME) as UNIQUE_USERS
    FROM snowflake.account_usage.query_history
    WHERE start_time between '{s}' and '{e}'
    GROUP BY 1
)
SELECT 
    *,
    ROUND(SPILLING_QUERIES::FLOAT / NULLIF(QUERY_COUNT, 0) * 100, 2) as SPILL_PERCENTAGE,
    ROUND(TOTAL_CREDITS / NULLIF(QUERY_COUNT, 0), 4) as CREDITS_PER_QUERY
FROM warehouse_metrics
ORDER BY TOTAL_CREDITS DESC
"""
optimization_opps_df = run_query(optimization_opps_sql)

# Create visualization for optimization opportunities
fig_optimization = px.scatter(
    optimization_opps_df,
    x='SPILL_PERCENTAGE',
    y='AVG_QUEUE_RATIO',
    size='TOTAL_CREDITS',
    color='AVG_CACHE_HIT',
    hover_data=['WAREHOUSE_NAME', 'QUERY_COUNT', 'CREDITS_PER_QUERY'],
    title="Warehouse Optimization Opportunities"
)

#############################################
#     User Cost Impact Analysis
#############################################
user_impact_sql = f"""
WITH user_costs AS (
    SELECT 
        USER_NAME,
        WAREHOUSE_NAME,
        COUNT(*) as QUERY_COUNT,
        SUM(CREDITS_USED_COMPUTE + CREDITS_USED_CLOUD_SERVICES) as TOTAL_CREDITS,
        AVG(TOTAL_ELAPSED_TIME/1000) as AVG_EXECUTION_SEC,
        SUM(BYTES_SCANNED)/POWER(1024,3) as TOTAL_GB_SCANNED,
        COUNT(DISTINCT DATABASE_NAME || '.' || SCHEMA_NAME || '.' || TABLE_NAME) as DISTINCT_TABLES_ACCESSED
    FROM snowflake.account_usage.query_history
    WHERE start_time between '{s}' and '{e}'
    GROUP BY 1, 2
)
SELECT 
    *,
    ROUND(TOTAL_CREDITS/NULLIF(QUERY_COUNT, 0), 4) as CREDITS_PER_QUERY,
    ROUND(TOTAL_GB_SCANNED/NULLIF(QUERY_COUNT, 0), 2) as GB_SCANNED_PER_QUERY
FROM user_costs
ORDER BY TOTAL_CREDITS DESC
"""
user_impact_df = run_query(user_impact_sql)

# Create visualization for user impact
fig_user_impact = px.scatter(
    user_impact_df,
    x='QUERY_COUNT',
    y='TOTAL_CREDITS',
    color='WAREHOUSE_NAME',
    size='TOTAL_GB_SCANNED',
    hover_data=['USER_NAME', 'CREDITS_PER_QUERY', 'GB_SCANNED_PER_QUERY', 'DISTINCT_TABLES_ACCESSED'],
    title="User Cost Impact Analysis"
)

# Display the visualizations
st.subheader("Cost Optimization Analysis")

# Table and Warehouse Costs
st.plotly_chart(fig_table_costs, use_container_width=True)

# Expensive Queries
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig_expensive_queries, use_container_width=True)
with col2:
    st.plotly_chart(fig_optimization, use_container_width=True)

# User Impact
st.plotly_chart(fig_user_impact, use_container_width=True)

# Add cost-saving recommendations
st.subheader("Cost Optimization Recommendations")

# Table Storage Recommendations
high_storage_tables = table_warehouse_cost_df[
    table_warehouse_cost_df['BYTES_PER_ROW'] > table_warehouse_cost_df['BYTES_PER_ROW'].median() * 2
]
if not high_storage_tables.empty:
    st.write("### Storage Optimization Opportunities")
    st.write("""
    Tables with high storage cost per row (potential optimization targets):
    """)
    for _, row in high_storage_tables.head().iterrows():
        st.write(f"- {row['DATABASE_NAME']}.{row['SCHEMA_NAME']}.{row['TABLE_NAME']}")
        st.write(f"  * {row['BYTES_PER_ROW']} bytes/row (vs median {table_warehouse_cost_df['BYTES_PER_ROW'].median():.2f})")

# Query Optimization Recommendations
high_cost_queries = expensive_queries_df[
    expensive_queries_df['CREDITS_PER_ROW'] > expensive_queries_df['CREDITS_PER_ROW'].median() * 3
]
if not high_cost_queries.empty:
    st.write("### Query Cost Optimization Opportunities")
    st.write("""
    Users and warehouses with expensive queries:
    """)
    for _, row in high_cost_queries.head().iterrows():
        st.write(f"- User: {row['USER_NAME']} on {row['WAREHOUSE_NAME']}")
        st.write(f"  * {row['CREDITS_PER_ROW']} credits/row")
        st.write(f"  * Query type: {row['QUERY_TYPE']}")

# Warehouse Optimization
high_spill_warehouses = optimization_opps_df[
    optimization_opps_df['SPILL_PERCENTAGE'] > 10
]
if not high_spill_warehouses.empty:
    st.write("### Warehouse Optimization Opportunities")
    st.write("""
    Warehouses with high spilling rates:
    """)
    for _, row in high_spill_warehouses.iterrows():
        st.write(f"- {row['WAREHOUSE_NAME']}")
        st.write(f"  * Spill rate: {row['SPILL_PERCENTAGE']}%")
        st.write(f"  * Queue ratio: {row['AVG_QUEUE_RATIO']:.2f}%")
