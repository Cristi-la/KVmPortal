"use client"

import { ResponsiveContainer, Bar, BarChart, Label, Rectangle, ReferenceLine, XAxis, YAxis, LabelList, CartesianGrid, Pie, PieChart  } from "recharts"

import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components//ui/card"
import {
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
} from "@/components/ui/chart"

export function VmCreationChart() {
  return (
        <ChartContainer
          config={{
            steps: {
              label: "VMs",
              color: "hsl(var(--chart-1))",
            },
          }}
        >
          <BarChart
            accessibilityLayer
            data={[
              {
                date: "2024-01-01",
                count: 2000,
              },
              {
                date: "2024-01-02",
                count: 2100,
              },
              {
                date: "2024-01-03",
                count: 2200,
              },
              {
                date: "2024-01-04",
                count: 1300,
              },
              {
                date: "2024-01-05",
                count: 1400,
              },
              {
                date: "2024-01-06",
                count: 2500,
              },
              {
                date: "2024-01-07",
                count: 1600,
              },
            ]}
          >
            <Bar
              dataKey="count"
              fill="var(--color-steps)"
              radius={5}
              fillOpacity={0.6}
              activeBar={<Rectangle fillOpacity={0.8} />}
            />
            <XAxis
              dataKey="date"
              tickLine={false}
              axisLine={false}
              tickMargin={4}
              tickFormatter={(value) => {
                return new Date(value).toLocaleDateString("en-US", {
                  weekday: "short",
                })
              }}
            />
            <ChartTooltip
              defaultIndex={2}
              content={
                <ChartTooltipContent
                  hideIndicator
                  labelFormatter={(value) => {
                    return new Date(value).toLocaleDateString("en-US", {
                      day: "numeric",
                      month: "long",
                      year: "numeric",
                    })
                  }}
                />
              }
              cursor={false}
            />
            <ReferenceLine
              y={1200}
              stroke="hsl(var(--muted-foreground))"
              strokeDasharray="3 3"
              strokeWidth={1}
            >
              <Label
                position="insideBottomLeft"
                value="Average VM creation"
                offset={10}
                fill="hsl(var(--foreground))"
              />
              <Label
                position="insideTopLeft"
                value="200"
                className="text-lg"
                fill="hsl(var(--foreground))"
                offset={10}
                startOffset={100}
              />
            </ReferenceLine>
          </BarChart>
        </ChartContainer>
  )
}


export const description = "A mixed bar chart"


const chartData = [
  { month: "January", desktop: 186, mobile: 80 },
  { month: "February", desktop: 305, mobile: 200 },
  { month: "March", desktop: 237, mobile: 120 },
  { month: "April", desktop: 73, mobile: 190 },
  { month: "May", desktop: 209, mobile: 130 },
  { month: "June", desktop: 214, mobile: 140 },
]

const chartConfig = {
  desktop: {
    label: "Desktop",
    color: "hsl(var(--chart-1))",
  },
  mobile: {
    label: "Mobile",
    color: "hsl(var(--chart-2))",
  },
  label: {
    color: "hsl(var(--background))",
  },
} 

export function HypervisorOsChart() {
  return (
    <ChartContainer config={chartConfig}>
      <BarChart
        accessibilityLayer
        data={chartData}
        layout="vertical"
        margin={{
          right: 16,
        }}
      >
        <CartesianGrid horizontal={false} />
        <YAxis
          dataKey="month"
          type="category"
          tickLine={false}
          tickMargin={10}
          axisLine={false}
          tickFormatter={(value) => value.slice(0, 3)}
          hide
        />
        <XAxis dataKey="desktop" type="number" hide />
        <ChartTooltip
          cursor={false}
          content={<ChartTooltipContent indicator="line" />}
        />
        <Bar
          dataKey="desktop"
          layout="vertical"
          fill="var(--color-desktop)"
          radius={4}
        >
          <LabelList
            dataKey="month"
            position="insideLeft"
            offset={8}
            className="fill-[--color-label]"
            fontSize={12}
          />
          <LabelList
            dataKey="desktop"
            position="right"
            offset={8}
            className="fill-foreground"
            fontSize={12}
          />
        </Bar>
      </BarChart>
    </ChartContainer>
  )
}




"use client"



export const ss = "A pie chart with a label list"

const data = [
  { browser: "chrome", visitors: 275, fill: "var(--color-chrome)" },
  { browser: "safari", visitors: 200, fill: "var(--color-safari)" },
  { browser: "firefox", visitors: 187, fill: "var(--color-firefox)" },
  { browser: "edge", visitors: 173, fill: "var(--color-edge)" },
  { browser: "other", visitors: 90, fill: "var(--color-other)" },
]
const conf = {
  visitors: {
    label: "Visitors",
  },
  chrome: {
    label: "Chrome",
    color: "hsl(var(--chart-1))",
  },
  safari: {
    label: "Safari",
    color: "hsl(var(--chart-2))",
  },
  firefox: {
    label: "Firefox",
    color: "hsl(var(--chart-3))",
  },
  edge: {
    label: "Edge",
    color: "hsl(var(--chart-4))",
  },
  other: {
    label: "Other",
    color: "hsl(var(--chart-5))",
  },
}

export function VMStatusChart() {
  return (
      <ChartContainer
        config={chartConfig}
        className="mx-auto aspect-square max-h-[250px]"
      >
        <PieChart>
          <ChartTooltip
            content={<ChartTooltipContent nameKey="visitors" hideLabel />}
          />
          <Pie data={data} dataKey="visitors">
            <LabelList
              dataKey="browser"
              className="fill-background"
              stroke="none"
              fontSize={12}
              formatter={(value: keyof typeof chartConfig) =>
                  chartConfig[value]?.label
                }
            />
          </Pie>
        </PieChart>
      </ChartContainer>
  )
}
