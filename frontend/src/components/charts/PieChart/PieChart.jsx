import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';
import { Pie } from 'react-chartjs-2';
import { CHART_COLORS_ARRAY } from '../../../utils/constants';

ChartJS.register(ArcElement, Tooltip, Legend);

const PieChart = ({ data, title }) => {
  if (!data || !data.labels || data.labels.length === 0) {
    return (
      <div className="chart-empty">
        <p>No data available for chart</p>
      </div>
    );
  }

  const chartData = {
    labels: data.labels,
    datasets: [
      {
        data: data.data,
        backgroundColor: CHART_COLORS_ARRAY.slice(0, data.labels.length),
        borderColor: CHART_COLORS_ARRAY.slice(0, data.labels.length).map((c) =>
          c.replace('0.8', '1')
        ),
        borderWidth: 2,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'right',
        labels: {
          padding: 20,
          usePointStyle: true,
        },
      },
      title: {
        display: !!title,
        text: title,
        font: {
          size: 16,
          weight: 'bold',
        },
      },
      tooltip: {
        callbacks: {
          label: (context) => {
            const total = context.dataset.data.reduce((a, b) => a + b, 0);
            const percentage = ((context.raw / total) * 100).toFixed(1);
            return `${context.label}: ${context.raw} (${percentage}%)`;
          },
        },
      },
    },
  };

  return (
    <div className="chart-container" style={{ height: '400px' }}>
      <Pie data={chartData} options={options} />
    </div>
  );
};

export default PieChart;
