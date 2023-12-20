import pandas as pd
import requests
import json

import plotly.graph_objs as go
from plotly.offline import plot

"""
	This file contains all the tools used for plotting data.

	It currently contains a general purpose plotting function which plots 
	candlestick charts, overlayed with indicators, signals, & trendlines.

	Eventually, there should be more functions here, each of which would solve a 
	single purpose, to provide more flexibility to developers as to what to plot 
	and how to style it. Modular is the aim.
"""

# TI & TA
def GetPlotData(df, 
	add_volume:bool=True,
	add_candles:bool=True,
	buy_signals:bool or list=False,
	sell_signals:bool or list=False,
	signals:bool or list=False,
	plot_indicators=[],
	trend_points=False,
	trends=False):
	""" Generates the plotly traces to be plotted. """

	data=[]
	if add_volume:
		volume = go.Bar(
			x = df['time'],	
			y = df['volume'], 
			xaxis="x", 
			yaxis="y2", 
			name = "Volume")

		data = [volume]

	if add_candles:
		candle = go.Candlestick(
			x = df['time'],
			open = df['open'],
			close = df['close'],
			high = df['high'],
			low = df['low'],
			name = "Candlesticks")
		data.append(candle)
		
	for ind in plot_indicators:
		if df.__contains__(ind['name']):
			if ind.get('showlegend', None) is None:
				ind['showlegend'] = True
			if ind.get('color', None) is None:
				ind['color'] = 'rgba(102, 207, 255, 50)'
			if ind.get('yaxis', None) is None:
				ind['yaxis'] = 'y'
			if ind.get('xaxis', None) is None:
				ind['xaxis'] = 'x'
			if ind.get('type', None) is None:
				ind['type'] = 'scatter'
			if ind.get('width', None) is None:
				ind['width'] = 300000
			if ind.get('fill', None) is None:
				ind['fill'] = None
			if ind.get('mode', None) is None:
				ind['mode'] = 'lines'

			if ind['type'] == 'bar':
				trace = go.Bar(
					x = df['time'], 
					y = df[ind['name']], 
					name = ind['title'],
					xaxis = ind['xaxis'], 
					yaxis = ind['yaxis'], 
					marker_color = ind['color'], 
					showlegend=ind['showlegend'],
					width = ind['width'],
				  marker = dict(color = ind['color']))
			else:
				trace = go.Scatter( 
					x = df['time'],
					y = df[ind['name']], 
					name = ind['title'],
					mode = ind['mode'], 
					xaxis = ind['xaxis'], 
					yaxis = ind['yaxis'], 
					fill = ind['fill'], 
					showlegend=ind['showlegend'],
					line = dict(color = ind['color']))

			data.append(trace)

	if trend_points:
		mins = go.Scatter( x = df['time'], 	y = df['min'], name = "Min Points",
			line = dict(color = ('rgba(255, 100, 100, 255)')),
			mode = "markers",)
		data.append(mins)

		maxs = go.Scatter( x = df['time'], y = df['max'], name = "Max Points",
				line = dict(color = ('rgba(100, 255, 100, 255)')),
				mode = "markers",)
		data.append(maxs)

	if signals:
		for signal in signals:
			scat = go.Scatter(
				x = [item[0] for item in signal['points']],
				y = [item[1] for item in signal['points']],
				name = signal['name'],
				mode = "markers",
				marker_size = 13
			)
			data.append(scat)


	if buy_signals:
		buys = go.Scatter(
				x = [item[0] for item in buy_signals],
				y = [item[1] for item in buy_signals],
				# marker=dict(
				# 	color = [item[2] for item in buy_signals]
				# ),
				name = "Buy Signals",
				mode = "markers",
				marker_size = 13
			)
		data.append(buys)

	if sell_signals:
		sells = go.Scatter(
				x = [item[0] for item in sell_signals],
				y = [item[1] for item in sell_signals],
				name = "Sell Signals",
				mode = "markers",
				marker_size = 13
			)
		data.append(sells)
	
	return data

def PlotData(df,
	add_candles:bool=True,
	add_volume:bool=True,
	buy_signals:bool or list=False,
	sell_signals:bool or list=False,
	signals:bool or list=False,
	trend_points=False,
	plot_indicators=[],
	plot_shapes=False,
	trends=False,
	save_plot=False,
	show_plot=False,
	plot_title:str="Unnamed"):
	'''
	Creates a plotly plot based on the options provided - which can be displayed
	in a front-end or saved as a standalone webpage.

	Params
	--
		buy signals: bool or list
			if not False it adds to the plot some points representing buy signals

		sell signals: bool or list
			if list, it adds to the plot some points representing sell signals

	'''

	data = GetPlotData(
		df,
		add_candles=add_candles,
		add_volume=add_volume,
		buy_signals=buy_signals,
		sell_signals=sell_signals,
		signals=signals,
		trend_points=trend_points,
		plot_indicators=plot_indicators,
		trends=trends)

	layout = go.Layout(
		# autosize=True,
		margin=dict(l=0, r=0, b=0, t=0),
		hovermode="closest",
		plot_bgcolor="#FFF",
		paper_bgcolor="#FFF",
		legend=dict(font=dict(size=8), orientation="h", x=0, y=0),
		# colorway=['#5E0DAC', '#FF4F00', '#375CB1', '#FF7400', '#FFF400', '#FF0056'],
		xaxis={
			'rangeslider': {
				'visible': False,
				'yaxis': {
					'rangemode':'match'
				}
			}, 
			"showticklabels":False,
			'type': 'date'},
	)
	
	y2, y3 = False, False
	if add_volume:
		y2 = True
	for ind in plot_indicators:
		if ind.__contains__('yaxis'):
			if ind['yaxis'] == 'y2':
				y2 = True
			if ind['yaxis'] == 'y3':
				y3 = True
		
	if y2 and y3:
		layout.update(
			yaxis={
				"domain": [0.3, 1],
				# "title": "Price", 
				"fixedrange":False,
				"ticks": '',
				"showticklabels":False,
			})
		layout.update(
			yaxis2=dict(
				domain = [0.15, 0.29],
				side = 'right',
				showticklabels = False,
				# title  = "Volume"
			))
		layout.update(
			yaxis3=dict(
				domain = [0, 0.15],
				showticklabels = False,
				# title=""
			))
	elif y2:
		layout.update(
			yaxis={
				"domain": [0.25, 1],
				# "title": "Price", 
				"fixedrange":False,
				"ticks": '',
				"showticklabels":False},
		)
		layout.update(
			yaxis2=dict(
				domain = [0, 0.24],
				side = 'right',
				showticklabels = False,
				# title  = "Volume"
				))
	elif y3:
		layout.update(
			yaxis={
				"domain": [0.25, 1],
				# "title": "Price", 
				"fixedrange":False,
				"ticks": '',
				"showticklabels":False},
		)
		layout.update(
			yaxis3=dict(
				domain = [0, 0.24],
				showticklabels = False,
				# ticks="",
				# title=""
				))
	else:
		layout.update(
			yaxis={
				"domain": [0.1, 1],
				# "title": "Price", 
				"fixedrange":False,
				"ticks": '',
				"showticklabels":False},
		)

	if trends:
		layout.update(shapes=layout['shapes'].__add__(tuple(trends)))
	if plot_shapes:
		layout.update(shapes=layout['shapes'].__add__(tuple(plot_shapes)))

	# style and display
	fig = go.Figure(data = data, layout = layout)

	if save_plot or show_plot:
		plot(fig, filename="graphs/"+plot_title+'.html', auto_open=show_plot)

	return fig