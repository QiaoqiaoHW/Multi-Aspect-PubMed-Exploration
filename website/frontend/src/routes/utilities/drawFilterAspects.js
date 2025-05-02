import { drawWordClouds,drawOneCloud } from './drawWordClouds';
import { fetchFilteredWordDataByPost } from './fetchData';
import { removeChildNodes} from './utils'
import { getCyInstances } from "./varStore";
import { endpoints } from './endpoints'


function updateGraph(searchIds){
    let cyInstances = {};
    cyInstances = getCyInstances();
    const filteredNodesIds = [];
    Object.values(cyInstances).forEach(cy => {
        const filteredCyNodeIds = []
        cy.nodes().forEach(node => {
            if (!searchIds.includes(node.id())) {
                node.style('background-color', 'white');
            }else{
                node.style('background-color', node.data().color);
                filteredCyNodeIds.push(node.id());
            } 
          });
        filteredNodesIds.push(filteredCyNodeIds);
    });
    return filteredNodesIds
}

export async function drawFilterWC(filteredNodesIds,showGlobal=false,mode='',aspect='null',search_word='null'){
    // deal with wordcloud
    removeChildNodes(['wc-container','selected-wc'])

    const wordData = []
    for (const idsGroup of filteredNodesIds){
        if(idsGroup.length === 0){
            wordData.push({'id':'selectedWord','level':'selectedWord','word_group':[['NULL',1]]})
        }else{
            const idsGroupformData = new FormData();
            idsGroupformData.append('aspect',aspect)
            idsGroupformData.append('search_word',search_word)
            idsGroupformData.append("idsGroup",idsGroup)
            const data = await fetchFilteredWordDataByPost(endpoints.filter_wc_endpoint, idsGroupformData,100)
            wordData.push(data["selectedAllWord"])
        }
    }

    var state;
    // console.log("debug",showGlobal,mode)
    if(showGlobal&&mode=='topical'){
        state = 1
    }else{
        drawWordClouds(wordData)
        state = 2
    }

    const formData = new FormData();
    formData.append('aspect',aspect)
    formData.append('search_word',search_word)
    formData.append("idsGroup",[].concat(...filteredNodesIds))
    const selectedAllWord = await fetchFilteredWordDataByPost(endpoints.filter_wc_endpoint, formData, 100)
    const selectedContainer = document.getElementById('selected-wc')
    const selected_width = state*window.innerWidth/(wordData.length+state)
    drawOneCloud(selectedAllWord['selectedAllWord']['word_group'],selected_width, selected_width, selectedContainer)
}

export async function drawFilterAspects(aspect,search_word,start_date,end_date,showGlobal,mode){
    const searchForm = new FormData()
    searchForm.append('aspect',aspect)
    searchForm.append('search_word',search_word)
    
    if(start_date&&end_date){
        searchForm.append('start_date', start_date);
        searchForm.append('end_date', end_date);
    }else{
        searchForm.append('start_date', 'global');
        searchForm.append('end_date', 'global');
    }

    // deal with nodes
    let response
    try {
        response = await fetch(endpoints.filter_nodes_endpoint, {
                          method: 'POST',
                          body: searchForm,
                          cache:'reload'
                      });
    }catch (error) {
    console.error(error);
    }
    const searchDocs = await response.json();
    const filteredNodesIds = updateGraph(searchDocs["searchIds"]);

    drawFilterWC(filteredNodesIds,showGlobal,mode,aspect,search_word)
}

