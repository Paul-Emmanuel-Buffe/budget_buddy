const bouton = document.getElementById("dis")
const input = document.getElementById("mdp")
const upperLetter   = /[A-Z]/
const caractereSpe  = /[!@#$%^&*(),.?":{}|<>]/
const number = /\d/

input.addEventListener("input", () => {
    const value = input.value;

    const hasUpperLetter = upperLetter.test(value);
    const hasSpecialChar = caractereSpe.test(value);
    const hasNumber = number.test(value);
    const isLongEnough = value.length >= 10;

    if (!isLongEnough || !hasUpperLetter || !hasSpecialChar || !hasNumber) {
        bouton.disabled = true;
    } else {
        bouton.disabled = false;
    }
});

