<script>
  import { onMount } from 'svelte';
  import  drawGraphs from './utilities/drawGraphs';
  import { setCyInstances } from './utilities/varStore.js';

  export let endpoint;
  export let mode;

  let scroll_id = '';
  let cyInstances = {};

  let state;
  
  async function fetchData(endpoint, scroll_id='') {
    let response;
    try {
      if(!scroll_id){
        response = await fetch(endpoint, {
            cache:'reload'
        });
      }else{
        const endpoint1 = `${endpoint}?scroll_id=${scroll_id}`;
        response = await fetch(endpoint1, {
            cache:'reload'
        });
      }

      const batch_data = await response.json();
      const element_groups = batch_data['element_groups'];

      setCyInstances(cyInstances)
      drawGraphs(element_groups,state)

      if (batch_data['scroll_size'] > 0) {
        await fetchData(endpoint, batch_data['scroll_id']); // Fetch the next page
      }
    } catch (error) {
      console.error(error);
    }
  }

  onMount(async () => {
    if(mode=='topical'){
      state = 1;
    }else{
      state = 2;
    }
    await fetchData(endpoint, scroll_id);
  });
</script>
