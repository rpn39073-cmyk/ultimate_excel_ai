import streamlit as st
import pandas as pd
import io
import os
import plotly.express as px

# Import Local Logic
from ultimate_excel_ai.logic import data, ml, analysis, charts, nlu, export
# Import API Client
from ultimate_excel_ai.ui.api_client import APIClient

APP_MODE = 'SAAS' if os.getenv('API_URL') else 'LOCAL'
if APP_MODE == 'SAAS':
    api = APIClient(os.getenv('API_URL'))

def render_dashboard():
    # Sidebar
    st.sidebar.markdown(f"## 📊 Excel AI ({APP_MODE})")
    
    # Theme Customizer
    with st.sidebar.expander("🎨 Theme Customizer", expanded=False):
        t_primary = st.color_picker("Primary Color", st.session_state.get('theme_primary', '#00D2FF'))
        t_bg = st.color_picker("Background", st.session_state.get('theme_bg', '#0E1117'))
        t_card = st.color_picker("Card Background", st.session_state.get('theme_card_bg', '#1E2127'))
        t_text = st.color_picker("Text Color", st.session_state.get('theme_text', '#FAFAFA'))
        
        if st.button("Apply Theme"):
            st.session_state['theme_primary'] = t_primary
            st.session_state['theme_bg'] = t_bg
            st.session_state['theme_card_bg'] = t_card
            st.session_state['theme_text'] = t_text
            st.rerun()
            
    theme_dict = {
        "primary": st.session_state.get('theme_primary', '#00D2FF'),
        "bg": st.session_state.get('theme_bg', '#0E1117'),
        "card": st.session_state.get('theme_card_bg', '#1E2127'),
        "text": st.session_state.get('theme_text', '#FAFAFA'),
        "grid": "rgba(255,255,255,0.1)" if st.session_state.get('theme_bg', '#0E1117') < '#888888' else "rgba(0,0,0,0.1)"
    }
    
    st.sidebar.divider()

    uploaded_file = st.sidebar.file_uploader("Upload Excel/CSV", type=['csv', 'xlsx', 'xls'])
    
    if uploaded_file:
        # Load & Process
        if 'df' not in st.session_state or st.session_state.get('last_file') != uploaded_file.name:
            with st.spinner("Processing Data..."):
                if APP_MODE == 'LOCAL':
                    df, msg = data.load_data(uploaded_file, uploaded_file.name)
                    if df is not None:
                        df, num, cat, date, stats = data.process_data(df)
                        st.session_state['raw_df'] = df
                        st.session_state['num'] = num
                        st.session_state['cat'] = cat
                        st.session_state['date'] = date
                        st.session_state['clean_stats'] = stats
                        st.session_state['filename'] = uploaded_file.name
                        st.session_state['last_file'] = uploaded_file.name
                        st.sidebar.success(f"Loaded {len(df)} rows!")
                    else:
                        st.sidebar.error(msg)
                        return
                else:
                    uploaded_file.seek(0)
                    resp = api.upload_file(uploaded_file, uploaded_file.name)
                    if "error" not in resp:
                        uploaded_file.seek(0)
                        df, _ = data.load_data(uploaded_file, uploaded_file.name)
                        df, num, cat, date, stats = data.process_data(df)
                        
                        st.session_state['raw_df'] = df
                        st.session_state['num'] = num
                        st.session_state['cat'] = cat
                        st.session_state['date'] = date
                        st.session_state['clean_stats'] = stats
                        st.session_state['filename'] = uploaded_file.name
                        st.session_state['last_file'] = uploaded_file.name
                        st.sidebar.success(f"Uploaded to Cloud! ({len(df)} rows)")
                    else:
                        st.sidebar.error(f"Upload Failed: {resp['error']}")
                        return

        raw_df = st.session_state['raw_df']
        num_cols = st.session_state['num']
        cat_cols = st.session_state['cat']
        date_cols = st.session_state['date']
        filename = st.session_state.get('filename')
        
        # SLICERS (Filters)
        st.sidebar.markdown("### 🎛️ Filters (Slicers)")
        filtered_df = raw_df.copy()
        
        # Dynamically create slicers for top 3 categorical columns
        slicer_cols = cat_cols[:3] if len(cat_cols) > 0 else []
        for col in slicer_cols:
            unique_vals = raw_df[col].dropna().unique().tolist()
            if len(unique_vals) < 50: # Only if manageable number of unique values
                selected_vals = st.sidebar.multiselect(f"Filter {col}", unique_vals, default=[])
                if selected_vals:
                    filtered_df = filtered_df[filtered_df[col].isin(selected_vals)]
                    
        st.session_state['df'] = filtered_df
        df = filtered_df
        
        # Tabs
        tabs = st.tabs(["📊 Dashboard", "🔮 Predictive Analytics", "💡 Smart Insights", "💬 Data Chat", "📥 Reports"])
        
        # 1. Overview Dashboard (Power BI Style Blinkit Layout)
        with tabs[0]:
            # Main layout: Left (40%) and Right (60%)
            col_left, col_right = st.columns([4, 6], gap="small")
            
            with col_left:
                # 4 KPIs in 2x2 grid
                k1, k2 = st.columns(2)
                with k1:
                    primary_val = f"${df[num_cols[0]].sum():,.2f}" if num_cols else f"{len(df):,}"
                    primary_label = f"TOTAL {num_cols[0]}" if num_cols else "TOTAL ROWS"
                    st.markdown(f"""
                    <div class="metric-card" style="background: linear-gradient(135deg, #FAD02C 0%, #FFFFFF 100%);">
                        <h3>{primary_label}</h3>
                        <h2>{primary_val}</h2>
                    </div>""", unsafe_allow_html=True)
                with k2:
                    avg_val = f"${df[num_cols[0]].mean():,.2f}" if num_cols and not df.empty else "N/A"
                    avg_label = f"AVG {num_cols[0]}" if num_cols else "AVG ROWS"
                    st.markdown(f"""<div class="metric-card"><h3>{avg_label}</h3><h2>{avg_val}</h2></div>""", unsafe_allow_html=True)
                
                st.write("") # small gap
                k3, k4 = st.columns(2)
                with k3:
                    st.markdown(f"""<div class="metric-card"><h3>NO OF ITEMS</h3><h2>{len(df):,}</h2></div>""", unsafe_allow_html=True)
                with k4:
                    sec_metric = f"AVG {num_cols[1]}" if len(num_cols) > 1 else "CATEGORIES"
                    sec_val = f"{df[num_cols[1]].mean():.1f}" if len(num_cols) > 1 and not df.empty else str(len(cat_cols))
                    st.markdown(f"""<div class="metric-card"><h3>{sec_metric}</h3><h2>{sec_val}</h2></div>""", unsafe_allow_html=True)
                
                st.markdown("<hr style='margin: 1rem 0; opacity: 0.2;'/>", unsafe_allow_html=True)
                
                # Bottom Left: Donut Chart and Horizontal Bar Chart
                if len(cat_cols) > 0 and len(num_cols) > 0:
                    cat1 = cat_cols[0]
                    num1 = num_cols[0]
                    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                    st.plotly_chart(charts.generate_donut_chart(df, cat1, num1, theme_dict), use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    st.write("")
                    
                    cat2 = cat_cols[1] if len(cat_cols) > 1 else cat_cols[0]
                    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                    st.plotly_chart(charts.generate_horizontal_bar_chart(df, cat2, num1, theme_dict), use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)

            with col_right:
                # Top Right: Wide Area Chart
                if len(date_cols) > 0 and len(num_cols) > 0:
                    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                    st.plotly_chart(charts.generate_area_chart(df, date_cols[0], num_cols[0], theme_dict), use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                elif len(num_cols) > 0 and len(cat_cols) > 0:
                    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                    st.plotly_chart(charts.generate_line_chart(df, cat_cols[0], num_cols[0], theme_dict), use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                
                st.write("")
                
                # Middle Right: Donut and Funnel
                if len(cat_cols) > 2 and len(num_cols) > 0:
                    r1, r2 = st.columns(2)
                    with r1:
                        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                        st.plotly_chart(charts.generate_donut_chart(df, cat_cols[2], num_cols[0], theme_dict), use_container_width=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                    with r2:
                        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                        st.plotly_chart(charts.generate_funnel_chart(df, cat_cols[2], num_cols[0], theme_dict), use_container_width=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                
                st.write("")
                
                # Bottom Right: Data Tutorials Table
                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                st.markdown("<h3 style='text-align:center; opacity:0.5;'>DATA PREVIEW</h3>", unsafe_allow_html=True)
                if not df.empty:
                    # Style the dataframe with data bars for numeric columns
                    styled_df = df.head(10).style
                    for col in num_cols:
                        styled_df = styled_df.bar(subset=[col], color=theme_dict['primary'])
                    st.dataframe(styled_df, use_container_width=True, hide_index=True)
                st.markdown('</div>', unsafe_allow_html=True)

        # 2. Predictive Analytics
        with tabs[1]:
            st.header("Predictive Analytics")
            
            if date_cols and num_cols:
                st.subheader("Forecast")
                d_col = st.selectbox("Date Column", date_cols)
                t_col = st.selectbox("Target Column", num_cols)
                days = st.slider("Days to Forecast", 7, 365, 30)
                
                if st.button("Generate Forecast"):
                    if APP_MODE == 'LOCAL':
                        engine = ml.MachineLearningEngine()
                        f_df = engine.forecast_series(df, d_col, t_col, days)
                    else:
                        resp = api.forecast(filename, d_col, t_col, days)
                        if "error" not in resp:
                            f_df = pd.DataFrame(resp['forecast'])
                        else:
                            st.error(resp['error'])
                            f_df = None
                            
                    if f_df is not None:
                        st.session_state['forecast_df'] = f_df
                        st.plotly_chart(charts.generate_line_chart(f_df, 'Date', f_df.columns[1], theme_dict), use_container_width=True)
                    else: st.error("Not enough data to forecast.")
            
            st.divider()
            
            # Anomaly
            st.subheader("Anomaly Detection")
            if st.button("Detect Anomalies"):
                if APP_MODE == 'LOCAL':
                    engine = ml.MachineLearningEngine()
                    df_anom = engine.detect_anomalies(df.copy(), num_cols)
                    anoms = df_anom
                else:
                    resp = api.detect_anomalies(filename)
                    if "error" not in resp:
                        anoms = df.copy() 
                        engine = ml.MachineLearningEngine()
                        anoms = engine.detect_anomalies(df.copy(), num_cols)
                    else:
                        st.error(resp['error'])
                        anoms = None
                
                if anoms is not None:
                    st.session_state['anomaly_df'] = anoms
                    st.write(f"Detected {anoms['Is_Anomaly'].sum()} anomalies.")
                    if len(num_cols) >= 2:
                        st.plotly_chart(charts.generate_scatter_chart(anoms, num_cols[0], num_cols[1], 'Is_Anomaly', theme_dict), use_container_width=True)

        # 3. Smart Insights
        with tabs[2]:
            st.markdown("### 💡 AI Data Insights")
            if APP_MODE == 'LOCAL':
                insights = analysis.generate_insights(df, num_cols, date_cols)
            else:
                resp = api.analyze(filename)
                insights = resp.get('insights', []) if "error" not in resp else [resp['error']]
            
            for i, insight in enumerate(insights):
                st.markdown(f"""
                <div class="metric-card" style="text-align: left; margin-bottom: 1rem;">
                    <strong>Insight {i+1}:</strong> {insight}
                </div>
                """, unsafe_allow_html=True)

        # 4. Data Chat
        with tabs[3]:
            st.header("Chat with Data")
            q = st.text_input("Ask a question (e.g. 'trend of sales' or 'distribution of profit')...")
            if q:
                req = nlu.parse_query(q, num_cols, cat_cols, date_cols)
                if req:
                    st.success(f"Action: {req.action}, Chart: {req.chart_type}, Cols: {req.target_cols}")
                    if req.action == 'plot':
                        if req.chart_type == 'line': st.plotly_chart(charts.generate_line_chart(df, req.target_cols[1], req.target_cols[0], theme_dict), use_container_width=True)
                        elif req.chart_type == 'bar': st.plotly_chart(charts.generate_bar_chart(df, req.target_cols[0], req.target_cols[1], theme_dict), use_container_width=True)
                        elif req.chart_type == 'hist': st.plotly_chart(charts.generate_distribution_chart(df, req.target_cols[0], theme_dict), use_container_width=True)
                        elif req.chart_type == 'heatmap': st.plotly_chart(charts.generate_correlation_heatmap(df, num_cols, theme_dict), use_container_width=True)
                else: st.warning("I didn't understand the query.")

        # 5. Reports
        with tabs[4]:
            st.header("Export Reports")
            from ultimate_excel_ai.logic import pivots
            
            pivot_data = pivots.generate_pivot_tables(df, num_cols, cat_cols, date_cols)
            insights = analysis.generate_insights(df, num_cols, date_cols)
            
            excel_data = export.generate_excel_report(
                df, pivot_data, 
                st.session_state.get('forecast_df'),
                st.session_state.get('anomaly_df'),
                st.session_state.get('model_metrics'),
                insights
            )
            
            st.download_button("📥 Download Excel Report", excel_data, "power_bi_report.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    else:
        st.markdown(f"""
        <div style="text-align:center; padding: 5rem 0;">
            <h1 style="color:{theme_dict['primary']} !important; font-size:4rem;">📊</h1>
            <h2>Welcome to Ultimate Excel AI</h2>
            <p style="opacity:0.7">Upload your Excel or CSV file in the sidebar to generate a stunning Power BI style dashboard instantly.</p>
        </div>
        """, unsafe_allow_html=True)
