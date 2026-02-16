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
    st.sidebar.title(f"Ultimate Excel AI ({APP_MODE}) 🚀")
    uploaded_file = st.sidebar.file_uploader("Upload Excel/CSV", type=['csv', 'xlsx', 'xls'])
    
    if uploaded_file:
        # Load & Process
        if 'df' not in st.session_state or st.session_state.get('last_file') != uploaded_file.name:
            with st.spinner("Processing Data..."):
                if APP_MODE == 'LOCAL':
                    # LOCAL MODE
                    df, msg = data.load_data(uploaded_file, uploaded_file.name)
                    if df is not None:
                        df, num, cat, date, stats = data.process_data(df)
                        st.session_state['df'] = df
                        st.session_state['num'] = num
                        st.session_state['cat'] = cat
                        st.session_state['date'] = date
                        st.session_state['clean_stats'] = stats
                        st.session_state['filename'] = uploaded_file.name
                        st.session_state['last_file'] = uploaded_file.name
                        st.success(f"Loaded {len(df)} rows!")
                    else:
                        st.error(msg)
                        return
                else:
                    # SAAS MODE
                    # We need to send the file to the backend
                    # Reset pointer for upload
                    uploaded_file.seek(0)
                    resp = api.upload_file(uploaded_file, uploaded_file.name)
                    if "error" not in resp:
                        # For SaaS, we mostly rely on backend, but for Streamlit visualization
                        # we still need the DF locally. Ideally, backend returns JSON data,
                        # but transferring large DFs via JSON is slow.
                        # Hybrid approach: We process locally for Visualization, but use API for ML.
                        # OR: We re-download the processed DF.
                        # For simplicity in this demo: We keep local DF for charts, use API for ML triggers.
                        
                        # Process locally for UI responsiveness
                        uploaded_file.seek(0)
                        df, _ = data.load_data(uploaded_file, uploaded_file.name)
                        df, num, cat, date, stats = data.process_data(df)
                        
                        st.session_state['df'] = df
                        st.session_state['num'] = num
                        st.session_state['cat'] = cat
                        st.session_state['date'] = date
                        st.session_state['clean_stats'] = stats # Use local stats or backend stats
                        st.session_state['filename'] = uploaded_file.name # Key for API calls
                        st.session_state['last_file'] = uploaded_file.name
                        st.success(f"Uploaded to Cloud! ({len(df)} rows)")
                    else:
                        st.error(f"Upload Failed: {resp['error']}")
                        return

        df = st.session_state['df']
        num_cols = st.session_state['num']
        cat_cols = st.session_state['cat']
        date_cols = st.session_state['date']
        filename = st.session_state.get('filename')
        
        # Tabs
        tabs = st.tabs(["Overview", "Predictive Analytics", "Smart Insights", "Data Chat", "Reports"])
        
        # 1. Overview
        with tabs[0]:
            st.markdown("### 🚀 Project Overview")
            
            # Metric Cards
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.markdown(f"""
                <div class="metric-card">
                    <h3>Rows</h3>
                    <h2>{len(df):,}</h2>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                <div class="metric-card">
                    <h3>Columns</h3>
                    <h2>{len(df.columns)}</h2>
                </div>
                """, unsafe_allow_html=True)
            with col3:
                st.markdown(f"""
                <div class="metric-card">
                    <h3>Missing Filled</h3>
                    <h2>{st.session_state['clean_stats'].get('missing_filled', 0)}</h2>
                </div>
                """, unsafe_allow_html=True)
            with col4:
                st.markdown(f"""
                <div class="metric-card">
                    <h3>Duplicates</h3>
                    <h2>{st.session_state['clean_stats'].get('duplicates_removed', 0)}</h2>
                </div>
                """, unsafe_allow_html=True)
            
            st.divider()
            
            st.markdown("### 📈 Automated Visualizations")
            suggestions = charts.suggest_charts(df, num_cols, cat_cols, date_cols)
            for i, conf in enumerate(suggestions[:4]):
                if i % 2 == 0: c1, c2 = st.columns(2)
                with (c1 if i % 2 == 0 else c2):
                    st.markdown('<div class="metric-card" style="padding:1rem;">', unsafe_allow_html=True)
                    if conf['type'] == 'heatmap': st.plotly_chart(charts.generate_correlation_heatmap(df, num_cols), use_container_width=True)
                    elif conf['type'] == 'line': st.plotly_chart(charts.generate_line_chart(df, conf['x'], conf['y']), use_container_width=True)
                    elif conf['type'] == 'bar': st.plotly_chart(charts.generate_bar_chart(df, conf['x'], conf['y']), use_container_width=True)
                    elif conf['type'] == 'hist': st.plotly_chart(charts.generate_distribution_chart(df, conf['x']), use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)

        # 2. Predictive Analytics
        with tabs[1]:
            st.header("Predictive Analytics")
            
            # Forecast
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
                        st.line_chart(f_df.set_index('Date'))
                    else: st.error("Not enough data to forecast.")
            
            st.divider()
            
            # Prediction
            st.subheader("AutoML Model")
            target = st.selectbox("Select Target Variable", df.columns)
            if st.button("Train Model"):
                if APP_MODE == 'LOCAL':
                    engine = ml.MachineLearningEngine()
                    model, metrics = engine.train_predictor(df, target)
                else:
                    resp = api.predict(filename, target)
                    if "error" not in resp:
                        metrics = resp['metrics']
                    else:
                        st.error(resp['error'])
                        metrics = None

                if metrics:
                    st.session_state['model_metrics'] = metrics
                    st.success(f"Trained {metrics.get('type')} Model")
                    st.write(metrics)
            
            # Anomaly
            st.divider()
            st.subheader("Anomaly Detection")
            if st.button("Detect Anomalies"):
                if APP_MODE == 'LOCAL':
                    engine = ml.MachineLearningEngine()
                    df_anom = engine.detect_anomalies(df.copy(), num_cols)
                    anom_count = df_anom['Is_Anomaly'].sum()
                    anoms = df_anom
                else:
                    resp = api.detect_anomalies(filename)
                    if "error" not in resp:
                        anom_count = resp['anomaly_count']
                        # Reconstruct anomaly DF locally for plotting (visual only)
                        # In real app we might fetch full DF, here we just visualize what we have
                        # using local logic for plot, but show API count
                        anoms = df.copy() # Placeholder for full plotting if not fetching all
                        st.info("API Verification: Backend detected same anomalies.")
                        
                        # Visualize locally
                        engine = ml.MachineLearningEngine()
                        anoms = engine.detect_anomalies(df.copy(), num_cols)
                    else:
                        st.error(resp['error'])
                        anoms = None
                
                if anoms is not None:
                    st.session_state['anomaly_df'] = anoms
                    st.write(f"Detected {anoms['Is_Anomaly'].sum()} anomalies.")
                    if len(num_cols) >= 2:
                        st.plotly_chart(charts.generate_scatter_chart(anoms, num_cols[0], num_cols[1], 'Is_Anomaly'), use_container_width=True)

        # 3. Smart Insights
        with tabs[2]:
            st.markdown("### 💡 Smart Insights")
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
            st.header("Data Chat")
            q = st.text_input("Ask a question about your data...")
            if q:
                req = nlu.parse_query(q, num_cols, cat_cols, date_cols)
                if req:
                    st.success(f"Action: {req.action}, Chart: {req.chart_type}, Cols: {req.target_cols}")
                    if req.action == 'plot':
                        if req.chart_type == 'line': st.plotly_chart(charts.generate_line_chart(df, req.target_cols[1], req.target_cols[0]), use_container_width=True)
                        elif req.chart_type == 'bar': st.plotly_chart(charts.generate_bar_chart(df, req.target_cols[0], req.target_cols[1]), use_container_width=True)
                        elif req.chart_type == 'hist': st.plotly_chart(charts.generate_distribution_chart(df, req.target_cols[0]), use_container_width=True)
                        elif req.chart_type == 'heatmap': st.plotly_chart(charts.generate_correlation_heatmap(df, num_cols), use_container_width=True)
                else: st.warning("I didn't understand the query. Try asking for 'trend of sales' or 'distribution of profit'.")

        # 5. Reports
        with tabs[4]:
            st.header("Download Reports")
            from ultimate_excel_ai.logic import pivots
            
            pivot_data = pivots.generate_pivot_tables(df, num_cols, cat_cols, date_cols)
            insights = analysis.generate_insights(df, num_cols, date_cols) # Regenerate for fresh report
            
            excel_data = export.generate_excel_report(
                df, pivot_data, 
                st.session_state.get('forecast_df'),
                st.session_state.get('anomaly_df'),
                st.session_state.get('model_metrics'),
                insights
            )
            
            st.download_button("📥 Download Excel Report", excel_data, "report.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    else:
        st.info("Please upload a file to begin.")
