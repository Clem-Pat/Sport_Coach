function reglages(){
    var typeRepetition = document.querySelector('#typeRepetition').value;
    document.querySelector("#reglagesPopupBg").style.visibility = 'visible';
    document.querySelector('#spaceShortcut').focus();
    console.log(typeRepetition);
    document.querySelector('#textReglagesPopup2').innerHTML = typeRepetition.toString();
}

function exitReglagesPopup(e){

    forbiddenId = ["reglagesPopup"];
    forbiddenId.push("logo");
    forbiddenId.push("reglagesPopupTextParent");
    forbiddenId.push("textReglagesPopup");
    forbiddenId.push("spaceShortcutBox");
    forbiddenId.push("spaceShortcut");
    forbiddenId.push("textReglagesPopup2");
    forbiddenId.push("reglages");

    if (forbiddenId.includes(e.target.id) == false) {
        document.querySelector("#reglagesPopupBg").style.visibility = 'hidden';
    }
}

function updateSpaceShortcut(e){
    let key = e.which || e.keyCode;
    var initWidth = e.target.getAttribute("data-initWidth");
    var newWidth = ((e.target.value.length*9)+10);
    if (initWidth < newWidth) {
        e.target.style.width = newWidth.toString()+'%';
    }
    else{
        e.target.style.width = initWidth.toString()+'%';
    }
    if (key == 13){
        if (e.target.value.length === 0) {
            spaceShortcut = 5;
        }
        else{
            e.target.style.color = "green";
            spaceShortcut = e.target.value;
            setTimeout(function () {
                document.querySelector("#reglagesPopupBg").style.visibility = 'hidden';
            }, 300);
        }
    }
    else {e.target.style.color = "black";}
}
