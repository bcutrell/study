from datetime import datetime
import pandas as pd
import plotly.express as px
import yfinance as yf

def plot_sp500_returns(start_date, end_date, vertical_line_dates):
    # Download S&P 500 data
    sp500 = yf.Ticker("^GSPC")
    data = sp500.history(start=start_date, end=end_date)

    # Calculate daily returns
    data['Return'] = data['Close'].pct_change()

    # Calculate cumulative returns
    data['Cumulative Return'] = (1 + data['Return']).cumprod() - 1

    # Create the plot
    fig = px.line(data, x=data.index, y=data['Cumulative Return'] * 100,
                  title=f'S&P 500 Cumulative Returns ({start_date} to {end_date})')

    # Add vertical lines
    for date in vertical_line_dates:
        fig.add_vline(x=date, line_dash="dot", line_color="gray")

    # Customize the plot
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Cumulative Return (%)",
        showlegend=False
    )

    # Show the plot
    fig.show()

def main():
    current_date = datetime.now().strftime('%Y-%m-%d')
    plot_sp500_returns(
        start_date="2023-01-01",
        end_date=current_date,
        vertical_line_dates=['2023-03-31', '2023-06-30', '2023-09-30', '2023-12-31', '2024-03-31', '2024-06-30', '2024-09-30', '2024-12-31']
    )

if __name__ == "__main__":
    main()
