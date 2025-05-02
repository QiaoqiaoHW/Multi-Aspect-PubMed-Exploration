export async function fetchWordData(endpoint,size){
    let response
    try {
        endpoint = `${endpoint}?size=${size}`;
        response = await fetch(endpoint, {
            cache:'reload'
        });
    }catch (error) {
      console.error(error);
    }
    const data = await response.json();
    const wordData = data['wordData']
    return wordData
}

export async function fetchWordDataByPost(endpoint,submit_dates,size){
    let response
    try {
        endpoint = `${endpoint}?size=${size}`;
        response = await fetch(endpoint, {
                              method: 'POST',
                              body: submit_dates,
                              cache:'reload'
                          });
    }catch (error) {
      console.error(error);
    }
    const data = await response.json();
    return data
}

export async function fetchFilteredWordDataByPost(endpoint,idsGroupformData,size){
    let response
    try {
        response = await fetch(`${endpoint}?size=${size}`, {
                        method: 'POST',
                        body: idsGroupformData,
                        cache:'reload'
                    });
    }catch (error) {
    console.error(error);
    }
    const data = await response.json()
    return data
}