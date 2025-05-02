<script>
    import GlobalNodes from './GlobalNodes.svelte';
    import SelectedNodes from './SelectedNodes.svelte';
    
    import GlobalWordCloud from './GlobalWordCloud.svelte';
    import SelectedWordCloud from './SelectedWordCloud.svelte';

   
    import { drawFilterAspects } from './utilities/drawFilterAspects'
    import { removeChildNodes } from './utilities/utils'
    import { endpoints } from './utilities/endpoints'
    import { getMode, getShowGlobal, setMode, setShowGlobal } from './utilities/varStore'

    import './styles.css';
    import { onMount } from "svelte";
 
    let start_date = '';
    let end_date = '';
    let submit_dates;

    let search_word = '';
    let aspect = 'title'

    let showGlobal = true;
    let mode='topical';
    let isChecked = true;

    let showAfterSelectDates = false;

    function handleCheckboxClick(event) {  
        start_date = '';
        end_date = '';
        search_word = ''  
        showGlobal = true    
        isChecked = event.target.checked;
        mode = isChecked ? 'topical' : 'temporal';

        setShowGlobal(showGlobal)
        setMode(mode)

        removeChildNodes(['graph-container','wc-container','selected-wc'])
    }

    async function handleSubmitDates(event) {
        event.preventDefault();
        search_word = ''
        showGlobal = false;
        setShowGlobal(showGlobal)

        submit_dates = new FormData(event.target);
        // console.log('start_date',start_date)
        // console.log('end_date',end_date)

        showAfterSelectDates = !showAfterSelectDates
        removeChildNodes(['graph-container','wc-container','selected-wc'])
    }

    async function handleSearch(event){
        event.preventDefault();
        // console.log('aspect:',aspect)
        // console.log('search_word:',search_word)
        showGlobal = getShowGlobal()
        mode = getMode()
        drawFilterAspects(aspect,search_word,start_date,end_date,showGlobal,mode)
    }

    onMount(async () => {
        setShowGlobal(showGlobal)
        setMode(mode)
        await handleSubmitDates();   
        await handleSearch();
    });
</script>


{#if showGlobal}
    {#if mode=='topical'}
        <GlobalNodes endpoint={endpoints.topical_endpoint} mode={mode} />
        <GlobalWordCloud endpoint = {endpoints.global_wordcloud_endpoint} mode={mode}/>
    {:else if mode=='temporal'}
        <GlobalNodes endpoint={endpoints.temporal_endpoint} mode={mode} />
        <GlobalWordCloud endpoint = {endpoints.temporal_wordcloud_endpoint} mode={mode}/>
    {/if}
{:else}
    {#if showAfterSelectDates}
        <SelectedNodes  endpoint={endpoints.show_endpoint}  submit_dates={submit_dates}/>
        <SelectedWordCloud endpoint = {endpoints.show_wordcloud_endpoint} submit_dates={submit_dates} />
    {:else}
        <SelectedNodes  endpoint={endpoints.show_endpoint}  submit_dates={submit_dates}/>
        <SelectedWordCloud endpoint = {endpoints.show_wordcloud_endpoint} submit_dates={submit_dates} />
    {/if}
{/if}


<div class='form_container'>
    <div class='left-form'>
    <form id='postForm' method="post" on:submit={handleSubmitDates}>
        <label>From
            <input type="date" name="start_date" bind:value={start_date} >
        </label>
        <label>To
            <input type="date" name="end_date" bind:value={end_date}>
        </label>
        <input type="submit" value="show" id="show">
    </form>
    </div>
        
    <div class='middle-form'>
    <form id='searchForm'  method="post" on:submit={handleSearch}>
        <input id="search_word" name="search_word" type="text" bind:value={search_word}>
        <select id="aspect" name="aspect" bind:value={aspect}>
            <option value="title">Title</option>
            <option value="abstract">Abstract</option>
            <option value="title+abstract">Title+Abstract</option>
            <option value="keywords">Keywords</option>
            <option value="journal">Journal</option>
            <option value="authors">Authors</option>
            <option value="affiliations">Affiliations</option>
        </select>
        <input type="submit" value="filter" id='filter'>
    </form>
    </div>

    <div class='right-forms'>
    <form id='switchForm' method="post">
        <input id='modebox' class="mui-switch" type="checkbox" bind:checked={isChecked} on:change={handleCheckboxClick}>
    </form>
    <p id="mode">{mode}</p>
    </div> 
</div>


    
<div class="container" id="container">
    <div class="temporal-container" id="temporal-container">
        <div class="graph-container" id="graph-container">
        </div>
        <div class="wc-container" id='wc-container'>
        </div>
    </div>
    <div id='instruction' class='instruction'>
    <div class='instruction-title'>The Total WordCloud</div>
    <div class="selected-wc" id='selected-wc'></div>   
    </div> 
</div>





