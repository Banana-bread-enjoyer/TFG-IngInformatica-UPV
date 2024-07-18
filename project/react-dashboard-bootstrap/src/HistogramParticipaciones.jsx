import React from "react";
import { Bar } from "react-chartjs-2";
import { Container } from "react-bootstrap";
import "bootstrap/dist/css/bootstrap.min.css";

// Import Chart.js and necessary components
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";

// Register the components
ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

const Histogram = ({ data }) => {
  // Assuming data is an array of objects with contractValue and participations properties
  // Example: [{ contractValue: 100, participations: 5 }, { contractValue: 200, participations: 10 }, ...]

  // Step 3: Calculate average participations per contract value range
  const ranges = [0, 100, 200, 300, 400, 500]; // Example ranges
  const rangeLabels = ranges.map((value, index) => {
    if (index === ranges.length - 1) return `${value}+`;
    return `${value}-${ranges[index + 1]}`;
  });

  const participationSums = new Array(ranges.length).fill(0);
  const participationCounts = new Array(ranges.length).fill(0);

  data.forEach((item) => {
    const value = item.contractValue;
    const participations = item.participations;

    for (let i = 0; i < ranges.length; i++) {
      if (
        i === ranges.length - 1 ||
        (value >= ranges[i] && value < ranges[i + 1])
      ) {
        participationSums[i] += participations;
        participationCounts[i]++;
        break;
      }
    }
  });

  const averageParticipations = participationSums.map((sum, index) => {
    const count = participationCounts[index];
    return count === 0 ? 0 : sum / count;
  });

  const chartData = {
    labels: rangeLabels,
    datasets: [
      {
        label: "Average Participations",
        data: averageParticipations,
        backgroundColor: "rgba(75,192,192,0.6)",
        borderColor: "rgba(75,192,192,1)",
        borderWidth: 1,
      },
    ],
  };

  return (
    <Container>
      <h2>Average Participations per Contract Value Range</h2>
      <Bar
        data={chartData}
        options={{
          scales: {
            y: {
              beginAtZero: true,
              title: {
                display: true,
                text: "Average Participations",
              },
            },
            x: {
              title: {
                display: true,
                text: "Contract Value Range",
              },
            },
          },
        }}
      />
    </Container>
  );
};

export default Histogram;
