import re

class AnalysisRequest:
    def __init__(self, action, target_cols, chart_type=None):
        self.action = action 
        self.target_cols = target_cols
        self.chart_type = chart_type

def parse_query(query, numeric_cols, categorical_cols, date_cols):
    """
    Parses a natural language query and returns an AnalysisRequest.
    """
    query = query.lower()
    all_cols = numeric_cols + categorical_cols + date_cols
    found_cols = [col for col in all_cols if col.replace('_', ' ') in query or col in query]
    
    if 'trend' in query or 'over time' in query:
        if date_cols and (found_cols or numeric_cols):
             target = [c for c in found_cols if c in numeric_cols]
             if not target and numeric_cols: target = [numeric_cols[0]]
             return AnalysisRequest('plot', target + [date_cols[0]], 'line')
             
    if 'correlation' in query:
        return AnalysisRequest('plot', numeric_cols, 'heatmap')
        
    if 'distribution' in query:
        target = [c for c in found_cols if c in numeric_cols]
        if target: return AnalysisRequest('plot', target, 'hist')
            
    if 'compare' in query or 'bar' in query:
        cat_target = [c for c in found_cols if c in categorical_cols]
        num_target = [c for c in found_cols if c in numeric_cols]
        if cat_target and num_target: return AnalysisRequest('plot', [cat_target[0], num_target[0]], 'bar')
             
    if 'average' in query or 'mean' in query:
        target = [c for c in found_cols if c in numeric_cols]
        if target: return AnalysisRequest('stat', target, 'mean')
            
    if 'sum' in query or 'total' in query:
        target = [c for c in found_cols if c in numeric_cols]
        if target: return AnalysisRequest('stat', target, 'sum')

    return None
