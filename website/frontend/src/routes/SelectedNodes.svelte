<script>
  import { onMount } from 'svelte';
  import  drawGraphs from './utilities/drawGraphs.js'
  import { setCyInstances } from './utilities/varStore.js';

  export let endpoint;
  export let submit_dates;

  let scroll_id = '';
  let element_groups;
  let cyInstances = {};

  async function fetchData(endpoint, submit_dates, scroll_id='') {    
    let response;
    try {
      if(!scroll_id){
        response = await fetch(endpoint, {
                              method: 'POST',
                              body: submit_dates,
                              cache:'reload'
                          });
      }else{
        const endpoint1 = `${endpoint}?scroll_id=${scroll_id}`;
        response = await fetch(endpoint1, {
                              method: 'POST',
                              body: submit_dates,
                              cache:'reload'
                          });
      }

      const batch_data = await response.json();
      element_groups = batch_data['element_groups'];

      setCyInstances(cyInstances)
      drawGraphs(element_groups)

      if (batch_data['scroll_size'] > 0) {
        fetchData(endpoint, submit_dates, batch_data['scroll_id']); // Fetch the next page
      }
    } catch (error) {
      console.error(error);
    }
  }

  onMount(async () => {
    await fetchData(endpoint, submit_dates, scroll_id);
  });

</script>

