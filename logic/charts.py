import plotly.express as px
import plotly.graph_objects as go

# Professional Color Palette
PRIMARY_COLOR = "#007BFF"
SECONDARY_COLOR = "#6C757D"
ACCENT_COLOR = "#28A745"
BACKGROUND_COLOR = "rgba(0,0,0,0)"
GRID_COLOR = "rgba(128,128,128,0.2)"

def update_layout(fig, title):
    """Applies a consistent professional theme to the figure."""
    fig.update_layout(
        title=dict(text=title, font=dict(size=18, family="Arial, sans-serif", color="#333")),
        plot_bgcolor=BACKGROUND_COLOR,
        paper_bgcolor=BACKGROUND_COLOR,
        font=dict(family="Arial, sans-serif", color="#333"),
        xaxis=dict(showgrid=True, gridcolor=GRID_COLOR, zeroline=False),
        yaxis=dict(showgrid=True, gridcolor=GRID_COLOR, zeroline=False),
        margin=dict(l=20, r=20, t=50, b=20),
        hovermode="x unified"
    )
    return fig

def generate_correlation_heatmap(df, numeric_cols):
    """Generates a correlation heatmap."""
    if len(numeric_cols) < 2: return None
    corr = df[numeric_cols].corr()
    fig = px.imshow(corr, text_auto=".2f", aspect="auto", color_continuous_scale='RdBu_r')
    return update_layout(fig, "Correlation Heatmap")

def generate_distribution_chart(df, col):
    """Generates a histogram."""
    fig = px.histogram(df, x=col, nbins=30, color_discrete_sequence=[PRIMARY_COLOR])
    fig.update_traces(marker_line_width=0, opacity=0.8)
    return update_layout(fig, f"Distribution of {col}")

def generate_bar_chart(df, cat_col, num_col):
    """Generates a bar chart."""
    data = df.groupby(cat_col)[num_col].sum().reset_index().sort_values(num_col, ascending=False).head(15)
    fig = px.bar(data, x=cat_col, y=num_col, color_discrete_sequence=[PRIMARY_COLOR])
    fig.update_traces(marker_line_width=0, opacity=0.9)
    return update_layout(fig, f"Top {num_col} by {cat_col}")

def generate_line_chart(df, date_col, num_col):
    """Generates a line chart for time series."""
    data = df.groupby(date_col)[num_col].sum().reset_index().sort_values(date_col)
    fig = px.line(data, x=date_col, y=num_col, markers=True)
    fig.update_traces(line_color=PRIMARY_COLOR, line_width=2, marker_size=6)
    return update_layout(fig, f"{num_col} Trend over {date_col}")

def generate_scatter_chart(df, num_col_x, num_col_y, color_col=None):
    """Generates a scatter plot."""
    fig = px.scatter(df, x=num_col_x, y=num_col_y, color=color_col, color_discrete_sequence=px.colors.qualitative.Prism)
    fig.update_traces(marker=dict(size=8, opacity=0.7, line=dict(width=1, color='DarkSlateGrey')))
    return update_layout(fig, f"{num_col_y} vs {num_col_x}")

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
