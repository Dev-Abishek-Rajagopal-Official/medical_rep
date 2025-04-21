import React from 'react';
import Highcharts from 'highcharts';
import HighchartsReact from 'highcharts-react-official';

const ChartSection = ({ jsonData }) => {
  const getChartOptions = () => {
    const clinicalTrials = jsonData?.clinical_trials || {};
    const categories = Object.keys(clinicalTrials);
    const data = Object.values(clinicalTrials);

    return {
      chart: { type: 'bar' },
      title: { text: 'Clinical Trials by Phase' },
      xAxis: { categories, title: { text: 'Phase' } },
      yAxis: { min: 0, title: { text: 'Number of Trials' } },
      series: [{ name: 'Trials', data }]
    };
  };

  return jsonData?.clinical_trials ? (
    <HighchartsReact highcharts={Highcharts} options={getChartOptions()} />
  ) : null;
};

export default ChartSection;
