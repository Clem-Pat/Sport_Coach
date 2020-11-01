
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

function startMain(){
    if (stopped == false){
        window.setInterval(chronometer, 1000);
        window.setInterval(idealRepetitionCalculator, 1000);
        drawChart();

    }
}

function idealRepetitionCalculator(){
    var objectifRepetitions = document.querySelector("#objectifRepetitions").value;
    var objectifTemps = document.querySelector("#objectifTemps").value;
    var objectifTempsSec = Number(objectifTemps.charAt(0))*36000 + Number(objectifTemps.charAt(1))*3600 + Number(objectifTemps.charAt(3))*600 + Number(objectifTemps.charAt(4))*60 + Number(objectifTemps.charAt(6))*10 + Number(objectifTemps.charAt(7));
    var totalIdeal = (totalSeconds*objectifRepetitions)/objectifTempsSec;

    document.querySelector("#textTotalIdeal").innerHTML = parseInt(totalIdeal);
}

function plus(e){
    let number = Number(e.target.name);

    document.querySelector("#TotalRepetition").textContent = Number(document.querySelector("#TotalRepetition").textContent)+number;
    document.querySelector("#serieRepetition").textContent = Number(document.querySelector("#serieRepetition").textContent)+number;

    var nbreRepetitionParSerie = Number(document.querySelector("#nbreRepetitionParSerie").value);
    var nbreRepetitionDansSerie = Number(document.querySelector("#serieRepetition").textContent);

    if (nbreRepetitionDansSerie >= nbreRepetitionParSerie){

        tempsSerie = document.querySelector('#textSerieChronometer1').innerHTML;
        tempsSerieSec = Number(tempsSerie.charAt(0))*36000 + Number(tempsSerie.charAt(1))*3600 + Number(tempsSerie.charAt(3))*600 + Number(tempsSerie.charAt(4))*60 + Number(tempsSerie.charAt(6))*10 + Number(tempsSerie.charAt(7));
        allData.push({ x: Number(numeroSerie), y: tempsSerieSec});

        var table = document.querySelector('#seriesTable')
        numeroSerie += 1;
        for (var i = 3; i >= 0; i--) {
            table.rows[i+1].cells[0].innerHTML = table.rows[i].cells[0].textContent[0];
            table.rows[i+1].cells[1].innerHTML = table.rows[i].cells[1].textContent;

            table.rows[i].cells[0].innerHTML = numeroSerie + "ème".sup() + " série de " + nbreRepetitionParSerie.toString();

            if (table.rows[i+1].cells[1].innerHTML.length <= 2) {
                table.rows[i+1].cells[0].appendChild(document.createElement('br'));
            }
            else {
                if (table.rows[i+1].cells[0].innerHTML === "1"){
                    table.rows[i+1].cells[0].innerHTML = table.rows[i+1].cells[0].innerHTML + "ère".sup() + " série de " + nbreRepetitionParSerie.toString();
                }
                else {
                    table.rows[i+1].cells[0].innerHTML = table.rows[i+1].cells[0].innerHTML + "ème".sup() + " série de " + nbreRepetitionParSerie.toString();
                }
            }
        }

        currentData.push({ x: Number(nbreRepetitionDansSerie), y: Number(tempsRepetitionsSec) });
        let offsetGraph = { x: currentData[currentData.length - 1].x - nbreRepetitionParSerie, y: currentData[currentData.length - 1].y }
        previousData = currentData.map(value => value.x > nbreRepetitionParSerie ? { x: nbreRepetitionParSerie, y: value.y } : value)
        currentData = [{ x: 0, y: 0 }];
        if (offsetGraph.x > 0) currentData.push(offsetGraph)
        tempsRepetitionsSec=0;

        serieSeconds = 0;
        serieMinutes = 0;
        serieHours = 0;
        displaySerieSeconds = 0;
        displaySerieMinutes = 0;
        displaySerieHours = 0;
        document.querySelector("#textSerieChronometer1").textContent = "00:00:00";
        document.querySelector("#serieRepetition").textContent = Number(document.querySelector("#TotalRepetition").textContent) - (nbreRepetitionParSerie * (numeroSerie-1));

        // lightningEffect(true);
    }
    if (nbreRepetitionDansSerie < nbreRepetitionParSerie) {
        currentData.push({x: Number(nbreRepetitionDansSerie), y: Number(tempsRepetitionsSec)});
        tempsRepetitionsSec=0;

        // lightningEffect(false);
    }

    if (Number(document.querySelector("#TotalRepetition").innerHTML) > Number(document.querySelector("#textTotalIdeal").innerHTML)) {
        document.querySelector('body').style.background = '#00cc00';
        document.querySelector('#reglages').style.background = '#00cc00';
        window.setTimeout(function(){document.querySelector('body').style.background = 'rgb(173,216,230)';}, 1000)
        window.setTimeout(function(){document.querySelector('#reglages').style.background = 'rgb(173,216,230)';}, 1000)
    }
    if (Number(document.querySelector("#TotalRepetition").innerHTML) < Number(document.querySelector("#textTotalIdeal").innerHTML)) {
        document.querySelector('body').style.background = '#ff0000';
        document.querySelector('#reglages').style.background = '#ff0000';
        window.setTimeout(function(){document.querySelector('body').style.background = 'rgb(173,216,230)';}, 1000)
        window.setTimeout(function(){document.querySelector('#reglages').style.background = 'rgb(173,216,230)';}, 1000)
    }

    drawChart();

}

function drawChart(){

    if (stopped == true){

        var nbreRepetitionParSerie = Number(document.querySelector("#nbreRepetitionParSerie").value);
        var typeRepetition = document.querySelector("#typeRepetition").value;
        var objectifRepetitions = Number(document.querySelector("#objectifRepetitions").value);
        var objectifTemps = document.querySelector("#objectifTemps").value;
        var TotalRepetition = document.querySelector("#TotalRepetition").innerHTML;
        var textTotalChronometer1 = document.querySelector("#textTotalChronometer1").innerHTML;
        // var totalChronometerSec = Number(textTotalChronometer1.charAt(0))*36000 + Number(textTotalChronometer1.charAt(1))*3600 + Number(textTotalChronometer1.charAt(3))*600 + Number(textTotalChronometer1.charAt(4))*60 + Number(textTotalChronometer1.charAt(6))*10 + Number(textTotalChronometer1.charAt(7));

        meanTimeSec = parseInt(mean(allData));
        meanTime = timeSecToClock(meanTimeSec);

        document.querySelector('#date').innerHTML = dateFr();
        document.querySelector('#objectif').innerHTML = objectifRepetitions.toString() + " " + typeRepetition + " en " + objectifTemps;
        document.querySelector('#resultats').innerHTML = TotalRepetition.toString() + " en " +  textTotalChronometer1;
        document.querySelector('#tempsMoyenTitle').innerHTML = "Temps moyen pour une série de " + nbreRepetitionParSerie + ' ' + typeRepetition + ' :'
        document.querySelector('#tempsMoyen').innerHTML = meanTime.toString();

        var lLabels = [];
        for (var i = 0; i <= numeroSerie; i++) {
            lLabels.push(i);
        }

        var ctx = document.querySelector('#mySecondChart').getContext('2d');
        var chart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: lLabels,
                datasets: [{
                    label: 'Evolution de la séance',
                    borderColor: 'white',
                    fill: false,
                    data: allData,
                    lineTension: 0
                }]
            },
            options: {
                animation: {duration: 0},
                scales: {
                    xAxes: [{ticks: { fontColor: "white" }}],
                    yAxes: [{ticks: { fontColor: "white" }}]
                },
                legend: {
                    display: true,
                    labels: {fontColor: 'white'}
                }
            }
        });
    }
    else{
        var nbreRepetitionParSerie = Number(document.querySelector("#nbreRepetitionParSerie").value);
        var lLabels = [];
        for (var i = 0; i <= 50; i++) {
            lLabels.push(i);
        }

        var ctx = document.querySelector('#myChart').getContext('2d');
        var chart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: lLabels,
                datasets: [{
                    label: 'Série actuelle',
                    borderColor: 'rgb(0, 0, 255)',
                    fill: false,
                    data: currentData,
                    lineTension: 0
                },
                {
                    label: 'Série précédente',
                    borderColor: '#ffa900',
                    fill: false,
                    data: previousData,
                    lineTension: 0
                }]
            },
            options: {animation: {duration: 0}}
        });
    }
}

function chronometer() {
    totalSeconds++;
    serieSeconds++;
    tempsRepetitionsSec++;

    if (totalSeconds/60 === 1) {
        totalSeconds = 0;
        totalMinutes++;

        if (totalMinutes/60 === 1) {
            totalMinutes = 0;
            totalHours++;
        }
    }
    if (totalSeconds < 10) {
        displayTotalSeconds = "0" + totalSeconds.toString();
    }
    else {
        displayTotalSeconds = totalSeconds;
    }
    if (totalMinutes < 10) {
        displayTotalMinutes = "0" + totalMinutes.toString();
    }
    else {
        displayTotalMinutes = totalMinutes;
    }
    if (totalHours < 10) {
        displayTotalHours = "0" + totalHours.toString();
    }


    if (serieSeconds/60 === 1) {
        serieSeconds = 0;
        serieMinutes++;

        if (serieMinutes/60 === 1) {
            serieMinutes = 0;
            serieHours++;
        }
    }
    if (serieSeconds < 10) {
        displaySerieSeconds = "0" + serieSeconds.toString();
    }
    else {
        displaySerieSeconds = serieSeconds;
    }
    if (serieMinutes < 10) {
        displaySerieMinutes = "0" + serieMinutes.toString();
    }
    else {
        displaySerieMinutes = serieMinutes;
    }
    if (serieHours < 10) {
        displaySerieHours = "0" + serieHours.toString();
    }

    document.querySelector('#textTotalChronometer1').innerHTML = displayTotalHours + ":" + displayTotalMinutes + ":" + displayTotalSeconds;
    document.querySelector('#textSerieChronometer1').innerHTML = displaySerieHours + ":" + displaySerieMinutes + ":" + displaySerieSeconds;
    document.querySelector('#actualSerieChronometer').innerHTML = displaySerieHours + ":" + displaySerieMinutes + ":" + displaySerieSeconds;
}

function stop(){
    stopped = true;
    document.querySelector('#main').style.visibility = 'hidden';
    document.querySelector('#results').style.visibility = 'visible';
    drawChart();
}

function textHover(color){
    document.querySelector("#textDeezer").style.color = color;
}
