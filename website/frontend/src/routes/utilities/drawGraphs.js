import cytoscape from 'cytoscape';
import { groupArrayByKey, getDaysDifference, removeChildNodes } from './utils.js'
import { fetchWordDataByPost } from './fetchData.js'
import { drawWordClouds,drawOneCloud } from './drawWordClouds.js';
import { drawFilterWC } from './drawFilterAspects.js'
import { setCyInstances, getCyInstances,getMode,getShowGlobal } from './varStore.js';
import { endpoints } from './endpoints'

export default drawGraphs;

let cyInstances = {}; // Object to store multiple instances of cytoscape
let selectedNode;
let filteredNodesIds;

const next_level_dict = {
                year: 'quarter',
                quarter: 'month',
                month: 'week',
                week: 'articleDate'};
  
const filterNodesWithSameProperties = () => {
    if (selectedNode) {
        filteredNodesIds = [];
        const properties = selectedNode.data();
        Object.values(cyInstances).forEach(cy => {
            const filteredCyNodeIds = []
            cy.nodes().forEach(node => {
                const elementData = node.data();
                if (elementData.color !== properties.color){
                node.style ('background-color', 'grey'); // Example: Change the style of matching nodes
                }else{
                node.style ('background-color', properties.color)
                filteredCyNodeIds.push(node.id());
                }
            });
            filteredNodesIds.push(filteredCyNodeIds);
        });
    }else {
        Object.values(cyInstances).forEach(cy => {
            cy.nodes().forEach(node => {
                const elementData = node.data();
                node.style('background-color', elementData.color);
            });
        });
    }
}

async function addFilter(cy,next_level){
    cy.on('select', 'node', async (event) => {
        selectedNode = event.target;
        // filter node graph
        filterNodesWithSameProperties();
        // filter word cloud
        const showGlobal = getShowGlobal()
        const mode = getMode()
        console.log(showGlobal,mode)
        drawFilterWC(filteredNodesIds,showGlobal,mode)
    });

    cy.on('unselect', 'node', () => {
        selectedNode = null;
        filterNodesWithSameProperties();
    });

    cy.on('click', () => {
        if (!selectedNode) {
        filterNodesWithSameProperties();
        }
    });

    cy.on('dblclick', async function(event) {
        removeChildNodes(['graph-container','wc-container','selected-wc'])

        cyInstances = getCyInstances();
        Object.values(cyInstances).forEach(cy => {
            cy.destroy();
        });
        cyInstances = {};
        setCyInstances(cyInstances);

        const selectedCy = event.target
        const elements = selectedCy.elements().map(element => ({
            'data': element.data(),
            'position': element.position()
        }));
       
        const start_date = elements[0]['data']['articleDate'];
        const end_date = elements.slice(-1)[0]['data']['articleDate'];
        const submit_dates = new FormData();
        submit_dates.append('start_date', start_date);
        submit_dates.append('end_date', end_date);

        const diffDays = getDaysDifference(start_date,end_date)
        if(diffDays<92&&next_level==="quarter"){
            next_level = 'month'
        }
        if(diffDays<31&&next_level==="month"){
            next_level = 'week'
        }

        // draw node graph
        const element_groups = groupArrayByKey(elements, next_level)
        const groups=[];
        element_groups.forEach( group =>{
            const start_date = group.elements[0]['data']['articleDate'];
            const end_date = group.elements.slice(-1)[0]['data']['articleDate'];
            groups.push({'id':group.id,'level':group.level,'elements':[],
                            'start_date':start_date,'end_date':end_date})  
        });
        // console.log('dblclick', groups);

        drawGraphs(groups)
        // drawGraphs(element_groups)

        const batchSize = 1000;
        element_groups.forEach(element_group => {
            const size = element_group['elements'].length
            let startIndex = 0;
            while (startIndex < size) {
                const part_group = {'id':element_group.id,'level':element_group.level,
                    'elements':element_group['elements'].slice(startIndex,startIndex+batchSize)}
                drawGraphs([part_group])
                startIndex += batchSize;
            }
        });
        
        // draw word cloud
        const data = await fetchWordDataByPost(endpoints.show_wordcloud_endpoint,submit_dates,100)
        const wordData = data['wordData']
        drawWordClouds(wordData)
        
        const selectedAllWord = data['selectedAllWord']
        const selectedContainer = document.getElementById('selected-wc')
        const selected_width = 2*window.innerWidth/(wordData.length+2)
        drawOneCloud(selectedAllWord['word_group'],selected_width, selected_width, selectedContainer)
      });
}

function initialNodeGraphs(graph,width,height,parentNode){
    const start_date = graph.start_date;
    const end_date = graph.end_date;

    const container = document.createElement('div');
    container.id = graph.id;
    container.className = 'graph';
    container.style.width = `${width}px`;
    container.style.height = `${height}px`;
    container.style.marginBottom = '10px';
    container.style.border = '0.5px solid #ccc';

    const title = document.createElement('div');
    title.style.fontSize = '15px';
    title.style.fontWeight = 'bold';
    title.style.textAlign = 'center';
    if(start_date!=end_date){
        title.textContent = `${start_date}~${end_date}`;
    }else{
        title.textContent = `${start_date}`;
    }
    
    const component = document.createElement('div');
    component.style.display = 'flex';
    component.style.flexDirection = 'column';
    component.style.paddingBottom = '10px'

    parentNode.appendChild(component);
    component.appendChild(title);
    component.appendChild(container);

    const cy = cytoscape({
        container: document.getElementById(graph.id),
        style: [{
            selector: 'node',
            style: {
            'width': '3',
            'height': '3',
            'background-color': `data(color)`,
            'border-color': 'grey',
            'border-width': '0.2',
            'color': 'white',
            'font-size': '0.2',
            'text-wrap': 'wrap',
            'text-valign': 'center',
            'label': node => `${node.data('id')}\n${node.data('topic')}`,
            }
        }],
        layout: { name: 'preset' }
    });

    const next_level = next_level_dict[graph.level]
    addFilter(cy, next_level)
    
    return cy
}

function drawGraphs(graphs,state=2){
    const temporalContainer = document.getElementById('temporal-container');
    if(state==1){
        temporalContainer.style.flexDirection = "row"
    }else if(state==2){
        temporalContainer.style.flexDirection = "column"
    }

    const parentNode = document.getElementById('graph-container');

    const width = window.innerWidth/(graphs.length+state)
    const height = width

    cyInstances = getCyInstances();
    graphs.forEach(graph => {
        if (!cyInstances[graph.id]) {
            cyInstances[graph.id] = initialNodeGraphs(graph,width,height,parentNode)
        }

        cyInstances[graph.id].add(graph.elements);
        cyInstances[graph.id].fit();
    }); 
    setCyInstances(cyInstances);
}