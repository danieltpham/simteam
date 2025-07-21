import React, { useEffect, useRef } from "react";
import {
  withStreamlitConnection,
  StreamlitComponentBase,
  Streamlit,
  ComponentProps,
} from "streamlit-component-lib";
import { OrgChart } from "d3-org-chart";

const OrgChartWrapper = (props: ComponentProps) => {
  const chartRef = useRef<HTMLDivElement>(null);
  const { args } = props;

  const data =
    args.data ?? [
      { id: "100", parentId: "", name: "Steven", lastName: "King", position: "COO" },
      { id: "101", parentId: "100", name: "Neena", lastName: "Kochhar", position: "Admin VP" },
    ];

  const height = args.height ?? 600;

  useEffect(() => {
    const container = chartRef.current;
    if (!container) return;

    container.innerHTML = "";
    const width = container.getBoundingClientRect().width;

    new OrgChart()
      .container(container)
      .data(data)
      .nodeHeight(() => 120)
      .childrenMargin(() => 40)
      .compact(false)
      .nodeContent((d: any) => `
        <div style="
          padding:8px;
          background:#fff;
          border:1px solid #ccc;
          border-radius:4px;
        ">
          <strong>${d.data.name} ${d.data.lastName}</strong><br/>
          <small>${d.data.position}</small>
        </div>
      `)
      .svgWidth(width)
      .svgHeight(height)
      .render()
      .fit();
  }, [args.data, args.height]);

  return (
    <div
      ref={chartRef}
      style={{
        width: "100%",
        height: `${height}px`,
      }}
    />
  );
};

export default withStreamlitConnection(OrgChartWrapper);
