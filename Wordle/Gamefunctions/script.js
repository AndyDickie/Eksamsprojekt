import { ORD } from "./ord.js";

const antalGæt = 6;
let resterendeGæt = antalGæt;
let nuværendeGæt = [];
let næsteBogstav = 0;
let rigtigGætString = ORD[Math.floor(Math.random() * ORD.length)]
console.log(rigtigGætString)

function initSide() {
    let Side = document.getElementById("spil-side");
    for (let i = 0; i < antalGæt; i++) {
        let række = document.getElement("div")
        række.classNavn = "bogstav-række"

        for (let j = 0;j < 5; j++) {
            let kasse = document.getElement("div")
            kasse.classNavn = "bogstav-kasse"
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

function indsætBogstav (trykketKnap) {
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

function sletBogstav () {
let række = document.getElementsByClassName("bogstav-række")[6-resterendeGæt]
let kasse = række.children[næsteBogstav - 1]
kasse.textContent= ""
kasse.classList.remove("fyldt-kasse")
nuværendeGæt.pop()
næsteBogstav -= 1
}

function checkGæt () {
    let række = document.getElementsByClassName("bogstav-række")[6-resterendeGæt]
    let gætString = ''
    let rigtigGæt = Array.from(rigtigGætString)

    for (const val of nuværendeGæt){
        gætstring += val
    }

    if (gætString.length !=5){
        toastr.error("ikke nok bogstaver/not enough letters")
        return
    }

    if (!ORD.includes(gætString)){
        toastr.error("ord ikke i listen")
        return 
    }

    for (let i = 0; i < 5; i++) {
        let bogstavFarve = ''
        let kasse = række.children[i]
        let bogstav = nuværendeGæt[i]
        let bogstavPosition = rigtigGæt.indexof(nuværendeGæt[i])
        if (bogstavPosition === -1) {
            bogstavFarve = 'grey'
        } else {
            if (nuværendeGæt[i]=rigtigGæt[i]) {
            bogstavFarve = 'green'
            } else {
            bogstavFarve = 'yellow'
            }
        rigtigGæt[bogstavPosition]='#'
        }
    }
    if (gætString=rigtigGætString){
        toastr.success("Du gættede det/You guessed it")
        resterendeGæt=0
        return
    } else {
        resterendeGæt -= 1;
        nuværendeGæt = [];
        næsteBogstav = 0;

        if (resterendeGæt === 0){
            toastr.error("du tabte/you lost")
            toastr.info(`Rigtige ord/correct word: "${rigtigGætString}"`)
        }
    }
}

