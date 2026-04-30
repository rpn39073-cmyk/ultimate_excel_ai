import plotly.express as px
import plotly.graph_objects as go

def update_layout(fig, title, theme=None):
    """Applies a consistent theme to the figure based on user settings."""
    if theme is None:
        theme = {
            "primary": "#007BFF",
            "bg": "rgba(0,0,0,0)",
            "text": "#333333",
            "grid": "rgba(128,128,128,0.2)"
        }
        
    fig.update_layout(
        title=dict(text=title, font=dict(size=18, family="Arial, sans-serif", color=theme["text"])),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Arial, sans-serif", color=theme["text"]),
        xaxis=dict(showgrid=True, gridcolor=theme["grid"], zeroline=False),
        yaxis=dict(showgrid=True, gridcolor=theme["grid"], zeroline=False),
        margin=dict(l=20, r=20, t=50, b=20),
        hovermode="x unified"
    )
    return fig

def generate_correlation_heatmap(df, numeric_cols, theme=None):
    """Generates a correlation heatmap."""
    if len(numeric_cols) < 2: return None
    corr = df[numeric_cols].corr()
    fig = px.imshow(corr, text_auto=".2f", aspect="auto", color_continuous_scale='RdBu_r')
    return update_layout(fig, "Correlation Heatmap", theme)

def generate_distribution_chart(df, col, theme=None):
    """Generates a histogram."""
    primary = theme["primary"] if theme else "#007BFF"
    fig = px.histogram(df, x=col, nbins=30, color_discrete_sequence=[primary])
    fig.update_traces(marker_line_width=0, opacity=0.8)
    return update_layout(fig, f"Distribution of {col}", theme)

def generate_bar_chart(df, cat_col, num_col, theme=None):
    """Generates a bar chart."""
    primary = theme["primary"] if theme else "#007BFF"
    data = df.groupby(cat_col)[num_col].sum().reset_index().sort_values(num_col, ascending=False).head(15)
    fig = px.bar(data, x=cat_col, y=num_col, color_discrete_sequence=[primary])
    fig.update_traces(marker_line_width=0, opacity=0.9)
    return update_layout(fig, f"Top {num_col} by {cat_col}", theme)

def generate_line_chart(df, date_col, num_col, theme=None):
    """Generates a line chart for time series."""
    primary = theme["primary"] if theme else "#007BFF"
    data = df.groupby(date_col)[num_col].sum().reset_index().sort_values(date_col)
    fig = px.line(data, x=date_col, y=num_col, markers=True)
    fig.update_traces(line_color=primary, line_width=2, marker_size=6)
    return update_layout(fig, f"{num_col} Trend over {date_col}", theme)

def generate_scatter_chart(df, num_col_x, num_col_y, color_col=None, theme=None):
    """Generates a scatter plot."""
    fig = px.scatter(df, x=num_col_x, y=num_col_y, color=color_col, color_discrete_sequence=px.colors.qualitative.Prism)
    fig.update_traces(marker=dict(size=8, opacity=0.7, line=dict(width=1, color='DarkSlateGrey')))
    return update_layout(fig, f"{num_col_y} vs {num_col_x}", theme)

def generate_donut_chart(df, cat_col, num_col, theme=None):
    """Generates a donut chart for composition."""
    data = df.groupby(cat_col)[num_col].sum().reset_index().sort_values(num_col, ascending=False).head(10)
    fig = px.pie(data, names=cat_col, values=num_col, hole=0.5, color_discrete_sequence=px.colors.qualitative.Set3)
    fig.update_traces(textposition='inside', textinfo='percent+label')
    return update_layout(fig, f"{num_col} Composition by {cat_col}", theme)

def suggest_charts(df, numeric_cols, categorical_cols, date_cols):
    """Returns a list of suggested chart configurations."""
    suggestions = []
    if len(numeric_cols) > 1:
        suggestions.append({'type': 'heatmap', 'title': 'Correlation Matrix'})
    if date_cols and numeric_cols:
        suggestions.append({'type': 'line', 'x': date_cols[0], 'y': numeric_cols[0], 'title': f"{numeric_cols[0]} Trend"})
    if categorical_cols and numeric_cols:
        suggestions.append({'type': 'bar', 'x': categorical_cols[0], 'y': numeric_cols[0], 'title': f"{numeric_cols[0]} by {categorical_cols[0]}"})
        if len(df[categorical_cols[0]].unique()) <= 15:
            suggestions.append({'type': 'donut', 'x': categorical_cols[0], 'y': numeric_cols[0], 'title': f"{numeric_cols[0]} Comp"})
    if numeric_cols:
        suggestions.append({'type': 'hist', 'x': numeric_cols[0], 'title': f"Dist of {numeric_cols[0]}"})
    return suggestions
