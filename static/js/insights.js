const score = document.querySelector("h3");
if(score){
    let s = parseInt(score.innerText.match(/\d+/));
    score.style.color = s < 50 ? "red" : "green";
}
