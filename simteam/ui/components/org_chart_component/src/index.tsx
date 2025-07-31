import React from "react";
import ReactDOM from "react-dom/client";
import OrgChartWrapper from "./OrgChartWrapper";

const root = ReactDOM.createRoot(document.getElementById("root")!);

// Fully typed assertion to satisfy JSX
root.render(<OrgChartWrapper /> as React.ReactElement);
