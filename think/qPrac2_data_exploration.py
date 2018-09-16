# Data Exploration

from quantopian.research import returns, symbols

# Select a time range to inspect
period_start = '2014-01-01'
period_end = '2014-12-31'

# Query returns data for AAPL
# over the selected time range
aapl_returns = returns(
    assets=symbols('AAPL'),
    start=period_start,
    end=period_end,
)

# Display first 10 rows
aapl_returns.head(10)

# Pipeline imports
from quantopian.research import run_pipeline
from quantopian.pipeline import Pipeline

# Note that we import something called "Returns" this is different ...
# ... different from the quantopian.research import returns, symbols idea!  

from quantopian.pipeline.factors import Returns
from quantopian.pipeline.data.psychsignal import stocktwits

# Pipeline definition
# Looks like you need to make a pipeline each time you use it.
# stocktwits is a library

def make_pipeline():

    returns = Returns(window_length=2)
    sentiment = stocktwits.bull_minus_bear.latest
    msg_volume = stocktwits.total_scanned_messages.latest
 
    # make_pipeline() specifically returns Pipeline(...)
    # Pipeline(...) looks to be a dataframe.

    return Pipeline(
        columns={
            'daily_returns': returns,
            'sentiment': sentiment,
            'msg_volume': msg_volume,
        },
    )

# Pipeline execution
# This is a little confusing to me, need to come back and revise this. 

data_output = run_pipeline(
    make_pipeline(),
    start_date=period_start,
    end_date=period_end
)

# Filter results for AAPL
# .xs = does

aapl_output = data_output.xs(
    symbols('AAPL'),
    level=1
)

# Plot results for AAPL
aapl_output.plot(subplots=True);
