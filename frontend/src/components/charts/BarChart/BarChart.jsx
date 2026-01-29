import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  PointElement,
  LineElement,
} from 'chart.js';
import { Bar } from 'react-chartjs-2';
import { CHART_COLORS_ARRAY } from '../../../utils/constants';

// Register ChartJS components
ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  PointElement,
  LineElement
);

const BarChart = ({ data, title, xLabel = '', yLabel = '' }) => {
  if (!data || !data.labels || data.labels.length === 0) {
    return (
      <div className="chart-empty">
        <p>No data available for chart</p>
      </div>
    );
  }

  const chartData = {
    labels: data.labels,
    datasets: data.datasets.map((dataset, index) => ({
      label: dataset.label,
      data: dataset.data,
      backgroundColor: CHART_COLORS_ARRAY[index % CHART_COLORS_ARRAY.length],
      borderColor: CHART_COLORS_ARRAY[index % CHART_COLORS_ARRAY.length].replace('0.8', '1'),
      borderWidth: 1,
    })),
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: !!title,
        text: title,
        font: {
          size: 16,
          weight: 'bold',
        },
      },
    },
    scales: {
      x: {
        title: {
          display: !!xLabel,
          text: xLabel,
        },
      },
      y: {
        title: {
          display: !!yLabel,
          text: yLabel,
        },
        beginAtZero: true,
      },
    },
  };

  return (
    <div className="chart-container" style={{ height: '400px' }}>
      <Bar data={chartData} options={options} />
    </div>
  );
};

export default BarChart;
