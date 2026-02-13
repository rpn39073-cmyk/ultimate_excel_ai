import plotly.express as px

def generate_correlation_heatmap(df, numeric_cols):
    """Generates a correlation heatmap."""
    if len(numeric_cols) < 2: return None
    corr = df[numeric_cols].corr()
    fig = px.imshow(corr, text_auto=True, aspect="auto", color_continuous_scale='RdBu_r', title="Correlation Heatmap")
    return fig

def generate_distribution_chart(df, col):
    """Generates a histogram."""
    return px.histogram(df, x=col, title=f"Distribution of {col}", nbins=30)

def generate_bar_chart(df, cat_col, num_col):
    """Generates a bar chart."""
    data = df.groupby(cat_col)[num_col].sum().reset_index()
    return px.bar(data, x=cat_col, y=num_col, title=f"{num_col} by {cat_col}")

def generate_line_chart(df, date_col, num_col):
    """Generates a line chart for time series."""
    data = df.sort_values(date_col)
    return px.line(data, x=date_col, y=num_col, title=f"{num_col} Trend over {date_col}")

def generate_scatter_chart(df, num_col_x, num_col_y, color_col=None):
    """Generates a scatter plot."""
    return px.scatter(df, x=num_col_x, y=num_col_y, color=color_col, title=f"{num_col_y} vs {num_col_x}")

def suggest_charts(df, numeric_cols, categorical_cols, date_cols):
    """Returns a list of suggested chart configurations."""
    suggestions = []
    if len(numeric_cols) > 1:
        suggestions.append({'type': 'heatmap', 'title': 'Correlation Matrix'})
    if date_cols and numeric_cols:
        suggestions.append({'type': 'line', 'x': date_cols[0], 'y': numeric_cols[0], 'title': f"{numeric_cols[0]} Trend"})
    if categorical_cols and numeric_cols:
        suggestions.append({'type': 'bar', 'x': categorical_cols[0], 'y': numeric_cols[0], 'title': f"{numeric_cols[0]} by {categorical_cols[0]}"})
    if numeric_cols:
        suggestions.append({'type': 'hist', 'x': numeric_cols[0], 'title': f"Dist of {numeric_cols[0]}"})
    return suggestions
