// TimelineChart.js
import Highcharts from 'highcharts';
import Timeline from 'highcharts/modules/timeline';
import HighchartsReact from 'highcharts-react-official';
import React from 'react';

// Initialize the timeline module
Timeline(Highcharts);

/**
 * Renders a timeline chart using Highcharts based on an array of events.
 *
 * @component
 * @param {Object} props - Component props.
 * @param {Array<Object|string>} props.arrayData - Array of data points for the timeline.
 *   Each item should be an object with optional `title` and `description`, or a string fallback.
 * @returns {JSX.Element} A timeline chart rendered using Highcharts.
 */
const TimelineChart = ({ arrayData }) => {
  const getTimelineChartOptions = () => {
    return {
      chart: {
        type: 'timeline',
        inverted: true,
        height: '100%',
      },
      title: {
        text: 'Drug Interaction Timeline',
      },
      xAxis: {
        type: 'datetime',
        visible: false,
      },
      yAxis: {
        gridLineWidth: 1,
        title: null,
        labels: {
          enabled: false,
        },
      },
      series: [
        {
          data:
            arrayData?.map((item, index) => ({
              name: `Event ${index + 1}`,
              label: item.title || `Point ${index + 1}`,
              description: item.description || item,
              x: new Date().getTime() + index * 1000 * 60 * 60, // stagger events hourly
            })) || [],
        },
      ],
      tooltip: {
        style: {
          width: 300,
        },
      },
    };
  };

  return (
    <HighchartsReact
      highcharts={Highcharts}
      options={getTimelineChartOptions()}
    />
  );
};

export default TimelineChart;
