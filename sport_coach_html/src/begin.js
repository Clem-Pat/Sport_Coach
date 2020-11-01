
//array.filter
//array.map

document.addEventListener("keydown", shortcut);
document.addEventListener("click", exitReglagesPopup);

begin()
function begin(){
    window.setTimeout( function(){
        // Change font style if navigator != Chrome (To make font style nicer on Explorer)
        document.querySelector("#init").style.visibility="hidden";
        document.querySelector("#settings").style.visibility="visible";

        document.addEventListener("keydown", shortcut);
        var isChrome = /Chrome/.test(navigator.userAgent) && /Google Inc/.test(navigator.vendor);
        var elements = document.querySelectorAll( 'body *' );
        for (var i = 0; i < elements.length; i++) {
            elements[i].style.fontFamily = "Impact,Charcoal,sans-serif";
        }

    } , 2700) //should be 2700
}

function shortcut(e) {
    key = e.keyCode || e.which;
    if (key === 33) {
        //Sans le compte à rebours
        var objectifRepetitions = Number(document.querySelector("#objectifRepetitions").value);
        var objectifTemps = document.querySelector("#objectifTemps").value;
        var nbreRepetitionParSerie = Number(document.querySelector("#nbreRepetitionParSerie").value);
        var typeRepetition = document.querySelector("#typeRepetition").value;
        var nomFichier = document.querySelector("#nomFichier").value;

        document.querySelector('#settings').style.visibility = 'hidden';
        document.querySelector('#main').style.visibility = 'visible';
        startMain();
        document.querySelector("#mainTitle").innerHTML = "Objectif : " + objectifRepetitions.toString() + " " + typeRepetition + " en " + objectifTemps;
        document.querySelector("#textSurNbreRepetitionParSerie").innerHTML = "/"+nbreRepetitionParSerie.toString();
        document.querySelector("#actualSerie").innerHTML = "1" + "ère".sup() + " série de " + nbreRepetitionParSerie.toString();

        // document.querySelector('#stop').click()
    }
    if (key === 32) {
        //pressed space
        plus({target: {name: spaceShortcut}});
    }
    if (key === 27) {
        document.querySelector("#reglagesPopupBg").style.visibility = 'hidden';
    }
}

function updateValue(e) {
    let key = e.which || e.keyCode;
    var initWidth = e.target.getAttribute("data-initWidth");
    var newWidth = ((e.target.value.length*9)+10);
    var initPaddingLeft = 5;
    var newPaddingLeft = 50 + initPaddingLeft;
    if (initWidth < newWidth) {
        e.target.style.width = newWidth.toString()+'px';
        if (e.target.id != "objectifRepetitions") {
            e.target.parentNode.style.paddingLeft = newPaddingLeft.toString()+'%';
        }
    }
    else{
        e.target.style.width = initWidth.toString()+'px';
        if (e.target.id != "objectifRepetitions") {
            e.target.parentNode.style.paddingLeft = initPaddingLeft.toString()+'%';
        }
    }
    if (key == 13){
        if (e.target.value.length === 0) {
            swal("Oups... " + "'" + e.target.name + "'" + " doit être rempli", {icon:"error"});
        }
        else{
            e.target.style.color = "green";

            if (e.target.id === "typeRepetition"){
                document.querySelector("#textObjectifRepetitions").textContent = e.target.value + " en :";
                document.querySelector("#textNbreRepetitionParSerie").textContent = "Nombre de " + e.target.value + " par série :";
            }

            // Automatically press Tab after Enter
            let inputs = Array.from(document.querySelectorAll('.inputBox')).map(el => el.firstElementChild);
            inputs.push(document.querySelector("#cParti"));
            let index = inputs.indexOf(document.activeElement);
            if (index >= 0) inputs[index + 1].focus();
        }
    }
    else {e.target.style.color = "black";}
}

function cParti() {

    let inputs = Array.from(document.querySelectorAll('.inputBox')).map(el => el.firstElementChild);
    var emptyInputs = [];
    for (i = 0; i < inputs.length; i++) {
        if (inputs[i].value.length === 0) {
            emptyInputs.push(inputs[i]);
        }
    }
    if (emptyInputs.length != 0) {
        swal("Oups... " + "'" + emptyInputs[0].name + "'" + " doit être rempli", {icon:"error"});
    }
    else {
        var objectifRepetitions = Number(document.querySelector("#objectifRepetitions").value);
        var objectifTemps = document.querySelector("#objectifTemps").value;
        var nbreRepetitionParSerie = Number(document.querySelector("#nbreRepetitionParSerie").value);
        var typeRepetition = document.querySelector("#typeRepetition").value;
        var nomFichier = document.querySelector("#nomFichier").value;
        var counter = 5;

        document.querySelector('#settings').style.visibility = 'hidden';
        document.querySelector('#compteARebours').style.visibility = 'visible';

        setInterval(function(){counter --; if(counter >= 0){document.querySelector("#numero").innerHTML = counter;}
                                           if(counter === 0){document.querySelector("#compteARebours").style.visibility = 'hidden';
                                                             document.querySelector('#main').style.visibility = 'visible';
                                                             document.querySelector("#mainTitle").innerHTML = "Objectif : " + objectifRepetitions.toString() + " " + typeRepetition + " en " + objectifTemps;
                                                             document.querySelector("#textSurNbreRepetitionParSerie").innerHTML = "/" + nbreRepetitionParSerie.toString();
                                                             document.querySelector("#actualSerie").innerHTML = "1" + "ère".sup() + " série de " + nbreRepetitionParSerie.toString();
                                                             startMain()}}, 1000);
    }
}

function lightningEffect(e){
    if (e==true) {
        document.getElementById("lightning").style.animation = "lightning 4s";
    }
    else {
        document.getElementById("lightning").style.animation = "";
    }
}
