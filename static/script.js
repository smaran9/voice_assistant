const orb = document.getElementById("orb");
const statusText = document.getElementById("status");
const picker = document.getElementById("colorPicker");
const resetBtn = document.getElementById("resetTheme");


/* ORB CLICK */

orb.addEventListener("click", () => {

    orb.classList.add("listening");
    statusText.innerText = "Listening...";

    fetch("/listen")
    .then(res => res.json())
    .then(data => {

// fade out/in effect
    statusText.classList.add('fade');
    setTimeout(()=>{
        statusText.innerText = data.response;
        statusText.classList.remove('fade');
    }, 300);
        addHistory(data.response);

        setTimeout(()=>{
            orb.classList.remove("listening");
        },1200);

    })
    .catch(()=>{
        orb.classList.remove("listening");
    });

});


/* COLOR */

picker.addEventListener("input", () => {

    let c = picker.value;

    orb.style.background =
        `radial-gradient(circle, ${c}, #000)`;

    orb.style.boxShadow =
        `0 0 80px ${c},
         0 0 160px ${c},
         inset 0 0 40px ${c}`;

});


resetBtn.onclick = () => {
    orb.removeAttribute("style");
};


/* PANELS TOGGLE */

function togglePanel(id){

    let panel = document.getElementById(id);

    if(panel.classList.contains("active")){
        panel.classList.remove("active");
    }else{
        closeAllPanels();
        panel.classList.add("active");
    }

}

function closeAllPanels(){
    document
    .querySelectorAll(".panel")
    .forEach(p=>p.classList.remove("active"));
}


/* HISTORY */

function addHistory(text){

    let p = document.createElement("p");
    p.innerText = text;

    document
    .getElementById("historyList")
    .appendChild(p);

    // remove duplicate listener - picker already handled above


}
