

function save(){

    html2canvas(document.body, {
        onrendered: function (canvas) {
            var tempcanvas=document.createElement('canvas');
            graph = document.querySelector('#resultsGraph');
            tempcanvas.width=screen.width;
            tempcanvas.height=screen.height;
            var context=tempcanvas.getContext('2d');
            context.drawImage(canvas, 10, 10);
            var link=document.createElement("a");
            link.href=tempcanvas.toDataURL('image/jpg');   //function blocks CORS
            link.download = 'screenshot.jpg';
            link.click();
        }
    });
    window.setTimeout(function(){location.reload();}, 3000);
}

function dateFr(){
     // les noms de jours / mois
     var jours = new Array("Dimanche", "Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi");
     var mois = new Array("janvier", "fevrier", "mars", "avril", "mai", "juin", "juillet", "aout", "septembre", "octobre", "novembre", "decembre");
     // on recupere la date
     var date = new Date();
     // on construit le message
     var message = jours[date.getDay()] + " ";   // nom du jour
     message += date.getDate() + " ";   // numero du jour
     message += mois[date.getMonth()] + " ";   // mois
     message += date.getFullYear();
     return message;
}

function mean(arg){
    meanTimeSec = 0;
    for (var i = 0; i < arg.length; i++) {
        meanTimeSec += arg[i].y;
    }
    meanTimeSec = meanTimeSec/(arg.length);

    return meanTimeSec
}

function timeSecToClock (arg) {
    var hours   = Math.floor(arg / 3600);
    var minutes = Math.floor((arg - (hours * 3600)) / 60);
    var seconds = arg - (hours * 3600) - (minutes * 60);

    if (hours   < 10) {hours   = "0"+hours;}
    if (minutes < 10) {minutes = "0"+minutes;}
    if (seconds < 10) {seconds = "0"+seconds;}
    return hours+':'+minutes+':'+seconds;
}
