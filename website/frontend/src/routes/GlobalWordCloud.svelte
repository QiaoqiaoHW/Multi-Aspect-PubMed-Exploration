<script>
  import { onMount } from 'svelte';
  import  { drawWordClouds,drawOneCloud } from './utilities/drawWordClouds';
  import { fetchWordData } from './utilities/fetchData'
  import { endpoints } from './utilities/endpoints';

  export let endpoint;
  export let mode;

  var state;

  onMount(async () => {
    const wordData = await fetchWordData(endpoint,100)
    if(mode=='topical'){
      state = 1;
      const wc_container = document.getElementById('wc-container')
      const width = window.innerWidth/(wordData.length+state)
      drawOneCloud(wordData[0]['word_group'],width,width,wc_container)
    }else{
      state = 2;
      drawWordClouds(wordData,state);

      const selectedAllWord = await fetchWordData(endpoints.global_wordcloud_endpoint,100)
      const selectedContainer = document.getElementById('selected-wc')
      selectedContainer.innerHTML = ''
      const selected_width = 2*window.innerWidth/(wordData.length+state)
      drawOneCloud(selectedAllWord[0]['word_group'],selected_width, selected_width, selectedContainer)
    }
  });
</script>


