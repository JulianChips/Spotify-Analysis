// section 1: set up the svg canvas
const svgWidth = 1000, svgHeight = 800;
const margin = {top: 0, right: 60, bottom: 160, left: 100};
const height = svgHeight - margin.top - margin.bottom;
const width = svgWidth - margin.left - margin.right;

let tip = d3.tip()
  .attr('class', 'd3-tip')
  .offset([-10, 0])
  .html(function(d) {if (ySelection === 'AdSupported'){
        return "<strong>R&D Cost:</strong><br><span style='color:red'> € " + d[ySelection] + "<br>Million Euros</span>";
        } else {
        return `<strong> ${ySelection} </strong><br><span style='color:red'> € ${d[ySelection]/1000} <br>Billion Euros</span>`;
        }
  })

const svg = d3.select('#viz2').append('svg').attr('width', svgWidth).attr('height', svgHeight);
const chartGroup = svg.append('g').attr('transform', `translate(${margin.left}, ${margin.top})`);
svg.call(tip);

let ySelection = 'Total'

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
function yScale(spotifyDataJson, ySelection){
    let yLinearScale = d3.scaleLinear()
        .domain([0, d3.max(spotifyDataJson, d => d[ySelection])])
        .range([height, 0]);
    return yLinearScale;
}

function numComma(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

// section 3: import data and draw the chart
(async function(){
    const spotifyData = await d3.json('/api/revenue/quarter')
    
    spotifyDataJson = [];
    let spotifyData2 = spotifyData.data;

    spotifyData2.forEach(data => {
        let tempName = {
            Quarter: data[0],
            Premium: data[1],
            AdSupported: data[2],
            Total: data[3]
        }

        spotifyDataJson.push(tempName)
    });
    
    console.log(spotifyDataJson);
    

    let tempColor;

    const xBandScale = d3.scaleBand()
        .domain(spotifyDataJson.map(d => d.Quarter))
        .paddingInner(.1)
        .paddingOuter(.1)    
        .range([0, width])
    
    let yLinearScale = yScale(spotifyDataJson, ySelection)  // call function yScale **

    const bottomAxis = d3.axisBottom(xBandScale);
    let leftAxis = d3.axisLeft(yLinearScale);

    let xAxis = chartGroup.append('g')
        .attr('transform', `translate(0, ${height})`)
        .call(bottomAxis);
    
    let yAxis = chartGroup.append('g')
        .call(leftAxis)
    
    const colors = d3.scaleLinear()
        .domain([0, spotifyDataJson.length * .33, spotifyDataJson.length * .66, spotifyDataJson.length])
        .range(['#b58929', '#c61c6f', '#268bd2', '#85992c'])
    
    let myChart = chartGroup.selectAll('rect')
        .data(spotifyDataJson)
        .enter()
        .append('rect')
        .attr('fill', (d, i) => colors(i))
        .attr('x', d => xBandScale(d.Quarter))
        .attr('y', height)
        // .attr('y', d => yLinearScale(d[ySelection]) - margin.bottom)
        .attr('width', xBandScale.bandwidth())
        .attr('height', 0)
        
    myChart
        .transition()
        .attr('y', d => yLinearScale(d[ySelection]))
        .attr('height', d => svgHeight - yLinearScale(d[ySelection]) - margin.top - margin.bottom)
        .delay((d,i) => i*120)
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
    
    const TotalLabel = xLabels.append('text')
        .attr('x', 0).attr('y', 20)
        .attr('value', 'Total')
        .attr('class', 'active')
        .text('Total Revenue by Year')
    
    const PremiumLabel = xLabels.append('text')
        .attr('x', 0).attr('y', 45)
        .attr('value', 'Premium')
        .attr('class', 'inactive')
        .text('Revenue from Premium Subscribers')
    
    const AdSupportedLabel = xLabels.append('text')
        .attr('x', 0).attr('y', 70)
        .attr('value', 'AdSupported')
        .attr('class', 'inactive')
        .text('Revenue from Ad-supported Users')
    
    const nextPageLabel = xLabels.append('text')
        .attr('x', 0).attr('y', 95)
        .attr('value', 'nextpage')
        .attr('class', 'inactive')
        .text('Go to Revenue by Year Page')
 
    
    xLabels.selectAll('text')
        .on('click', function(){
            const value = d3.select(this).attr('value')
            if (value === 'nextpage'){
                location.href = '/revenueYear'
            }
            else if (value !== ySelection){
                
                ySelection = value;
                
                console.log('y:', ySelection);
                
                yLinearScale = yScale(spotifyDataJson, ySelection);
                
                myChart = drawBars(myChart, yLinearScale, ySelection)

                
                yAxis = renderYAxes(yLinearScale, yAxis)

                
                if (ySelection === 'Total'){
                    TotalLabel
                        .classed('active', true).classed('inactive', false);
                    PremiumLabel
                        .classed('active', false).classed('inactive', true);
                    AdSupportedLabel
                        .classed('active', false).classed('inactive', true);
                    
                }
                else if (ySelection === 'AdSupported') {
                    TotalLabel
                        .classed('active', false).classed('inactive', true);
                    PremiumLabel
                        .classed('active', false).classed('inactive', true);
                    AdSupportedLabel
                        .classed('active', true).classed('inactive', false);

                }
                else {
                    TotalLabel
                        .classed('active', false).classed('inactive', true);
                    PremiumLabel
                        .classed('active', true).classed('inactive', false);
                    AdSupportedLabel
                        .classed('active', false).classed('inactive', true);
                }
                
            }

        })   
    



    
})()