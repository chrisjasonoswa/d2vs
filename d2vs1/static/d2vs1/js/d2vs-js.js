
//Table

//Navbar onLoad
function default_selected(){
	let bttnHome = document.querySelector("#home-bttn");
    bttnHome.style.backgroundColor = '#dfefff';
    bttnHome.style.color = '#418cdbff';
}
$(function(){
	$('div[onload]').trigger('onload');
});


//Button Navbar
let bttnA = document.querySelector("#home-a");
bttnA.addEventListener('click', () =>{
    inactive_all();
    //Active Home Button
    let bttnHome = document.querySelector("#home-bttn");
    bttnHome.style.backgroundColor = '#dfefff';
    bttnHome.style.color = '#418cdbff';

})

let bttnB = document.querySelector("#ctrl-a");
bttnB.addEventListener('click', () =>{
    inactive_all();
    //Active Logs Button
    let bttnCtrl = document.querySelector("#ctrl-bttn");
    bttnCtrl.style.backgroundColor = '#dfefff';
    bttnCtrl.style.color = '#418cdbff';

})

let bttnC = document.querySelector("#logs-a");
bttnC.addEventListener('click', () =>{
    inactive_all();
    //Active Logs Button
    let bttnLogs = document.querySelector("#logs-bttn");
    bttnLogs.style.backgroundColor = '#dfefff';
    bttnLogs.style.color = '#418cdbff';
})

function inactive_all(){
    //Inactive Home Button
    let bttnHome = document.querySelector("#home-bttn");
    bttnHome.style.backgroundColor = 'transparent';
    bttnHome.style.color = '#4e4e4e';

    //Inactive Logs Button
    let bttnCtrl = document.querySelector("#ctrl-bttn");
    bttnCtrl.style.backgroundColor = 'transparent';
    bttnCtrl.style.color = '#4e4e4e';

    //Inactive Logs Button
    let bttnLogs = document.querySelector("#logs-bttn");
    bttnLogs.style.backgroundColor = 'transparent';
    bttnLogs.style.color = '#4e4e4e';

}

