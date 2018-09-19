# Pipeline imports
from quantopian.pipeline import Pipeline
from quantopian.pipeline.data.psychsignal import stocktwits
from quantopian.pipeline.factors import SimpleMovingAverage
from quantopian.pipeline.experimental import QTradableStocksUS


# Pipeline definition
def  make_pipeline():

    base_universe = QTradableStocksUS()

    sentiment_score = SimpleMovingAverage(
        inputs=[stocktwits.bull_minus_bear],
        window_length=3,
    )

    return Pipeline(
        columns={
            'sentiment_score': sentiment_score,
        },
        screen=base_universe
    )
   
   
''' 
Note the way that pipelines work... 
It's all about defining a base_universe = QTradableStocksUS()

And then what you do is you define a sentiment_score as one of the factors. 
That factor comes from the library pipeline.factors import SimpleMovingAverage( ... ) 

Then, once base_universe and sentiment_score are defined, you return Pipeline ( columns = { ...}, screen = base_universe)
'''

