<script>
  import { onMount } from 'svelte';
  import { drawWordClouds,drawOneCloud } from './utilities/drawWordClouds';
  import {fetchWordDataByPost} from './utilities/fetchData'

  export let endpoint;
  export let submit_dates
  // export let size;

  onMount(async () => {
    const data = await fetchWordDataByPost(endpoint,submit_dates,100)
    const wordData = data['wordData']
    drawWordClouds(wordData)
    
    const selectedAllWord = data['selectedAllWord']
    const selectedContainer = document.getElementById('selected-wc')
    selectedContainer.innerHTML = ''
    const selected_width = 2*window.innerWidth/(wordData.length+2)
    drawOneCloud(selectedAllWord['word_group'],selected_width, selected_width, selectedContainer)
  });

</script>


