"use strict";
import Chart from "chart.js/auto";

const ctx = document.getElementById("barChart").getContext("2d");
const barChart = new Chart(ctx, {
  type: "bar",
  data: {
    labels: {},
    datasets: [
      {
        label: "Szerszam Statuszok",
        data: {},
        backgroundColor: "rgb(133, 97, 197)",
        borderColor: "rgb(133, 97, 197)",
      },
    ],
  },
  options: {
    responsive: true,
  },
});
