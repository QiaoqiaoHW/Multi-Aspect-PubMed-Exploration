import * as d3 from 'd3';
import cloud from 'd3-cloud';
import { schemeCategory10 } from 'd3-scale-chromatic';

export function drawOneCloud(wordGroup,width,height,container,font_size=80){
    // Extract words and their frequencies from the data
    const maxFrequency = Math.max(...wordGroup.map(([word, frequency]) => frequency));
    const words = wordGroup.map(([word, frequency], index) => {
        const normalizedSize = font_size*frequency / maxFrequency;
        return {
          text: word,
          size: normalizedSize,
          color: schemeCategory10[index % 10] // Assign different color to each word
        };
      });
      
    const layout = cloud()
                    .size([width, height]) // Set the size of the word cloud container
                    .words(words)
                    .padding(5) // Set padding between words
                    .rotate(() => (Math.random() > 0.5 ? 0 : 90)) // Randomly rotate words
                    .font('Impact')
                    .fontSize((d) => d.size)
                    .on('end', draw);
    layout.start();

    function draw(words) {
        const centerX = layout.size()[0] / 2; // Calculate X coordinate of the center
        const centerY = layout.size()[1] / 2; // Calculate Y coordinate of the center
    
        d3.select(container)
            .append('svg')
            .attr('width', layout.size()[0])
            .attr('height', layout.size()[1])
            .append('g')
            .attr('transform', 'translate(' + centerX + ',' + centerY + ')') // Translate to the center
            .selectAll('text')
            .data(words)
            .enter()
            .append('text')
            .style('font-size', (d) => d.size + 'px')
            .style('font-family', 'Impact')
            .style('fill', (d) => d.color) // Set the fill color of each word
            .attr('text-anchor', 'middle')
            .attr('transform', (d) => 'translate(' + [d.x, d.y] + ')rotate(' + d.rotate + ')')
            .text((d) => d.text);
        }
}


export function drawWordClouds(wordData, state=2){
    const num_wc = wordData.length
    const width = window.innerWidth/(num_wc+state)
    const height = width
    
    const wc_container = document.getElementById('wc-container')
    const font_size_switches = {1:30,2:30,3:20,4:20,5:15,6:10,7:10}
    const font_size = font_size_switches[num_wc]
    wordData.forEach(wordGroup => {
        const container = document.createElement('div');
        container.id = wordGroup.id 
        container.className = 'wordcloud';
        container.style.flex = '1';
        container.style.width = `${width}px`;
        container.style.height = `${height}px`;
        container.style.border = '0.5px solid #ccc';

        wc_container.appendChild(container);

        drawOneCloud(wordGroup['word_group'],width,height,container,font_size)
      });
}
    
  

  