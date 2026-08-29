import React, { useEffect, useRef, useState } from 'react';
import { createChart, IChartApi, ISeriesApi, Time } from 'lightweight-charts';
import { useAppStore } from '../../store/useAppStore';

interface ChartContainerProps {
  data: any[];
  type?: 'candlestick' | 'line' | 'area' | 'bar';
  showVolume?: boolean;
}

export const ChartContainer: React.FC<ChartContainerProps> = ({ data, type = 'candlestick', showVolume = false }) => {
  const chartContainerRef = useRef<HTMLDivElement>(null);
  const { isDarkMode } = useAppStore();

  const [chart, setChart] = useState<IChartApi | null>(null);
  const [mainSeries, setMainSeries] = useState<ISeriesApi<any> | null>(null);
  const [volumeSeries, setVolumeSeries] = useState<ISeriesApi<any> | null>(null);

  useEffect(() => {
    if (!chartContainerRef.current) return;

    const chartInstance = createChart(chartContainerRef.current, {
      layout: {
        background: { color: isDarkMode ? '#1e1e24' : '#ffffff' },
        textColor: isDarkMode ? '#d1d4dc' : '#333333',
      },
      grid: {
        vertLines: { color: isDarkMode ? '#2b2b36' : '#e1e1e1' },
        horzLines: { color: isDarkMode ? '#2b2b36' : '#e1e1e1' },
      },
      timeScale: {
        timeVisible: true,
        secondsVisible: false,
      },
      crosshair: {
        mode: 0,
      }
    });

    let series;
    switch (type) {
      case 'line':
        series = chartInstance.addLineSeries({ color: '#2962FF' });
        break;
      case 'area':
        series = chartInstance.addAreaSeries({ lineColor: '#2962FF', topColor: '#2962FF', bottomColor: 'rgba(41, 98, 255, 0.28)' });
        break;
      case 'bar':
        series = chartInstance.addBarSeries({ upColor: '#26a69a', downColor: '#ef5350' });
        break;
      case 'candlestick':
      default:
        series = chartInstance.addCandlestickSeries({ upColor: '#26a69a', downColor: '#ef5350', borderVisible: false, wickUpColor: '#26a69a', wickDownColor: '#ef5350' });
        break;
    }

    setChart(chartInstance);
    setMainSeries(series);

    if (showVolume) {
      const volSeries = chartInstance.addHistogramSeries({
        color: '#26a69a',
        priceFormat: { type: 'volume' },
        priceScaleId: '',
        scaleMargins: { top: 0.8, bottom: 0 },
      });
      setVolumeSeries(volSeries);
    }

    const handleResize = () => {
      if (chartContainerRef.current) {
        chartInstance.applyOptions({ width: chartContainerRef.current.clientWidth });
      }
    };

    window.addEventListener('resize', handleResize);
    // Initial size
    handleResize();

    return () => {
      window.removeEventListener('resize', handleResize);
      chartInstance.remove();
    };
  }, [type, showVolume, isDarkMode]);

  useEffect(() => {
    if (!mainSeries || !data || data.length === 0) return;

    // Formatting data for TradingView
    // Data expected from API: { timestamp: string, open, high, low, close, volume }
    const formattedData = data.map(d => ({
      time: (new Date(d.timestamp).getTime() / 1000) as Time,
      open: d.open,
      high: d.high,
      low: d.low,
      close: d.close,
      value: d.close // For line/area charts
    })).sort((a, b) => (a.time as number) - (b.time as number));

    mainSeries.setData(formattedData as any);

    if (showVolume && volumeSeries) {
      const volumeData = data.map(d => ({
        time: (new Date(d.timestamp).getTime() / 1000) as Time,
        value: d.volume,
        color: d.close >= d.open ? '#26a69a80' : '#ef535080'
      })).sort((a, b) => (a.time as number) - (b.time as number));
      volumeSeries.setData(volumeData);
    }
  }, [data, mainSeries, volumeSeries, showVolume]);

  return (
    <div className="w-full h-full relative" ref={chartContainerRef} />
  );
};
