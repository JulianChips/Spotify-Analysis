// section 1: set up the svg canvas
const svgWidth =1000, svgHeight = 800;
const margin = {top: 0, right: 60, bottom: 160, left: 100};
const height = svgHeight - margin.top - margin.bottom;
const width = svgWidth - margin.left - margin.right;

let tip = d3.tip()
  .attr('class', 'd3-tip')
  .offset([-10, 0])
  .html(function(d) {
      if (ySelection === 'RD_Cost'){
          return "<strong>R&D Cost:</strong><br><span style='color:red'> € " + d[ySelection] + "<br>Million Euros</span>";
      } else {
        return `<strong> ${ySelection} </strong><br><span style='color:red'> € ${d[ySelection]/1000} <br>Billion Euros</span>`;
      }
    
  })

const svg = d3.select('#viz').append('svg').attr('width', svgWidth).attr('height', svgHeight);
const chartGroup = svg.append('g').attr('transform', `translate(${margin.left}, ${margin.top})`);
svg.call(tip);

let ySelection = 'Total_Revenue'

function drawBars(myChart, newYScale, ySelection){
    myChart.transition()
    .duration(1000)
    .attr('height', d => svgHeight - newYScale(d[ySelection]) - margin.top - margin.bottom)
    .attr('y', d => newYScale(d[ySelection]))
    .delay((d,i) => i*90)
    .ease(d3.easeBounceOut)
    return myChart;
}


function renderYAxes(yLinearScale, yAxis){
    let leftAxis = d3.axisLeft(yLinearScale)
    yAxis.transition()
         .duration(1000)
         .call(leftAxis)
    return yAxis;
}


// section 2: important functions for building the svg
/* function - yScale */
function yScale(spotifyData, ySelection){
    let yLinearScale = d3.scaleLinear()
        .domain([0, d3.max(spotifyData, d => d[ySelection])])
        .range([height, 0]);
    return yLinearScale;
}

function numComma(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

// section 3: import data and draw the chart
(async function(){
    const spotifyData = await d3.json('/api/revenue')
    console.log(spotifyData.data)
    spotifyData.forEach(data => {
        data.Total_Revenue = +data.Total_Revenue;
        data.Premium_Revenue = +data.Premium_Revenue;
        data.Ad_Supported = +data.Ad_Supported;
        data.RD_Cost = +data.RD_Cost; 
    });
    
    let tempColor;

    const xBandScale = d3.scaleBand()
        .domain(spotifyData.map(d => d.Year))
        .paddingInner(.05)
        .paddingOuter(.05)    
        .range([0, width])
    
    let yLinearScale = yScale(spotifyData, ySelection)  // call function yScale **

    const bottomAxis = d3.axisBottom(xBandScale);
    let leftAxis = d3.axisLeft(yLinearScale);

    let xAxis = chartGroup.append('g')
        .attr('transform', `translate(0, ${height})`)
        .call(bottomAxis);
    
    let yAxis = chartGroup.append('g')
        .call(leftAxis)
    
    const colors = d3.scaleLinear()
        .domain([0, spotifyData.length * .33, spotifyData.length * .66, spotifyData.length])
        .range(['#b58929', '#c61c6f', '#268bd2', '#85992c'])
    
    let myChart = chartGroup.selectAll('rect')
        .data(spotifyData)
        .enter()
        .append('rect')
        .attr('fill', (d, i) => colors(i))
        .attr('x', d => xBandScale(d.Year))
        .attr('y', height)
        // .attr('y', d => yLinearScale(d[ySelection]) - margin.bottom)
        .attr('width', xBandScale.bandwidth())
        .attr('height', 0)
        
    myChart
        .transition()
        .attr('y', d => yLinearScale(d[ySelection]))
        .attr('height', d => svgHeight - yLinearScale(d[ySelection]) - margin.top - margin.bottom)
        .delay((d,i) => i*150)
        .duration(2000)
        .ease(d3.easeBounceOut)

    myChart
        .on('mouseover', tip.show)
        .on('mouseout', tip.hide)
    
    chartGroup.append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 0 - margin.left + 105)
        .attr("x",0 - (height / 2) + 240)
        .attr("dy", "1em")
        .attr("class", "sidelabel")
        .text("Revenue / Cost in Euro");      
  
    
    const xLabels = chartGroup.append('g')
        .attr('transform', `translate(${width/2}, ${height+20})`)
    
    const TotalRevenueLabel = xLabels.append('text')
        .attr('x', 0).attr('y', 20)
        .attr('value', 'Total_Revenue')
        .attr('class', 'active')
        .text('Total Revenue by Year')
    
    const PremiumLabel = xLabels.append('text')
        .attr('x', 0).attr('y', 45)
        .attr('value', 'Premium_Revenue')
        .attr('class', 'inactive')
        .text('Revenue from Premium Subscribers')
    
    const AdSupportedLabel = xLabels.append('text')
        .attr('x', 0).attr('y', 70)
        .attr('value', 'Ad_Supported')
        .attr('class', 'inactive')
        .text('Revenue from Ad-supported Users')
 
    const RDCostLabel = xLabels.append('text')
        .attr('x', 0).attr('y', 95)
        .attr('value', 'RD_Cost')
        .attr('class', 'inactive')
        .text('R&D Cost Per Year')
    
    const NextPageLabel = xLabels.append('text')
        .attr('x', 0).attr('y', 120)
        .attr('value', 'nextpage')
        .attr('class', 'inactive')
        .text('Revenue by Quarter Chart')

    xLabels.selectAll('text')
        .on('click', function(){
            const value = d3.select(this).attr('value')
            if (value === 'nextpage'){
                location.href = '/revenueQuarter'    
            }
            else if (value !== ySelection){
                
                ySelection = value;
                
                console.log('y:', ySelection);
                
                yLinearScale = yScale(spotifyData, ySelection);
                
                myChart = drawBars(myChart, yLinearScale, ySelection)
                // circles = drawCircles(circles, xLinearScale, yLinearScale, xSelection, ySelection);
                
                yAxis = renderYAxes(yLinearScale, yAxis)
                
                // circles = updateToolTip(xSelection, ySelection, circles);
                
                // abbrs = drawAbbrs(abbrs, xLinearScale, yLinearScale, xSelection, ySelection);
                
                if (ySelection === 'Premium_Revenue'){
                    TotalRevenueLabel
                        .classed('active', false).classed('inactive', true);
                    PremiumLabel
                        .classed('active', true).classed('inactive', false);
                    AdSupportedLabel
                        .classed('active', false).classed('inactive', true);
                    RDCostLabel
                        .classed('active', false).classed('inactive', true);
                }
                else if (ySelection === 'Ad_Supported') {
                    TotalRevenueLabel
                        .classed('active', false).classed('inactive', true);
                    PremiumLabel
                        .classed('active', false).classed('inactive', true);
                    AdSupportedLabel
                        .classed('active', true).classed('inactive', false);
                    RDCostLabel
                        .classed('active', false).classed('inactive', true);
                }
                else if (ySelection === 'RD_Cost') {
                    TotalRevenueLabel
                        .classed('active', false).classed('inactive', true);
                    PremiumLabel
                        .classed('active', false).classed('inactive', true);
                    AdSupportedLabel
                        .classed('active', false).classed('inactive', true);
                    RDCostLabel
                        .classed('active', true).classed('inactive', false);
                }
                else {
                    TotalRevenueLabel
                        .classed('active', true).classed('inactive', false);
                    PremiumLabel
                        .classed('active', false).classed('inactive', true);
                    AdSupportedLabel
                        .classed('active', false).classed('inactive', true);
                    RDCostLabel
                        .classed('active', false).classed('inactive', true);
                }
                
            }

        })   
    



    
})()