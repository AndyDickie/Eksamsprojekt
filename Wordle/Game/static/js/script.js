import { ORD } from "./ord.js";
const antalGæt = 6;
let resterendeGæt = antalGæt;
let nuværendeGæt = [];
let næsteBogstav = 0;
let rigtigGætString = ORD[Math.floor(Math.random() * ORD.length)]
console.log(rigtigGætString)

function initSide() {
    let Side = document.getElementById("spil-side");
    console.log('initSide');
    for (let i = 0; i < antalGæt; i++) {
        console.log('initSide');
        let række = document.createElement("div")
        række.className = "bogstav-række"

        for (let j = 0; j < 5; j++) {
            let kasse = document.createElement("div")
            kasse.className = "bogstav-kasse"
            række.appendChild(kasse)
        }
        Side.appendChild(række)
    }
}
initSide()

document.addEventListener("keyup", (e) => {

    if (resterendeGæt === 0) {
        return
    }

    let trykketKnap = String(e.key)
    if (trykketKnap === "Backspace" && næsteBogstav !== 0) {
        deleteLetter()
        return
    }

    if (trykketKnap === "Enter") {
        checkGuess()
        return
    }

    let find = trykketKnap.match(/[a-z]/gi)
    if (!find || find.length > 1) {
        return
    } else {
        insertLetter(trykketKnap)
    }
})

function insertLetter (trykketKnap) {
    if (næsteBogstav === 5) {
        return
    }
    trykketKnap = trykketKnap.toLowerCase()

    let række = document.getElementsByClassName("bogstav-række")[6-resterendeGæt]
    let kasse = række.children[næsteBogstav]
    kasse.textContent=trykketKnap
    kasse.classList.add("fyldt-kasse")
    nuværendeGæt.push(trykketKnap)
    næsteBogstav += 1
}

function deleteLetter () {
let række = document.getElementsByClassName("bogstav-række")[6-resterendeGæt]
let kasse = række.children[næsteBogstav - 1]
kasse.textContent= ""
kasse.classList.remove("fyldt-kasse")
nuværendeGæt.pop()
næsteBogstav -= 1
}

function checkGuess () {
    let række = document.getElementsByClassName("bogstav-række")[6-resterendeGæt]
    let gætString = ''
    let rigtigGæt = Array.from(rigtigGætString)

    for (const val of nuværendeGæt){
        gætString += val
    }

    if (gætString.length != 5){
        toastr.error("ikke nok bogstaver/not enough letters")
        return
    }

    if (!ORD.includes(gætString)){
        console.log("ord findes ikke");
        toastr.error("ord ikke i listen")
        return 
    }

    for (let i = 0; i < 5; i++) {
        let bogstavFarve = ''
        let kasse = række.children[i]
        let bogstav = nuværendeGæt[i]
        let bogstavPosition = rigtigGæt.indexOf(nuværendeGæt[i])
        console.log(nuværendeGæt[i], rigtigGæt[i])
        if (bogstavPosition === -1) {
            bogstavFarve = 'grey'
        } else {
            if (nuværendeGæt[i] == rigtigGæt[i]) {
                bogstavFarve = 'green'
            } else {
                bogstavFarve = 'yellow'
            }
            rigtigGæt[i]='#'
        }
        let delay = 0 * i
        setTimeout(()=> {
            //shade box
            kasse.style.backgroundColor = bogstavFarve
            //shadeKeyBoard(letter, letterColor)
        }, delay)
    }
    if (gætString === rigtigGætString){
        toastr.success("Du gættede det/You guessed it")
        resterendeGæt=0
        return
    } else {
        resterendeGæt -= 1;
        nuværendeGæt = [];
        næsteBogstav = 0;
        toastr.error("forkert gæt");

        if (resterendeGæt === 0){
            toastr.error("du tabte/you lost")
            toastr.info(`Rigtige ord/correct word: "${rigtigGætString}"`)
        }
    }
}

