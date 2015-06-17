import requests

def download(token, instrument, granularity, start, end):
    """
    Download historical FX rates from OANDA.

    See OANDA API documentation for more info:
    http://developer.oanda.com/rest-live/rates/#retrieveInstrumentHistory
    """

    headers = {'Authorization': 'Bearer {}'.format(token)}
    params = {'instrument': instrument,
              'granularity': granularity,
              'count': '5000'}

    print 'time,openBid,openAsk,highBid,highAsk,lowBid,lowAsk,closeBid,closeAsk,volume'
    while start < end:
        params['start'] = start
        r = requests.get('https://api-fxtrade.oanda.com/v1/candles', headers=headers, params=params)
        data = r.json
        for candle in data['candles']:
            print '{time},{openBid},{openAsk},{highBid},{highAsk},{lowBid},{lowAsk},{closeBid},{closeAsk},{volume}'.format(**candle)
        start = data['candles'][-1]['time']
        params['includeFirst'] = 'false'


if __name__ == '__main__':

    import argparse
    parser = argparse.ArgumentParser(description=download.__doc__)
    parser.add_argument('instrument', help='Instrument to retrieve history for')
    parser.add_argument('granularity', help='Time range represented by each candlestick')
    parser.add_argument('start', help='Start timestamp')
    parser.add_argument('end', help='End timestamp')
    parser.add_argument('--token-file', default='~/.oanda-token', help='File with OANDA access token (default: ~/.oanda-token)')
    args = parser.parse_args()

    import os.path
    token = open(os.path.expanduser(args.token_file)).read()

    download(token, args.instrument, args.granularity, args.start, args.end)
