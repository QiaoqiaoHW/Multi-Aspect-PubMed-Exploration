let cyInstances = {};
let showGlobal;
let mode;

// Getter method to retrieve the value of cyInstances
export function getCyInstances() {
  return cyInstances;
}

// Setter method to update the value of cyInstances
export function setCyInstances(newCyInstances) {
  cyInstances = newCyInstances;
}

export function getShowGlobal(){
  return showGlobal
}

export function setShowGlobal(newValue){
  showGlobal = newValue
}

export function getMode(){
  return mode
}

export function setMode(newValue){
  mode = newValue
}
