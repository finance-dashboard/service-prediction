import numpy as np
from statsmodels.tsa.arima.model import ARIMA


def job(timeseries: np.ndarray) -> float:
    """
    Fit ARIMA model on a specific time-series and predict next result

    :param timeseries: currency values from some time window
    :returns: predicted value
    """
    model = ARIMA(timeseries)
    model.fit()

    result = model.predict(len(timeseries) + 1)[0]

    return result
