// TimelineChart.js
import Highcharts from 'highcharts';
import Timeline from 'highcharts/modules/timeline';
import HighchartsReact from 'highcharts-react-official';
import React from 'react';


// Initialize the timeline module
Timeline(Highcharts);

const TimelineChart = ({ arrayData }) => {
  const getTimelineChartOptions = () => {
    return {
      chart: {
        type: 'timeline',
        inverted: true,
        height: '100%'
      },
      title: {
        text: 'Drug Interaction Timeline'
      },
      xAxis: {
        type: 'datetime',
        visible: false
      },
      yAxis: {
        gridLineWidth: 1,
        title: null,
        labels: {
          enabled: false
        }
      },
      series: [{
        data: arrayData?.map((item, index) => ({
          name: `Event ${index + 1}`,
          label: item.title || `Point ${index + 1}`,
          description: item.description || item,
          x: new Date().getTime() + index * 1000 * 60 * 60
        })) || []
      }],
      tooltip: {
        style: {
          width: 300
        }
      }
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
