import React from 'react';
import Highcharts from 'highcharts';
import HighchartsReact from 'highcharts-react-official';

/**
 * Component to render a bar chart displaying clinical trials by phase.
 *
 * @component
 * @param {Object} props - Component props
 * @param {Object} props.jsonData - JSON data containing clinical trials information
 * @returns {JSX.Element|null} Rendered chart component or null if no data
 */
const ChartSection = ({ jsonData }) => {
  /**
   * Generates chart options for Highcharts based on clinical trials data.
   *
   * @returns {Object} Highcharts configuration object
   */
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
