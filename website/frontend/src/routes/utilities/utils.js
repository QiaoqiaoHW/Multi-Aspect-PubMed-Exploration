export function groupArrayByKey(array, key) {
    const elements_groups = array.reduce((result, element) => {
        const keyValue = element['data'][key];
        if (!result[keyValue]) {
            result[keyValue] = {
                id: keyValue,
                level: key,
                elements: []
            };
        }
    
        result[keyValue].elements.push(element);
        return result;
    }, {});
    
    return Object.values(elements_groups);
}


export function getDaysDifference(date1, date2) {
    const d1 = new Date(date1);
    const d2 = new Date(date2);
  
    const diffMilliseconds = Math.abs(d2 - d1);
  
    const millisecondsPerDay = 24 * 60 * 60 * 1000;
    const diffDays = Math.floor(diffMilliseconds / millisecondsPerDay)+1;
  
    return diffDays;
  }

  
export function removeChildNodes(parentTagArr){
    parentTagArr.forEach(parentTagName => {
        const parentNode = document.getElementById(parentTagName);
        while (parentNode.firstChild) {
            parentNode.removeChild(parentNode.firstChild);
            }
    });  
}