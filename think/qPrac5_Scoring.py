# Pipeline imports
from quantopian.pipeline import Pipeline
from quantopian.pipeline.data.psychsignal import stocktwits
from quantopian.pipeline.factors import SimpleMovingAverage
from quantopian.pipeline.experimental import QTradableStocksUS


# STEP ONE, DEFINE THE UNIVERSE.
# Pipeline definition
def  make_pipeline():

    base_universe = QTradableStocksUS()


# STEP TWO, CREATE A FILTER
# sentiment_score is a simple moving average ... 
# where the inputs come from stocktwits.bull_minus_bear ...
# ... there's a bit of magic here with how this data works
# but not that it comes from pipeline.data.psychsignal import stocktwits 
# so it's obviously a data set that comes from a "psychsignal" library

    sentiment_score = SimpleMovingAverage(
        inputs=[stocktwits.bull_minus_bear],
        window_length=3,
    )

# Create filter for top 350 and bottom 350
# assets based on their sentiment scores
# NOTE: The "|" operator here is "OR" and creates a UNION. 
# The .top(350) and .bottom(350) is so powerful, wow.

    top_bottom_scores = (
        sentiment_score.top(350) | sentiment_score.bottom(350)
    )
    
# STEP THREE, return PIPELINE, AKA CREATE DATAFRAME AND SPECIFY SCREENING UNIVERSE.
# In place of "return Pipeline" maybe it's clearer to think... 
# return pandas dataframe ...
# What is Pipeline( ... ) doing? It's just defining columns of a pandas dataframe 
# and it's also inputing our specific SCREEN, that we've DEFINED 
# DEFINED as in... both base_universe and top_bottom_scores (that union we defined earlier)
# so Pipeline(...) is really taking these partial abstractions and running this targeted analysis. 
    
    return Pipeline(
        columns={
            'sentiment_score': sentiment_score,
        },
        # Set screen as the intersection between our filter
        # and trading universe
        screen=(
            base_universe
            & top_bottom_scores
        )
    )
    
# STEP FOUR: RUN THE PIPELINE
# At this point... we have not actually RUN the pipeline...
# In order to do this you need to import run_pipeline. 
# And then, from there, you need to specify a time range to evaluate this strategy. 
# That's where pipeline_output = run_pipeline( ...) comes into play. 
    
# Import run_pipeline method
from quantopian.research import run_pipeline

# Specify a time range to evaluate
period_start = '2013-01-01'
period_end = '2016-01-01'

# Execute pipeline over evaluation period
pipeline_output = run_pipeline(
    make_pipeline(),
    start_date=period_start,
    end_date=period_end
)

# STEP FIVE: IMPORT PRICING DATA 
# Notice that you need to naturally specify the start / end dates. 

# Import prices function
from quantopian.research import prices

# Get list of unique assets from the pipeline output
asset_list = pipeline_output.index.levels[1].unique()

# Query pricing data for all assets present during
# evaluation period
asset_prices = prices(
    asset_list,
    start=period_start,
    end=period_end
)

# STEP SIX: USE ALPHALENS TO CONNECT FACTOR AND PRICING DATA
# Alpha Lens, like the name implies... combines your factor data and your pricing data. 
# It then runs the returns that would've been generated, specifying the holding periods. 
# There are two quantiles because we are looking at two cohorts, the top and bottom quartiles. 
# The key function here is al.utils.get_clean_factor_and_forward_returns( ... ) 

# Import Alphalens
import alphalens as al

# Get asset forward returns and quantile classification
# based on sentiment scores
factor_data = al.utils.get_clean_factor_and_forward_returns(
    factor=pipeline_output['sentiment_score'],
    prices=asset_prices,
    quantiles=2,
    periods=(1,5,10),
)

# Display first 5 rows
factor_data.head(5)


# STEP SEVEN: EVALUATE THE RETURNS AND PLOT / VISUALIZE FINDINGS
# Calculate mean return by factor quantile
mean_return_by_q, std_err_by_q = al.performance.mean_return_by_quantile(factor_data)

# Plot mean returns by quantile and holding period
# over evaluation time range
al.plotting.plot_quantile_returns_bar(
    mean_return_by_q.apply(
        al.utils.rate_of_return,
        axis=0,
        args=('1D',)
    )
);

# STEP EIGHT: EVALUATE RETURN TIME SERIES, IDENTIFY PERIODS OF DRAWDOWN
# Calculate factor-weighted long-short portfolio returns
ls_factor_returns = al.performance.factor_returns(factor_data)

# Plot cumulative returns for 5 day holding period
al.plotting.plot_cumulative_returns(ls_factor_returns['5D'], '5D');
