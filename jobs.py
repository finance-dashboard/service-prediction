import numpy as np
import logging
from statsmodels.tsa.arima.model import ARIMA


def job(timeseries: np.ndarray) -> float:
    """
    Fit ARIMA model on a specific time-series and predict next result

    :param timeseries: currency values from some time window
    :returns: predicted value
    """
    logging.info('Processing new request')

    model = ARIMA(timeseries)
    res = model.fit()

    result = res.predict(len(timeseries) + 1)[0]

    logging.info('Finished processing')

    return result
