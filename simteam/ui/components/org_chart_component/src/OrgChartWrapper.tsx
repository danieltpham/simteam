import { useEffect, useRef } from "react";
import {
  withStreamlitConnection,
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
      .rootMargin(100)
      .nodeWidth((d:any) => 210)
      .nodeHeight((d:any) => 140)
      .childrenMargin((d:any) => 130)
      .compactMarginBetween((d:any) => 75)
      .compactMarginPair((d:any) => 80)
      .compact(false)
      .nodeContent((d: any) => {
        const colors = [
          "#6E6B6F",
          "#18A8B6",
          "#F45754",
          "#96C62C",
          "#BD7E16",
          "#802F74",
        ];
        const color = colors[d.depth % colors.length];
        const imageDim = 80;
        const lightCircleDim = 95;
        const outsideCircleDim = 110;

        return `
          <div style="background-color:white; position:absolute;width:${d.width}px;height:${d.height}px;">
            <div style="background-color:${color};position:absolute;margin-top:-${outsideCircleDim / 2}px;margin-left:${
          d.width / 2 - outsideCircleDim / 2
        }px;border-radius:100px;width:${outsideCircleDim}px;height:${outsideCircleDim}px;"></div>
            <div style="background-color:#ffffff;position:absolute;margin-top:-${
              lightCircleDim / 2
            }px;margin-left:${
          d.width / 2 - lightCircleDim / 2
        }px;border-radius:100px;width:${lightCircleDim}px;height:${lightCircleDim}px;"></div>
            <img src="${d.data.imageUrl}" style="position:absolute;margin-top:-${
          imageDim / 2
        }px;margin-left:${
          d.width / 2 - imageDim / 2
        }px;border-radius:100px;width:${imageDim}px;height:${imageDim}px;" />
            <div class="card" style="top:${
              outsideCircleDim / 2 + 10
            }px;position:absolute;height:30px;width:${d.width}px;background-color:#3AB6E3;">
              <div style="background-color:${color};height:28px;text-align:center;padding-top:10px;color:#ffffff;font-weight:bold;font-size:16px">
                ${d.data.name}
              </div>
              <div style="background-color:#F0EDEF;height:28px;text-align:center;padding-top:10px;color:#424142;font-size:16px">
                ${d.data.positionName}
              </div>
            </div>
          </div>
        `;
      })
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
