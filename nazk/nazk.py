from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from .exceptions import InvalidCurrency, InvalidSource, InvalidYearException, NoDataFoundException


class Nazk:
    ENDPOINT = 'http://www.sbs.gob.pe/app/stats/seriesH-tipo_cambio_moneda_excel.asp'
    CURRENCIES = {
        'USD': '02',
        'SEK': '55',
        'CHF': '57',
        'CAD': '11',
        'EUR': '66',
        'JPY': '38',
        'GBP': '34'
    }
    date_format = None
    source = None

    def __init__(self, date_format='%d/%m/%Y', source='SBS'):
        self.date_format = date_format
        if source in ['SBS', 'SUNAT']:
            self.source = source
        else:
            raise InvalidSource('The {0} source is invalid.'.format(source))

    def _get_currency(self, currency):
        try:
            return self.CURRENCIES[currency]
        except KeyError:
            raise InvalidCurrency('The {0} currency is invalid.'.format(currency))

    def _get_endpoint(self, currency, from_date, to_date):
        return '{0}?fecha1={1}&fecha2={2}&moneda={3}&cierre='.format(self.ENDPOINT, from_date, to_date, currency)

    def _data_frame(self, currency_code, date, to_date):
        # Valid dates
        self._valid_date(date)
        self._valid_date(to_date)
        # Dates
        date = datetime.strptime(date, '%d/%m/%Y')
        from_date = date - timedelta(days=7)
        to_date = datetime.strptime(to_date, '%d/%m/%Y')
        end_date = to_date + timedelta(days=7)
        # Get endpoint
        endpoint = self._get_endpoint(currency_code, from_date.strftime('%d/%m/%Y'), end_date.strftime('%d/%m/%Y'))
        # Create data frames
        dfs = pd.read_html(endpoint, header=0)
        df = dfs[0]
        if not df.empty:
            df.columns = ['date', 'currency', 'buy', 'sell']
            df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y')
            df['date'] = df['date'].dt.to_period('D')
            idx = pd.period_range(from_date, end_date)
            df = df.replace(0, np.nan).ffill()
            df = df.set_index('date').reindex(idx, method='pad')
            df = df.fillna(method='backfill')
            if self.source == 'SUNAT':
                df.index = df.index + timedelta(days=1)
            df = df.loc[date:to_date]
            df.index = df.index.strftime(self.date_format)
            return df
        return None

    @staticmethod
    def _convert_source(data_frame):
        idx = []
        for i in data_frame.index:
            i = i + timedelta(days=1)
            idx.append(i.strftime('%d/%m/%Y'))
        return idx

    @staticmethod
    def _to_dict(df):
        data = {}
        for d in df.itertuples():
            d = list(d)
            data[d[0]] = {
                'buy': '{:.3f}'.format(d[2]),
                'sell': '{:.3f}'.format(d[3])
            }
        return data

    @staticmethod
    def _valid_date(date):
        date = datetime.strptime(date, '%d/%m/%Y')
        if date.year < 2000:
            raise InvalidYearException('Information available from the 2000 year.')
        return True

    def get_exchange_rate(self, currency, date, to_date=None):
        currency_code = self._get_currency(currency)
        data_frame = self._data_frame(currency_code, date, to_date or date)
        if data_frame is not None:
            data = self._to_dict(data_frame)
            if date and not to_date:
                date = datetime.strptime(date, '%d/%m/%Y')
                return data[date.strftime(self.date_format)]
            return data
        else:
            raise NoDataFoundException('No data found.')
