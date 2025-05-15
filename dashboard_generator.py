import pandas as pd
import datetime
from pathlib import Path
from dashboard import generate_charts

def generate_dashboard(prediction_df):
    dashboard_dir = Path('dashboard')
    dashboard_dir.mkdir(exist_ok=True)
    
    # Get the symbols
    symbols = prediction_df['symbol'].unique()
    
    # Generate charts for each symbol
    all_charts = {}
    for symbol in symbols:
        all_charts[symbol] = generate_charts(prediction_df, symbol)
    
    # Creates the HTML Dashboard
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Stock Price Predictions</title>
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
        <style>
            :root {{
                --primary: #6366f1;
                --primary-light: #818cf8;
                --primary-dark: #4f46e5;
                --success: #10b981;
                --warning: #f59e0b;
                --danger: #ef4444;
                --bg-dark: #0f172a;
                --bg-card: #1e293b;
                --text-primary: #f8fafc;
                --text-secondary: #94a3b8;
                --border: #334155;
                --border-light: #475569;
                --card-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
                --transition: all 0.3s ease;
            }}
            
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{
                font-family: 'Inter', sans-serif;
                background-color: var(--bg-dark);
                color: var(--text-primary);
                line-height: 1.6;
                min-height: 100vh;
                padding: 1rem;
            }}
            
            .container {{
                max-width: 1300px;
                margin: 0 auto;
                padding: 1.5rem;
            }}
            
            .header {{
                display: flex;
                flex-direction: column;
                align-items: center;
                margin-bottom: 2rem;
                text-align: center;
            }}
            
            .header h1 {{
                font-size: 2.5rem;
                font-weight: 700;
                margin-bottom: 0.75rem;
                background: linear-gradient(90deg, var(--primary) 0%, var(--primary-light) 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }}
            
            .last-updated {{
                color: var(--text-secondary);
                font-size: 0.875rem;
            }}
            
            .symbol-selector {{
                display: flex;
                justify-content: center;
                align-items: center;
                margin: 2rem 0;
            }}
            
            .symbol-selector label {{
                margin-right: 1rem;
                font-weight: 500;
            }}
            
            .symbol-selector select {{
                padding: 0.75rem 1.5rem;
                border-radius: 8px;
                border: 1px solid var(--border);
                background-color: var(--bg-card);
                color: var(--text-primary);
                font-size: 1rem;
                cursor: pointer;
                transition: var(--transition);
                outline: none;
                min-width: 150px;
            }}
            
            .symbol-selector select:hover, .symbol-selector select:focus {{
                border-color: var(--primary);
                box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2);
            }}
            
            .symbol-section {{
                display: none;
                animation: fadeIn 0.3s ease-in-out;
            }}
            
            .active-section {{
                display: block;
            }}
            
            .predictions-panel {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 1.5rem;
                margin-bottom: 2.5rem;
            }}
            
            .prediction-card {{
                background-color: var(--bg-card);
                border-radius: 1rem;
                padding: 1.5rem;
                box-shadow: var(--card-shadow);
                transition: var(--transition);
                display: flex;
                flex-direction: column;
                align-items: center;
                text-align: center;
                border: 1px solid var(--border);
            }}
            
            .prediction-card:hover {{
                transform: translateY(-5px);
                box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
                border-color: var(--primary);
            }}
            
            .prediction-card h3 {{
                margin-bottom: 0.75rem;
                font-weight: 600;
                font-size: 1.1rem;
                color: var(--text-secondary);
            }}
            
            .prediction-value {{
                font-size: 2rem;
                font-weight: 700;
                background: linear-gradient(90deg, var(--primary-light) 0%, var(--primary) 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }}
            
            .date-card .prediction-value {{
                background: linear-gradient(90deg, #60a5fa 0%, #3b82f6 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }}
            
            .lstm-card .prediction-value {{
                background: linear-gradient(90deg, #34d399 0%, #10b981 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }}
            
            .xgb-card .prediction-value {{
                background: linear-gradient(90deg, #a78bfa 0%, #8b5cf6 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }}
            
            .chart-section {{
                background-color: var(--bg-card);
                border-radius: 1rem;
                padding: 1.5rem;
                margin-bottom: 2rem;
                box-shadow: var(--card-shadow);
                border: 1px solid var(--border);
            }}
            
            .chart-section h3 {{
                margin-bottom: 1.5rem;
                font-size: 1.25rem;
                font-weight: 600;
                text-align: center;
                color: var(--text-primary);
            }}
            
            .chart-container {{
                display: flex;
                justify-content: center;
                max-width: 100%;
                overflow: hidden;
                border-radius: 0.5rem;
            }}
            
            .chart-container img {{
                max-width: 100%;
                height: auto;
                border-radius: 0.5rem;
                transition: var(--transition);
            }}
            
            table {{
                width: 100%;
                border-collapse: collapse;
                border-radius: 0.5rem;
                overflow: hidden;
                margin-top: 1rem;
                background-color: var(--bg-card);
                box-shadow: var(--card-shadow);
            }}
            
            thead {{
                background-color: rgba(99, 102, 241, 0.1);
            }}
            
            th {{
                padding: 1rem;
                text-align: left;
                font-weight: 600;
                color: var(--primary-light);
                border-bottom: 1px solid var(--border);
            }}
            
            td {{
                padding: 0.75rem 1rem;
                border-bottom: 1px solid var(--border-light);
            }}
            
            tbody tr:last-child td {{
                border-bottom: none;
            }}
            
            tbody tr {{
                transition: var(--transition);
            }}
            
            tbody tr:hover {{
                background-color: rgba(99, 102, 241, 0.05);
            }}
            
            .footer {{
                margin-top: 3rem;
                text-align: center;
                padding-top: 1.5rem;
                border-top: 1px solid var(--border);
                color: var(--text-secondary);
                font-size: 0.875rem;
            }}
            
            @keyframes fadeIn {{
                from {{ opacity: 0; transform: translateY(10px); }}
                to {{ opacity: 1; transform: translateY(0); }}
            }}
            
            .grid-layout {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(600px, 1fr));
                gap: 1.5rem;
            }}
            
            @media (max-width: 768px) {{
                .grid-layout {{
                    grid-template-columns: 1fr;
                }}
                
                .header h1 {{
                    font-size: 1.75rem;
                }}
                
                .predictions-panel {{
                    grid-template-columns: 1fr;
                }}
                
                .symbol-selector select {{
                    min-width: 120px;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <header class="header">
                <h1>Stock Price Prediction Dashboard</h1>
                <p class="last-updated">Last updated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}</p>
            </header>
            
            <div class="symbol-selector">
                <label for="symbolSelect">Select Stock Symbol:</label>
                <select id="symbolSelect" onchange="showSymbolSection()">
                    {' '.join([f'<option value="{s}">{s}</option>' for s in symbols])}
                </select>
            </div>
    """
    
    # Add the sections for each symbol
    for symbol in symbols:
        charts = all_charts[symbol]
        
        html_content += f"""
            <div id="{symbol}-section" class="symbol-section">
                <h2 style="text-align: center; margin-bottom: 2rem; color: var(--primary-light);">{symbol} Analysis & Predictions</h2>
        """
        
        # updates with the latest predictions
        if 'latest_date' in charts:
            html_content += f"""
                <div class="predictions-panel">
                    <div class="prediction-card date-card">
                        <h3>Prediction Date</h3>
                        <div class="prediction-value">{charts['latest_date']}</div>
                    </div>
                    <div class="prediction-card lstm-card">
                        <h3>LSTM Prediction</h3>
                        <div class="prediction-value">${charts['lstm_prediction']:.2f}</div>
                    </div>
                    <div class="prediction-card xgb-card">
                        <h3>XGBoost Prediction</h3>
                        <div class="prediction-value">${charts['xgb_prediction']:.2f}</div>
                    </div>
                </div>
            """
        
        html_content += """<div class="grid-layout">"""
        
        if 'price_chart' in charts:
            html_content += f"""
                <div class="chart-section">
                    <h3>Price Predictions vs Actual</h3>
                    <div class="chart-container">
                        <img src="data:image/png;base64,{charts['price_chart']}" alt="Price Predictions Chart">
                    </div>
                </div>
            """
        
        if 'error_chart' in charts:
            html_content += f"""
                <div class="chart-section">
                    <h3>Prediction Errors</h3>
                    <div class="chart-container">
                        <img src="data:image/png;base64,{charts['error_chart']}" alt="Prediction Errors Chart">
                    </div>
                </div>
            """
        
        html_content += """</div>"""
        
        if 'performance_chart' in charts:
            html_content += f"""
                <div class="chart-section">
                    <h3>Model Performance Comparison</h3>
                    <div class="chart-container">
                        <img src="data:image/png;base64,{charts['performance_chart']}" alt="Model Performance Chart">
                    </div>
                </div>
            """
        
        symbol_df = prediction_df[prediction_df['symbol'] == symbol].copy()
        symbol_df = symbol_df.sort_values('date', ascending=False)
        
        html_content += f"""
                <div class="chart-section">
                    <h3>Historical Predictions</h3>
                    <div style="overflow-x: auto;">
                        <table>
                            <thead>
                                <tr>
                                    <th>Date</th>
                                    <th>LSTM Prediction</th>
                                    <th>XGBoost Prediction</th>
                                    <th>Actual Price</th>
                                    <th>LSTM Error</th>
                                    <th>XGBoost Error</th>
                                </tr>
                            </thead>
                            <tbody>
        """
        
        for _, row in symbol_df.iterrows():
            html_content += f"""
                                <tr>
                                    <td>{row['date']}</td>
                                    <td>${row['lstm_prediction']:.2f}</td>
                                    <td>${row['xgb_prediction']:.2f}</td>
                                    <td>{f"${row['actual_price']:.2f}" if not pd.isna(row['actual_price']) else "Pending"}</td>
                                    <td>{f"${row['lstm_error']:.2f}" if not pd.isna(row['lstm_error']) else "N/A"}</td>
                                    <td>{f"${row['xgb_error']:.2f}" if not pd.isna(row['xgb_error']) else "N/A"}</td>
                                </tr>
            """
        
        html_content += """
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        """
    
    html_content += """
            <footer class="footer">
                <p>This dashboard automatically updates with new prediction data daily</p>
                <p>&copy; 2025 Stock Price Prediction Tool</p>
            </footer>
        </div>
        
        <script>
            function showSymbolSection() {
                const sections = document.querySelectorAll('.symbol-section');
                sections.forEach(section => {
                    section.classList.remove('active-section');
                });
                
                const select = document.getElementById('symbolSelect');
                const selectedSymbol = select.value;
                document.getElementById(selectedSymbol + '-section').classList.add('active-section');
            }
            
            window.onload = function() {
                showSymbolSection();
            };
        </script>
    </body>
    </html>
    """
    
    with open(dashboard_dir / 'index.html', 'w') as f:
        f.write(html_content)
    
    return dashboard_dir / 'index.html'