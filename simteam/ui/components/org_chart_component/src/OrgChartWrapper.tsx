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

    // Inject Orbitron and Quantico fonts
    const linkOrbitron = document.createElement("link");
    linkOrbitron.href = "https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap";
    linkOrbitron.rel = "stylesheet";
    document.head.appendChild(linkOrbitron);

    const linkQuantico = document.createElement("link");
    linkQuantico.href = "https://fonts.googleapis.com/css2?family=Quantico:wght@400;700&display=swap";
    linkQuantico.rel = "stylesheet";
    document.head.appendChild(linkQuantico);

    container.innerHTML = "";
    const width = container.getBoundingClientRect().width;

    const chart = new OrgChart()
      .container(container)
      .data(data)
      .rootMargin(100)
      .nodeWidth((d: any) => 330)
      .nodeHeight((d: any) => 170)
      .childrenMargin((d: any) => 90)
      .compactMarginBetween((d: any) => 65)
      .compactMarginPair((d: any) => 100)
      .neightbourMargin(() => 50)
      .siblingsMargin(() => 100)
      .compact(false)
      .linkUpdate(function (this: SVGPathElement) {
        this.setAttribute("stroke", "#00F0FF");
        this.setAttribute("stroke-opacity", "0.8");
        this.setAttribute("stroke-width", "2");
      })
      .buttonContent(({ node }: any) => {
        return `<div style="color:#00F0FF;border-radius:5px;padding:3px;font-family:'Orbitron';font-size:10px;margin:auto auto;background-color:#0B0F1A;border: 1px solid #00F0FF"> 
          <span style="font-family:'Orbitron'; font-size:9px">${node.children ? "▲" : "▼"}</span> ${node.data._directSubordinates} </div>`;
      })
      .nodeContent((d: any) => {
        const borderColor = "#00F0FF";
        const bgColor = "#0B0F1A";
        const nameColor = "#D8F3FF";
        const imageDim = 80;
        const glow = `0 0 10px ${borderColor}, 0 0 20px ${borderColor}`;
        const svgCorner = `<svg width=150 height=75 style=\"opacity:0.8\"><path d=\"M 0,15 L15,0 L135,0 L150,15 L150,60 L135,75 L15,75 L0,60\" fill=\"${borderColor}\" stroke=\"${borderColor}\"/></svg>`;

        const progressBars = Array.from({ length: 5 }, () =>
          Math.floor(Math.random() * 25 + 5)
        );

        return `
          <div class=\"left-top\" style=\"position:absolute;left:-10px;top:-10px\">${svgCorner}</div>
          <div class=\"right-top\" style=\"position:absolute;right:-10px;top:-10px\">${svgCorner}</div>
          <div class=\"right-bottom\" style=\"position:absolute;right:-10px;bottom:-14px\">${svgCorner}</div>
          <div class=\"left-bottom\" style=\"position:absolute;left:-10px;bottom:-14px\">${svgCorner}</div>

          <div style=\"font-family:'Quantico', sans-serif; background-color:${bgColor}; color:${nameColor}; position:absolute; width:${d.width}px; height:${d.height}px; border:2px solid ${borderColor}; border-radius:8px;\">
            
            <!-- Info Text -->
            <div style=\"position:absolute; top:10px; right:20px; text-align:right; font-family:'Orbitron', sans-serif;\">
              <div style=\"font-size:14px; color:${nameColor}; font-weight:bold;\">${d.data.name}</div>
              <div style=\"font-size:12px;\">${d.data.positionName || ""}</div>
              <div style=\"font-size:11px;\">${d.data.id || ""}</div>
            </div>

            <!-- Avatar -->
            <div style=\"position:absolute; top:35px; left:${(d.width - imageDim) / 2}px;\">
              <img src=\"${d.data.imageUrl}\" style=\"width:${imageDim}px; height:${imageDim}px; border-radius:50%; border:2px solid ${borderColor}; box-shadow:${glow};\" />
            </div>

            <!-- Simulated Pie / Progress Bars -->
            <div style=\"position:absolute; top:${imageDim + 25}px; left:20px;\">
              <div style=\"font-size:10px; margin-bottom:4px; color:${nameColor}; font-family:'Orbitron', sans-serif;\">Workload</div>
              <svg width=\"130\" height=\"30\">
                ${progressBars
                  .map(
                    (val, i) =>
                      `<rect width=\"10\" x=\"${i * 20}\" height=\"${val}\" y=\"${30 - val}\" fill=\"#00F0FF\" rx=\"2\" />`
                  )
                  .join("")}
              </svg>
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
